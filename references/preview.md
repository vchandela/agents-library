# Preview before publishing

Applied by the spec, plan and plan-review skills. Required every time a document is published or republished.

A document that parses is not a document that reads well. Look at it the way the reader will, then publish.

## Steps

1. **Parse every diagram.** Run each Mermaid block through Mermaid's own parser (a local `mermaid` + `jsdom` script). Confirm the check fails on a known-broken diagram once, so a pass means something.
2. **Build a local preview** that renders diagrams the way the host does. For claude.ai artifacts: Mermaid in `securityLevel: 'strict'`, `useMaxWidth: false`, theme `base`. Add `<meta charset="utf-8">`.
3. **Serve it and open it in Chrome** (`python3 -m http.server` on 127.0.0.1; Chrome tools can't open `file://` or scroll inside an artifact's sandboxed frame).
4. **Check, with a screenshot of each diagram and each table:**
   - every diagram rendered (no raw source left on the page);
   - each diagram fits the page column at full size, and its text is readable;
   - labels are intact: no words run together, which is what stripped line breaks look like;
   - identifiers in tables don't break mid-word;
   - spacing between sections, tables and figures is comfortable;
   - colours work in dark mode too.
5. **Ship what you previewed.** For claude.ai artifacts, don't rely on the host's Mermaid renderer: it can fail where a local render works. Save each rendered SVG from the preview and embed it in place of the `<pre class="mermaid">` block; keep the Mermaid source in your working files for edits.
6. **Fix, then repeat from step 1.** Publish only when every check passes.
7. **Clean up:** stop the server and close the tab.

## Rules that prevent most failures

- No `;` inside Mermaid labels or messages. It ends the statement.
- No `<br/>` in labels. Strict mode strips it and runs the words together. Keep labels on one line.
- Give every diagram a full light theme (nodes, edge labels, state colours), since the page may be viewed in dark mode.
- Sequence diagrams: wrap long messages (`sequence: {wrap: true}`) and keep participants few.
- Monospace blocks are for worked examples and timelines. Tabular content goes in real tables.
