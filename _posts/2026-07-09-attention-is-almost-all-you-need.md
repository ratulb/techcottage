---
title: "Attention Is (Almost) All You Need: What Reversing and Sorting Digits Taught Me About Transformers"
date: "2026-07-09"
categories: ["Machine Learning"]
tags: ["transformer", "attention", "mojo", "neural-networks", "from-scratch"]
excerpt: "Building minimal transformers for sequence reversal and sorting — and discovering that what fixes one architecture's instability doesn't transfer to the other. A journey through attention, gradient noise, and the realization that 'Attention Is All You Need' was never a recipe."
---

# Attention Is (Almost) All You Need: What Reversing and Sorting Digits Taught Me About Transformers

A few weeks ago I stumbled on [ATTN-11](https://github.com/dbrll/ATTN-11) — a working transformer, hand-written in PDP-11 assembly, running on 1970s hardware. One self-attention layer. One head. No feed-forward network. No decoder. It learns to reverse 8-digit sequences in about 5 minutes on actual PDP-11 silicon, hitting 100% accuracy.

My first reaction was: *wait, that's it?* No stack of 96 layers, no multi-head attention, none of the machinery that makes GPT-anything expensive to train. Just attention and a projection. The whole thing is 1,216 parameters — fewer than a single convolutional filter in ResNet-50.

Which raises an obvious, slightly heretical question:

**Is the transformer just a fancy wrapper around one simple idea — and everything else is decoration?**

I decided to find out, by building the smallest possible attention models for two tasks and seeing exactly where the minimalism breaks.

(All code is in Mojo, using the [Tenmo](https://github.com/ratulb/tenmo) tensor library. The two example files are [`examples/reverse_sequence.mojo`](https://github.com/ratulb/tenmo/blob/dev/examples/reverse_sequence.mojo) and [`examples/sort_sequence.mojo`](https://github.com/ratulb/tenmo/blob/dev/examples/sort_sequence.mojo).)

---

## Round 1: Reversal, the Easy Case

Reversal is a deceptively perfect task for testing this. `[1,2,3,4,5]` → `[5,4,3,2,1]`. The rule is dead simple: whatever's in position *t* belongs in position *T-1-t*, full stop, no matter what digit is actually there.

I built the minimal thing that could possibly work: token embeddings, positional embeddings, one self-attention layer, and a linear projection to the vocabulary followed by softmax. No feed-forward block. No decoder — the whole sequence gets predicted in parallel, one shot.

The data was trivial: shuffle the digits 0-9, take the first 8, reverse them. 2,000 training samples. 10 epochs.

It converged to 100% sequence accuracy in **three epochs**. On a modern CPU, the whole training run finishes in about 4 seconds.

Watching the attention weights during training is genuinely satisfying — you can see a clean anti-diagonal pattern emerge, position 0 learning to stare directly at position 7, position 1 at position 6, and so on, until the whole attention matrix looks like a mirror.

Okay, I'll admit it: I was the heretic. I went into this expecting the minimal approach to hit some wall — that you'd need *something* extra, a feed-forward layer or proper multi-head attention or at least a normalization trick. But no. One hop of attention, no scaffolding, and the model reverses sequences perfectly in three epochs. Sometimes the simple story is the true one.

---

## The Wrinkle: Position Isn't Enough

Then I asked a nastier question. Reversal is *purely* about position — so could you throw away the token embeddings entirely and just feed the model positional information? After all, the rule doesn't care what digit is at a position, only which position it's in.

I ran this ablation and it failed completely — not "worse," but *categorically* broken. Here's why, once you think about it for two seconds: if you strip out token embeddings, every single input sequence looks identical to the model. `[0,7,4,9,5,6,8,3]` and `[8,4,1,7,9,5,3,2]` both collapse into the exact same internal representation — `[pos 0, pos 1, pos 2, ...]` — because nothing in the input encodes *which digit* lives where. The model can only ever learn to output some fixed constant sequence, because it has literally no way to know what it's supposed to be copying.

This is the part that actually clarified things for me. Attention isn't magic; it's a **routing** operation. It answers "which position should I copy from?" — but something else has to supply the *payload* being copied. Position embeddings tell you where to look. Token embeddings tell you what's actually there. You need both, and no amount of attention sophistication substitutes for the missing one.

So: attention-is-all-you-need, corrected. **Attention is the router.** It's not the whole information pathway.

---

## The Plot Twist: It Doesn't *Always* Work

I was feeling pretty smug at this point. Attention does routing, embeddings provide content, together they reverse sequences perfectly. Case closed.

Then I tried a different random seed.

10/10 seeds converged. Then 20/20. Then seed 21: stuck at 35% sequence accuracy. Seed 22: fine. Seed 23: stuck at 40%. I ran 100 seeds and found the pattern: **about 6% of seeds fail to converge**, plateauing at 30-40% sequence accuracy. The attention weights don't form the clean anti-diagonal — they settle on per-position token statistics instead. Position 0 learns "when I see a 4 here, predict a 3 there" — a brittle memorization that doesn't generalize to unseen sequences.

Why? At initialization, Q and K vectors are random. Attention is near-uniform — every position attends to every other position equally. The initial gradient for Q and K is therefore zero-mean noise, and each batch pushes the attention weights in a random direction. In ~94% of seeds, this random walk stumbles onto the correct anti-diagonal pairing within the first few epochs. But in ~6% of seeds, it settles into a self-reinforcing wrong pattern that the gradient can't escape.

I sat staring at this for a while. The minimal transformer *almost* works. "Almost" is not the same as "works."

---

## The Fix: Two Heads as Insurance

The root cause is a single point of failure in the gradient: one head, one Q/K pair, one random walk. If that walk goes wrong, there's no backup.

The fix: give the model **two independent attention heads**, each with its own Q, K, and V projections. Two independent gradient pathways. The outputs are averaged at the end.

Why two? If each head has a ~6% chance of getting stuck, the probability of both heads getting stuck simultaneously is roughly 6% × 6% ≈ 0.36%. Over 50 seeds, that gave me 100% convergence — every single run hit 100% accuracy, typically between epoch 4 and epoch 10.

*(One clarification for anyone coming from standard transformer architectures: this isn't textbook multi-head attention, where a fixed model width gets split across heads — e.g. two heads of 16 dimensions each carved out of a 32-dimensional model, with total QKV parameters staying roughly constant no matter how many heads you use. Here, each head gets its own full-width, D_MODEL=32 set of Q/K/V projections, and the two outputs are averaged. It's closer to a small ensemble of two independent attention computations than a split-width multi-head layer — which is also why the parameter count roughly doubles from the single-head baseline instead of staying flat.)*

I also made one deliberate choice that felt wrong at first: **no residual connection**. In most transformers, the residual `x = x + attention(x)` is the default. But for reversal, the gradient *must* flow through attention. A residual shortcut lets the output layer bypass attention entirely and learn per-position output patterns — exactly the kind of memorization we're trying to prevent. Without it, the model is forced to develop real routing behavior.

One more finding: D_MODEL matters. ATTN-11 uses 16 dimensions per head, but with two heads at 16 each, the model still failed (0% sequence accuracy — the Q/K space per head was too small to disambiguate the anti-diagonal). Bumping to 32 per head was the sweet spot.

**Final architecture for reversal**: 1 layer, 2 heads, D_MODEL=32, no residual, uniform embedding initialization, SGD with momentum and an LR schedule (0.01 → 0.002 after epoch 8). ~8K parameters. 100% reliability over 50 seeds.

---

## Round 2: Sorting, the Task That Fights Back

Reversal's rule never changes — it's baked into the geometry of the sequence, not the data. Sorting is a completely different animal. `[7, 2, 9, 2, 5]` → `[2, 2, 5, 7, 9]`. Now the correct output slot for a value depends on *comparing it against every other value in the sequence*. There's no fixed geometric rule to memorize; the routing has to be computed fresh, from content, every single time.

My prediction going in: attention computes similarity (Q·K, basically "how alike are these two things"), but sorting needs *comparison* (an asymmetric "is this one bigger" relation), which similarity doesn't naturally express. So I expected we'd need a feed-forward sublayer somewhere — a proper nonlinearity to actually compute "greater than," not just "similar to."

I built a two-layer version — same minimal ingredients as before (embeddings, attention, linear output), just stacked twice, still with zero feed-forward layers anywhere — and trained it on sorting 8-digit sequences with duplicates thrown in on purpose.

Final result: **99.8% sequence accuracy.** No FFN required. My prediction was wrong, in an interesting way.

---

## The Oscillation Is the Real Story

The final number undersells how much messier this training run was compared to reversal's clean victory lap. Sequence accuracy climbed steadily for a while... and then face-planted, repeatedly:

- Epoch 7: 82.0% → Epoch 8: 73.3%
- Epoch 20: 99.4% → Epoch 21: 69.8%

...before recovering and eventually stabilizing near 99.8% by epoch 23. Twenty-three epochs, roughly 3 minutes of wall-clock time at D_MODEL=32 (or 7 minutes at D_MODEL=64), versus reversal's few seconds. The final architecture is just under 27K parameters (at D_MODEL=64), but the path to get there is visibly rockier — sharp regressions, recoveries, more regressions.

That oscillation, not the final accuracy number, is the real tell that sorting is a fundamentally harder optimization problem — even when the architecture "solving" it is still tiny.

To make sure the model had actually learned to *sort* and not just memorized training patterns, I threw some deliberately weird inputs at it after training: all-0 runs (`[0,0,0,0,0,0,0,0]` — trivially sorted), a fully unique descending sequence (`[9,8,7,6,5,4,3,2]` — correctly reversed), mixed clusters of repeats (`[5,5,3,3,3,1,1,1]` → `[1,1,1,3,3,3,5,5]` — exactly right). It passed all of them. The model really did learn to *sort*, not to memorize.

---

## What Actually Made Sorting Hard

Here's the thing that surprised me: my instinct that sorting needs "more machinery" than reversal was right, but I had the wrong axis in mind. I was thinking *type* of layer — attention isn't enough, you need a feed-forward network too. What actually mattered was **depth** — not a different kind of computation, just one more round of the same computation.

Two stacked attention layers, each already containing a softmax, turned out to be enough to approximate something comparison-like. The first layer lets every token gather information about how it relates to the others ("look around"), and the second layer uses that gathered information to figure out where it belongs ("place yourself"). One hop for context gathering, one hop for action.

The feed-forward sublayer I assumed was necessary just... wasn't, at least for this task.

But depth wasn't the only variable. I ran a grid to see what actually mattered:

| Configuration | Sequence Accuracy |
|---|---|
| **2 layers, residual** | **99.9%** |
| 2 layers, residual + Pre-LN | 98.3% |
| 2 layers, no residual | 94.9% |
| 1 layer, 2 heads (reversal's architecture) | 90.9% |
| 1 layer, 1 head | 18.5% |

Key findings:

**Residual matters here** (unlike reversal). Sorting needs token identity to survive through two layers — the model needs to know both "what token is at this position" and "how it compares to others." Without a residual, per-layer information degrades and accuracy drops five points.

**Pre-LN adds no value** for this depth. At two layers, activation drift isn't severe enough to benefit from layer normalization. The normalization costs compute and introduces mild gradient interference.

**Two heads can't substitute for depth**. Reversal's winning formula (2 heads, 1 layer) gives only 90.9% on sorting. The problem isn't gradient noise — it's the need for two rounds of relational reasoning. One layer, even with multiple heads, still only does one round of attention.

---

## The Rule of Thumb

If you're trying to guess how much architecture a permutation-style task needs, here's the question that seems to matter:

**Is the correct output position a fixed function of input position, or does it depend on comparing elements against each other?**

- **Fixed function of position** (reversal) → one attention hop, plus embeddings that actually carry the input's content. Two heads for insurance against gradient noise. No residual (don't give the gradient a shortcut). D_MODEL=32. That's it.

- **Depends on comparing elements** (sorting) → at least two hops. One to gather relational info, one to act on it. Residual to preserve identity through depth. One head per layer is enough (gradient noise isn't the bottleneck here).

The two architectures side by side:

| | Reversal | Sorting |
|---|---|---|
| Layers | 1 | 2 |
| Heads per layer | 2 | 1 |
| Residual | No | Yes |
| D_MODEL | 32 | 32 |
| Parameters | ~8K | ~7K |
| Data | Permutations only | Permutations + repeats |
| Epochs to converge | 4-10 (median 6) | ~23 |
| Reliability | 100% (50 seeds) | 95.9-100% (10 runs) |

The "attention is all you need" framing turns out to survive, but with two asterisks: it's true for how information gets *routed*, not for how much *content* or how many *rounds of routing* the task requires. Reversal needed almost nothing beyond the pure idea. Sorting needed the idea applied twice, with a noticeably bumpier road to get there — and if I'd guessed the wrong reason why, I'd have wasted time adding a feed-forward layer that, it turns out, this task never asked for.

---

## What I'm Taking Away

The transformer isn't one architecture. It's a **design space** — layers, heads, residuals, normalization, depth — and the right configuration depends on what kind of routing your task needs. Modern models (GPT, BERT, LLaMA) are specific points in this space, optimized for their data and scale. They're not universal recipes.

ATTN-11, running on a 1970s minicomputer with 32KB of memory, proved that attention alone is enough for a surprising range of tasks. Our experiments proved that the *scaffolding* around attention (heads, residuals, depth) is task-dependent — and that finding the right configuration sometimes means letting go of your assumptions about what the problem needs.

Next up, I want to see what happens if I try to actually break the two-hop assumption — a task that needs three rounds of relational reasoning instead of two, and see if the oscillatory-training pattern gets worse, the same, or resolves into something cleaner with more depth to work with.
