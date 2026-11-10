# Verifying generated answers

A generated answer bank is a set of rows where each row has a stem, options and a key. The stem is the question text. The key is the correct answer. An agent writes the rows. The person who will use the bank needs evidence that the keys are right. These six rules come from the GP Rating question banks built on 9 and 10 November 2026. GP Rating is a merchant navy pre-sea course. The rules apply to any set of generated answers that a person will rely on.

## Contents

- A second person solves every row blind
- Freeze the batch before review
- Say supports or coverage, never a heading
- Confidence is a person's decision
- Two checkers, and a planted defect for every gate
- Normalise without changing meaning
- The rates that justify the rules
- Done when

## A second person solves every row blind

The reviewer answers each row from the stem and options only. The reviewer never sees the key. The reviewer exports the sheet, not the author, so the second answer is independent. A mismatch is fixed in the questions file, never in the answers file.

**Measured:** the 120-row English bank agreed 120 of 120. Mock 1 agreed 200 of 200 on three versions. The blind pass also found what the structural checks could not. In the 120-row reasoning bank it found two wrong keys and one ambiguous row. The sources are the GP practice plan, the GP mock 1 plan and review gp-practice (10 November 2026).

## Freeze the batch before review

When a batch goes to review, hash-pin the questions, the notes, the blind sheet and the manifest. A hash-pin records a hash of each file, so a later reader can tell the file did not change. Change nothing until the verdict. Any change means a fresh export and a fresh solve. This stops the target moving under the reviewer and lets a later reader reproduce the verdict.

**Measured:** mock 1's frozen v4 pair produced `SHA256SUMS` and `PROVENANCE` for 200 rows (GP mock 1 plan, "Frozen batches").

## Say supports or coverage, never a heading

Every factual row declares one of two citation types. A `supports` row quotes an exact sentence from a named primary source, with the locator and the quoted words. A `coverage` row is heading-level textbook knowledge. Its stem and explanation may carry no digit or regulatory marker. A heading is never a support.

**Measured:** mock 1's audit found 11 supports and 89 heading-only rows. 31 of the 89 were regulatory or numeric and had to be sourced or rewritten; 58 stayed coverage (GP mock 1 plan, 10 November 2026).

## Confidence is a person's decision

Agents write every row at `confidence=low`. The blind pass and the strict checks are the agents' evidence. Record that evidence with counts and hashes in `PROVENANCE`. That file records how the batch was made and checked. Add the line "agent checks passed; person approval pending". A person, the owner or a domain expert, reads a seeded sample sheet and sets `confidence=high`. The seed is recorded, so the sample is not chosen by the writer. That is a separate commit, at the time of the production load. An agent that flips the column bypasses the approval that `low` exists to force.

**Measured:** both GP banks did this wrong and reverted. The commits `64afeddb` and `16527b15` are titled "fix: agent checks do not raise confidence". Mock 1's flip and revert are `6321a3fd` and `bed7a965` (GP git history, 10 November 2026).

## Two checkers, and a planted defect for every gate

The writer's script and an independent checker written by the reviewer are two implementations. A writer's "0 failures" is never accepted alone. Every gate is proven by a planted defect. A planted defect is a deliberate fault in a test input, and the gate must catch it. A gate nobody has seen red is not known to work.

**Measured:** the reviewer's strict substring check found a paraphrase inside quotation marks (`coswp_manual`). It also found two quotes that failed only on list-bullet glyphs, rows 001 and 070. The writer's sweep passed all three. The strict check found 98 of 100 quotes contiguous (review gp-mocks, PR #127, 10 November 2026).

## Normalise without changing meaning

A duplicate check must preserve operators and signs. To normalise two texts is to reduce them to a common form before comparing them. One check stripped non-alphanumerics, merged `x²+y²+6x` with `x²+y²−6x`, and reported 25 duplicate groups. An independent check found 0. Match exactly after lowercasing and whitespace collapse, and keep a planted sign pair that must pass as distinct.

**Measured:** the 25-group claim was withdrawn. A check that stripped punctuation faked 17 groups on the 3,000-row IMU bank. Every group was a sign or radical difference, such as `+6x` against `−6x` or `√2` against `2`. The sources are review gp-practice, session `0004eabb`, and the review gate checklist of 10 November 2026.

## The rates that justify the rules

Typed keys in a computed-family bank were wrong 2.5 to 4.4 percent of the time before a self-check. A computed-family row is one whose answer can be calculated from the stem, such as an arithmetic or reasoning puzzle. The reasoning bank alone had 3 wrong or ambiguous rows in 120, a 2.5 percent miss rate. Generate the key from the same data that renders the stem. Then the key cannot disagree with the stem. Keep only the genuinely verbal or non-verbal rows typed.

**Measured:** 3 of 120 reasoning rows, 2.5 percent (review gp-practice, 10 November 2026). The 4.4 percent top of the range is the week's measure across the computed-family banks.

## Done when

- Every row has a second answer from a reviewer who never saw the key, and every mismatch is resolved in the questions file.
- The reviewed batch is hash-pinned, and no row changed after the export.
- Every factual row says `supports` or `coverage`, and no heading is used as a support.
- Every row is `low` until a person reads a seeded sample and sets it `high` in a separate commit.
- A second checker exists, and every gate has a planted defect that was seen red.
- Duplicate matching keeps operators and signs, with a planted sign pair that stays distinct.
- The rate of wrong typed keys is measured, and computed families generate their keys from the stem's data.
