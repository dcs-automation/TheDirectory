const DEFAULT_BOOKMARKS = [
  {
    name: "Frequently Visited",
    links: [
      { label: "Google", url: "https://www.google.com" },
      { label: "YouTube", url: "https://www.youtube.com" },
      { label: "GitHub", url: "https://github.com" },
      { label: "Reddit", url: "https://www.reddit.com" },
      { label: "Wikipedia", url: "https://en.wikipedia.org" },
      { label: "Twitter / X", url: "https://x.com" },
    ],
  },
  {
    name: "Productivity",
    links: [
      { label: "Gmail", url: "https://mail.google.com" },
      { label: "Google Drive", url: "https://drive.google.com" },
      { label: "Calendar", url: "https://calendar.google.com" },
      { label: "Notion", url: "https://www.notion.so" },
    ],
  },
  {
    name: "Entertainment",
    links: [
      { label: "Netflix", url: "https://www.netflix.com" },
      { label: "Spotify", url: "https://open.spotify.com" },
      { label: "Twitch", url: "https://www.twitch.tv" },
    ],
  },
];

export async function onRequest(context) {
  const { request, env } = context;

  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };

  if (request.method === "OPTIONS") {
    return new Response(null, { status: 204, headers });
  }

  if (request.method === "GET") {
    const value = await env.BOOKMARKS.get("bookmarks");
    const data = value ? JSON.parse(value) : DEFAULT_BOOKMARKS;
    return new Response(JSON.stringify(data), { headers });
  }

  if (request.method === "PUT") {
    const body = await request.json();
    if (!Array.isArray(body)) {
      return new Response(JSON.stringify({ error: "expected array" }), {
        status: 400,
        headers,
      });
    }
    await env.BOOKMARKS.put("bookmarks", JSON.stringify(body));
    return new Response(JSON.stringify({ ok: true }), { headers });
  }

  return new Response(JSON.stringify({ error: "method not allowed" }), {
    status: 405,
    headers,
  });
}
