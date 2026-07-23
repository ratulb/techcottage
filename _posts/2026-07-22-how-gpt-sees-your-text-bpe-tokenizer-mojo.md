---
title: "How GPT-4 Sees Your Text: Building a BPE Tokenizer From Scratch in Mojo"
date: "2026-07-22"
categories: ["Machine Learning", "Mojo"]
tags: ["bpe", "tokenizer", "mojo", "nlp", "from-scratch"]
excerpt: "A step-by-step build of a byte pair encoding tokenizer in Mojo, tracing every merge, every byte, and every design decision from raw text to token IDs."
---

## 1. The Problem

Every sentence you send to ChatGPT arrives at the model as a sequence of integers. Not words, not characters — integers. The bridge between human language and those integers is called a **tokenizer**, and the most widely used algorithm in modern LLMs is **[Byte Pair Encoding (BPE)](https://en.wikipedia.org/wiki/Byte-pair_encoding)**.

GPT-4 uses it. Llama 3 uses it. Mistral, Claude, Gemini — all of them. And here's the strange part: while the transformer architectures powering these models have been rewritten multiple times (GQA, RoPE, flash attention, MoE), the BPE algorithm powering their tokenizers has remained essentially unchanged since 1994, when Philip Gage described it as a text compression technique.

In 2016, Sennrich, Haddow, and Birch adapted BPE for neural machine translation, showing that encoding rare words as sequences of subword units allowed translation systems to handle vocabulary they'd never seen during training. OpenAI adopted it for GPT-2 in 2019, adding a byte-level base vocabulary and a regex pre-tokenizer, and the resulting design has been the industry standard ever since.

In this post we'll build a BPE tokenizer from scratch in Mojo — every merge, every byte, every design decision. By the end you'll know exactly what happens when you call `tokenizer.encode()` under the hood.

## 2. Stage 1 — From Text to Bytes: the Base Vocabulary

Before we can learn anything, we need a starting vocabulary. The most basic approach is to look at a training corpus and collect every unique character (technically, every Unicode codepoint) that appears. That's what our `BPETokenizer.train()` does in its first few steps.

```mojo
# Build the alphabet from all unique characters
var alphabet: List[String] = []
for word in word_freqs.keys():
    for letter in word.codepoints():
        var char_str = chr(Int(letter))
        if char_str not in alphabet:
            alphabet.append(char_str)
sort(alphabet)

# Initialize vocab: special token + every character
self.vocab = List[String](capacity=vocab_size)
self.vocab.append(String("<UNK>"))
self.stoi = Dict[String, Int]()
self.stoi["<UNK>"] = 0
for i, char in enumerate(alphabet):
    self.vocab.append(char)
    self.stoi[char] = i + 1
```

Every codepoint in the corpus becomes a token. The token `"<UNK>"` occupies ID 0 as a fallback for any character we encounter at inference time that wasn't in the training data. The `vocab` list stores tokens by ID (so `vocab[5]` is the token with ID 5), and `stoi` is the reverse mapping — `stoi["e"]` returns the ID for `"e"`.

For a sentence like `"hello world"`, the alphabet is `{Ġ, d, e, h, l, o, r, w}` — the special `Ġ` character (U+0120) is a sentinel inserted by the pre-tokenizer to mark positions where a space originally appeared. The base vocabulary size is 9 (8 characters + `<UNK>`).

This character-level approach works, but it has a fundamental limitation: **every character is one token**. The sentence `"hello world"` would be 11 tokens (one per character, including the space-marker `Ġ`). That's inefficient for an LLM — every token consumes precious context window. We want common subwords like `"he"`, `"ll"`, `"orl"`, and eventually whole words like `"hello"` and `"Ġworld"` to be single tokens.

That's where the learning comes in.

## 3. Stage 2 — The Merge Loop: Learning Subwords

The core BPE insight is beautifully simple:

> Find the most frequently adjacent pair of tokens. Merge them into a single new token. Repeat.

Each merge creates a new vocabulary entry and compresses the text by one token per occurrence of that pair. By repeatedly merging the most common pairs, the algorithm discovers the subword units that best compress the training corpus — and those subword units turn out to be exactly the tokens the LLM wants.

Here's how we count pairs:

```mojo
def _compute_pair_freqs(
    splits: Dict[String, List[String]], word_freqs: Dict[String, Int]
) raises -> Dict[Tuple[String, String], Int]:
    var pair_freqs = Dict[Tuple[String, String], Int]()
    for word_freq in word_freqs.items():
        var word = word_freq.key
        var freq = word_freq.value
        ref split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            var pair = (split[i], split[i + 1])
            pair_freqs[pair] = pair_freqs.get(pair, 0) + freq
    return pair_freqs^
```

For each word in the corpus (weighted by its frequency), we look at its current split — the sequence of tokens it's composed of — and tally every adjacent pair. The result is a frequency map of every token pair across the entire corpus.

Then we find the most frequent pair and merge it:

```mojo
def _merge_pair(
    a: String, b: String,
    mut splits: Dict[String, List[String]],
    word_freqs: Dict[String, Int],
) raises:
    for word in word_freqs:
        ref split = splits[word]
        if len(split) == 1:
            continue
        var i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                split = (
                    [e for e in split[:i]]
                    + [a + b]
                    + [e for e in split[i + 2 :]]
                )
            else:
                i += 1
        splits[word] = split.copy()
```

This function walks every word's token sequence and replaces every occurrence of the pair `(a, b)` with the concatenated token `a + b`. Note that `i` does **not** increment when a merge succeeds — this lets the algorithm handle consecutive merges at the same position. If we merged `"l" + "l" → "ll"` at position 2 in `[h, e, l, l, o]`, the new split becomes `[h, e, ll, o]`, and we immediately check if `(e, ll)` is also a merge candidate at the same position.

The training loop ties it together:

```mojo
while len(self.vocab) < vocab_size:
    var pair_freqs = _compute_pair_freqs(splits, word_freqs)
    if len(pair_freqs) == 0:
        break  # no more pairs to merge — exhausted
    var best_pair: Tuple[String, String] = ("", "")
    var max_freq = -1
    for pair_freq in pair_freqs.items():
        var pair = pair_freq.key
        var freq = pair_freq.value
        if max_freq == -1 or max_freq < freq:
            best_pair = pair
            max_freq = freq
    _merge_pair(best_pair[0], best_pair[1], splits, word_freqs)
    var joined = best_pair[0].copy() + best_pair[1].copy()
    self.merges[best_pair] = joined
    self.vocab.append(joined)
    self.stoi[joined] = len(self.vocab) - 1
```

Each iteration: find the most frequent pair, merge it everywhere, record the merge rule. Stop when we've reached the desired `vocab_size` or when no pairs remain to merge (all words have been reduced to single tokens).

### Tracing Through "hello world"

Let's see what happens with our tiny corpus. The initial splits:

| Word | Initial split |
|---|---|
| `"hello"` | `[h, e, l, l, o]` |
| `"Ġworld"` | `[Ġ, w, o, r, l, d]` |

All pair frequencies are 1 (each pair appears once across both words). The algorithm picks the first pair encountered — say `(h, e)` — and merges it:

| Word | After merge 1 |
|---|---|
| `"hello"` | `[he, l, l, o]` |
| `"Ġworld"` | `[Ġ, w, o, r, l, d]` |

Continue. After 9 merges, every word is a single token:

| Word | After all merges |
|---|---|
| `"hello"` | `["hello"]` |
| `"Ġworld"` | `["Ġworld"]` |

The vocab now has 18 entries (9 base + 9 merge results), and the training stops. The merge rules are recorded in order:

```
(Ġ, t) → Ġt    (if we had a larger corpus)
(i, s) → is
(e, r) → er
...
```

With a richer corpus like the four-sentence Hugging Face example, 19 merges fill the vocab to 50 tokens, compressing text noticeably:

```
"This is not a token." → [This, Ġis, Ġ, n, o, t, Ġa, Ġtoken, .]
```

Nine tokens instead of 19 characters — a 53% reduction.

## 4. Stage 3 — Encoding: Applying the Merge Rules

Once the tokenizer is trained, encoding new text reverses the training process. We pre-tokenize the input, split each word into individual characters, then apply the merge rules in the order they were learned.

```mojo
def _tokenize(self, text: String) raises -> List[String]:
    if text.byte_length() == 0:
        return List[String]()
    var words = PreTokenizer.tokenize(text)
    var splits = [
        [chr(Int(code)) for code in word.codepoints()]
        for word in words
    ]
    for pair_merge in self.merges.items():
        ref pair = pair_merge.key
        ref merge = pair_merge.value
        for idx, split in enumerate(splits):
            var i = 0
            var split_copied = split.copy()
            while i < len(split_copied) - 1:
                if split_copied[i] == pair[0] and split_copied[i + 1] == pair[1]:
                    split_copied = (
                        [e for e in split_copied[:i]]
                        + [merge]
                        + [e for e in split_copied[i + 2 :]]
                    )
                else:
                    i += 1
            splits[idx] = split_copied^
    return [item for sublist in splits for item in sublist]
```

Notice the structure: we iterate over all merge rules in order, and for each rule we scan every word's token split. This is O(N × M) where N is the number of merge rules and M is the total token count across all words — not optimized, but completely transparent.

The pre-tokenizer handles the GPT-2 `Ġ` convention:

```mojo
struct PreTokenizer:
    @staticmethod
    def tokenize[
        spacer: StaticString = "Ġ",
    ](var text: String) raises -> List[String]:
        var splits = (
            StringSlice(text)
            .replace(" ", " " + spacer)
            .replace(".", " .")
            .split(" ")
        )
        var result = List[String](capacity=len(splits))
        for split in splits:
            result.append(String(from_utf8=split.as_bytes()))
        return result^
```

Every space in the input becomes a `Ġ` prefix on the following word. `"hello world"` becomes `["hello", "Ġworld"]`. This is a simplified approximation of GPT-2's byte-level pre-tokenizer — real production tokenizers use a sophisticated regex pattern to split on category boundaries (letters vs numbers vs punctuation vs whitespace) so that BPE never merges across them.

Finally, `encode()` maps the resulting token strings to their integer IDs:

```mojo
def encode(self, text: String) raises -> List[Int]:
    var tokens = self._tokenize(text)
    var ids = List[Int](capacity=len(tokens))
    for token in tokens:
        ids.append(self.stoi.get(token, 0))
    return ids^
```

The `.get(token, 0)` fallback is where `<UNK>` handling lives — if a character wasn't in the training corpus, it maps to ID 0.

## 5. Stage 4 — Decoding: Recovering Text

Decoding is simpler than encoding. We look up each token ID in the vocabulary, join the strings, and replace the `Ġ` sentinel with an actual space.

```mojo
def decode(self, ids: List[Int]) raises -> String:
    if len(ids) == 0:
        return String("")
    var raw = StringSlice("").join([self.vocab[i] for i in ids])
    return String(StringSlice(raw).replace("Ġ", " "))
```

For the trained tokenizer, this gives us a perfect roundtrip:

```mojo
var tok = BPETokenizer()
tok.train(corpus, 50)

var text = "This is not a token."
var ids = tok.encode(text)          # [38, 44, 30, 19, 20, 24, 34, 42, 2]
var decoded = tok.decode(ids)       # "This is not a token."

assert decoded == text              # roundtrip preserved
```

## 6. The Demo — Train, Encode, Decode

Let's train the tokenizer on the Hugging Face course corpus and see the full pipeline. The corpus has four sentences covering ~30 unique characters and enough word variety for 19 merges.

```mojo
var corpus = List[String]()
corpus.append(String("This is the Hugging Face Course."))
corpus.append(String("This chapter is about tokenization."))
corpus.append(String("This section shows several tokenizer algorithms."))
corpus.append(String(
    "Hopefully, you will be able to understand how they are trained and"
    " generate tokens."
))

var tok = BPETokenizer()
tok.train(corpus, 50)

print(tok.merges)
# {(Ġ, t): Ġt, (i, s): is, (e, r): er, (Ġ, a): Ġa, (Ġt, o): Ġto, ...}

print(tok.decode(tok.encode("This is not a token.")))
# "This is not a token."
```

The merge rules show the algorithm's priorities: `(Ġ, t)` is first because `Ġ` followed by `t` appears in 7 different words (`Ġthe`, `Ġto`, `Ġtrained`, `Ġtokenization`, `Ġtokenizer`, `Ġtokens`, `Ġthey`), more than any other pair.

We can also test the UNK fallback:

```mojo
var unk_ids = tok.encode("xyz")
print(unk_ids)    # [0, 0, 0] — every char is UNK
print(tok.decode(unk_ids))  # "<UNK><UNK><UNK>"
```

Characters `x`, `y`, `z` weren't in the Hugging Face corpus, so they each map to `<UNK>` (ID 0). In a production tokenizer this is avoided by starting with a byte-level base vocabulary covering all 256 possible byte values — but for our character-level tokenizer, UNK is the safety net.

## 7. Gaps — What Production Tokenizers Do Differently

Our tokenizer works, but if you compare it against GPT-4's tokenizer (tiktoken), Karpathy's minBPE, or Hugging Face's tokenizers library, you'll find three significant gaps.

### Gap 1: Regex Pre-Tokenization

Our `PreTokenizer` replaces spaces with `Ġ` and splits on periods. GPT-2 uses a regex that categorizes text into groups:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}++| ?\p{N}++| ?[^\s\p{L}\p{N}]++|\s++$|\s+(?!\S)|\s
```

This pattern splits contractions (`'s`, `'t`, `'re`, `'ve`, `'m`, `'ll`, `'d`) into separate tokens, groups letters and numbers into their own categories, and handles whitespace independently. The result is that BPE **never merges across category boundaries** — a digit won't merge with a letter, and punctuation stays separate.

Karpathy's [minBPE](https://github.com/karpathy/minbpe) has two tokenizer classes: `BasicTokenizer` (no regex) and `RegexTokenizer` (with GPT-4-style regex). The `GPT4Tokenizer` adds GPT-4 specific patterns and matches tiktoken's `cl100k_base` output exactly.

### Gap 2: Byte-Level Base Vocabulary

Our character-level vocabulary only covers codepoints seen during training. If you send an emoji or CJK character that wasn't in the corpus, it maps to `<UNK>`. This is the approach used by BERT and DistilBERT.

GPT-2, GPT-4, Llama 3, and Mistral all use a **byte-level** base vocabulary instead. Every UTF-8 character decomposes into 1-4 bytes (values 0-255), so by starting with all 256 possible bytes as the base vocabulary, the tokenizer is **lossless** — no character can ever be unknown. This is why `encode(decode(x)) == x` holds for any Unicode string with GPT-4's tokenizer.

The implementation is straightforward: instead of scanning the corpus for unique characters, initialize the vocabulary with `[chr(i) for i in range(256)]`:

```python
# From minBPE — the byte-level base
unique_chars = [chr(i) for i in range(256)]
```

The only complication is that some byte values correspond to Unicode control characters or whitespace that would break the BPE logic. OpenAI's solution is a `bytes_to_unicode` table that maps each byte to a visible Unicode character, ensuring the BPE algorithm only sees "safe" characters.

### Gap 3: Rank-Based Encoding (tiktoken)

Our tokenizer stores merge rules as an ordered list of `(pair) → merged` mappings and applies them sequentially. tiktoken takes a different approach: instead of storing explicit pairs, it stores a flat `bytes → rank` table. The rank is simply the order in which the merge was learned.

Encoding becomes a **greedy longest-match** algorithm:
1. Start with the raw bytes of the word
2. Find the lowest-ranked token that matches a prefix of the byte sequence
3. Emit that token's ID
4. Advance past those bytes and repeat

This is algorithmically equivalent to applying merge rules in order, but it's faster (single lookup per token instead of scanning all merge rules) and the file format is simpler — one line per token, base64-encoded bytes plus rank.

You can see the educational version in [tiktoken's own `_educational.py`](https://github.com/openai/tiktoken/blob/main/tiktoken/_educational.py).

### Gap 4: The Full Pipeline

Hugging Face's `tokenizers` library adds even more stages. Their `Tokenizer` is a five-stage pipeline:

| Stage | Role | Examples |
|---|---|---|
| **Normalizer** | Pre-processing | NFKC unicode normalization, lowercasing |
| **Pre-tokenizer** | Split into words | Whitespace, ByteLevel, Metaspace |
| **Model** | Core BPE/WordPiece | Our `_tokenize` equivalent |
| **Post-processor** | Add special tokens | Template: `[CLS] $A [SEP] $B [SEP]` |
| **Decoder** | Reverse tokenization | ByteLevel, Metaspace |

All five stages are stored in a single `tokenizer.json` file, making the tokenizer fully self-contained and portable.

## 8. Common Pitfalls

**Dict iteration order.** Our implementation stores merges in a `Dict[Tuple[String, String], String]`. Mojo (like most systems languages) doesn't guarantee iteration order for hash maps. If `merges.items()` returns pairs in a different order than they were inserted, the encoding will apply merge rules in the wrong sequence and produce incorrect tokens. The fix is to switch to a `List[Tuple[Tuple[String, String], String]]` — slower insertion, guaranteed order.

**Running out of merges.** If the training corpus is too small for the target `vocab_size`, the training loop runs out of pairs to merge and would loop forever without the `if len(pair_freqs) == 0: break` guard. This happens with our `"hello world"` corpus at vocab_size 30 — only 9 merges are possible before each word is a single token.

**The `Ġ` character is U+0120.** It's a real Unicode codepoint (Latin capital letter G with inverted breve), not a special marker invented for tokenization. If your source code or training data accidentally contains a literal `Ġ`, it will be treated as a space marker and cause decoding errors. GPT-2 chose this character because it almost never appears in real text.

**UNK vs unknown characters.** Character-level tokenizers (ours) produce `<UNK>` for characters outside the training set. Byte-level tokenizers don't have this problem — every possible byte is in the vocabulary. If you're building a tokenizer for production use, start with byte-level.

## 9. Conclusion

We built a complete BPE tokenizer in Mojo — train, encode, decode, save, and load. Along the way we saw:

1. **BPE is a compression algorithm first.** It finds the most frequent adjacent pairs, merges them, and repeats. The same algorithm that compressed text in 1994 now tokenizes every message you send to an LLM.

2. **The merge order is the model.** Each merge rule is a learned piece of linguistic structure. The order in which merges are applied during encoding determines which subwords form. Get the order wrong, and the tokenization breaks.

3. **Production tokenizers add guardrails.** Regex pre-tokenization prevents merges across category boundaries. Byte-level base vocabularies eliminate UNK. Rank-based encoding (tiktoken) replaces explicit merge rules with a faster greedy lookup.

The next step is to swap our character-level base vocabulary for the full 256-byte range and add a proper GPT-2-style regex pre-tokenizer. At that point, our tokenizer would be functionally equivalent to GPT-2's, capable of encoding any Unicode string without a single `<UNK>`.

The full source for this post is at [github.com/ratulb/simple_bpe](https://github.com/ratulb/simple_bpe). If you want to see these concepts pushed further, study [minBPE](https://github.com/karpathy/minbpe) (clean educational Python), [tiktoken](https://github.com/openai/tiktoken) (production Rust), and the [Hugging Face tokenizers](https://huggingface.co/docs/tokenizers/) library.

---

*Thanks to Sebastian Raschka's [BPE from scratch](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html) post and the [Hugging Face NLP course](https://huggingface.co/learn/nlp-course/chapter6/5) for their excellent references.*
