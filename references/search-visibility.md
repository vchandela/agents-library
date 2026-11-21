# Search visibility

What search engines read when they decide a site's name, its logo and what a page is about. Every claim here comes from the search engine's own documentation, linked at the end, not from agency blogs. The rule under all of it: there is no trick that beats being the page a person wanted.

## The site name

Google's site-name system is fully automated and picks the label it shows as the result's source. Its own words: the `WebSite` structured data is "most important".

- Put `WebSite` schema on the crawlable root homepage: `name` (the preferred name), `url` (the canonical homepage), and optionally `alternateName` with fallbacks in order of preference.
- One site name per site. Subdirectory names are unsupported, and duplicate homepages must carry identical markup.
- Other signals: `og:site_name`, the `<title>`, headings, homepage text, and references to the site elsewhere on the web.
- A different name appears when the markup is missing or inconsistent, the homepage is hard to crawl, the name is generic, or Google is not yet confident. Confidence grows with consistent, outside references.

## The organization entity

`Organization` structured data has no required fields, but the identity ones are what tie a name to profiles elsewhere.

- `name`, `alternateName`, `legalName`, `url`, `sameAs`, `logo`, `description`.
- `sameAs` lists the social, review and profile URLs for the same organization. This is how a search engine learns the accounts and the site are one entity.
- `logo` must be crawlable, at least 112 by 112 pixels, square-friendly, and suitable on white. A wide sharing image is not a logo.
- Place the block on the homepage or one about page, not every page, and use the most specific valid subtype.

## The favicon in results

- The icon beside a result is the favicon, and it must be at a crawlable URL declared with `rel="icon"` on the home page.
- Google's documented supported formats are BMP, GIF, ICO, PNG, JPEG, PPM and TIFF. It must be square, at least 8 by 8, and Google recommends larger than 48 by 48.
- A data URI is not a crawlable URL, and SVG is not in the supported list, so a data-URI SVG favicon shows a default globe.
- One favicon per hostname. It is not guaranteed to appear; an inappropriate one is replaced.

## Page titles and headings

Search engines generate the title link from several sources: the `<title>`, the main visible headline, the `<h1>`, `og:title`, prominent text, anchor text pointing at the page, and the `WebSite` data.

- Every page gets a descriptive, page-specific title, with the brand as a concise suffix and delimiter.
- One clearly dominant main heading per page. Equally prominent headings leave the machine to guess.
- No boilerplate title repeated across pages, no keyword stuffing, no year left stale.
- Blocked pages cannot be read; use `noindex` for "do not index" and robots rules for "do not crawl".

## AI answers and AI modes

The official guidance is the absence of a special lever.

- Pages appear when they are indexed and eligible for a snippet. There are no additional requirements and no special AI markup.
- The work is ordinary: crawlable pages, internal links, good page experience, important text in HTML, quality images and video, structured data that matches the visible page, and helpful, people-first content.
- Snippet controls: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`.

## What does not work

- **Coordinated votes, reviews or thumbs-up from many accounts.** It is a policy violation, the platforms are built to detect the shared-device and shared-network pattern, and the usual outcome is discounting or demotion. Spacing it out to "avoid detection" makes it deliberate manipulation.
- **Special "AI" files or markup.** None exist; anyone selling them sells nothing.
- **Keyword-stuffed pages built around a misspelling or a competitor's name.** The content policies treat it as unhelpful, and it reads as spam to a person too.
- **Expecting FAQ rich results.** Google limited them to authoritative government and health sites in 2023; keep the markup only if another consumer needs it.

## Honest limits

Entity strength compounds over time and cannot be forced on a date. The read on what actually happens is the search console's own query report: which queries show the site, which corrections the engine applies, and which page it chooses. Watch that, fix the pages it names, and repeat.

Related: [performance-frontend](performance-frontend.md) for the page-experience half, and the UI quality bar for the craft that keeps a visitor once the result is clicked.

## Sources, read in full

- Site names: https://developers.google.com/search/docs/appearance/site-names
- Organization structured data: https://developers.google.com/search/docs/appearance/structured-data/organization
- Title links: https://developers.google.com/search/docs/appearance/title-link
- AI features: https://developers.google.com/search/docs/appearance/ai-features
- Favicon in Search: https://developers.google.com/search/docs/appearance/favicon-in-search
