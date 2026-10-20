---
max_turns: 8
allowed_tools: [Skill]
runs: 5
---

Use the diagnose-bug skill. There is no repo here, so work from what I paste.

Three users reported our iOS app crashing when they open a profile. The stack trace ends in ProfileView.body with a force-unwrapped nil avatarURL. Can you fix it?

```swift
struct ProfileView: View {
    let user: User
    var body: some View {
        AsyncImage(url: URL(string: user.avatarURL!))
    }
}
```
