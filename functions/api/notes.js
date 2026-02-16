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
    const value = await env.NOTES.get("notes");
    const data = value ? JSON.parse(value) : { content: "" };
    return new Response(JSON.stringify(data), { headers });
  }

  if (request.method === "PUT") {
    const body = await request.json();
    const data = { content: body.content || "" };
    await env.NOTES.put("notes", JSON.stringify(data));
    return new Response(JSON.stringify({ ok: true }), { headers });
  }

  return new Response(JSON.stringify({ error: "method not allowed" }), {
    status: 405,
    headers,
  });
}
