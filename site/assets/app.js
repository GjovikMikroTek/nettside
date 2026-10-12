// Henter innhold fra /content/*.json (det adminpanelet redigerer) og fyller sidene.

// Språk: norsk (nb) eller engelsk (en).
// Valget leses fra ?lang= i adressen, deretter fra forrige besøk, ellers fra nettleserens språk.
const SPRAK = (() => {
  const fraUrl = new URLSearchParams(location.search).get('lang');
  if (fraUrl === 'en' || fraUrl === 'nb') { lagreSprak(fraUrl); return fraUrl; }
  try { const lagret = localStorage.getItem('sprak'); if (lagret === 'en' || lagret === 'nb') return lagret; } catch (e) {}
  return /^(nb|nn|no|da|sv)/i.test(navigator.language || '') ? 'nb' : 'en';
})();

function lagreSprak(s) {
  try { localStorage.setItem('sprak', s); } catch (e) {}
}

// Faste tekster på siden. Innhold fra adminpanelet oversettes i adminpanelet (feltene som slutter på «(engelsk)»).
const TEKST = {
  nb: {
    nav_om: 'Om', nav_artikler: 'Artikler', nav_styret: 'Styret', nav_sponsorer: 'Sponsorer', nav_kontakt: 'Kontakt',
    om_tittel: 'Om oss', siste_artikler: 'Siste artikler', alle_artikler: 'Alle artikler →', tilbake: '← Alle artikler',
    artikler: 'Artikler', ingen_artikler: 'Ingen artikler ennå.', fant_ikke: 'Fant ikke artikkelen.', kunne_ikke: 'Kunne ikke laste innholdet.',
    fra_instagram: 'Fra Instagram', folg_instagram: 'Følg oss på Instagram →', instagram_alt: 'Innlegg på Instagram',
    styret: 'Styret', styret_tom: 'Styret legges inn snart.',
    sponsorer: 'Sponsorer og samarbeidspartnere', sponsor_tom: 'Vil du støtte oss? Ta kontakt!',
    Hovedsponsor: 'Hovedsponsor', Sponsor: 'Sponsor', Samarbeidspartner: 'Samarbeidspartner',
    kontakt: 'Kontakt', epost_tekst: 'Send oss en e-post på', skjema: 'Fyll ut kontaktskjema',
    bunn: 'Studentorganisasjon ved NTNU Campus Gjøvik', bytt: 'English', bytt_tittel: 'Switch to English',
    meny: 'Meny', nav_medlem: 'Bli medlem', banner_tittel: 'Bli med og bygg!',
    banner_tekst: 'Medlemskap er gratis og åpent for studenter ved NTNU Campus Gjøvik.',
    apne_skjema: 'Åpne innmeldingsskjemaet', skjema_tittel: 'Innmeldingsskjema',
    skjema_mangler: 'Innmeldingsskjemaet kommer snart. Ta kontakt med styret i mellomtiden.'
  },
  en: {
    nav_om: 'About', nav_artikler: 'News', nav_styret: 'Board', nav_sponsorer: 'Sponsors', nav_kontakt: 'Contact',
    om_tittel: 'About us', siste_artikler: 'Latest news', alle_artikler: 'All news →', tilbake: '← All news',
    artikler: 'News', ingen_artikler: 'No articles yet.', fant_ikke: 'Article not found.', kunne_ikke: 'Could not load the content.',
    fra_instagram: 'From Instagram', folg_instagram: 'Follow us on Instagram →', instagram_alt: 'Instagram post',
    styret: 'The board', styret_tom: 'Board members coming soon.',
    sponsorer: 'Sponsors and partners', sponsor_tom: 'Want to support us? Get in touch!',
    Hovedsponsor: 'Main sponsor', Sponsor: 'Sponsor', Samarbeidspartner: 'Partner',
    kontakt: 'Contact', epost_tekst: 'Email us at', skjema: 'Fill out the contact form',
    bunn: 'Student organisation at NTNU Campus Gjøvik', bytt: 'Norsk', bytt_tittel: 'Bytt til norsk',
    meny: 'Menu', nav_medlem: 'Join us', banner_tittel: 'Come build with us!',
    banner_tekst: 'Membership is free and open to students at NTNU Campus Gjøvik.',
    apne_skjema: 'Open the membership form', skjema_tittel: 'Membership form',
    skjema_mangler: 'The membership form is coming soon. Please contact the board in the meantime.'
  }
};

function t(nokkel) {
  return TEKST[SPRAK][nokkel] ?? TEKST.nb[nokkel] ?? nokkel;
}

// Henter et innholdsfelt på valgt språk. Er det engelske feltet tomt, brukes det norske.
function felt(obj, navn) {
  if (SPRAK === 'en' && obj && obj[navn + '_en']) return obj[navn + '_en'];
  return obj ? obj[navn] : '';
}

function settOppSprak() {
  document.documentElement.lang = SPRAK;
  document.querySelectorAll('[data-tekst]').forEach(el => { el.textContent = t(el.dataset.tekst); });
  const knapp = document.getElementById('sprak-knapp');
  if (knapp) {
    knapp.textContent = t('bytt');
    knapp.title = t('bytt_tittel');
    knapp.lang = SPRAK === 'en' ? 'nb' : 'en';
    knapp.addEventListener('click', () => {
      const nytt = SPRAK === 'en' ? 'nb' : 'en';
      lagreSprak(nytt);
      const url = new URL(location.href);
      url.searchParams.set('lang', nytt);
      location.href = url.toString();
    });
  }
}

// Menyknappen på mobil
function settOppMeny() {
  const knapp = document.getElementById('meny-knapp');
  const meny = document.getElementById('meny');
  if (!knapp || !meny) return;
  const lukk = () => { meny.classList.remove('apen'); knapp.setAttribute('aria-expanded', 'false'); };
  knapp.addEventListener('click', () => {
    const apen = meny.classList.toggle('apen');
    knapp.setAttribute('aria-expanded', String(apen));
  });
  meny.querySelectorAll('a').forEach(a => a.addEventListener('click', lukk));
}

async function hent(fil) {
  const svar = await fetch('/content/' + fil + '.json', { cache: 'no-cache' });
  if (!svar.ok) throw new Error('Fant ikke ' + fil);
  return svar.json();
}

function esc(t) {
  return String(t ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function md(t) {
  return window.marked ? marked.parse(t || '') : '<p>' + esc(t) + '</p>';
}

function trygLenke(url) {
  return /^(https?:|mailto:|\/)/i.test(url || '') ? url : '';
}

// Artikkeladressen bygges alltid av den norske tittelen, så lenker virker på begge språk.
function slug(a) {
  const s = (a.tittel || '').toLowerCase()
    .replace(/æ/g, 'ae').replace(/ø/g, 'o').replace(/å/g, 'a')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return (a.dato || '') + '-' + s;
}

function datoTekst(d) {
  if (!d) return '';
  const dt = new Date(d + 'T12:00:00');
  return isNaN(dt) ? d : dt.toLocaleDateString(SPRAK === 'en' ? 'en-GB' : 'nb-NO', { day: 'numeric', month: 'long', year: 'numeric' });
}

function synligeArtikler(data) {
  return (data.artikler || [])
    .filter(a => a.publisert !== false)
    .sort((x, y) => String(y.dato).localeCompare(String(x.dato)));
}

function artikkelKort(a) {
  const bilde = a.bilde ? `<img src="${esc(a.bilde)}" alt="" loading="lazy">` : '<div class="bilde-tom"></div>';
  return `<a class="kort" href="/artikler.html?a=${encodeURIComponent(slug(a))}">
    ${bilde}
    <div class="kort-tekst">
      <time>${esc(datoTekst(a.dato))}</time>
      <h3>${esc(felt(a, 'tittel'))}</h3>
      <p>${esc(felt(a, 'ingress'))}</p>
    </div>
  </a>`;
}

async function fellesInnstillinger() {
  settOppSprak();
  settOppMeny();
  const s = await hent('innstillinger');
  if (s.aksentfarge) document.documentElement.style.setProperty('--aksent', s.aksentfarge);
  document.querySelectorAll('[data-felt]').forEach(el => {
    const v = felt(s, el.dataset.felt);
    if (v) el.textContent = v;
  });
  return s;
}

// Instagram-bilder via Behold (behold.so), som henter de siste innleggene fra Instagram-kontoen.
// Seksjonen vises bare når feed-lenken er fylt inn i adminpanelet.
async function visInstagram(s) {
  const feed = s.instagram_feed || '';
  if (!/^https:\/\/feeds\.behold\.so\/[A-Za-z0-9_-]+$/.test(feed)) return;
  const svar = await fetch(feed);
  if (!svar.ok) return;
  const data = await svar.json();
  const bildeUrl = p => {
    const u = p.mediaType === 'VIDEO' ? p.thumbnailUrl : (p.sizes?.medium?.mediaUrl || p.mediaUrl);
    return /^https:\/\//.test(u || '') ? u : '';
  };
  const innlegg = (data.posts || []).filter(p => bildeUrl(p) && /^https:\/\/(www\.)?instagram\.com\//.test(p.permalink || '')).slice(0, 6);
  if (!innlegg.length) return;
  document.getElementById('instagram-bilder').innerHTML = innlegg.map(p => `
    <a class="insta" href="${esc(p.permalink)}" target="_blank" rel="noopener">
      <img src="${esc(bildeUrl(p))}" alt="${esc(p.altText || p.prunedCaption || t('instagram_alt'))}" loading="lazy">
    </a>`).join('');
  const folg = document.getElementById('instagram-folg');
  const profil = trygLenke(s.instagram);
  if (profil) { folg.href = profil; folg.hidden = false; }
  document.getElementById('instagram').hidden = false;
}

async function visForside() {
  try {
    const [s, prosjekt, artikler, styret, sponsorer] = await Promise.all([
      fellesInnstillinger(), hent('prosjekt'), hent('artikler'), hent('styret'), hent('sponsorer')
    ]);
    document.title = s.navn || 'Gjøvik MikroTek';
    visInstagram(s).catch(e => console.error('Instagram:', e));

    if (s.hovedbilde) {
      const h = document.getElementById('hero');
      h.style.backgroundImage = `linear-gradient(rgba(0,0,0,.45), rgba(0,0,0,.45)), url("${encodeURI(s.hovedbilde)}")`;
      h.classList.add('med-bilde');
    }

    document.getElementById('om-tittel').textContent = felt(prosjekt, 'tittel') || t('om_tittel');
    document.getElementById('om-tekst').innerHTML = md(felt(prosjekt, 'tekst'));

    const siste = synligeArtikler(artikler).slice(0, 3);
    document.getElementById('artikler-siste').innerHTML = siste.length
      ? siste.map(artikkelKort).join('')
      : `<p class="tom">${esc(t('ingen_artikler'))}</p>`;

    document.getElementById('styret-liste').innerHTML = (styret.medlemmer || []).map(m => `
      <div class="person">
        ${m.bilde ? `<img src="${esc(m.bilde)}" alt="${esc(m.navn)}" loading="lazy">` : `<div class="initialer">${esc((m.navn || '?').split(' ').map(x => x[0]).join('').slice(0, 2))}</div>`}
        <strong>${esc(m.navn)}</strong>
        <span>${esc(felt(m, 'rolle'))}</span>
        ${m.epost ? `<a href="mailto:${esc(m.epost)}">${esc(m.epost)}</a>` : ''}
      </div>`).join('') || `<p class="tom">${esc(t('styret_tom'))}</p>`;

    const nivaer = ['Hovedsponsor', 'Sponsor', 'Samarbeidspartner'];
    const sp = sponsorer.sponsorer || [];
    document.getElementById('sponsor-liste').innerHTML = sp.length ? nivaer.map(n => {
      const gruppe = sp.filter(x => (x.niva || 'Sponsor') === n);
      if (!gruppe.length) return '';
      return `<h3 class="niva">${esc(t(n))}</h3><div class="sponsorer ${n === 'Hovedsponsor' ? 'stor' : ''}">` +
        gruppe.map(x => {
          const inni = x.logo ? `<img src="${esc(x.logo)}" alt="${esc(x.navn)}" loading="lazy">` : `<span>${esc(x.navn)}</span>`;
          const url = trygLenke(x.lenke);
          return url ? `<a class="sponsor" href="${esc(url)}" target="_blank" rel="noopener">${inni}</a>` : `<div class="sponsor">${inni}</div>`;
        }).join('') + '</div>';
    }).join('') : `<p class="tom">${esc(t('sponsor_tom'))}</p>`;

    const ep = document.getElementById('kontakt-epost');
    ep.textContent = s.epost || '';
    ep.href = 'mailto:' + (s.epost || '');
    document.getElementById('epost-boks').hidden = !s.epost;
    const skjema = trygLenke(s.skjema_lenke);
    if (skjema) {
      document.getElementById('skjema-lenke').href = skjema;
      document.getElementById('skjema-boks').hidden = false;
    }
    document.getElementById('sosiale').innerHTML = [
      trygLenke(s.instagram) && `<a href="${esc(s.instagram)}" target="_blank" rel="noopener">Instagram</a>`,
      trygLenke(s.linkedin) && `<a href="${esc(s.linkedin)}" target="_blank" rel="noopener">LinkedIn</a>`
    ].filter(Boolean).join(' · ');
  } catch (e) {
    console.error(e);
  }
}

async function visArtikler() {
  const boks = document.getElementById('innhold');
  try {
    const [s, data] = await Promise.all([fellesInnstillinger(), hent('artikler')]);
    const alle = synligeArtikler(data);
    const valgt = new URLSearchParams(location.search).get('a');

    if (valgt) {
      const a = alle.find(x => slug(x) === valgt);
      if (!a) { boks.innerHTML = `<p>${esc(t('fant_ikke'))} <a href="/artikler.html">${esc(t('tilbake'))}</a></p>`; return; }
      document.title = felt(a, 'tittel') + ' – ' + (s.navn || 'Gjøvik MikroTek');
      boks.innerHTML = `<article class="artikkel">
        <a href="/artikler.html" class="lenke-pil">${esc(t('tilbake'))}</a>
        <time>${esc(datoTekst(a.dato))}</time>
        <h1>${esc(felt(a, 'tittel'))}</h1>
        <p class="ingress">${esc(felt(a, 'ingress'))}</p>
        ${a.bilde ? `<img src="${esc(a.bilde)}" alt="" class="artikkel-bilde">` : ''}
        <div class="brodtekst">${md(felt(a, 'tekst'))}</div>
      </article>`;
      return;
    }

    document.title = t('artikler') + ' – ' + (s.navn || 'Gjøvik MikroTek');
    boks.innerHTML = `<h1>${esc(t('artikler'))}</h1><div class="kort-rutenett">` +
      (alle.map(artikkelKort).join('') || `<p class="tom">${esc(t('ingen_artikler'))}</p>`) + '</div>';
  } catch (e) {
    console.error(e);
    boks.innerHTML = `<p>${esc(t('kunne_ikke'))}</p>`;
  }
}

// Microsoft Forms-skjemaet kan limes inn som lenke eller som hele «Bygg inn»-koden (<iframe ...>).
// Bare adresser hos Microsoft Forms godtas.
function skjemaAdresse(verdi) {
  const v = String(verdi || '').trim();
  const fraIframe = v.match(/src=["']([^"']+)["']/i);
  const url = (fraIframe ? fraIframe[1] : v).replace(/&amp;/g, '&');
  if (!/^https:\/\/forms\.(office|microsoft)\.com\//i.test(url)) return null;
  const visning = url.includes('ResponsePage.aspx') && !/[?&]embed=true/i.test(url) ? url + '&embed=true' : url;
  return { visning, lenke: url.replace(/[?&]embed=true/i, '') };
}

async function visMedlem() {
  try {
    const [s, medlem] = await Promise.all([fellesInnstillinger(), hent('medlem')]);
    document.title = (felt(medlem, 'tittel') || t('nav_medlem')) + ' – ' + (s.navn || 'Gjøvik MikroTek');
    if (felt(medlem, 'tittel')) document.getElementById('medlem-tittel').textContent = felt(medlem, 'tittel');
    document.getElementById('medlem-tekst').innerHTML = md(felt(medlem, 'tekst'));

    const skjema = skjemaAdresse(medlem.skjema);
    if (!skjema) { document.getElementById('skjema-mangler').hidden = false; return; }
    const ramme = document.getElementById('skjema-ramme');
    const iframe = document.createElement('iframe');
    iframe.src = skjema.visning;
    iframe.title = t('skjema_tittel');
    iframe.loading = 'lazy';
    iframe.setAttribute('allowfullscreen', '');
    ramme.appendChild(iframe);
    ramme.hidden = false;
    document.getElementById('skjema-reserve-lenke').href = skjema.lenke;
    document.getElementById('skjema-reserve').hidden = false;
  } catch (e) {
    console.error(e);
  }
}
