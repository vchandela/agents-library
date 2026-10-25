# Amphetamine settings

Amphetamine (Mac App Store) keeps the Mac awake so coordinated sessions keep running with the lid closed. tmux does not do this: when the Mac sleeps, every session freezes. `scripts/amphetamine-settings` applies every setting below and `--check` compares a Mac against them; `scripts/setup-machine` runs it when Amphetamine is installed. Tested on 25 Oct 2026: with these settings the lid closed and macOS logged no sleep (`AppleClamshellCausesSleep = No`).

After setup, start a session from the menu bar icon: Start New Session, then Indefinitely. Keep the charger in for a long run; the session ends at 30% battery otherwise, and restarts by itself when the charger is plugged back in. Don't put the Mac in a bag while it runs closed, because it stays at full speed with no airflow.

On means ticked, off means unticked.

## General
- Quick-Start a Session: right click (left click shows menu)
- Launch Amphetamine at login: on (a login item, set in the app, not by the script)
- Start session when Amphetamine launches: off
- Start session after waking from sleep: off
- Hide Amphetamine in the Dock: on
- Reduce motion: off

## Session Defaults
- Default Duration: Indefinitely
- End Time Calculation: Use timer
- End session when Mac is forced to sleep: off
- Allow display sleep: on (saves battery, the work keeps running)
- Allow system sleep when display is closed: off (this is what keeps work running with the lid closed)
- Allow screen saver after inactivity: off
- End session if charge is below 30%: on
- Prompt before ending a session: off
- Ignore charge if power adapter is connected: on
- Start a new session if reconnected: on

## System Control
- Lock screen after 1 minute of inactivity: off
- Use cursor movement to determine inactivity: off
- Lock screen immediately after display is closed: on (the Mac stays awake and signed in, so it locks)
- Allow display sleep when screen is locked: off
- Move cursor every 1 minute after 5 minutes of inactivity: off
- Stop moving cursor after 30 minutes: off
- End session when switching accounts: off

## Triggers and Drive Alive
- Enable Triggers: off
- Enable Drive Alive: off

## Hot Keys
- No shortcuts recorded
- If a session is already running: end the session and start a new session
- Start Session with duration: Indefinitely

## Notifications
- Remind every 60 minutes: off
- Notify when trigger or scheduled sessions auto-start: on
- Notify when trigger or scheduled sessions auto-end: on
- Play with session reminders and other notifications: on
- Play when any session starts or ends: on
- Play when any session is extended: on
- Play closed-display warning tone: off
- Remove notifications after delivery: on

## Appearance
- Menu Bar Image: Pill
- Use low opacity when inactive: off
- Manually manage padding for menu bar image: off
- Show session time remaining in menu bar: off
- Show current session details: on
- Show Drive Alive details: off

## Statistics
- Enable statistics collection: on
