# Changelog

## [Unreleased]

### Added
- `references/research-sources.md`: the eight source types, engineering blogs to target, access workarounds, the sub-agent and fact-check prompts, the authority score, and the report shape.

### Changed
- `research-prior-art` maps a whole landscape: a confirmed brief, one parallel sub-agent per source type, merge by idea, a mandatory fact-check agent, authority badges counted by organisation, and a step-by-step report.
- Skills carry real copies of `references/` instead of symlinks, so a single skill folder works on its own. `scripts/sync-references.sh` regenerates the copies, and a CI check fails when one is stale.

## [0.1.0] - 2026-09-18

### Added
- Sixteen skills, built from prompts in daily use and generalised.
- `references/handoff-protocol.md`, the rule the pipeline is shaped around.
- `references/engineering-principles.md` and `references/writing-voice.md`, each the single home for text that was previously copied into four and six prompts.
- `docs/references.md`, recording what was taken from other harnesses and what was refused.
