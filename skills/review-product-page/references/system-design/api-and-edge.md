# APIs and the edge

Ask first who is calling, how much they can send, and what happens when they send it twice. Most mistakes at the edge come from trusting a caller or failing to bound one.

## REST for the public, gRPC between services

Use REST for a public API, with resources as plural nouns and the resource's ID in the path. Between services you own, gRPC gives typed contracts and streaming, though browsers need a proxy. Pick GraphQL only when many clients want different slices of the same data, and batch it, or each list item runs its own query. Make changes additive and version anything breaking.

Sources: [API design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design), [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)

## Methods, status codes and safe retries

Callers retry, so pick each verb for what repeating it does. GET has no side effects, and PUT or DELETE can run twice safely. A POST that moves money needs an idempotency key (see [consistency-and-concurrency](consistency-and-concurrency.md)). Never return 200 with an error flag. Browsers cache a 301, often with no expiry unless you set one, so count or change redirects with a 302.

Sources: [API design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design), [Bitly](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly)

## Pagination and bounded results

Any list that can grow returns a capped page and a cursor. Base the cursor on the last seen ID, or a timestamp paired with an ID, with a matching index. Offset paging repeats or skips items as rows arrive. A timestamp alone drops ties.

Sources: [API design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design), [News feed](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-news-feed)

## Trust at the edge

The server decides who the caller is and what the facts are. Take the user from the verified token, stamp times yourself and look prices up, then check the user may touch the record. API keys suit servers, never end users, because they carry no expiry or user. Partner calls sign each request with a timestamp and nonce so replays fail.

Sources: [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials), [API design](https://www.hellointerview.com/learn/system-design/core-concepts/api-design), [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system)

## Load balancers and stateless servers

Add a balancer when one server falls short, or when a second server is needed for failover, since health checks are what move traffic off a dead one. Keep app servers stateless so any of them can answer, since hidden state forces sticky sessions. L4 forwards TCP fast, while L7 routes on path or header at more CPU. Long-lived connections need least-connections balancing, or old servers pile them up.

Sources: [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials), [Real-time updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates)

## API gateway

A gateway gives several services one front door for auth, limits and early rejection. One service needs only a load balancer. It is a thin layer, so spend design time on the services, but run more than one, because every request passes through it.

Sources: [API gateway](https://www.hellointerview.com/learn/system-design/deep-dives/api-gateway)

## Rate limits and admission control

Keep limit counters in a shared store, because each server sees only its share. A single server can count in memory. Reject an abuser at once rather than queueing them, because queued requests hold resources and invite retries. A token bucket allows bursts, but a fixed window leaks them at its edge. Debit costly work by what it costs rather than by call count, and give each tenant on a shared backend its own bounded queue so one heavy tenant cannot starve the rest. Run increment and expiry atomically (see "Correct by construction" in [engineering-principles](../engineering-principles.md)). Limiter outages arrive with spikes, so choose fail open or closed on purpose.

Sources: [Distributed rate limiter](https://www.hellointerview.com/learn/system-design/problem-breakdowns/distributed-rate-limiter), [ChatGPT](https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt), [Meta ZGateway](https://www.hellointerview.com/learn/system-design/in-the-wild/meta-zgateway-zippydb)

## Calling dependencies that fail

Remote calls hang. Cap in-flight calls and give each dependency a circuit breaker with a fallback. Plain retries keep a recovering service down. When a provider limits you, throttle yourself with a shared counter plus jitter, or every waiting worker fires at once when the window resets. A single caller with no shared quota can skip the shared counter.

Sources: [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials), [Notification system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system)

## Polite crawling

Prefer the source's API or webhooks, since scraping breaks. When you must crawl, obey robots rules and lock a per-domain last-fetch time. Polite rates make big crawls slow, so decide what to skip.

Sources: [Web crawler](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)

## Outbound webhooks

Tell partners about async outcomes with signed webhooks, retried with growing delays (see [long-running-work](long-running-work.md)). Include an event ID, because receivers will see retries. Browsers get [real-time-updates](real-time-updates.md) instead.

Sources: [Payment system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/payment-system)

## Connections and transport

A handshake per call can cost more than the work, so reuse connections through pooling or HTTP/2. A huge client fleet should reach the database through a gateway holding few connections. Use TCP by default. Live media wants UDP, where a resent stale frame hurts more than a gap.

Sources: [Meta ZGateway](https://www.hellointerview.com/learn/system-design/in-the-wild/meta-zgateway-zippydb), [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)
