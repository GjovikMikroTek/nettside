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
Adminpanel (/admin) → lagrer i GitHub → Cloudflare Pages publiserer → gjovik-mikrotek.pages.dev
```

1. **Innholdet** ligger som JSON-filer i `site/content/` (artikler, styret, sponsorer, innstillinger, om prosjektet).
2. **Adminpanelet** (Decap CMS, `site/admin/`) er et skjema i nettleseren som redigerer disse filene direkte i GitHub. Innlogging skjer med GitHub.
3. **Cloudflare Pages** oppdager endringen og publiserer siden på nytt, vanligvis innen ett minutt.
4. **Sidene** (`index.html`, `artikler.html`) henter innholdet fra JSON-filene med JavaScript (`site/assets/app.js`).

Alle endringer lagres som historikk i GitHub. En feil kan derfor alltid rulles tilbake.

## Hvem eier hva
Alle kontoer eies av Gjøvik MikroTek / Paulina, ikke av Richard:
- **GitHub:** lagrer koden og innholdet
- **Cloudflare:** hosting og innlogging til adminpanelet
- **Domene:** kjøpes av Paulina
- **Microsoft 365 / Outlook (NTNU):** brukes til Microsoft Forms for kontakt- og sponsorskjema. Svarene havner automatisk i Excel.

Kontoene bør opprettes med en e-post som ikke stenges etter studiene (ikke NTNU-adressen).

## Status (12.10.2026)
- [x] Startpakke: forside, artikler, styret, sponsorer, kontakt, «Bli medlem», adminpanel (Decap CMS)
- [x] Logo (alltid original), lys byggteknisk palett, gruppebilde som uskarp toppbakgrunn
- [x] Norsk/engelsk, mobilmeny, Instagram-feed (Behold 5LIqyMhQTSSTbr09vbVQ, @gjovik_mikrotek)
- [x] Styret 2026 lagt inn (fra «26.1102.A Medlemsregister.docx»); PR-ansvarlig i styret ukjent
- [x] GitHub: github.com/GjovikMikroTek/nettside (offentlig, main). Paulina (paucz05) invitert med skrivetilgang
- [x] Hosting: Cloudflare Pages «gjovik-mikrotek» → https://gjovik-mikrotek.pages.dev (Netlify sperret kontoen 12.10.2026)
- [x] Innlogging til /admin: Cloudflare Worker `auth/` → https://gjovik-mikrotek-auth.gjovik-mikrotek.workers.dev, GitHub OAuth App «Gjøvik MikroTek admin» (secret i Cloudflare). Styret logger inn med GjovikMikroTek-kontoen
- [x] Spørsmålsliste til styremøtet sendt (Word); venter på svar
- [x] Excel-mal for medlemsregister laget lokalt («Medlemsregister Gjøvik MikroTek.xlsx»): fanene Oversikt (logo, tallkort, graf, styret, per år), Medlemmer (tabell «Medlemmer», Status Aktiv/Utmeldt/Test) og Statistikk (tabell «Innmeldinger», bare dato + medlemsnr). Velkomst-e-post med logo: «Velkomst-e-post (Power Automate).html». Medlemsnr MT-0001 fra Forms-svar-ID
- [x] 12.10.2026: Forms-skjema «Innmelding Gjøvik MikroTek» (tittel nå «Bli med i tidenes studentprosjekt») + Power Automate-flyt «Ny innmelding til medlemsregister» (Paulinas konto paulia@stud.ntnu.no, Excel i OneDrive /GMT/) virker: rad i Medlemmer + Innmeldinger, velkomst-e-post. Testrad MT-0001 (sett Status=Test). Skjemaet har ikke Institutt; Årstrinn er fritekst; Telefon er påkrevd (bevisst valg)
- [x] Prosjekter-side (`prosjekter.html`, `content/prosjekter.json`, `?p=<slug av tittel>`), egen seksjon på forsiden og menypunkt. Første prosjekt: GMT Mikrohus med 3D-bilde (gmt-mikrohus-3d.png)
- [x] Adminpanelet i GMT-stil: `site/admin/admin.css` (mørk topp, logo, rutenett). Treffer Decaps klassenavn med `[class*="-Komponent"]`, derfor er Decap låst til 3.16.3 i `admin/index.html`
- [x] 13.10.2026: Mørk «tech»-stil på nettsiden (hero, «//»-overskrifter, banner, bunn) som adminpanelet. Toppmenyen har fortsatt original logo; på mørk bakgrunn brukes `logo-hvit.svg`. 3D-huset ligger i `assets/mikrohus-3d.svg`
- [x] 13.10.2026: Innmeldingsskjemaet (Forms, forms.cloud.microsoft) er bygd inn på `/bli-medlem.html` med stor logo + 3D-hus. Det er lenken som skal deles (QR, Instagram). Skjemagrafikk ligger i `../Skjema-grafikk/`
- [x] 13.10.2026: Forms-skjemaet har fått GMT-utseende (mørkt toppfelt, rundt logomerke, rutenett)
- [x] 13.10.2026: `[FOTO]` i velkomst-e-posten koblet til Foto/video-samtykke. «Bli medlem» hopper til toppen av siden etter innsending (iframe-load / postMessage i `visMedlem()`), testet
- [ ] 20.10.2026: Innmelding gjør deg ikke til medlem automatisk. Flyt 1 skal sette Status=**Ny**, og HR setter **Aktiv** for hånd etter oppfølging. E-posten sier at HR tar kontakt. Må gjøres i Power Automate (Status i «Add a row») og i Excel (Ny i Status-listen, «Slik brukes arket»)
- [ ] Venter (13.10.2026): styret har ikke bestemt om innmeldingsskjemaet skal brukes. Flyt 2 «Utmelding og sletting» er satt på vent, oppskrift: planlagt skyflyt kl. 03 (hver natt: Status=Utmeldt → fyll Utmeldt dato + Slettes dato (+30 d) → slett raden når Slettes dato er passert). Kolonnene finnes alt i tabellen Medlemmer. Innmeldinger (bare dato + ID) beholdes for statistikk
- [x] 13.10.2026: QR-kode til https://gjovik-mikrotek.pages.dev/bli-medlem i `../QR-kode/` (med emblem, med hele logoen, uten logo som PNG/SVG) + A4-plakat «Plakat Bli medlem (A4).pdf/.png» (kilde og lag.py i `../QR-kode/kilde/`). pages.dev-adressen virker også etter eget domene, så koden trenger ikke lages på nytt
- [ ] Pause fra 13.10.2026: styret gjør de endringene de selv vil på nettsiden først. Richard kommer tilbake til prosjektet senere (domene, svar fra styremøtet, oppdatere BRUKSANVISNING.md, flyt 2 hvis skjemaet skal brukes)
- [ ] Medlemsregister: bygges midlertidig på Paulinas egen NTNU-konto (12.10.2026, passordet til mikrotek@ivb.ntnu.no mangler). Flyttes til mikrotek@ivb.ntnu.no når tilgangen er på plass (overfør Forms-eierskap, kopier Excel, lag flytene på nytt). Steg: sjekk Power Automate-lisens → last opp Excel til OneDrive → lag Forms-skjema → flyt 1 (ny innmelding → ny rad, Status=Ny) → flyt 2 (hver natt: Utmeldt → sett datoer, slett etter 30 dager) → sjekk Power Automate-lisens → last opp Excel til OneDrive → lag Forms-skjema → flyt 1 (ny innmelding → ny rad, Status=Ny) → flyt 2 (hver natt: Utmeldt → sett datoer, slett etter 30 dager) →
- [ ] Legge inn svarene fra styremøtet (kontakt-e-post, PR-ansvarlig, frivillige?, utforming, domene)
- [ ] Eget domene (valgfritt) – legg da også til i ALLOWED_ORIGINS i `auth/wrangler.toml`
- [ ] Gå gjennom BRUKSANVISNING.md med Paulina
- [ ] Logge ut Wrangler (`npx wrangler logout`) når oppsettet er ferdig

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
