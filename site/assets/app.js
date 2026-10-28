// Henter innhold fra /content/*.json (det adminpanelet redigerer) og fyller sidene.

// Når siden lastes på nytt, starter man øverst i stedet for der man var (nettleseren husker det ellers).
// Lenker med anker (/#styret osv.) går fortsatt til riktig sted, se hoppTilAnker.
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
if (!location.hash) window.scrollTo(0, 0);

// Adresselinjen viser alltid https://gjovikmikrotek.no/, uansett side (ønske fra styret).
// Den egentlige adressen (side, ?a=, ?p=, #anker) ligger i EKTE og i historikken (history.state),
// så Tilbake-knappen og «Last inn på nytt» kommer til riktig side, se skriptet øverst i index.html.
// Ankeret (#kontakt osv.) lagres ikke i historikken, så «Last inn på nytt» alltid starter øverst på siden.
const EKTE = new URL(location.href);
function skjulAdresse() {
  const uten = new URL(EKTE.href);
  uten.hash = '';
  history.replaceState({ ekte: uten.href }, '', '/');
}
skjulAdresse();
window.addEventListener('hashchange', skjulAdresse);

// Når adressen er «/», tror nettleseren at lenkene /#styret, /#kontakt osv. peker til samme side,
// og blir stående (f.eks. på Artikler). Utenfor forsiden går de derfor via /index.html, som laster forsiden.
if (!/^\/(index\.html)?$/.test(EKTE.pathname)) {
  document.querySelectorAll('a[href^="/#"], a[href="/"]').forEach(a => {
    a.setAttribute('href', '/index.html' + a.getAttribute('href').slice(1));
  });
}

// Språk: norsk (nb) eller engelsk (en).
// Valget leses fra ?lang= i adressen, deretter fra forrige besøk, ellers fra nettleserens språk.
const SPRAK = (() => {
  const fraUrl = EKTE.searchParams.get('lang');
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
    fra_instagram: 'Fra Instagram', folg_instagram: 'Følg oss på Instagram →', instagram_alt: 'Innlegg på Instagram', insta_tekst: 'Bilder fra byggingen og arrangementene våre legges ut på Instagram.',
    styret: 'Styret', styret_tom: 'Styret legges inn snart.', mer_om_styret: 'Mer om styret →', les_mer: 'Les mer',
    sponsorer: 'Sponsorer og samarbeidspartnere', sponsor_tom: 'Vil du støtte oss? Ta kontakt!',
    Hovedsponsor: 'Hovedsponsor', Sponsor: 'Sponsor', Samarbeidspartner: 'Samarbeidspartner',
    kontakt: 'Kontakt', epost_tekst: 'Send oss en e-post på', k_organisasjon: 'Organisasjon', k_leder: 'Leder', k_kontakt: 'Ta kontakt', k_orgnr: 'Org.nr.', k_tlf: 'Telefon', k_epost: 'E-post', skjema: 'Fyll ut kontaktskjema',
    bunn: 'Studentorganisasjon ved NTNU Gjøvik', bytt: 'English', bytt_tittel: 'Switch to English',
    meny: 'Meny', nav_medlem: 'Bli medlem', banner_tittel: 'Bli med og bygg!',
    banner_tekst: 'Medlemskap er gratis og åpent for studenter ved NTNU Gjøvik.',
    skjema_tittel: 'Innmeldingsskjema',
    skjema_mangler: 'Innmeldingsskjemaet kommer snart. Ta kontakt med styret i mellomtiden.',
    nav_prosjekter: 'Prosjekter', prosjekter: 'Prosjekter', alle_prosjekter: 'Alle prosjekter →',
    tilbake_prosjekter: '← Alle prosjekter', ingen_prosjekter: 'Ingen prosjekter ennå.', fant_ikke_prosjekt: 'Fant ikke prosjektet.',
    Planlegges: 'Planlegges', 'Pågår': 'Pågår', Ferdig: 'Ferdig'
  },
  en: {
    nav_om: 'About', nav_artikler: 'News', nav_styret: 'Board', nav_sponsorer: 'Sponsors', nav_kontakt: 'Contact',
    om_tittel: 'About us', siste_artikler: 'Latest news', alle_artikler: 'All news →', tilbake: '← All news',
    artikler: 'News', ingen_artikler: 'No articles yet.', fant_ikke: 'Article not found.', kunne_ikke: 'Could not load the content.',
    fra_instagram: 'From Instagram', folg_instagram: 'Follow us on Instagram →', instagram_alt: 'Instagram post', insta_tekst: 'Photos from our builds and events are posted on Instagram.',
    styret: 'The board', styret_tom: 'Board members coming soon.', mer_om_styret: 'More about the board →', les_mer: 'Read more',
    sponsorer: 'Sponsors and partners', sponsor_tom: 'Want to support us? Get in touch!',
    Hovedsponsor: 'Main sponsor', Sponsor: 'Sponsor', Samarbeidspartner: 'Partner',
    kontakt: 'Contact', epost_tekst: 'Email us at', k_organisasjon: 'Organisation', k_leder: 'Chair', k_kontakt: 'Get in touch', k_orgnr: 'Org. no.', k_tlf: 'Phone', k_epost: 'Email', skjema: 'Fill out the contact form',
    bunn: 'Student organisation at NTNU Gjøvik', bytt: 'Norsk', bytt_tittel: 'Bytt til norsk',
    meny: 'Menu', nav_medlem: 'Join us', banner_tittel: 'Come build with us!',
    banner_tekst: 'Membership is free and open to students at NTNU Gjøvik.',
    skjema_tittel: 'Membership form',
    skjema_mangler: 'The membership form is coming soon. Please contact the board in the meantime.',
    nav_prosjekter: 'Projects', prosjekter: 'Projects', alle_prosjekter: 'All projects →',
    tilbake_prosjekter: '← All projects', ingen_prosjekter: 'No projects yet.', fant_ikke_prosjekt: 'Project not found.',
    Planlegges: 'Planned', 'Pågår': 'In progress', Ferdig: 'Completed'
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
      const url = new URL(EKTE.href);
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

// Artikkel- og prosjektadressen bygges alltid av den norske tittelen, så lenker virker på begge språk.
function tittelSlug(a) {
  return (a.tittel || '').toLowerCase()
    .replace(/æ/g, 'ae').replace(/ø/g, 'o').replace(/å/g, 'a')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function personSlug(m) {
  return tittelSlug({ tittel: m.navn || '' });
}

function portrett(m) {
  return m.bilde ? `<img src="${esc(m.bilde)}" alt="${esc(m.navn)}" loading="lazy">`
    : `<div class="initialer">${esc((m.navn || '?').split(' ').map(x => x[0]).join('').slice(0, 2))}</div>`;
}

function slug(a) {
  return (a.dato || '') + '-' + tittelSlug(a);
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

// Prosjektene vises i den rekkefølgen de står i adminpanelet (dra for å endre).
function synligeProsjekter(data) {
  return (data.prosjekter || []).filter(p => p.publisert !== false);
}

function statusMerke(p) {
  return p.status ? `<span class="status status-${esc(tittelSlug({ tittel: p.status }))}">${esc(t(p.status))}</span>` : '';
}

function prosjektKort(p) {
  const bilde = p.bilde ? `<img src="${esc(p.bilde)}" alt="" loading="lazy">` : '<div class="bilde-tom bilde-prosjekt"></div>';
  return `<a class="kort" href="/prosjekter.html?p=${encodeURIComponent(tittelSlug(p))}">
    ${bilde}
    <div class="kort-tekst">
      ${statusMerke(p)}
      <h3>${esc(felt(p, 'tittel'))}</h3>
      <p>${esc(felt(p, 'ingress'))}</p>
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
// Uten feed-lenke (eller hvis feeden ikke svarer) vises en knapp til profilen i stedet.
// Samme løsning som på gronnefingre-uis.no.
async function visInstagram(s) {
  const profil = trygLenke(s.instagram);
  const feed = s.instagram_feed || '';
  const visKnapp = () => {
    if (!profil) return;
    const k = document.getElementById('instagram-knapp');
    k.href = profil;
    k.textContent = '@' + (profil.match(/instagram\.com\/([^/?#]+)/i) || [, 'instagram'])[1];
    document.getElementById('instagram-boks').hidden = false;
    document.getElementById('instagram').hidden = false;
  };
  if (!/^https:\/\/feeds\.behold\.so\/[A-Za-z0-9_-]+$/.test(feed)) return visKnapp();
  const svar = await fetch(feed);
  if (!svar.ok) return visKnapp();
  const data = await svar.json();
  // Alle bildene i feeden: hvert innlegg, og hvert bilde inni karuseller. Videoer vises som stillbilde.
  const https = u => /^https:\/\//.test(u || '') ? u : '';
  const stillbilde = m => https(m.sizes?.medium?.mediaUrl) || (m.mediaType === 'VIDEO' ? https(m.thumbnailUrl) : https(m.mediaUrl));
  const perInnlegg = (data.posts || []).filter(p => /^https:\/\/(www\.)?instagram\.com\//.test(p.permalink || '')).map(p => {
    const alt = p.altText || p.prunedCaption || t('instagram_alt');
    const deler = p.children && p.children.length ? p.children : [p];
    return deler.map(m => ({ lenke: p.permalink, bilde: stillbilde(m), alt })).filter(b => b.bilde);
  });
  // Blandes på tvers av innleggene (første bilde fra hvert, så andre fra hvert …), så rutenettet ikke fylles fra én karusell
  const bilder = [];
  for (let i = 0; perInnlegg.some(l => l[i]); i++) perInnlegg.forEach(l => { if (l[i]) bilder.push(l[i]); });
  if (!bilder.length) return visKnapp();
  const rute = document.getElementById('instagram-bilder');
  const SYNLIGE = 6;
  rute.innerHTML = bilder.slice(0, SYNLIGE).map(b => `
    <a class="insta" href="${esc(b.lenke)}" target="_blank" rel="noopener">
      <img src="${esc(b.bilde)}" alt="${esc(b.alt)}" loading="lazy">
    </a>`).join('') +
    // Færre enn seks bilder (som i starten): en rute med lenke til profilen fyller resten av raden
    (bilder.length < SYNLIGE && profil ? `<a class="insta insta-folg" href="${esc(profil)}" target="_blank" rel="noopener" style="grid-column: span ${SYNLIGE - bilder.length}">
      <span>@${esc((profil.match(/instagram\.com\/([^/?#]+)/i) || [, 'instagram'])[1])}</span><span class="lenke-pil">${esc(t('folg_instagram'))}</span></a>` : '');
  rullerInstagram(rute, bilder, SYNLIGE);
  const folg = document.getElementById('instagram-folg');
  // Lenken i overskriften trengs bare når «Følg oss»-ruten ikke vises
  if (profil && bilder.length >= SYNLIGE) { folg.href = profil; folg.hidden = false; }
  document.getElementById('instagram').hidden = false;
}

// Viser seks bilder om gangen og bytter ett av dem med neste bilde med noen sekunders mellomrom,
// til alle bildene har vært vist, og så starter den på nytt.
// Står bare stille når fanen ikke vises. Byttet er en ren toning uten bevegelse,
// så den går også når animasjoner er slått av i operativsystemet.
function rullerInstagram(rute, bilder, synlige) {
  if (bilder.length <= synlige) return;
  let neste = synlige, plass = 0;
  const forhandslast = n => { const b = bilder[n % bilder.length]; if (b) new Image().src = b.bilde; };
  forhandslast(neste);
  setInterval(() => {
    if (document.hidden) return;
    const lenke = rute.children[plass];
    const b = bilder[neste];
    if (!lenke || !b) return;
    const img = lenke.querySelector('img');
    // Kryssovergang: det nye bildet legges bak, det gamle tones ut, og så byttes bildet uten blink
    lenke.style.backgroundImage = `url("${encodeURI(b.bilde)}")`;
    lenke.classList.add('bytter');
    setTimeout(() => {
      lenke.href = b.lenke;
      img.alt = b.alt;
      const ferdig = () => {
        img.style.transition = 'none';
        lenke.classList.remove('bytter');
        void img.offsetWidth;
        img.style.transition = '';
      };
      img.onload = ferdig;
      img.src = b.bilde;
      if (img.complete) ferdig();
    }, 1200);
    plass = (plass + 1) % synlige;
    neste = (neste + 1) % bilder.length;
    forhandslast(neste);
  }, 3500);
}

async function visForside() {
  try {
    const [s, prosjekt, artikler, styret, sponsorer, prosjekter] = await Promise.all([
      fellesInnstillinger(), hent('prosjekt'), hent('artikler'), hent('styret'), hent('sponsorer'),
      hent('prosjekter').catch(() => ({}))
    ]);
    document.title = s.navn || 'Gjøvik MikroTek';
    visInstagram(s).catch(e => console.error('Instagram:', e)).then(hoppTilAnker);

    if (s.hovedbilde) {
      const h = document.getElementById('hero');
      // Bildet vises uskarpt med et lyst slør over (se .hero.med-bilde i style.css)
      h.style.setProperty('--hero-bilde', `url("${encodeURI(s.hovedbilde)}")`);
      h.classList.add('med-bilde');
    }

    document.getElementById('om-tittel').textContent = felt(prosjekt, 'tittel') || t('om_tittel');
    document.getElementById('om-tekst').innerHTML = md(felt(prosjekt, 'tekst'));

    // To av hver side ved side (se .forside-par i style.css). Resten ligger under «Alle prosjekter/artikler».
    const pr = synligeProsjekter(prosjekter).slice(0, 2);
    if (pr.length) {
      document.getElementById('prosjekter-liste').innerHTML = pr.map(prosjektKort).join('');
      document.getElementById('prosjekter').hidden = false;
    }

    const siste = synligeArtikler(artikler).slice(0, 2);
    document.getElementById('artikler-siste').innerHTML = siste.length
      ? siste.map(artikkelKort).join('')
      : `<p class="tom">${esc(t('ingen_artikler'))}</p>`;

    // Hver person lenker til sin plass på styresiden, der teksten om personen åpnes
    document.getElementById('styret-liste').innerHTML = (styret.medlemmer || []).map(m => `
      <a class="person" href="/styret.html#${esc(personSlug(m))}">
        ${portrett(m)}
        <strong>${esc(m.navn)}</strong>
        <span>${esc(felt(m, 'rolle'))}</span>
      </a>`).join('') || `<p class="tom">${esc(t('styret_tom'))}</p>`;

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

    // Kontakt i to spalter: organisasjonen og kanalene
    const linje = (etikett, verdi) => verdi ? `<span class="k-etikett">${esc(etikett)}</span>${verdi}` : '';
    const orgnr = String(s.orgnr || '').replace(/\D/g, '');
    document.getElementById('k-org').innerHTML = [
      `<strong>${esc(s.navn || 'Gjøvik MikroTek')}</strong>`,
      orgnr && linje(t('k_orgnr'), `<a href="https://virksomhet.brreg.no/nb/oppslag/enheter/${orgnr}" target="_blank" rel="noopener">${esc(orgnr.replace(/(\d{3})(\d{3})(\d{3})/, '$1 $2 $3'))}</a>`),
      s.adresse && esc(s.adresse),
      s.epost && linje(t('k_epost'), `<a href="mailto:${esc(s.epost)}">${esc(s.epost)}</a>`)
    ].filter(Boolean).join('<br>');
    // E-posten står under organisasjonen til venstre; Instagram og LinkedIn som ikoner til høyre
    const insta = trygLenke(s.instagram);
    const li = trygLenke(s.linkedin);
    const ikon = (url, navn, svg) => url ? `<a class="k-ikon k-ikon-${navn.toLowerCase()}" href="${esc(url)}" target="_blank" rel="noopener" aria-label="${esc(navn)}" title="${esc(navn)}">${svg}</a>` : '';
    const IKON_INSTA = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>';
    const IKON_LI = '<svg viewBox="4.6 4.6 15.4 15.4" aria-hidden="true"><g fill="currentColor"><rect x="6.4" y="10" width="2.6" height="7.6"/><circle cx="7.7" cy="7.1" r="1.55"/><path d="M11.1 10h2.5v1.1c.4-.7 1.3-1.3 2.6-1.3 2.2 0 2.8 1.4 2.8 3.4v4.4h-2.6v-3.9c0-1-.2-1.8-1.2-1.8-1.1 0-1.5.8-1.5 1.9v3.8h-2.6z"/></g></svg>';
    const ikoner = ikon(insta, 'Instagram', IKON_INSTA) + ikon(li, 'LinkedIn', IKON_LI);
    document.getElementById('k-kanaler').innerHTML = [
      ikoner && `<span class="k-ikoner">${ikoner}</span>`
    ].filter(Boolean).join('<br>');
    const skjema = trygLenke(s.skjema_lenke);
    if (skjema) {
      document.getElementById('skjema-lenke').href = skjema;
      document.getElementById('skjema-boks').hidden = false;
    }
    hoppTilAnker();
  } catch (e) {
    console.error(e);
  }
}

// Lenkene /#styret, /#sponsorer osv. hopper til ankeret idet siden lastes, før innholdet over er hentet.
// Når innholdet kommer, dyttes ankeret nedover, og man blir stående på feil sted (typisk ved Prosjekter).
// Derfor hopper vi til ankeret på nytt når innholdet er på plass.
function hoppTilAnker() {
  if (!EKTE.hash) return;
  const el = document.getElementById(EKTE.hash.slice(1));
  if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
}

async function visArtikler() {
  const boks = document.getElementById('innhold');
  try {
    const [s, data] = await Promise.all([fellesInnstillinger(), hent('artikler')]);
    const alle = synligeArtikler(data);
    const valgt = EKTE.searchParams.get('a');

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

async function visProsjekter() {
  const boks = document.getElementById('innhold');
  try {
    const [s, data] = await Promise.all([fellesInnstillinger(), hent('prosjekter')]);
    const alle = synligeProsjekter(data);
    const valgt = EKTE.searchParams.get('p');

    if (valgt) {
      const p = alle.find(x => tittelSlug(x) === valgt);
      if (!p) { boks.innerHTML = `<p>${esc(t('fant_ikke_prosjekt'))} <a href="/prosjekter.html">${esc(t('tilbake_prosjekter'))}</a></p>`; return; }
      document.title = felt(p, 'tittel') + ' – ' + (s.navn || 'Gjøvik MikroTek');
      boks.innerHTML = `<article class="artikkel">
        <a href="/prosjekter.html" class="lenke-pil">${esc(t('tilbake_prosjekter'))}</a>
        <div class="prosjekt-status">${statusMerke(p)}</div>
        <h1>${esc(felt(p, 'tittel'))}</h1>
        <p class="ingress">${esc(felt(p, 'ingress'))}</p>
        ${p.bilde ? `<img src="${esc(p.bilde)}" alt="" class="artikkel-bilde">` : ''}
        <div class="brodtekst">${md(felt(p, 'tekst'))}</div>
      </article>`;
      return;
    }

    document.title = t('prosjekter') + ' – ' + (s.navn || 'Gjøvik MikroTek');
    boks.innerHTML = `<h1>${esc(t('prosjekter'))}</h1><div class="kort-rutenett">` +
      (alle.map(prosjektKort).join('') || `<p class="tom">${esc(t('ingen_prosjekter'))}</p>`) + '</div>';
  } catch (e) {
    console.error(e);
    boks.innerHTML = `<p>${esc(t('kunne_ikke'))}</p>`;
  }
}

// Styresiden: alle styremedlemmene. Har personen en tekst («Om personen» i adminpanelet),
// åpnes den i et felt under navnet når man klikker på navnet eller bildet.
async function visStyret() {
  const boks = document.getElementById('innhold');
  try {
    const [s, styret] = await Promise.all([fellesInnstillinger(), hent('styret')]);
    document.title = t('styret') + ' – ' + (s.navn || 'Gjøvik MikroTek');
    const medl = styret.medlemmer || [];
    boks.innerHTML = `<h1>${esc(t('styret'))}</h1>` +
      (felt(styret, 'intro') ? `<div class="brodtekst styret-intro">${md(felt(styret, 'intro'))}</div>` : '') +
      (medl.length ? '<div class="styre-kort">' + medl.map(m => {
        const om = felt(m, 'om');
        const hode = `${portrett(m)}<strong>${esc(m.navn)}</strong><span>${esc(felt(m, 'rolle'))}</span>`;
        const epost = m.epost ? `<p><a href="mailto:${esc(m.epost)}">${esc(m.epost)}</a></p>` : '';
        return om
          ? `<details class="person styre-person" id="${esc(personSlug(m))}"><summary>${hode}<em class="les-mer" aria-hidden="true">${esc(t('les_mer'))}</em></summary><div class="person-om brodtekst">${md(om)}${epost}</div></details>`
          : `<div class="person styre-person" id="${esc(personSlug(m))}">${hode}${epost ? `<div class="person-om">${epost}</div>` : ''}</div>`;
      }).join('') + '</div>' : `<p class="tom">${esc(t('styret_tom'))}</p>`);
    // Kommer man fra forsiden (/styret.html#navn), åpnes den personen
    const valgt = EKTE.hash && document.getElementById(decodeURIComponent(EKTE.hash.slice(1)));
    if (valgt) {
      if (valgt.tagName === 'DETAILS') valgt.open = true;
      valgt.scrollIntoView({ behavior: 'instant', block: 'center' });
    }
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
  if (!/^https:\/\/forms\.(office\.com|microsoft\.com|cloud\.microsoft)\//i.test(url)) return null;
  const visning = url.includes('ResponsePage.aspx') && !/[?&]embed=true/i.test(url) ? url + '&embed=true' : url;
  return { visning };
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
    // Skjemaet har egen rullefelt (se style.css). Takkemeldingen fra Forms vises øverst i skjemaet,
    // og med egen rullefelt står den synlig i boksen idet man trykker «Send».
    // Forms sender ingen melding ut av skjemaet ved innsending (testet 20.10.2026), så siden kan ikke reagere på det.
    ramme.appendChild(iframe);
    ramme.hidden = false;
  } catch (e) {
    console.error(e);
  }
}
