// Innlogging til adminpanelet (Decap CMS) med GitHub, kjørt som Cloudflare Worker.
// Gjør det samme som Netlify gjorde: sender brukeren til GitHub, tar imot svaret
// og gir tilgangsnøkkelen tilbake til adminpanelet.
//
// Innstillinger (Cloudflare → Workers → denne workeren → Settings → Variables and Secrets):
//   GITHUB_CLIENT_ID      – fra GitHub OAuth App
//   GITHUB_CLIENT_SECRET  – fra GitHub OAuth App (lagres som «Secret»)
//   ALLOWED_ORIGINS       – adressene til nettsiden, kommaseparert, f.eks.
//                           https://gjovik-mikrotek.pages.dev,https://gjovikmikrotek.no

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/auth') return start(url, env);
    if (url.pathname === '/callback') return callback(request, url, env);
    return new Response('Innlogging for Gjøvik MikroTek sitt adminpanel.', { headers: { 'content-type': 'text/plain; charset=utf-8' } });
  }
};

function start(url, env) {
  const state = crypto.randomUUID();
  const github = new URL('https://github.com/login/oauth/authorize');
  github.searchParams.set('client_id', env.GITHUB_CLIENT_ID);
  github.searchParams.set('redirect_uri', url.origin + '/callback');
  github.searchParams.set('scope', url.searchParams.get('scope') || 'repo');
  github.searchParams.set('state', state);
  return new Response(null, {
    status: 302,
    headers: {
      location: github.toString(),
      'set-cookie': `oauth_state=${state}; Path=/callback; HttpOnly; Secure; SameSite=Lax; Max-Age=600`
    }
  });
}

async function callback(request, url, env) {
  const code = url.searchParams.get('code');
  const state = url.searchParams.get('state');
  const cookie = (request.headers.get('cookie') || '').match(/(?:^|;\s*)oauth_state=([^;]+)/);
  if (!code || !state || !cookie || cookie[1] !== state) {
    return svar(env, 'error', { message: 'Ugyldig innlogging. Prøv igjen.' });
  }

  const res = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { 'content-type': 'application/json', accept: 'application/json', 'user-agent': 'gjovik-mikrotek-auth' },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: url.origin + '/callback'
    })
  });
  const data = await res.json().catch(() => ({}));
  if (!data.access_token) {
    return svar(env, 'error', { message: data.error_description || 'GitHub ga ingen tilgang.' });
  }
  return svar(env, 'success', { token: data.access_token, provider: 'github' });
}

// Sender resultatet til adminpanelet i vinduet som åpnet innloggingen.
// Nøkkelen sendes bare til adresser som står i ALLOWED_ORIGINS.
function svar(env, status, innhold) {
  const tillatte = String(env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
  const melding = 'authorization:github:' + status + ':' + JSON.stringify(innhold);
  const html = `<!doctype html><meta charset="utf-8"><title>Logger inn …</title>
<p>Logger inn … Du kan lukke dette vinduet hvis det ikke lukker seg selv.</p>
<script>
  const tillatte = ${JSON.stringify(tillatte)};
  const melding = ${JSON.stringify(melding)};
  window.addEventListener('message', e => {
    if (!tillatte.includes(e.origin)) return;
    window.opener.postMessage(melding, e.origin);
    setTimeout(() => window.close(), 500);
  });
  if (window.opener) window.opener.postMessage('authorizing:github', '*');
</script>`;
  return new Response(html, {
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'no-store',
      'set-cookie': 'oauth_state=; Path=/callback; HttpOnly; Secure; SameSite=Lax; Max-Age=0'
    }
  });
}
