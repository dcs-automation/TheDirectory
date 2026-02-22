# CLAUDE.md — TheDirectory

AI-readable project context for working on this codebase.

## What this is

A personal new-tab homepage. Single HTML file frontend, Cloudflare Pages + Workers backend, KV for persistence. Local dev uses a Python server with JSON files instead of KV.

## File map

```
public/index.html          Single-page app — all HTML, CSS, and JS in one file
functions/api/notes.js     Cloudflare Worker — Notes API
functions/api/bookmarks.js Cloudflare Worker — Bookmarks API
functions/api/lists.js     Cloudflare Worker — Lists API
server.py                  Local dev server (mirrors the Workers API using JSON files)
wrangler.toml              Cloudflare Pages config + KV namespace bindings
bookmarks.json             Local dev data (not deployed)
lists.json                 Local dev data (not deployed)
notes.json                 Local dev data (not deployed, created on first save)
.env                       CLOUDFLARE_API_TOKEN — gitignored, never commit
```

## API contract

All endpoints accept and return JSON.

### Notes
- `GET /api/notes` → `{ "content": "<string>" }`
- `PUT /api/notes` body: `{ "content": "<string>" }` → `{ "ok": true }`

### Bookmarks
- `GET /api/bookmarks` → `Category[]`
- `PUT /api/bookmarks` body: `Category[]` → `{ "ok": true }`

```ts
type Category = {
  name: string
  links: Link[]
}
type Link = {
  label: string
  url: string   // always fully-qualified (https://...)
}
```

### Lists
- `GET /api/lists` → `List[]`
- `PUT /api/lists` body: `List[]` → `{ "ok": true }`

```ts
type List = {
  name: string
  items: Item[]
}
type Item = {
  id: string    // random alphanumeric, generated client-side via genId()
  text: string
  done: boolean
}
```

## Local dev

```bash
python3 server.py   # serves on http://localhost:8080
```

The Python server (`server.py`) mirrors the Workers API exactly. Data persists to `bookmarks.json`, `lists.json`, `notes.json` in the project root. These files are not deployed.

Static files are served from the project root (not `public/`) in dev. In production, Cloudflare Pages serves from `public/`.

## Production

Cloudflare Pages hosts `public/index.html`. Workers functions in `functions/api/` are auto-deployed alongside it. KV namespaces are bound via `wrangler.toml`.

Deploy command (requires `CLOUDFLARE_API_TOKEN` in env):
```bash
source .env && npx wrangler pages deploy ./public --project-name=thedirectory
```

## Adding a new KV-backed widget

1. Create the KV namespace: `npx wrangler kv namespace create <NAME>`
2. Add a `[[kv_namespaces]]` block to `wrangler.toml`
3. Create `functions/api/<name>.js` — follow the pattern of `notes.js` or `lists.js`
4. Add matching `GET` and `PUT` handlers to `server.py`
5. Add the fetch/save logic and render function to `public/index.html`

## Frontend architecture

`public/index.html` is self-contained — no build step, no bundler, no framework.

Key globals in the JS:
- `data` — bookmarks array, loaded from `/api/bookmarks` on startup
- `listsData` — lists array, loaded from `/api/lists` on startup
- `render()` — re-renders the entire bookmarks section from `data`
- `renderLists()` — re-renders the lists widget from `listsData`
- `save(d)` — PUT to `/api/bookmarks`
- `saveLists()` — debounced PUT to `/api/lists` (400ms)
- Notes autosave with 500ms debounce on the textarea input event

CSS uses custom properties defined on `:root`. Dark theme only. Layout: fixed left sidebar (notes + lists panels), fixed right sidebar (calendar), scrollable center (bookmarks). Sidebars hide below 1200px and become mobile toggles.

## Constraints

- No build step. Keep everything in the single HTML file — don't split JS or CSS out.
- No npm dependencies in the frontend. Vanilla JS only.
- The Python dev server must stay in sync with the Workers functions — same endpoints, same request/response shapes.
- Max 10 lists, max 100 items per list (enforced client-side).
- Bookmarks and lists use full client-side re-render on every change (no partial DOM updates).
