# Introduksjon: Prosjektside for Gjøvik MikroTek (studentorganisasjon ved NTNU Campus Gjøvik)

## Hva vi gjør
Vi lager en nettside for et studentprosjekt ved NTNU. Richard bygger og setter opp siden for Paulina, som er med i prosjektet.

**Hovedmålet:** Når oppsettet er ferdig, skal Paulina og prosjektgruppen kunne drive siden selv, uten Richard og uten å kunne kode. Paulina skal kunne:
- skrive og publisere artikler/innlegg
- oppdatere informasjon om styret
- legge til og fjerne sponsorer
- endre tekst, bilder, kontaktinfo og profilfarge

## Hvordan det fungerer
Siden er en statisk nettside med et adminpanel. Det finnes ingen server eller database å drifte.

```
Adminpanel (/admin) → lagrer i GitHub → Netlify publiserer → dittdomene.no
```

1. **Innholdet** ligger som JSON-filer i `site/content/` (artikler, styret, sponsorer, innstillinger, om prosjektet).
2. **Adminpanelet** (Decap CMS, `site/admin/`) er et skjema i nettleseren som redigerer disse filene direkte i GitHub. Innlogging skjer med GitHub.
3. **Netlify** oppdager endringen og publiserer siden på nytt, vanligvis innen ett minutt.
4. **Sidene** (`index.html`, `artikler.html`) henter innholdet fra JSON-filene med JavaScript (`site/assets/app.js`).

Alle endringer lagres som historikk i GitHub. En feil kan derfor alltid rulles tilbake.

## Hvem eier hva
Alle kontoer eies av Gjøvik MikroTek / Paulina, ikke av Richard:
- **GitHub:** lagrer koden og innholdet
- **Netlify:** hosting
- **Domene:** kjøpes av Paulina
- **Microsoft 365 / Outlook (NTNU):** brukes til Microsoft Forms for kontakt- og sponsorskjema. Svarene havner automatisk i Excel.

Kontoene bør opprettes med en e-post som ikke stenges etter studiene (ikke NTNU-adressen).

## Status (12.10.2026)
- [x] Startpakke bygget og testet lokalt (forside, artikler, styret, sponsorer, kontakt, adminpanel)
- [x] Logo lagt inn (SVG, hvit variant for mørk modus, favicon/app-ikoner i `site/assets/`)
- [x] Navn, slagord, beskrivelse, «Om oss» og profilfarger (blå `#2a529a`, oransje `#f39228`) fra logo, vedtekter og stiftelsesprotokoll
- [x] Språkvalg norsk/engelsk (alt eksisterende innhold er oversatt)
- [x] Instagram-bilder på forsiden fra @gjovik_mikrotek (Behold-feed 5LIqyMhQTSSTbr09vbVQ)
- [x] «Bli medlem»-side (`bli-medlem.html`, `content/medlem.json`) med Microsoft Forms innebygd → Excel = medlemsregister (kode ferdig; venter på skjemalenke)
- [x] Mobilmeny (menyknapp under 760 px) og mobiltilpasning testet på 375 px
- [ ] Ekte innhold som mangler: nåværende styre (seks roller etter vedtekter versjon B, 08.09.2026), kontakt-e-post, forsidebilde, sosiale medier
- [x] GitHub-repo: github.com/GjovikMikroTek/nettside (offentlig, branch main)
- [ ] Koble repoet til Netlify
- [ ] Sette opp GitHub-innlogging til adminpanelet (OAuth via Netlify)
- [ ] Koble til domenet
- [ ] Lage Microsoft Forms-skjema og lime lenken inn i adminpanelet
- [ ] Gå gjennom BRUKSANVISNING.md med Paulina

## Filer
| Fil | Til hvem |
|---|---|
| `README.md` | Teknisk oppsett, steg for steg (Richard) |
| `BRUKSANVISNING.md` | Hvordan Paulina oppdaterer siden |
| `site/admin/config.yml` | Hvilke felt som finnes i adminpanelet. `repo:` og `site_url:` må endres ved oppsett. |

## Regler for endringer i koden
- Omtal alltid personen siden lages for som **Paulina**, aldri «venninne» eller lignende.
- Hold det enkelt: ingen byggesteg, ingen database, ingen ekstra tjenester uten god grunn. Målet er at Paulina klarer seg selv.
- Nye typer innhold legges til ved å
  1. lage en JSON-fil i `site/content/`,
  2. legge til feltene i `site/admin/config.yml`,
  3. vise innholdet i `site/assets/app.js`.
- Siden er tospråklig (norsk bokmål og engelsk, knapp i toppmenyen, `?lang=nb|en`).
  - Faste tekster i HTML har `data-tekst="nokkel"` og står i `TEKST` i `app.js`, på begge språk.
  - Innholdsfelt som skal oversettes, får et tvillingfelt med `_en` (f.eks. `tittel_en`) i JSON og `config.yml`, og leses med `felt(obj, 'tittel')`. Tomt engelsk felt gir norsk tekst.
- Instagram-bilder hentes fra en Behold-feed (behold.so, JSON v2). Lenken ligger i `instagram_feed` i innstillingene. Krever profesjonell Instagram-konto.
- All tekst fra JSON-filene skal escapes (`esc()`) før den settes inn i HTML. Unntaket er markdown-felt, som går gjennom `md()`.
