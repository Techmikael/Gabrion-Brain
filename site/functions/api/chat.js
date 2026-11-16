// POST /api/chat  — the website chat. Body: { messages: [{role, content}] }
// Returns: { reply, leadSaved }
import Anthropic from "@anthropic-ai/sdk";
import { MODEL, SYSTEM_PROMPT, TOOLS } from "../_lib/frontdesk.js";

const MAX_TURNS = 24;            // messages kept from the conversation
const MAX_CHARS = 1500;          // per visitor message
const HOURLY_LIMIT = 40;         // visitor messages per IP per hour

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

function cleanHistory(raw) {
  if (!Array.isArray(raw)) return null;
  const msgs = raw
    .filter((m) => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_CHARS).trim() }))
    .filter((m) => m.content)
    .slice(-MAX_TURNS);
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (!msgs.length || msgs[msgs.length - 1].role !== "user") return null;
  return msgs;
}

async function overLimit(env, ip) {
  if (!env.LEADS) return false;
  const key = `rate:${ip}:${new Date().toISOString().slice(0, 13)}`;
  const n = parseInt((await env.LEADS.get(key)) || "0", 10);
  if (n >= HOURLY_LIMIT) return true;
  await env.LEADS.put(key, String(n + 1), { expirationTtl: 3900 });
  return false;
}

async function saveLead(env, input, ip) {
  const email = String(input.email || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return "Not saved: that email address looks incomplete. Ask the visitor to check it.";
  const id = `${new Date().toISOString().replace(/[-:.TZ]/g, "").slice(0, 14)}-${crypto.randomUUID().slice(0, 6)}`;
  const lead = {
    id,
    created: new Date().toISOString(),
    name: String(input.name || "").slice(0, 120),
    email: email.slice(0, 200),
    phone: String(input.phone || "").slice(0, 40),
    company: String(input.company || "").slice(0, 160),
    industry: String(input.industry || "").slice(0, 80),
    factory: String(input.factory || "unsure"),
    need: String(input.need || "").slice(0, 800),
    source: "website-chat",
  };
  if (!env.LEADS) return "Not saved: lead storage is not set up yet.";
  await env.LEADS.put(`lead:${id}`, JSON.stringify(lead), { expirationTtl: 60 * 60 * 24 * 90 });
  return "Saved. Tell the visitor the founder will email within one working day to arrange the free discovery call.";
}

export async function onRequestPost({ request, env }) {
  if (!env.ANTHROPIC_API_KEY) return json({ error: "Chat is not configured yet." }, 503);
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Bad request." }, 400);
  }
  const messages = cleanHistory(body?.messages);
  if (!messages) return json({ error: "Bad request." }, 400);

  const ip = request.headers.get("cf-connecting-ip") || "local";
  if (await overLimit(env, ip)) {
    return json({ reply: "We've had a lot of messages from you this hour. Please email us instead and we'll reply within one working day.", leadSaved: false });
  }

  const client = new Anthropic({
    apiKey: env.ANTHROPIC_API_KEY,
    ...(env.ANTHROPIC_BASE_URL ? { baseURL: env.ANTHROPIC_BASE_URL } : {}), // local testing only
    maxRetries: 1,
    timeout: 45_000,
  });

  let leadSaved = false;
  try {
    for (let step = 0; step < 3; step++) {
      const response = await client.beta.messages.create({
        model: MODEL,
        max_tokens: 1500,
        betas: ["server-side-fallback-2026-07-01"],
        fallbacks: "default",
        output_config: { effort: "low" },
        system: SYSTEM_PROMPT,
        tools: TOOLS,
        messages,
      });

      if (response.stop_reason === "refusal") {
        return json({ reply: "Sorry, I can't help with that here. For anything else about Gabrion's services, just ask.", leadSaved });
      }

      const toolUses = response.content.filter((b) => b.type === "tool_use");
      if (response.stop_reason !== "tool_use" || !toolUses.length) {
        const reply = response.content.filter((b) => b.type === "text").map((b) => b.text).join("\n").trim();
        return json({ reply: reply || "Sorry, could you say that another way?", leadSaved });
      }

      messages.push({ role: "assistant", content: response.content });
      const results = [];
      for (const t of toolUses) {
        let content = "Unknown tool.";
        if (t.name === "save_lead" && !leadSaved) {
          content = await saveLead(env, t.input || {}, ip);
          leadSaved = content.startsWith("Saved");
        } else if (t.name === "save_lead") {
          content = "Already saved in this chat.";
        }
        results.push({ type: "tool_result", tool_use_id: t.id, content });
      }
      messages.push({ role: "user", content: results });
    }
    return json({ reply: "Thanks, I've got that. The founder will be in touch.", leadSaved });
  } catch (err) {
    console.error("chat error", err?.status, err?.message);
    return json({ error: "The assistant is unavailable right now. Please email us instead." }, 502);
  }
}
