# Preview before publishing

**Non-negotiable.** No page is published or republished without this preview, however small the edit.

Applied by the spec, plan, plan-review and explain-simply skills. Required every time a document is published or republished.

A document that parses is not a document that reads well. Look at it the way the reader will, then publish.

## Steps

1. **Parse every diagram.** Run each Mermaid block through Mermaid's own parser (a local `mermaid` + `jsdom` script). Confirm the check fails on a known-broken diagram once, so a pass means something.
2. **Build a local preview** that renders diagrams the way the host does. For claude.ai artifacts: Mermaid in `securityLevel: 'strict'`, `useMaxWidth: false`, theme `base`. Add `<meta charset="utf-8">`.
3. **Serve it and open it in Chrome** (`python3 -m http.server --bind 127.0.0.1 --directory <a folder holding only the preview> <unusual port>`; Chrome tools can't open `file://` or scroll inside an artifact's sandboxed frame).
   Without `--bind 127.0.0.1` it serves the folder to the whole network. `curl` the page and grep for a string from your file before screenshotting: another session's server on a common port (8765) silently served a different page, and the first round of screenshots showed the wrong document.
   No Chrome tools in the session? Drive the installed Chrome with Playwright (`playwright-core` with `executablePath` set to the local Chrome), screenshot each section element, and read the screenshots back as images. Checking that the HTML parses is not a preview.
4. **Check, with a screenshot of each diagram and each table:**
   - no secrets, tokens, signed URLs, internal hostnames or customer personal data on the page;
   - at desktop width AND phone width (390 px), in light AND dark mode, with every `<details>` opened;
   - no horizontal page scroll at phone width, and no script errors in the console;
   - on a phone, wide diagrams scroll sideways at a readable size instead of shrinking to fit: the SVG has a `min-width` equal to its drawn width, inside its own `overflow-x: auto` wrapper. An `overflow: hidden` ancestor clips it with no scrollbar, and a page-overflow check still passes, so look;
   - every screenshot shows what its name claims, with nothing blank; a missing width or theme is a failed check, not a skipped one;
   - no line or label crosses a box or another label;
   - tooltips appear and are not clipped;
   - every diagram rendered (no raw source left on the page);
   - each diagram fits the page column at full size, and its text is readable;
   - labels are intact: no words run together, which is what stripped line breaks look like;
   - identifiers in tables don't break mid-word;
   - spacing between sections, tables and figures is comfortable;
   - colours work in dark mode too.
5. **Ship what you previewed.** For claude.ai artifacts, don't rely on the host's Mermaid renderer: it can fail where a local render works. Save each rendered SVG from the preview and embed it in place of the `<pre class="mermaid">` block; keep the Mermaid source in your working files for edits.
6. **Fix every defect from the round in one batch, then run one full confirming round** from step 1. A defect found then came from the batch; fix it and confirm once more. Publish only when a full round passes.
7. **Clean up:** stop the server and close the tab.

## Rules that prevent most failures

- No `;` inside Mermaid labels or messages. It ends the statement.
- No `<br/>` in labels. Strict mode strips it and runs the words together. Keep labels on one line.
- Give every diagram a full light theme (nodes, edge labels, state colours), since the page may be viewed in dark mode.
- Sequence diagrams: wrap long messages (`sequence: {wrap: true}`) and keep participants few.
- Monospace blocks are for worked examples and timelines. Tabular content goes in real tables.
