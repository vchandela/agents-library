# Observability

An unobserved production system cannot answer "what happened to this request". This guide is the floor: one wide event per request per service, structured and queryable, with traces carrying the same context. Source: Boris Tane, "Logging Sucks - Your Logs Are Lying To You" (https://loggingsucks.com), read 23 November 2026; the quotes below are his. The definition-level span rule, the lint check and traceparent forwarding come from the prompt Vivek pasted the same day, not from the article.

## One wide event per request per service

- Write one event per request per service hop, built through the request and emitted once at the end, in a `finally`, on success and on failure. "One log line per request that serves as the authoritative record of what happened." Stripe popularised the name, canonical log line.
- Fields, not messages. Each fact gets its own field, with one spelling across the codebase. "Structured logging is necessary but not sufficient": JSON lines that still read like a diary are still a diary.
- Aim for 50+ fields, not 5: request id, trace id, method, path, status, duration; service, version, region; user id, plan, account age; the product's own unit (order, tenant, exam, whatever the business acts on); outcome; error type, code, retriable and the provider's code; feature flags; and what the handlers learned along the way.
- Handlers add to one shared context object held on the request. They never write their own lines.
- Ask incident questions as field queries. "You're not searching logs anymore. You're running analytics on your production traffic." If an incident question cannot be asked that way, the event is missing a field.

## Levels and secrets

- Put the outcome in a field, not in the severity. Emit one event per request at info, carrying status and error, on success and on failure. Error severity is for the process being unhealthy, not for one failed request, or every 4xx reads as an outage.
- Never log secrets, tokens, passwords, full card numbers, or personal data the privacy policy does not allow. Log the identifier, not the content.

## Traces are complementary, not a substitute

- OTel is transport. "OpenTelemetry is a delivery mechanism." It does not choose what to log, and it adds no business context.
- Trace at the function definition, never inline. Every exported function that makes an I/O call gets its own span, named for the operation. An inline span inside a function body duplicates work and loses the call shape.
- A lint rule holds it. If the rule is "every exported I/O function has a span", a custom lint rule or a semgrep pattern finds the ones that do not. That is the only form that survives a busy week.
- Put the request context on every span: trace id, request id, user or tenant, the product's unit, outcome.
- The ideal: "your wide events ARE your trace spans, enriched with all the context you need".
- Read the incoming `traceparent` and pass it downstream. Never start a new trace mid-request. A broken chain turns one request into several unrelated ones.

## Sampling

- Decide after the outcome is known (tail sampling). "naive sampling is dangerous": it can drop the one request that explains the outage.
- "Always keep errors. 100% of 500s, exceptions, and failures get stored."
- "Always keep slow requests. Anything above your p99 latency threshold."
- Keep named cohorts: staff, internal test accounts, flagged sessions, the largest customers.
- "Randomly sample the rest. Happy, fast requests? Keep 1-5%."

## The first version, for a new service or endpoint

1. A request id and a trace id on every event and every span.
2. One wide event per request, emitted in a finally, on success and on failure.
3. The deployed version in every event, so a spike can be tied to a release.
4. Errors carry type, code and whether they are retriable.
5. One saved query for each incident class the product can have, written when the endpoint ships, not after the first outage.

## What this is not

- Not "we use OTel". Spans carrying name, duration and status are the bare minimum.
- Not many JSON lines per request. Thirteen structured lines are still a diary.
- Not uniform sampling.
- Not logs for debugging and metrics for dashboards. "This distinction is artificial and harmful."
- Not retention or price advice: the article gives neither. Set retention from the tool's cost model and the data's sensitivity.

## In another language

The article's code is TypeScript, and the rules do not depend on it. In Python, middleware plus a contextvar carries the shared event, and a decorator on exported I/O functions opens spans. In Go, a value on the context and a handler wrapper. The lint rule is per language: a custom rule or a semgrep pattern.

Related: the `diagnose-bug` skill when production is dark, and `references/performance-backend.md` when the symptom is slowness rather than darkness.
