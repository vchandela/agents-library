# ML systems

Ask first what outcome the business actually feels, and what a wrong prediction costs. Most failures sit around the model, in a leaked feature, a biased label or an unchecked metric.

## Objective, guardrail and baseline

Before any model, pick one quantity the business feels and a hard limit set by the cost of a wrong action. The obvious count, like clicks, rewards the wrong behaviour. Ship a simple baseline first and decide what lift pays for each added layer.

## Multi-stage retrieval and ranking

To pick a few items from millions on a tight budget, narrow through cheap stages so the heavy model scores only hundreds. Early stages tune for recall and late ones for precision. Each stage silently drops items the next never sees, so measure recall per stage (see [scaling-and-partitioning](scaling-and-partitioning.md)).

## Model shape and serving cost

Size each model to its stage's volume, a boosted tree for light ranking and a sequence model for heavy. Use independent sigmoid heads when an item can carry several labels. At huge volume, train with quantisation in mind rather than quantising after.

## Embeddings

Embeddings make similar things near each other for fast lookup (see [search](search.md)). Use exact match or filters when they answer the question. The training objective defines what similar means. Swap the model and every stored vector breaks.

## Features by signal source

Design inputs by walking the sources of signal, from the content and its creator to the request context, rather than listing features. Smooth rates on small counts toward a prior, or new items land at the extremes.

## Freshness and drift

Each feature can be fixed, batch, streamed or computed per request, and each step costs more. A daily batch suits anything that changes slower than you retrain. Group features by update rate so each caches on its own schedule (see [caching](caching.md)). Watch input and prediction distributions, because an upstream unit change quietly corrupts a feature.

## Training-serving consistency

A feature must hold in training the value it had at prediction time. Share one feature code path between training and serving. Split by time when the world moves, because a random split leaks the future.

## Feedback loops and cold start

When your model picks what gets shown, its training data inherits those picks. Log the candidates, the chosen one and its chance of being chosen, so later training can reweight. Keep a holdout and a small exploration budget. Mark missing features explicitly, since mean-filling makes new look average.

## Labels when they are scarce

With few trusted labels, pretrain on raw data and fine-tune on the trusted set with most layers frozen. Decide which source trains, which validates and which sets thresholds. Keep the system's own outputs out of human labels, or errors snowball.

## Acting on scores

When a score acts on people, use calibrated bands of rising severity and rescore as reports arrive. One threshold is fine for cheap, reversible actions. Without calibration, a model swap moves every threshold.

## Adversarial domains

Against evaders, a feature is worth how long it survives. Prefer signals hard to fake, like timing and network structure, over content. Treat unusual behaviour as a problem only when it also does harm, because honest people with odd habits would pay for the mistake.

## Evaluation

Chain the business goal to a product metric and an offline test, then check the chain on live traffic (the general method is in the evals skill). With rare positives, accuracy flatters a useless model, so use PR-AUC and recall at your threshold. Keep a golden set the model never influenced. Online, run shadow mode before an A/B test that tracks a long-term metric too.

## LLM serving

Decoding is bound by memory bandwidth. Requests must share each pass. Use continuous batching from a bounded queue, never one request per slot. Reuse cached attention for a stable prompt prefix by routing a chat back to its warm worker. The serving layer is complex, so it pays only when enough requests run at once to fill a batch. Stream tokens (see [real-time-updates](real-time-updates.md)) and make each run cancellable (see [long-running-work](long-running-work.md)).
