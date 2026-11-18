// Cloudflare Pages Function: GET /api/counts
// Returns every template's download count as JSON, e.g. {"expense-tracker": 42}.
// Uses the DOWNLOADS KV binding. Generated files: edit here if the counter changes.

export async function onRequestGet({ env }) {
  const counts = {};
  let cursor;
  do {
    const page = await env.DOWNLOADS.list({ prefix: "dl:", cursor });
    await Promise.all(
      page.keys.map(async (k) => {
        counts[k.name.slice(3)] = parseInt((await env.DOWNLOADS.get(k.name)) || "0", 10);
      })
    );
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);

  return new Response(JSON.stringify(counts), {
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}
