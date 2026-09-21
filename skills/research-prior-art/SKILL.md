---
name: research-prior-art
description: Use when you are about to design something and want to know how other companies or projects already solved it. Not for reading one specific repo; that is understand-codebase.
---

# Research prior art

Designing from first principles is good. Designing from scratch, when five companies have already published how they did it, is waste.

## Where to look

Engineering blogs, conference talks, papers, postmortems, and the source itself. Individual authors on Substack and Medium as well as company blogs: an engineer writing about what broke is usually more useful than a company writing about what shipped.

Search for the problem, not the product name. "How X does Y" finds marketing. "Y at scale" and "Y postmortem" find engineering.

## What to bring back

For each source: what they built, the constraint that forced it, and what it cost them. A design without its constraint does not transfer, because you probably do not have that constraint.

Prefer diagrams and concrete numbers. Note the date. Distributed systems advice from 2015 was written for different hardware and different prices.

## Say what you did not find

If three searches found nothing, say so plainly. **An empty result is information**, and reporting silence as though it were validation is how a design gets called novel when it is actually unexamined.

## Output

A short list of approaches, each with its constraint, its cost, and a link. Then one paragraph on which parts apply to the problem at hand and which do not.

## Done when

Every approach names the constraint that forced it, every claim has a link, and the gaps are stated as gaps.
