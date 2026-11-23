const CONFIG = __CONFIG_JSON__;
const HELPER = __HELPER_JSON__;
const PACKET_BASE64 = __PACKET_BASE64_JSON__;
const PACKET_SHA256 = __PACKET_SHA256_JSON__;
const PDF_NAME = 'Caesar_Solo_Print_and_Play.pdf';
let packet;

const catalogEntry = `<article class="companion" data-game="caesar-rome-vs-gaul" aria-labelledby="caesar-rome-vs-gaul-title">
  <div class="companion-content">
    <p class="companion-type">Imperator and Concilium · Either side</p>
    <h2 id="caesar-rome-vs-gaul-title">Caesar: Rome vs. Gaul</h2>
    <p>Play Rome or Gaul on your physical board. Draw the opposing bot's Directive cards digitally, track turns and level bonuses, and consult the quick references.</p>
    <p class="scenarios">Physical game required · v1.3</p>
    <div class="actions">
      <a class="button button-primary" href="${CONFIG.app_path}">Open companion</a>
      <a class="button button-secondary" href="${CONFIG.app_path}${PDF_NAME}" download="${PDF_NAME}">Print-and-play rules (PDF)</a>
    </div>
  </div>
</article>`;

function localResponse(body, type, method, extra = {}) {
  return new Response(method === 'HEAD' ? null : body, {
    headers: { 'Content-Type': type, 'Cache-Control': 'no-cache',
      'X-Content-Type-Options': 'nosniff', ...extra }
  });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname;
    const prefix = CONFIG.app_path;
    if (path === prefix.slice(0, -1)) {
      return Response.redirect(new URL(prefix + url.search, url.origin), 308);
    }
    const app = path === prefix || path === prefix + 'index.html';
    const pdf = path === prefix + PDF_NAME;
    const offline = path === '/downloads/caesar-rome-vs-gaul';
    if (app || pdf || offline) {
      if (request.method !== 'GET' && request.method !== 'HEAD') {
        return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
      }
      if (pdf) {
        const etag = '"' + PACKET_SHA256 + '"';
        if (request.headers.get('If-None-Match') === etag) {
          return new Response(null, { status: 304, headers: { ETag: etag } });
        }
        packet ??= Uint8Array.from(atob(PACKET_BASE64), c => c.charCodeAt(0));
        return localResponse(packet, 'application/pdf', request.method, {
          'Content-Disposition': `attachment; filename="${PDF_NAME}"`,
          'Content-Length': String(packet.byteLength), ETag: etag
        });
      }
      return localResponse(HELPER, 'text/html; charset=utf-8', request.method,
        offline ? { 'Content-Disposition': 'attachment; filename="Caesar_Solo_Deck.html"' } : {});
    }

    // Preserve the complete preceding site, including routes and downloads that
    // are not represented in this game's repository. Never proxy to the mutable
    // production alias, which would recurse back into this Worker.
    const upstream = new URL(request.url);
    upstream.host = new URL(CONFIG.previous_deployment_url).host;
    const response = await fetch(new Request(upstream, request));
    if ((path === '/' || path === '/index.html') && request.method === 'GET'
        && response.ok && response.headers.get('Content-Type')?.includes('text/html')) {
      const rewritten = new HTMLRewriter()
        .on('article[data-game="caesar-rome-vs-gaul"]', { element(el) { el.remove(); } })
        .on('#companions', { element(el) { el.append(catalogEntry, { html: true }); } })
        .on('a[href*="github.com"]', { element(el) { el.removeAndKeepContent(); } })
        .transform(response);
      const headers = new Headers(rewritten.headers);
      headers.delete('Content-Length');
      headers.delete('ETag');
      headers.set('Cache-Control', 'no-cache');
      return new Response(rewritten.body, { status: rewritten.status, headers });
    }
    return response;
  }
};
