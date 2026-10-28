# Slik oppdaterer du nettsiden

## Logge inn
1. Gå til **https://gjovikmikrotek.no/admin/** (den gamle adressen gjovik-mikrotek.pages.dev/admin/ virker også)
2. Trykk **«Login with GitHub»**. Et lite vindu åpnes.
3. Logg inn med foreningens GitHub-konto:
   - Brukernavn: **GjovikMikroTek**
   - Passord: får du av styreleder (deles aldri på e-post eller i chat)
4. Ber GitHub om en kode, ligger den i innboksen til **foreningens felles e-post** (den styret har tilgang til). Skriv den inn.
   Koden går alltid til hovedadressen på GitHub-kontoen. Byttes e-posten, gjøres det på github.com → **Settings** → **Emails** (legg til, bekreft, velg som «Primary»).
5. Første gang: trykk **«Authorize»**.
6. Vinduet lukker seg, og du er inne i adminpanelet.

Husk å logge ut når du bruker en delt eller lånt PC.

Etter at du har trykket **Publish / Publiser**, er endringen ute på nettsiden etter ca. ett minutt.

## Skrive en ny artikkel
1. Velg **Artikler** → **Alle artikler**.
2. Trykk **«Legg til artikkel»** (øverst i listen).
3. Fyll inn tittel, dato, ingress (kort tekst som vises i oversikten), bilde og selve teksten.
4. Trykk **Publiser** øverst.

Vil du skjule en artikkel uten å slette den: slå av «Vis på nettsiden».

## Legge til eller oppdatere et prosjekt
1. Velg **Prosjekter** → **Alle prosjekter**.
2. Trykk **«Legg til prosjekt»**, eller åpne et prosjekt som finnes fra før.
3. Fyll inn tittel, status (Planlegges, Pågår eller Ferdig), bilde, ingress og prosjekttekst.
4. Trykk **Publiser** øverst.

Prosjektene vises på siden **Prosjekter** og øverst på forsiden, i samme rekkefølge som i adminpanelet. Dra dem for å endre rekkefølgen. Når et prosjekt er ferdig, endrer du bare statusen til «Ferdig».

## Oppdatere styret
**Sider og innhold** → **Styret**. Legg til, fjern eller dra medlemmer i den rekkefølgen de skal vises. Bilde er valgfritt. Uten bilde vises initialene.
- **Om personen:** litt om hvert styremedlem (studie, årstrinn, hva personen gjør i styret). Teksten vises på siden **Styret** når man klikker på navnet eller bildet.
- **Innledning på styresiden:** valgfri tekst øverst på siden Styret.
- Styret vises både på forsiden og på en egen side. Begge oppdateres når du publiserer.

## Legge til eller fjerne sponsorer
**Sider og innhold** → **Sponsorer**. Velg nivå (Hovedsponsor vises størst). Last opp logo (helst PNG eller SVG med gjennomsiktig bakgrunn).

## Endre tekst om prosjektet, e-post, farge osv.
- **Om prosjektet:** teksten i «Om»-delen.
- **Innstillinger:** prosjektnavn, slagord, forsidebilde, profilfarge, kontakt-e-post, Instagram/LinkedIn og lenke til kontaktskjema.

## Medlemsregister («Bli medlem»)
Siden **gjovikmikrotek.no/bli-medlem** har et eget innmeldingsskjema. Hver innmelding blir en ny rad i regnearket **«Gjøvik MikroTek – Medlemsregister»** i Google-kontoen til foreningen (den felles e-posten). Regnearket er medlemsregisteret som vedtektene § 3.1 krever.

**Slik går en innmelding:**
1. Den nye fyller ut skjemaet og kommer til forsiden med en takkemelding og et medlemsnummer (MT-0001, MT-0002 …).
2. En rad legges til i fanen **Medlemmer** med Status **Ny** (blå rad).
3. Den felles e-posten får e-posten **«⚠ Ny innmelding venter på oppfølging»**, og den nye får en velkomst-e-post med kopi av svarene.
4. HR tar kontakt, og setter Status til **Aktiv** når personen er tatt opp som medlem.

**Fanen Oversikt** viser «Venter på HR» (med navn), aktive medlemmer, nye denne måneden og i år, utmeldte, en graf over innmeldinger og styret. Navnene i styret skriver dere over i den hvite kolonnen ved styreskifte.

**Utmelding (vedtektene § 3.2):** sett Status til **Utmeldt**. Datoene fylles inn av seg selv, og raden slettes automatisk 30 dager senere. Angrer personen seg før det, setter dere Status tilbake til **Aktiv**. Medlemmer som er ferdige med studiene, meldes ut på samme måte.

**Testrader:** sett Status til **Test** (grå), og slett dem når dere er ferdige.

**Viktig:**
- Regnearket inneholder personopplysninger. Del det bare med styret (Del → legg til personene), aldri «alle med lenken».
- Ikke endre kolonneoverskriftene i fanen Medlemmer. Registeret bruker dem.
- Koden og hele oppsettet ligger i mappen `medlemsregister-google` (OPPSETT.md), hos den som har ansvaret for nettsiden.
- Lenken til registeret står i adminpanelet under **Sider og innhold** → **Bli medlem** → «Innmeldingsskjema (Google-registeret)». Ikke endre den. Står feltet tomt, vises det gamle Microsoft Forms-skjemaet i stedet.

## Engelsk versjon av siden
Besøkende kan bytte mellom norsk og engelsk med knappen øverst til høyre.
- De fleste tekstfelt i adminpanelet har et felt ved siden av som heter **«(engelsk)»**. Skriv den engelske teksten der.
- Lar du et engelsk felt stå tomt, vises den norske teksten også på den engelske siden. Ingenting blir tomt.
- Navn, bilder, e-post og lenker er like på begge språk og skrives bare én gang.

## Instagram-bilder på forsiden
De siste bildene fra Instagram vises automatisk på forsiden, under «Fra Instagram». Dere trenger ikke gjøre noe når dere legger ut nye bilder. Siden oppdateres av seg selv (gratisversjonen av Behold henter nye bilder én gang i døgnet).

Oppsett, én gang:
1. Instagram-kontoen må være en **profesjonell konto** (Bedrift eller Innholdsskaper). Gjøres i Instagram-appen: Innstillinger → Kontotype og verktøy → Bytt til profesjonell konto. Det er gratis.
2. Gå til **behold.so**, lag en gratis konto og koble til Instagram-kontoen.
3. Lag en ny feed av typen **JSON**, og kopier feed-lenken (`https://feeds.behold.so/...`).
4. I adminpanelet: **Innstillinger** → lim lenken inn i «Instagram-bilder (Behold-feed)». Lim også inn lenken til profilen i «Instagram-lenke».

Vil dere skjule bildene, tømmer dere feltet «Instagram-bilder».

## Kontaktskjema (valgfritt)
Vil dere ha en knapp «Fyll ut kontaktskjema» under Kontakt på forsiden:
1. Logg inn på foreningens Google-konto og lag et skjema på **forms.google.com**.
2. Trykk **Send** → lenke-ikonet → kopier lenken.
3. Lim den inn under **Innstillinger** → «Lenke til kontaktskjema» → Publiser.
Svarene finner du i Google Forms under **Svar** (og i et regneark hvis du trykker «Koble til Regneark»).

## Tips
- Bilder: hold dem under ca. 1–2 MB. Mobilbilder kan gjerne forminskes først.
- Gjort noe feil? Alle versjoner lagres. Den som satte opp siden kan rulle tilbake i Cloudflare eller GitHub.
- Gi andre tilgang: legg dem til som «collaborator» i GitHub-repoet. Da kan de logge inn på /admin.
