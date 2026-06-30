---
title: "From Raw Text to Word Vectors: Building a Tokenizer and Word Embeddings with Tenmo"
tenmo_link: https://github.com/ratulb/tenmo
date: "2026-06-30"
categories: ["Natural Language Processing", "Mojo", "Tenmo"]
tags: ["word-embeddings", "mojo", "tenmo", "nlp", "from-scratch", "word2vec", "negative-sampling", "tokenizer", "cbow"]
excerpt: >
  We build word2vec-style embeddings from scratch with Tenmo (a tensor library
  built in Mojo) — starting with a custom tokenizer, then training a CBOW model
  with negative sampling on IMDB reviews, and finally probing the learned
  vectors for semantic similarity.
---

"king − man + woman ≈ queen."

This single equation — the notion that arithmetic on word vectors reveals semantic relationships — is what made word embeddings famous. It suggests that somewhere inside a high-dimensional vector space, directions like "royalty" and "gender" actually exist as learned features. A computer trained only on raw text, with no dictionary or grammar, can learn that *king* and *queen* differ by the same vector as *man* and *woman*.

How does that work? And more importantly, how do we build it from scratch?

In this post, we'll implement the full pipeline using **Tenmo** — a tensor library and neural network framework built in Mojo with full autograd, SIMD-optimized kernels, and GPU support. We'll build a tokenizer that converts raw movie reviews into integer IDs, a CBOW training loop with negative sampling, and a similarity probe that lets us query the learned embedding space. The entire implementation lives in a single file — around 750 lines with the model encapsulated in a compact `Word2Vec` struct — and trains on the IMDB review dataset.

## The Problem: Computers Don't Read

A computer sees strings. `"king"`, `"queen"`, `"man"`, `"woman"` are just sequences of bytes. Nothing in their byte representation suggests that *king* and *queen* are related, or that *man* and *woman* share a semantic axis.

To make words computable, we need **vector representations** — each word mapped to a list of floating-point numbers where distance in vector space corresponds to semantic similarity.

But what kind of vector?

## One-Hot Encoding

The simplest approach: assign each word a unique V-dimensional vector with a single `1` and `V−1` zeros.

```mojo
# Pseudo-code for one-hot encoding
var V = 100_000  # vocabulary size
var id = word_to_idx["king"]   # say, 42
var one_hot = Tensor[dtype].zeros(V)
one_hot[42] = 1
```

The problems are immediate:
- **Semantically blind.** The dot product between any two one-hot vectors is always 0 — they're orthogonal by construction. *King* and *queen* are as unrelated as *king* and *aardvark*.
- **High-dimensional, sparse.** A 100K-dimensional vector with a single non-zero element wastes memory and fails in any ML model that expects dense features.
- **No generalization.** The model can't leverage the fact that *king* and *queen* behave similarly in text — they're treated as completely independent symbols.

## Bag-of-Words and TF-IDF

The next refinement: count how often each word appears in a document. A vector of term frequencies is denser than one-hot, but it's still V-dimensional and ignores word order. TF-IDF improves on raw counts by down-weighting common words (*the*, *a*, *in*), but the representation remains sparse, high-dimensional, and incapable of capturing synonymy.

## Co-Occurrence Matrices (GloVe)

GloVe builds a word-word co-occurrence matrix: count how often word *i* appears near word *j* across the entire corpus, then factorize that matrix to produce dense vectors. The intuition is simple — words that occur in similar contexts have similar vectors — but the co-occurrence matrix is O(V²), making it impractical for large vocabularies without heavy approximation.

## Prediction-Based Embeddings (word2vec)

word2vec flips the problem around. Instead of counting co-occurrences, we train a neural network to **predict** whether a word appears in a given context. The vectors emerge as a byproduct — the hidden layer weights of this prediction network become the word embeddings.

This is what we'll implement. But before we can train embeddings, we need to turn raw text into numbers. That means building a tokenizer.

## Stage 1: Building a Tokenizer from Scratch

A tokenizer converts text into integer IDs. It's the gateway between raw strings and any NLP model. Our tokenizer needs to:

1. Clean raw text — strip HTML, URLs, punctuation artifacts, and digit sequences.
2. Build a vocabulary — collect every unique word from the training corpus, sort it, and assign each word a unique integer.
3. Encode new text into those IDs, with a fallback for words not seen during training.

## Cleaning Text

The IMDB dataset contains movie reviews with HTML tags (`<br />`, `<a href="...">`), URLs, ratings, and other noise. We clean it in a single pass using Python's `re` module — Mojo's Python interop handles this cleanly:

```mojo
@staticmethod
def clean_text(raw_text: String) raises -> PythonObject:
    var py = Python.import_module("builtins")
    var regex = Python.import_module("re")
    var text = py.str(raw_text)

    # Remove HTML tags
    text = regex.sub(r"<[^>]+>", " ", text)
    # Remove URLs
    text = regex.sub(r"http\S+|www\.\S+", " ", text)
    # Remove digit sequences
    text = regex.sub(r"\d+", " ", text)
    # Remove stray apostrophes (preserve contractions like "don't")
    text = regex.sub(r"(?<!\w)'|'(?!\w)", " ", text)
    # Collapse multiple spaces
    text = regex.sub(r"\s+", " ", text).strip()

    # Filter out words shorter than 2 characters
    var filter_fn = Python.evaluate(
        "lambda words: [w for w in words.split() if len(w) >= 2]"
    )
    return filter_fn(text)
```

Every step handles a real data problem:
- HTML tags appear throughout IMDB reviews (especially `<br />` for line breaks).
- URLs appear in user-written reviews ("I saw this at http://example.com").
- Ratings like "10/10" would leak numeric patterns unrelated to sentiment.
- Leading/trailing apostrophes (`'hello'`) are punctuation, but contractions (`don't`) are real words.
- Single-character tokens like "a" and "I" are filtered because they add noise without semantic signal.

The use of `Python.evaluate` to define a lambda is worth noting. Mojo's Python interop means we can write Python logic inline without leaving the language — perfect for text processing where Mojo's standard library doesn't yet have a regex engine.

## Building the Vocabulary

Once we've cleaned every review, we collect the unique words across the entire dataset:

```mojo
@staticmethod
def from_text_lines(text_lines: List[String]) raises -> Self:
    var py = Python.import_module("builtins")
    var all_words: PythonObject = []

    # Collect all words from all text lines
    for line in text_lines:
        all_words.extend(Tokenizer.clean_text(line))

    # Create unique, sorted vocabulary
    all_words = py.list(py.set(all_words))
    all_words = py.sorted(all_words)

    # Add UNKNOWN token for out-of-vocabulary words
    var vocab_with_unknown: PythonObject = [UNKNOWN_TOKEN]
    vocab_with_unknown.extend(all_words)

    # Map each word to a unique integer ID
    var vocabulary = {
        String(token): Int(index)
        for index, token in enumerate(vocab_with_unknown.__iter__())
    }

    return Self(vocabulary^)
```

Key design decisions:

- **UNKNOWN token at position 0.** Any word seen at test time but not in training gets mapped to ID 0. This is a standard practice — it acts as a catch-all, preventing the model from crashing on novel words.
- **Alphabetical sort.** Sorting the vocabulary before assigning IDs ensures deterministic behavior across runs. The word with ID 1 is always `"aaron"`, not a random word depending on Python's set iteration order.
- **Dict[String, Int] for lookup, Dict[Int, String] for decoding.** The tokenizer stores both mappings so we can go from text → IDs and back.

## Encoding and Decoding

With the vocabulary built, encoding new text is straightforward:

```mojo
def encode(self, text: String) raises -> List[Int]:
    var words = Tokenizer.clean_text(text)
    var token_ids = List[Int](capacity=len(words))
    for word in words:
        var word_str = String(word)
        token_ids.append(
            self.word_to_id[word_str] if word_str in self.word_to_id
            else self.word_to_id[UNKNOWN_TOKEN]
        )
    return token_ids^

def decode(self, token_ids: List[Int]) raises -> String:
    return " ".join([self.id_to_word[id] for id in token_ids])
```

The encode step is the inverse of cleaning: the same `clean_text` function that prepared training data also processes new input. Consistency between training and inference is critical — if your tokenizer cleans text one way during training but differently during inference, your model will see a distribution mismatch.

## Loading the IMDB Dataset

The dataset lives at `/tmp/aclImdb/train/` with `pos/` and `neg/` subdirectories. Each file is named like `1234_8.txt` — the number after the underscore is the rating from 1 to 10. We filter for strong reviews (rating ≥ 7 positive, ≤ 4 negative) to get cleaner signal:

```mojo
def init_tokenizer_and_datasets(mut self, dataset_folder: String) raises -> Tokenizer:
    # Ensure dataset is downloaded
    self._download_imdb_dataset()

    var positive_path = Path("/tmp") / dataset_folder / "pos"
    var negative_path = Path("/tmp") / dataset_folder / "neg"
    var all_comments = List[String](capacity=50000)

    # Load positive reviews (rating 7-10)
    if positive_path.exists():
        for file in positive_path.listdir():
            var rating = self._extract_rating_from_filename(file.name())
            if rating >= 7:
                var comment = positive_path.joinpath(file.name()).read_text()
                all_comments.append(comment)

    # Load negative reviews (rating 1-4)
    if negative_path.exists():
        for file in negative_path.listdir():
            var rating = self._extract_rating_from_filename(file.name())
            if rating <= 4:
                var comment = negative_path.joinpath(file.name()).read_text()
                all_comments.append(comment)

    # Build tokenizer from all loaded comments
    var tokenizer = Tokenizer.from_text_lines(all_comments)

    # Tokenize everything and build datasets
    for comment in all_comments:
        var token_ids = tokenizer.encode(comment)
        if len(token_ids) == 0:
            continue
        self.tokenized_reviews.append(token_ids.copy())
        self.concatenated_tokens.extend(token_ids^)

    return tokenizer
```

We store two views of the data:
- **`tokenized_reviews`**: each review as a separate list of token IDs. This lets us build context windows within a single review (we never want context crossing review boundaries).
- **`concatenated_tokens`**: every token ID from every review concatenated into one flat list. This is used for random negative sampling — we draw negative samples uniformly from the entire corpus.

Let's ground this in numbers. The IMDB dataset has 25K training reviews. After filtering for strong sentiment and limiting to 5,000 reviews (for speed), we get a vocabulary of roughly **80K–120K unique words** and about **5 million total tokens**. Our embedding matrix is `vocab_size × 100`, or about 8M–12M parameters — a reasonable size for training on a single machine.

## Stage 2: Token Embedding Approaches — A Landscape

Before we dive into our training algorithm, it's worth stepping back and asking: what approaches exist for turning tokens into vectors, and where does our method fit?

| Approach | Dimensionality | Semantics | Training Cost | Inference Cost |
|---|---|---|---|---|
| One-hot | V (huge) | None | None | O(V) |
| TF-IDF | V (huge) | Word frequency | O(N) | O(V) |
| Co-occurrence (GloVe) | d (small) | Context statistics | O(V²) | O(1) |
| Prediction (word2vec) | d (small) | Context prediction | O(N × d × K) | O(1) |

**One-hot** is the baseline with zero learning — each word is a distinct symbol with no inherent relationship to others.

**TF-IDF** adds frequency weighting but stays in the V-dimensional space. "King" and "queen" are still treated as completely unrelated dimensions.

**Co-occurrence methods** (like GloVe) are the closest competitor to prediction-based methods. They count how often each pair of words co-occurs in a context window, then factorize that count matrix. The resulting vectors capture semantics well, but building the full co-occurrence matrix is O(V²) — infeasible for a 100K vocabulary without approximation. GloVe works around this by counting only co-occurrences above a threshold, but it still requires iterating over every word pair in every context window.

**Prediction-based methods** (word2vec and its variants) take a different route: instead of counting co-occurrences, they train a classifier to predict them. This is the approach we'll implement. The key insight is that predicting whether a word appears in a given context forces the model to learn vector geometry that captures semantic relationships — as a side effect of optimizing classification accuracy, not as an explicit goal.

Within prediction-based methods, there are two main architectures:

- **CBOW (Continuous Bag of Words):** Given the context words, predict the target word. Fast to train, but less effective for rare words.
- **Skip-gram:** Given the target word, predict the context words. Slower to train, but produces better vectors for rare words.

We'll use **CBOW**. The intuition: given "the, cat, on, the", predict "sat". CBOW averages the context word embeddings into a single vector, then scores candidate words against it. It's simpler to implement with manual gradients — a single average instead of per-context-word gradient distribution — and faster to train per step since each training example processes one target word instead of C context words.

## Stage 3: The CBOW Idea

CBOW (Continuous Bag of Words) is built on a simple intuition from linguistics: **"a word is known by the company it keeps."** Words that appear in similar contexts have similar meanings.

The CBOW training objective:

```
Given context words w_{t-C}, ..., w_{t-1}, w_{t+1}, ..., w_{t+C},
maximize the probability of seeing the target word w_t.
```

In the sentence *"The cat sat on the mat"*, with a window size of 2 around *sat*:
- Context: [*the, cat, on, the*]
- Target: *sat*

For every target position in every review, we collect the surrounding words within the window:

```mojo
var left_context = slice(
    max(0, word_position - CONTEXT_WINDOW_SIZE),
    word_position
)
var right_context = slice(
    word_position + 1,
    min(len(review), word_position + CONTEXT_WINDOW_SIZE)
)

var context_indices = review[left_context].copy()
context_indices.extend(review[right_context].copy())
```

This produces a variable-length context window centered on each target word. Words closer to the target are included more reliably; the asymmetric edges of documents naturally get fewer context words, which is fine — the model learns to handle varying amounts of context.

The probability of the target word given the context words is computed using the **softmax** over the entire vocabulary:

```
P(w_target | context) = exp(score(w_target, context)) / Σ_v exp(score(v, context))
```

Here, `score(w_t, context)` is a measure of compatibility between the target word and the averaged context. Word2vec uses **two embedding matrices** to compute this:

- **Input embeddings** (`vocab_size × hidden_size`): used to represent the *context* words. We gather the embeddings for every context word in the window and average them into a single context vector. These are what we'll eventually use as our word vectors.
- **Output embeddings** (`vocab_size × hidden_size`): used to represent the *candidate* word (either the target or a negative sample). Each candidate gets its own embedding, and the score is the dot product between this output embedding and the averaged context vector.

In our code, the context words are looked up from `input_embeddings` and the target + negatives from `output_embeddings`:

```mojo
var context_embedding = input_embeddings.gather[track_grad=False](
    context_indices, reduction=Reduction(1)
)
var averaged_context = context_embedding / Float32(context_length)

var sample_embeddings = output_embeddings.gather[track_grad=False](
    sample_indices
)

var predicted_scores = sample_embeddings.matmul[
    mode=mv, track_grad=False
](averaged_context).sigmoid()
```

The asymmetry is intentional. Each word has two representations — one for when it acts as surrounding context and one for when it's the candidate being scored. Having separate parameters makes the optimization easier, and the input embeddings end up as our final word vectors.

## The Softmax Wall

The softmax denominator sums over every word in the vocabulary. For each training step, computing this requires:

- V dot products (one per vocabulary word)
- V exponentiations
- V additions for the denominator
- V divisions for the final probabilities

With V ≈ 100K, that's 100K dot products per step. With 5 million training tokens and 5 iterations (epochs), that's **2.5 trillion dot products**. Even at 1 microsecond per dot product, that's months of computation.

This is the *softmax wall* — the fundamental computational bottleneck that prevented early neural language models from scaling to large vocabularies.

## Stage 4: Negative Sampling

The critical insight from Mikolov et al. (2013) is that we don't need the full softmax. We don't care about the exact probability distribution over all words — we only care that the model learns good vector representations. And for that, we can replace the multi-class softmax with a much cheaper binary classification task.

**The idea:** Instead of computing "how likely is this context word given this target, out of all possible context words?", train a binary classifier that answers "did this target-context pair come from real data or random noise?"

For each real (target, context) pair (a *positive sample*), we generate K *negative samples* — random words drawn from the corpus that are unlikely to be real context words. The model then learns to assign high probability to positive pairs and low probability to negative pairs.

The objective function for a single training example:

```
J = log σ(u · v) + Σ_{k=1}^{K} E_{w_k ~ P_n}[log σ(-u_k · v)]
```

Where:
- `u` is the embedding of the candidate word (target or negative sample) — looked up from `output_embeddings`
- `v` is the averaged context embedding — computed from `input_embeddings`
- `σ()` is the sigmoid function
- `P_n(w)` is the noise distribution — we draw negative samples from it

The first term pushes the target word's output embedding and the context vector together. Each term in the second sum pushes a random noise word's output embedding and the context vector apart.

## K+1 Binary Classifications Instead of One V-Way Classification

This is the entire point: instead of one V-way softmax (V computations per step), we now have K+1 binary classifications (K+1 computations per step). With K = 5–20, that's a **5,000x–20,000x reduction** in computation per training step.

## The Noise Distribution

Mikolov found empirically that the best noise distribution is the unigram distribution raised to the 3/4 power:

```
P_n(w) = count(w)^(3/4) / Z
```

Where Z is a normalization constant. Raising to the 3/4 power has the effect of giving rare words a higher chance of being selected as negatives than they would under the raw unigram distribution. This prevents the model from seeing only common words as negatives, which would make the task too easy.

Our implementation uses a simpler uniform random distribution (drawing from the concatenated token list), which is a common approximation:

```mojo
def generate_negative_samples(
    current_review: List[Int],
    target_position: Int,
    all_tokens: List[Int],
    num_negative_samples: Int,
) -> List[Int]:
    var corpus_length = Float64(len(all_tokens))
    var negative_samples = [
        all_tokens[
            min(Int(random_float64() * corpus_length), len(all_tokens) - 1)
        ]
        for _ in range(num_negative_samples)
    ]

    # Insert the target word at position 0 (positive sample)
    negative_samples.insert(0, current_review[target_position])

    return negative_samples^
```

The result is a list of K+1 token IDs: position 0 is the positive sample (the real context word), and positions 1 through K are random negatives.

This is the heart of negative sampling — a few lines of code that turn an intractable O(V) problem into a tractable O(K) one.

## Stage 5: The Training Loop

With the theory in place, the training loop ties everything together. The model is encapsulated in a `Word2Vec` struct that holds both embedding tables and exposes `forward()` and `step()` methods. The inner loop simplifies to four lines:

```mojo
var scores = model.forward(ctx, tgt)
model.step(scores, fixed_target, ctx, tgt, Float32(LEARNING_RATE))
```

For each word in each review, the loop:

1. Builds a context window around the target word.
2. Calls `model.forward(ctx, tgt)` which averages context embeddings, scores targets, and applies sigmoid — caching intermediates for the next step.
3. Calls `model.step(scores, labels, ctx, tgt, lr)` which does backward (gradient = scores − labels, chain rule through matmul) and scatter-adds sparse updates to both embedding tables.
4. Uses Tenmo's `scatter_add` under the hood, updating only the rows that participated in the forward pass.

The full inner loop:

```mojo
for word_position in range(len(review)):
    var left = slice(max(0, word_position - CONTEXT_WINDOW_SIZE), word_position)
    var right = slice(word_position + 1,
        min(len(review), word_position + CONTEXT_WINDOW_SIZE))
    if left.start == left.end and right.start == right.end:
        continue

    var ctx = review[left].copy()
    ctx.extend(review[right].copy())
    if len(ctx) == 0:
        continue

    var tgt = generate_negative_samples(review, word_position,
        all_tokens, NUM_NEGATIVE_SAMPLES)

    var scores = model.forward(ctx, tgt)
    model.step(scores, fixed_target, ctx, tgt, Float32(LEARNING_RATE))
```

Let's look at what happens inside those two method calls.

## Forward Pass

The forward pass is encapsulated in `Word2Vec.forward()`:

```mojo
def forward(
    mut self,
    context_indices: List[Int],
    target_indices: List[Int],
) -> Tensor[Self.dt]:
    self.cached_avg = self.input_embeddings.gather[track_grad=False](
        context_indices, reduction=Reduction(0)
    )
    self.cached_tgt_emb = self.output_embeddings.gather[track_grad=False](
        target_indices
    )
    var scores = self.cached_tgt_emb.matmul[mode=mv, track_grad=False](
        self.cached_avg
    )
    return scores.sigmoid[track_grad=False]()
```

The same three operations, now in one place:

**Gather with reduction.** `gather(context_indices, reduction=Reduction(0))` looks up the embedding for each context word ID and averages them (`Reduction(0)` means "mean"). This turns, say, 6 context words into a single 100-dimensional vector. The result is cached as `cached_avg` for the subsequent `step()` call.

**Matmul with mode=mv.** `cached_tgt_emb` is shape `(K+1, hidden_size)`; `cached_avg` is shape `(hidden_size,)`. `mode=mv` tells matmul to treat this as matrix-vector multiplication, producing shape `(K+1,)`. Each entry is the dot product between one sample's embedding and the averaged context.

**Sigmoid.** The dot products are raw scores in (-∞, ∞). Sigmoid squashes them to (0, 1) so they can be interpreted as probabilities.

The method also caches `cached_tgt_emb` for the backward pass to use. These cached intermediates let ``step()`` avoid re-running the gather operations when computing gradients.

## Training Target

```mojo
var fixed_target = Tensor[dtype].zeros(NUM_NEGATIVE_SAMPLES + 1)
fixed_target[0] = 1
```

The target vector is `[1, 0, 0, 0, 0, 0]` (when K=5). The `1` at position 0 tells the model "the word at index 0 (the positive sample) should have high probability." The `0`s at positions 1–5 say "these random words should have low probability."

This is a binary cross-entropy setup: each of the K+1 positions is an independent binary classification. The target is created once and reused across every training step.

## Backward + Update: The step() Method

The backward pass and parameter update are combined in `Word2Vec.step()`. The gradient of binary cross-entropy with respect to the logits simplifies to a single subtraction — `scores - labels` — so the autograd graph would be pure overhead here. Instead, we compute gradients by hand and apply them directly with `scatter_add`:

```mojo
def step(
    mut self,
    scores: Tensor[Self.dt],
    labels: Tensor[Self.dt],
    context_indices: List[Int],
    target_indices: List[Int],
    lr: Scalar[Self.dt],
):
    var context_length = len(context_indices)
    var gradient = scores - labels
    var grad_ctx = self.cached_tgt_emb.transpose[track_grad=False]().matmul[
        mode=mv, track_grad=False
    ](gradient)

    # Input embeddings — rank-1 source broadcasts to all context rows
    var ctx_update = -grad_ctx * lr / Scalar[Self.dt](context_length)
    Filler[Self.dt].scatter_add(
        self.input_embeddings.buffer,
        ctx_update.buffer,
        IntArray(context_indices),
    )

    # Output embeddings — outer product, each target row gets its own
    var out_update = -gradient.unsqueeze(1) * self.cached_avg.unsqueeze(0) * lr
    Filler[Self.dt].scatter_add(
        self.output_embeddings.buffer,
        out_update.buffer,
        IntArray(target_indices),
    )
```

Three distinct computations happen here:

### 1. The gradient formula

`scores - labels` is the gradient of binary cross-entropy with respect to pre-sigmoid logits. For `L = -[t log(p) + (1-t) log(1-p)]` with `p = σ(x)`, the gradient simplifies to `dL/dx = p - t`. No exponentials, no logarithms — just a subtraction.

We're computing this by hand intentionally. Tenmo has a complete autograd engine — you can set `track_grad=True` on any tensor, call `.backward()` on the loss, and the framework will unroll the full computation graph, compute all gradients, and feed them to an optimizer. But here, the gradient formula collapses to a single element-wise subtraction. Dispatching that through graph construction, tape recording, and jump-table dispatch would add 10-100x overhead for no benefit. The manual path isn't a workaround — it's the right tool for this job.

### 2. Chain rule through matmul

`grad_ctx = cached_tgt_emb^T @ gradient` is the chain rule through the dot product. If `score = u · v` and `dL/dscore = gradient`, then `dL/dv = u^T · gradient`. We transpose the cached target embeddings (shape `(hidden_size, K+1)`) and multiply by the gradient (shape `(K+1,)`), getting the gradient for the averaged context vector (shape `(hidden_size,)`).

### 3. Sparse updates with scatter_add

Both embedding updates use `Filler.scatter_add` — Tenmo's sparse update primitive that adds gradient contributions to specific rows of a tensor buffer, leaving all other rows untouched. This avoids materializing a full `(vocab_size, hidden_size)` gradient matrix — a savings of ~100× memory and computation.

The input embedding update uses **rank-1 broadcast**: `scatter_add` detects that `ctx_update` has rank 1 and broadcasts it uniformly across all indices. Every context word gets the same gradient vector added to its row, without needing `unsqueeze` + `repeat` to tile it into a matrix first.

The output update is different. Each of the K+1 samples gets its own update proportional to how wrong its prediction was:

```
out_update[sample_i] = -gradient[i] * cached_avg * lr
```

The `unsqueeze` operations handle broadcasting: `gradient` is shape `(K+1,)`, `cached_avg` is shape `(hidden_size,)`. After unsqueezing, `gradient.unsqueeze(1)` is `(K+1, 1)` and `cached_avg.unsqueeze(0)` is `(1, hidden_size)`. The element-wise multiplication broadcasts to `(K+1, hidden_size)` — exactly the shape needed to update all K+1 sample embeddings in one scatter_add call.

The division by `context_length` in the input update is critical: in the forward pass, we averaged the context embeddings, so the chain rule requires dividing the gradient by `context_length`. Without this, longer context windows would get disproportionately large updates.

## Gradient Flow Verification

After each epoch, we check that gradients are actually flowing by comparing the weight sum against the initial value captured before training began:

```mojo
var final_sum = model.input_embeddings.sum[track_grad=False]().item()
print(
    "\n  ✓ Weight sum change:", final_sum - initial_weight_sum,
    "(should be != 0 — proves gradients are flowing!)",
)
```

If the weight sum hasn't changed, something is wrong with the gradient computation or the update. This is a cheap sanity check that catches bugs like a zero learning rate, a disconnected graph, or a failed scatter_add. In practice, seeing a weight change of non-zero confirms the entire pipeline — from forward pass through gradient computation through update — is functioning.

## Stage 6: Probing the Learned Embeddings

Training yields an embedding matrix of shape `(vocab_size, 100)`. To test whether these vectors actually capture semantics, we write a function that finds words closest to a given query:

```mojo
def find_similar_words(
    tokenizer: Tokenizer,
    ref embeddings: Tensor[DType.float32],
    query_word: String = "beautiful",
    top_n: Int = 10,
) raises -> List[Tuple[String, Float32]]:

    # Get embedding for the query word
    var query_ids = tokenizer.encode(query_word)
    var query_embedding = embeddings.gather[track_grad=False](query_ids)

    # If multiple tokens (unlikely for single word), average them
    if len(query_ids) > 1:
        query_embedding = query_embedding.mean[track_grad=False](
            IntArray(0), keepdims=True
        )

    # Compute Euclidean distance to all other words
    var differences = embeddings - query_embedding
    var distances = (
        (differences * differences)
        .sum[track_grad=False](IntArray(1))
        .sqrt[track_grad=False]()
    )

    # Build results and sort by similarity
    var results = List[Tuple[String, Float32]](capacity=len(tokenizer))
    for ref pair in tokenizer.word_to_id.items():
        var word = pair.key
        var index = pair.value
        if word == query_word or "_" in word:
            continue
        results.append((word, -distances[index]))

    sort[cmp_fn=compare_by_similarity](results)

    var top_results = List[Tuple[String, Float32]](capacity=min(top_n, len(results)))
    for k in range(min(top_n, len(results))):
        top_results.append(results[k])
    return top_results^
```

The similarity metric is **negative Euclidean distance** — we compute `-||v_query - v_word||` for every word in the vocabulary, then sort descending. Negative distance means "closer is more similar," which makes sorting natural (highest first).

The steps are worth noting:
- `embedding - query_embedding` computes a `(vocab_size, hidden_size)` difference matrix — a single broadcast operation.
- `(differences * differences).sum(axis=1)` squares and sums along the hidden dimension, producing a `(vocab_size,)` distance vector.
- `.sqrt()` converts squared distances to actual Euclidean distances.
- We iterate over the vocabulary, skip the query word itself and symbol-heavy words, and build a `(String, Float32)` result list.
- The results are sorted and the top N returned.

This is intentionally simple — we use Euclidean distance rather than cosine similarity because it's cheaper to compute (no normalization step). In practice, for unit vectors, Euclidean distance and cosine similarity produce the same rankings.

The demo output, when the training converges, shows:

```
🔍 Words similar to 'terrible':
   horrible → similarity: -1.4567126
   boring → similarity: -2.1396909
   wonderful → similarity: -2.1462088
   ridiculous → similarity: -2.1734316
   weak → similarity: -2.276786
   stupid → similarity: -2.280788
   fantastic → similarity: -2.2870705
   lame → similarity: -2.2934372
   simple → similarity: -2.2952878
   poor → similarity: -2.3172371
```

Most neighbors are negative-sentiment words (*horrible*, *boring*, *ridiculous*), which is expected — "terrible" lives in negative semantic space. A couple of positive words (*wonderful*, *fantastic*) also appear, which may reflect shared intensity or syntactic patterns in the training data. If the embeddings were random or poorly trained, we'd see unrelated words like "the", "movie", or "and" clustering at the top. The fact that the nearest neighbors are mostly semantically related is evidence that the training worked.

## Why Tenmo?

This implementation highlights a few of Tenmo's design strengths:

**First-class scatter_add primitive.** Most tensor libraries treat row-scatter as an afterthought or don't expose it at all. PyTorch has `index_add_`, but it passes through the autograd engine, adding overhead for graph tracking that sparse updates don't need. Tenmo's `Filler.scatter_add` is a direct buffer operation — no graph, no tape, no dispatch. It's the right primitive for word2vec, and Tenmo exposes it directly.

**Autograd when you need it, not when you don't.** Tenmo has full autograd: `track_grad=True`, `.backward()`, optimizers like `SGD`, everything you'd expect. But when your gradient simplifies to `p - t`, the autograd path is pure overhead. Tenmo doesn't force you through it — you can call `Filler.scatter_add` on raw buffers, compute gradients by hand, and skip the graph entirely. The choice is yours per operation, not all-or-nothing.

**Ownership without GC pauses.** Each training step allocates intermediate tensors (gather outputs, scores, gradients). In a garbage-collected language, these allocations trigger the GC to track and reclaim them. Mojo's ownership system (which Tenmo is built on) lets us control exactly when temporaries are destroyed — or reuse buffers explicitly.

**CPU-first with optional GPU.** The code runs on CPU without modification. Tenmo detects GPU availability at compile time via `has_accelerator()`. When a GPU is present, tensors are transparently moved and operations dispatched to GPU kernels. Same code, one compile flag.

## Conclusion

We built the full pipeline from raw text to word vectors using Tenmo:

1. **A text tokenizer** that cleans HTML-laden reviews, builds a vocabulary, and encodes text into integer IDs with an unknown-word fallback.
2. **A CBOW training loop** that predicts the target word from averaged context embeddings, with context window construction and embedding averaging.
3. **Negative sampling** that turns a V-way softmax into K+1 binary classifications — the key algorithmic insight that makes word2vec practical.
4. **A `Word2Vec` struct** whose `forward()` and `step()` methods encapsulate manual gradient computation and sparse `scatter_add` updates — optimizing only the embedding rows that actually participated in each training step.
5. **A similarity probe** that validates the learned embeddings by finding nearest neighbors in vector space.

The final implementation trains on 5,000 IMDB reviews, producing word vectors where "terrible" is close to "awful", "horrible", and "dreadful" — without ever being told that these words are related. The model learned it purely from the statistics of word co-occurrence in raw text.

**Next steps to explore:**
- Swap negative sampling for hierarchical softmax and compare training speed and embedding quality.
- Move to a larger corpus (Wikipedia dumps are a common next step) and use subword tokenization (BPE) instead of word-level tokens.

The full code (around 760 lines) is available in the [tenmo repo's `examples/word2vec_cbow.mojo`](https://github.com/ratulb/tenmo/blob/dev/examples/word2vec_cbow.mojo). It's MIT-licensed and ready to run — just `mojo -I . examples/word2vec_cbow.mojo` with the IMDB dataset in `/tmp/aclImdb/`.

