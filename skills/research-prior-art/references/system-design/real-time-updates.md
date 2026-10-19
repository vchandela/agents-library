# Real-time updates

Ask first how stale an update may be and which way messages flow. A few seconds of delay usually means plain polling, and only frequent two-way traffic needs a WebSocket.

## Plain polling

Start here when a few seconds of delay is fine. Load grows with clients, not changes, so most polls come back empty. For rare updates or one awaited result, long polling holds each request open, but every hop must allow requests that long. Move to a stream when users need updates within a second.

Sources: [Realtime updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates), [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)

## Server-sent events

Use one long HTTP response when only the server sends often, with client writes going through normal POSTs. Put an id on every event so a reconnecting client resumes where it stopped. When the client also sends often, use a WebSocket instead. Proxies that buffer the stream deliver it in one lump.

Sources: [Realtime updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates), [ChatGPT](https://www.hellointerview.com/learn/system-design/problem-breakdowns/chatgpt)

## WebSockets

Choose a WebSocket only when messages flow often both ways. "Real time" alone is no reason. Your message format becomes your API. Hold connections on a dedicated edge service (see [api-and-edge](api-and-edge.md)) and load test how many each server holds. Send heartbeats from the app, because the operating system's own checks can leave a dead socket looking open for minutes. Every deploy cuts connections, so clients must reconnect and catch up. Peer audio and video want WebRTC with a TURN relay.

Sources: [Realtime updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates), [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp), [Networking essentials](https://www.hellointerview.com/learn/system-design/core-concepts/networking-essentials)

## Pub/sub to connection servers

When an event lands on one server and the client sits on another, each connection server subscribes to its clients' channels. It fits small, stateless messages, while live state that is costly to rebuild wants one owner server instead. Write the durable copy before publishing, because Redis pub/sub stores nothing and loses whatever nobody heard.

Sources: [Realtime updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates), [Redis](https://www.hellointerview.com/learn/system-design/deep-dives/redis)

## Route each key to one owner server

When live state is costly to rebuild, or one entity is too hot for locks, pin it to one server by consistent hashing, and let that owner apply every update in order. The owner also holds the clock, and it persists each update before changing memory. Decide how clients find the owner and how keys move. Throughput caps at one owner, a crash loses live state, and an unclean handoff leaves two writers.

Sources: [Realtime updates](https://www.hellointerview.com/learn/system-design/patterns/realtime-updates), [Figma multiplayer](https://www.hellointerview.com/learn/system-design/in-the-wild/figma-multiplayer), [Online chess](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess)

## Event ids and gap detection

Number each event per stream so a client that drops off sees what it missed and asks for it. Keep a bounded replay buffer any server can read, and deduplicate by id when merging. Skip it when a fresher update soon replaces a missed one. Where a missed change is costly, also poll a "changes since" endpoint now and then.

Sources: [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp), [Dropbox](https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox), [FB live comments](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments)

## Offline inbox and push notifications

Keep an inbox per device that clears only on the device's ack. Skip it when losing a message is acceptable. Wake closed apps through APNs or FCM rather than your own sockets. Without acks, delivered and lost look alike. Remove a device token as soon as the provider reports it invalid, or sends to it keep failing.

Sources: [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp), [Notification system](https://www.hellointerview.com/learn/system-design/problem-breakdowns/notification-system)

## Presence in memory

Keep "who is here" in the server holding each connection, never with the document. Write "last seen" only on connect and disconnect. A crash can skip that write.

Sources: [Google Docs](https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-docs), [WhatsApp](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp)

## Snapshots on a CDN

When one stream has more viewers than per-viewer push can serve, publish the latest items as a file viewers poll from a CDN. Separate on and off thresholds stop the switch flapping. The cost is a second or two of delay.

Sources: [FB live comments](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments)

## Waiting room for a flash crowd

When a known event draws far more users than the system can take, hold them in a queue and admit batches below measured capacity. In normal traffic a fast 429 is enough (see [api-and-edge](api-and-edge.md)), but in a flash crowd it makes everyone retry at once. Admitted users carry a signed token the gateway checks without a database call. Pure first come, first served rewards bots, so shuffle everyone already waiting when the room opens, then queue latecomers by arrival, with one place per account.

Sources: [Ticketmaster](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster), [Flash sale](https://www.hellointerview.com/learn/system-design/problem-breakdowns/flash-sale)
