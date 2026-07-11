---
title: "Attention Is (Almost) All You Need: What Reversing and Sorting Digits Taught Me About Transformers"
date: "2026-07-09"
categories: ["Machine Learning"]
tags: ["transformer", "attention", "mojo", "neural-networks", "from-scratch"]
excerpt: "Building minimal transformers for sequence reversal and sorting — and discovering that what fixes one architecture's instability doesn't transfer to the other. A journey through attention, gradient noise, and the realization that 'Attention Is All You Need' was never a recipe."
---

A few weeks ago I stumbled on [ATTN-11](https://github.com/dbrll/ATTN-11) — a working transformer, hand-written in PDP-11 assembly, running on 1970s hardware. One self-attention layer. One head. No feed-forward network. No decoder. It learns to reverse 8-digit sequences in about 5 minutes on actual PDP-11 silicon, hitting 100% accuracy.

My first reaction was: *wait, that's it?* No stack of 96 layers, no multi-head attention, none of the machinery that makes GPT-anything expensive to train? Just attention and a projection. The whole thing is 1,216 parameters — fewer than a single convolutional filter in ResNet-50.

Which raises an obvious, slightly heretical question:

<span class="highlight-idea">Is the transformer just a fancy wrapper around one simple idea — and everything else is decoration?</span>

I decided to find out, by building the smallest possible attention models for two tasks and seeing exactly where the minimalism breaks.

(All code is in Mojo, using the [Tenmo](https://github.com/ratulb/tenmo) tensor library. The two example files are [`examples/reverse_sequence.mojo`](https://github.com/ratulb/tenmo/blob/dev/examples/reverse_sequence.mojo) and [`examples/sort_sequence.mojo`](https://github.com/ratulb/tenmo/blob/dev/examples/sort_sequence.mojo).)

---

## Round 1: Reversal, the Easy Case

Reversal is a deceptively perfect task. `[1,2,3,4,5]` → `[5,4,3,2,1]`. The rule is dead simple: whatever's in position *t* belongs in position *T-1-t*, regardless of what digit is there.

I built the minimal thing that could possibly work: token embeddings, positional embeddings, one self-attention layer, and a linear projection to the vocabulary followed by softmax. No feed-forward block. No decoder — the whole sequence gets predicted in parallel, one shot. 2,000 training samples. 10 epochs.

It converged to 100% sequence accuracy in **three epochs**. On a modern CPU, the whole training run finishes in about 4 seconds.

I went into this expecting the minimal approach to hit some wall — that you'd need *something* extra, a feed-forward layer or proper multi-head attention or at least a normalization trick. But no. One hop of attention, no scaffolding, and the model reverses sequences perfectly in three epochs.

---

## The Wrinkle: Position Isn't Enough

Then I asked a nastier question. Reversal is *purely* about position — so could you throw away the token embeddings entirely and just feed the model positional information?

No. Without token embeddings, every input sequence looks identical to the model — `[pos 0, pos 1, pos 2, ...]` — because nothing encodes *which digit* lives where. The model can only ever learn to output some fixed constant sequence.

This clarified something: attention isn't magic, it's a **routing** operation. It answers "which position should I copy from?" — but something else has to supply the *payload*. Position embeddings tell you where to look. Token embeddings tell you what's there. You need both.

<span class="highlight-idea">Attention is the router.</span> It's not the whole information pathway.

---

## The Plot Twist: It Doesn't *Always* Work

I was feeling pretty smug at this point. Then I tried a different random seed.

10/10 seeds converged. Then 20/20. Then seed 21: stuck at 35% sequence accuracy. Seed 22: fine. Seed 23: stuck at 40%. I ran 100 seeds and found the pattern: **about 6% of seeds fail to converge**, plateauing at 30-40%. The model settles on per-position token statistics instead — a brittle memorization that doesn't generalize.

Why? At initialization, Q and K are random and attention is near-uniform — every position attends equally to every other. The initial gradient is zero-mean noise, and each batch pushes attention in a random direction. In ~94% of seeds, this random walk finds the anti-diagonal pairing. In ~6%, it settles into a self-reinforcing wrong pattern the gradient can't escape.

The minimal transformer *almost* works. "Almost" is not the same as "works."

---

## The Fix: Two Heads as Insurance

The root cause: one head, one Q/K pair, one random walk. If that walk goes wrong, there's no backup.

The fix: give the model **two independent attention heads**[^1], each with its own Q, K, and V projections. Two independent gradient pathways. The outputs are averaged.

If each head has a ~6% chance of getting stuck, the probability of both failing simultaneously is ~0.36%. Over 50 seeds, that gave 100% convergence — every run hit 100% accuracy between epochs 4 and 10.

I also made one deliberate choice: **no residual connection**. A residual shortcut would let the output layer bypass attention and learn per-position patterns — exactly the memorization we're preventing. Without it, the model is forced to develop real routing behavior.

One more finding: D_MODEL matters. ATTN-11 uses 16 dimensions per head, but at 16 the model still failed. Bumping to 32 per head was the sweet spot.

**Final architecture**: 1 layer, 2 heads, D_MODEL=32, no residual, SGD with momentum and an LR schedule (0.01 → 0.002 after epoch 8). ~8K parameters. 100% reliability over 50 seeds.

---

## Round 2: Sorting, the Task That Fights Back

Reversal's rule is baked into geometry, not data. Sorting is different: `[7, 2, 9, 2, 5]` → `[2, 2, 5, 7, 9]`. The correct output slot depends on *comparing every value against every other*. The routing has to be computed fresh from content, every time.

My prediction: attention computes similarity (Q·K), but sorting needs *comparison* ("is this bigger?"), which similarity doesn't express. I expected a feed-forward sublayer.

I built a two-layer version — same minimal ingredients stacked twice, zero feed-forward layers — and trained it on 8-digit sequences with duplicates.

Final result: **99.8% sequence accuracy.** No FFN required. My prediction was wrong.

---

## The Oscillation Is the Real Story

The final number undersells how much messier this was. Sequence accuracy climbed... then face-planted, repeatedly:

- Epoch 7: 82.0% → Epoch 8: 73.3%
- Epoch 20: 99.4% → Epoch 21: 69.8%

...before stabilizing near 99.8% by epoch 23. Twenty-three epochs (~3 minutes at D_MODEL=32) versus reversal's few seconds. Sharp regressions, recoveries, more regressions.

That oscillation — not the final number — is the real tell that sorting is a fundamentally harder optimization problem, even when the "solving" architecture is still tiny. The model passed generalization tests on all-0, descending, and repeat-cluster inputs — it really learned to *sort*, not memorize.

---

## What Actually Made Sorting Hard

My instinct that sorting needs "more machinery" was right, but I had the wrong axis. I assumed a *type* of layer (feed-forward). What actually mattered was **depth** — one more round of the same computation.

Two stacked attention layers turn out to be enough to approximate something comparison-like. The first layer gathers relational info ("look around"), the second acts on it ("place yourself"). One hop for context, one for action.

I ran a grid to see what actually mattered:

| Configuration | Sequence Accuracy |
|---|---|
| **2 layers, residual** | **99.9%** |
| 2 layers, residual + Pre-LN | 98.3% |
| 2 layers, no residual | 94.9% |
| 1 layer, 2 heads (reversal's architecture) | 90.9% |
| 1 layer, 1 head | 18.5% |

Residual matters here (unlike reversal) — token identity needs to survive two layers. Pre-LN adds nothing at this depth. Two heads can't substitute for depth — the bottleneck isn't gradient noise, it's needing two rounds of reasoning.

---

## The Rule of Thumb

**Is the correct output position a fixed function of input position, or does it depend on comparing elements against each other?**

| | Reversal | Sorting |
|---|---|---|
| Layers | 1 | 2 |
| Heads per layer | 2 | 1 |
| Residual | No | Yes |
| D_MODEL | 32 | 32 |
| Parameters | ~8K | ~7K |
| Epochs to converge | 4-10 (median 6) | ~23 |
| Reliability | 100% (50 seeds) | 95.9-100% (10 runs) |

The "attention is all you need" framing survives, but with two asterisks: it's true for how information gets *routed*, not for how much *content* or how many *rounds of routing* the task requires. Reversal needed almost nothing beyond the pure idea. Sorting needed the idea applied twice, with a bumpier road to get there.

---

## What I'm Taking Away

The transformer isn't one architecture. <span class="highlight-idea">It's a design space</span> — layers, heads, residuals, normalization, depth — and the right configuration depends on what kind of routing your task needs. Modern models (GPT, BERT, LLaMA) are specific points in this space, optimized for their data and scale. They're not universal recipes.

ATTN-11, running on a 1970s minicomputer with 32KB of memory, proved that attention alone is enough for a surprising range of tasks. Our experiments proved that the *scaffolding* around attention is task-dependent — and that finding the right configuration sometimes means letting go of your assumptions about what the problem needs.

Next up, I want to see what happens if I try to break the two-hop assumption — a task needing three rounds of relational reasoning — and see if the oscillatory-training pattern gets worse, the same, or resolves into something cleaner.

---

[^1]: Unlike standard multi-head attention, where a fixed D_MODEL is evenly split across heads — e.g. two heads of 16 dimensions each from a 32-dimensional model, keeping total QKV parameters constant. Here, each head gets the full D_MODEL=32, so the outputs are two independent attention computations that get averaged. The parameter count roughly doubles instead of staying flat.
