// /api/leads — private endpoint the Brain uses to collect website leads.
//   GET    → { leads: [...] }                     (Authorization: Bearer ADMIN_TOKEN)
//   DELETE → body { ids: [...] } removes collected leads
function authorised(request, env) {
  const expected = env.ADMIN_TOKEN || "";
  const got = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (expected.length < 20 || got.length !== expected.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ got.charCodeAt(i);
  return diff === 0;
}
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export async function onRequestGet({ request, env }) {
  if (!authorised(request, env)) return json({ error: "Not authorised." }, 401);
  const leads = [];
  let cursor;
  do {
    const page = await env.LEADS.list({ prefix: "lead:", cursor });
    for (const k of page.keys) {
      const v = await env.LEADS.get(k.name);
      if (v) leads.push(JSON.parse(v));
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return json({ leads });
}

export async function onRequestDelete({ request, env }) {
  if (!authorised(request, env)) return json({ error: "Not authorised." }, 401);
  const { ids } = await request.json().catch(() => ({}));
  if (!Array.isArray(ids)) return json({ error: "Send { ids: [...] }." }, 400);
  for (const id of ids) if (/^[\w-]+$/.test(id)) await env.LEADS.delete(`lead:${id}`);
  return json({ deleted: ids.length });
}
