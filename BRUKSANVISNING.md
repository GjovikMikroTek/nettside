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

## Legge til eller fjerne sponsorer
**Sider og innhold** → **Sponsorer**. Velg nivå (Hovedsponsor vises størst). Last opp logo (helst PNG eller SVG med gjennomsiktig bakgrunn).

## Endre tekst om prosjektet, e-post, farge osv.
- **Om prosjektet:** teksten i «Om»-delen.
- **Innstillinger:** prosjektnavn, slagord, forsidebilde, profilfarge, kontakt-e-post, Instagram/LinkedIn og lenke til kontaktskjema.

## Medlemsregister («Bli medlem»)
Siden **/bli-medlem.html** har et innmeldingsskjema fra Microsoft Forms. Hver innmelding blir en ny rad i en Excel-fil i Microsoft-kontoen deres. Excel-filen er medlemsregisteret som vedtektene § 3.1 krever.

Oppsett, én gang (logget inn på foreningens Microsoft-konto):
1. Gå til **forms.office.com** → «Nytt skjema». Kall det f.eks. «Innmelding Gjøvik MikroTek».
2. Foreslåtte spørsmål:
   - Fullt navn (tekst, påkrevd)
   - E-post (tekst, påkrevd)
   - Telefon (tekst, valgfritt)
   - Studieprogram (tekst, påkrevd)
   - Årstrinn (valg: 1, 2, 3, 4, 5)
   - Institutt (valg: IVB, IES, annet)
   - «Jeg samtykker til at opplysningene lagres i medlemsregisteret til Gjøvik MikroTek» (valg: Ja, påkrevd)
3. Under **Svar** → «Åpne i Excel». Da opprettes en Excel-fil i OneDrive som fylles automatisk med nye svar.
4. Trykk **Samle inn svar** → «Hvem som helst kan svare». Kopier lenken. Du kan også bruke «Bygg inn» og kopiere hele koden.
5. I adminpanelet: **Sider og innhold** → **Bli medlem (medlemsregister)** → lim inn i «Microsoft Forms-skjema» → Publiser.

Tips:
- Skru på e-postvarsel for nye svar i Forms (… → Innstillinger), så styret ser nye medlemmer med en gang.
- Utmeldinger (vedtektene § 3.2) håndteres i Excel-filen. Slett raden 30 dager etter at noen har meldt seg ut. Slett også medlemmer som er ferdige med studiene.
- Excel-filen inneholder personopplysninger. Del den bare med styret.

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

## Kontaktskjema som havner i Excel
1. Lag et skjema i **Microsoft Forms** (med Outlook-/NTNU-kontoen).
2. Trykk «Samle inn svar» → kopier lenken.
3. Lim den inn under **Innstillinger** → «Microsoft Forms-lenke».
Svarene finner du i Forms under «Svar» → «Åpne i Excel».

## Tips
- Bilder: hold dem under ca. 1–2 MB. Mobilbilder kan gjerne forminskes først.
- Gjort noe feil? Alle versjoner lagres. Den som satte opp siden kan rulle tilbake i Cloudflare eller GitHub.
- Gi andre tilgang: legg dem til som «collaborator» i GitHub-repoet. Da kan de logge inn på /admin.
