/**
 * /img/video/* with byte ranges.
 *
 * The static assets binding answers a Range request with the whole file and a 200. Chrome
 * copes, but Safari on an iPhone asks for "bytes=0-1" first and will not play an MP4 whose
 * server does not answer with a 206, so every video request comes through here (listed in
 * run_worker_first) and is cut to the range asked for. The files are small (about 10 MB),
 * so reading one whole and slicing it is fine.
 */
export async function video(request, env) {
  if (request.method !== "GET" && request.method !== "HEAD") {
    return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, HEAD" } });
  }
  const res = await env.ASSETS.fetch(new Request(request.url, { method: "GET" }));
  if (!res.ok) return res;
  const buf = await res.arrayBuffer();
  const size = buf.byteLength;
  const headers = new Headers({
    "Content-Type": res.headers.get("Content-Type") || "video/mp4",
    "Accept-Ranges": "bytes",
    // Every URL carries ?v=<hash of the file>, so a cached copy can never go stale.
    "Cache-Control": "public, max-age=31536000, immutable",
  });
  const m = /^bytes=(\d*)-(\d*)$/.exec(request.headers.get("Range") || "");
  if (!m || (m[1] === "" && m[2] === "")) {
    headers.set("Content-Length", String(size));
    return new Response(request.method === "HEAD" ? null : buf, { status: 200, headers });
  }
  let start, end;
  if (m[1] === "") { start = Math.max(0, size - Number(m[2])); end = size - 1; }   // the last N bytes
  else { start = Number(m[1]); end = m[2] === "" ? size - 1 : Math.min(Number(m[2]), size - 1); }
  if (start >= size || start > end) {
    headers.set("Content-Range", `bytes */${size}`);
    return new Response(null, { status: 416, headers });
  }
  headers.set("Content-Range", `bytes ${start}-${end}/${size}`);
  headers.set("Content-Length", String(end - start + 1));
  return new Response(request.method === "HEAD" ? null : buf.slice(start, end + 1), { status: 206, headers });
}
