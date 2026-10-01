# Changelog

## [Unreleased]

### Added
- `references/research-sources.md`: the eight source types, engineering blogs to target, access workarounds, the sub-agent and fact-check prompts, the authority score, and the report shape.

### Changed
- `respect-human-attention` covers the systems a skill designs: list every human touchpoint, ask a person only when a machine can't decide, in a place they already work, with evidence attached. `write-tech-doc` and `explain-simply` now apply it.
- `explain-simply` and `write-tech-doc` add one page shape for designs with a handful of parts: problem first, a big-box map, nested layers per part, one real case through every section, and state diagrams for lifecycles. Marked as one shape among several.
- `research-prior-art` adds an exhaustive per-company sweep (inventory every post from sitemaps, feeds and GitHub before reading, then read each in full), checks that each citation points at the right page, and ends reports with numbered references and every source grouped by company, both collapsed.
- `research-prior-art` maps a whole landscape: a confirmed brief, one parallel sub-agent per source type, merge by idea, a mandatory fact-check agent, authority badges counted by organisation, and a step-by-step report.
- Skills carry real copies of `references/` instead of symlinks, so a single skill folder works on its own. `scripts/sync-references.sh` regenerates the copies, and a CI check fails when one is stale.

## [0.1.0] - 2026-09-18

### Added
- Sixteen skills, built from prompts in daily use and generalised.
- `references/handoff-protocol.md`, the rule the pipeline is shaped around.
- `references/engineering-principles.md` and `references/writing-voice.md`, each the single home for text that was previously copied into four and six prompts.
- `docs/references.md`, recording what was taken from other harnesses and what was refused.
