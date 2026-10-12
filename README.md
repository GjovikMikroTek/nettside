# Prosjektside – oppsett

Statisk nettside + adminpanel (Decap CMS). Ingen server, database eller byggesteg.

**Slik henger det sammen:**
Innholdet ligger som JSON-filer i `site/content/`. Adminpanelet (`/admin`) redigerer de filene direkte i GitHub. Netlify oppdager endringen og publiserer siden på nytt (ca. 30–60 sek).

```
Adminpanel (/admin) ──lagrer──▶ GitHub-repo ──varsler──▶ Netlify ──publiserer──▶ dittdomene.no
```

## Mappestruktur

| Fil / mappe | Hva |
|---|---|
| `site/index.html` | Forsiden (om, siste artikler, styret, sponsorer, kontakt) |
| `site/artikler.html` | Artikkeloversikt og enkeltartikler (`?a=...`) |
| `site/bli-medlem.html` | Innmelding (Microsoft Forms → Excel-medlemsregister) |
| `site/content/*.json` | **Alt innhold** – det adminpanelet endrer |
| `site/admin/config.yml` | Hvilke felt som finnes i adminpanelet |
| `site/assets/` | Design (`style.css`), logikk (`app.js`), logo |
| `site/images/uploads/` | Bilder lastet opp i adminpanelet |
| `netlify.toml` | Forteller Netlify at `site/` er nettsiden |

## Kontoer (alle eies av Gjøvik MikroTek / Paulina, ikke av Richard)

1. **E-post til kontoene.** Bruk en e-post som ikke forsvinner når Paulina er ferdig på NTNU (f.eks. privat eller en felles prosjektadresse). En NTNU-adresse stenges etter studiene, og da mister man tilgang til GitHub/Netlify-gjenoppretting.
2. **GitHub** (github.com) – lagrer koden og innholdet.
3. **Netlify** (netlify.com) – hosting. Logg inn med «Sign up with GitHub».
4. **Domene** – Paulina kjøper selv (f.eks. hos Domeneshop, one.com). Gratis alternativ: `prosjektnavn.netlify.app`.

## Oppsett, steg for steg (gjøres én gang, ca. 30–45 min)

### 1. Repo på GitHub
- Logget inn på foreningens GitHub (GjovikMikroTek): «New repository» → navn f.eks. `prosjektside` → Public eller Private (begge fungerer).
- Åpne denne mappen i VS Code, og i terminalen:
  ```bash
  git init
  git add .
  git commit -m "Første versjon av nettsiden"
  git branch -M main
  git remote add origin https://github.com/BRUKERNAVN/prosjektside.git
  git push -u origin main
  ```
- Hvis du (Richard) pusher fra din egen PC: Paulina legger deg til som *collaborator* midlertidig (Settings → Collaborators), og fjerner deg når alt virker.

### 2. Endre to linjer i `site/admin/config.yml`
```yaml
repo: BRUKERNAVN/prosjektside
site_url: https://dittdomene.no
```
Commit og push.

### 3. Netlify
- «Add new site» → «Import an existing project» → GitHub → velg repoet.
- Byggeinnstillinger: la build command stå tom. Publish directory leses fra `netlify.toml` (`site`).
- Deploy. Siden ligger nå på `noe-tilfeldig.netlify.app`.

### 4. Innlogging til adminpanelet (GitHub OAuth via Netlify)
- GitHub (foreningens konto, GjovikMikroTek): Settings → Developer settings → OAuth Apps → **New OAuth App**
  - Homepage URL: `https://dittdomene.no` (eller netlify-adressen)
  - Authorization callback URL: `https://api.netlify.com/auth/done`
  - Kopier **Client ID** og lag en **Client secret**.
- Netlify: Site configuration → Access & security → OAuth → **Install provider** → GitHub → lim inn ID og secret.
- Test: gå til `/admin`, «Login with GitHub».

Alle med skrivetilgang til repoet kan logge inn. Nye redaktører (f.eks. styremedlemmer) legges til som collaborators i GitHub.

### 5. Domene
- Netlify: Domain management → Add domain → skriv domenet.
- Hos domeneleverandøren: legg inn DNS-oppføringene Netlify viser (enklest: bytt navnetjenere til Netlify).
- HTTPS kommer automatisk når DNS er på plass (kan ta noen timer).

## Instagram-bilder (Behold)

Instagram stengte den gratis koblingen for vanlige profiler i desember 2024. Den offisielle koblingen krever nå en server som fornyer en tilgangsnøkkel hver 60. dag, og det passer ikke en statisk side. Derfor brukes **Behold** (behold.so). Tjenesten henter innleggene og lager en JSON-feed som nettsiden leser.

- Krever en profesjonell Instagram-konto (Bedrift/Innholdsskaper). Det er gratis å bytte.
- Gratisplanen: 1 feed, opptil 6 innlegg, oppdateres én gang i døgnet, 1 200 visninger per måned. Når taket er nådd, skjules bildene til neste måned. Resten av siden fungerer som før.
- Kontoen opprettes av prosjektet, ikke av Richard. Oppsett: se BRUKSANVISNING.md.

## Microsoft 365 / Outlook (NTNU-kontoen)

Nettsiden trenger ikke kobles direkte til Outlook. Det som gir mening:

- **Kontakt- og sponsorskjema → Excel:** Lag et skjema i **Microsoft Forms** med prosjektets/NTNU-kontoen. Svarene havner automatisk i et Excel-ark («Åpne i Excel»). Lim inn skjemalenken i adminpanelet → Innstillinger → «Microsoft Forms-lenke». Da vises en knapp på nettsiden.
- **Varsel i Outlook:** I Forms kan man skru på e-postvarsel for hvert nytt svar.
- **Word:** Ingen naturlig automatisk kobling. Artikler kan skrives i Word og limes inn i adminpanelet; formatering (fet, lister, overskrifter) blir med.

## Hvis noe går galt
- **Siden viser gammelt innhold:** vent ett minutt og last inn på nytt. Sjekk «Deploys» i Netlify.
- **Feil etter en endring:** Netlify → Deploys → velg en tidligere versjon → «Publish deploy». Alt ligger også som historikk i GitHub.
- **Kan ikke logge inn i /admin:** sjekk at `repo:` i `config.yml` stemmer, og at OAuth-provideren er installert i Netlify.
