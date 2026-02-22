# TheDirectory

A personal new-tab homepage with bookmarks, notepad, lists, and calendar. Runs on Cloudflare Pages + Workers with KV storage.

<img width="1851" height="1294" alt="image" src="https://github.com/user-attachments/assets/fc178590-5d33-4c89-b6de-89e660c85864" />


## Local Development

```bash
python3 server.py
```

Serves on `http://localhost:8080`. Static files from `public/`, API endpoints backed by local JSON files (`notes.json`, `bookmarks.json`, `lists.json`).

## Project Structure

```
public/index.html          # Single-page app (HTML + CSS + JS)
functions/api/notes.js      # Cloudflare Worker – Notes API
functions/api/bookmarks.js  # Cloudflare Worker – Bookmarks API
functions/api/lists.js      # Cloudflare Worker – Lists API
server.py                   # Local dev server with API endpoints
wrangler.toml               # Cloudflare Pages config + KV bindings
```

## Deploying to Cloudflare

### Prerequisites

- Node.js (for `npx wrangler`)
- A Cloudflare API token with Pages + KV permissions

### First-time setup: Create KV namespaces

Each data store needs a KV namespace. Create them via the Cloudflare dashboard (Workers & Pages > KV) or via API:

```bash
export CLOUDFLARE_API_TOKEN=<your-token>
npx wrangler kv namespace create NOTES
npx wrangler kv namespace create BOOKMARKS
npx wrangler kv namespace create LISTS
```

Copy each namespace ID into `wrangler.toml` under the matching `[[kv_namespaces]]` entry.

### Deploy

If you have a `.env` file with `CLOUDFLARE_API_TOKEN` set:

```bash
source .env && npx wrangler pages deploy ./public --project-name=thedirectory
```

Or pass the token directly:

```bash
CLOUDFLARE_API_TOKEN=<your-token> npx wrangler pages deploy ./public --project-name=thedirectory
```

This uploads static files, compiles the Workers functions, and deploys everything. The site will be available at `https://thedirectory.pages.dev`.

### Adding a new KV-backed feature

1. Create the KV namespace (dashboard or `wrangler kv namespace create <NAME>`)
2. Add a `[[kv_namespaces]]` block to `wrangler.toml` with the binding name and ID
3. Create `functions/api/<name>.js` (see existing ones for the pattern)
4. Add the matching endpoint to `server.py` for local dev
5. Deploy with the command above
