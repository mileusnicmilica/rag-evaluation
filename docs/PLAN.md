# Nedelja 7: plan rada u paru

Radni folder: `C:\Users\HP\Desktop\AI Bootcamp\week7-rag`

## Podela

### Milica — početno stanje i specifikacija

1. Preuzima tutorovu arhivu `rag-week-7-weak-checkpoint.zip` i dokument „Šablon za izveštaj pre/posle“. Čuva izvorni checkpoint bez izmena.
2. Prema projektnom README-u podešava okruženje, pokreće početne testove i svih 12 eval pitanja. Čuva rezultat kao `results/before.json` i beleži tačnu komandu.
3. Za najmanje dva konkretna eval pitanja beleži ID, očekivani odgovor/citat, dobijeni odgovor/citat i vrstu propusta.
4. Bira **jednu** nameravanu promenu i piše specifikaciju *pre izmene*: problem, hipotezu, mesto i obim izmene, očekivani efekat, rizik regresije i način provere. Predaje Nemanji specifikaciju i početni rezultat.

### Nemanja — implementacija i ponovno merenje

1. Proveri specifikaciju i sprovedi tačno jednu dogovorenu promenu. Ne menjaj `eval/eval_set.json` ni kod koji računa metrike.
2. Pokreni `python -m pytest`, zatim svih 12 eval pitanja istom komandom kao pre izmene. Sačuvaj `results/after.json`.
3. Sačuvaj izlaz alata za poređenje i `diff` (ili commit). Proveri da je otisak eval skupa isti; navedi sva popravljena pitanja, regresije i promenu metrika.
4. Za jedno promenjeno pitanje ručno pokreni CLI i proveri odgovor i citat.

### Zajedno — izveštaj i predaja

1. Milica i Nemanja popunjavaju izveštaj pre/posle prema tutorovom šablonu. Milica opisuje početne propuste i hipotezu; Nemanja opisuje izmenu i rezultat. Zajedno proveravaju zaključke i navode bar jedno preostalo ograničenje.
2. Zabeležite stvarni doprinos svakog člana, upotrebu AI asistenta i način na koji ste proverili njegove predloge. Dogovorite ko vodi demonstraciju na Sesiji 2.
3. Milica i Nemanja zajedno pregledaju dodeljeni izveštaj drugog para i ostavljaju zajednički komentar. Zajedno čitaju komentar para koji pregleda njihov izveštaj i unose ga u svoj izveštaj.
4. Svako šalje sopstveni nedeljni izveštaj, uz isti zajednički izveštaj pre/posle i potrebne dokaze.

## Redosled i rokovi

`checkpoint → before → dva propusta → pisana specifikacija → jedna izmena → after → poređenje i CLI → izveštaj → pregled para → predaja`

- Ponedeljak, 19. oktobar 2026, 20:00: komentar u Discord niti „Nedelja 7: pregled para“.
- Utorak, 20. oktobar 2026, 12:00: pojedinačni imejlovi tutoru.
- Sreda, 21. oktobar 2026: demonstracija na Sesiji 2.

## Potrebni materijali

Tutorov `rag-week-7-weak-checkpoint.zip` je naknadno dostavljen; original se nalazi u Downloads, a raspakovan projekat u radnom folderu. Početni rezultat i Milicina analiza nalaze se u `pocetno-stanje.md`, a specifikacija u `specifikacija-promene.md`. „Šablon za izveštaj pre/posle“ još nije pronađen među dostupnim fajlovima.

**Status:** Milica je potvrdila plan 19. oktobra 2026. Početna provera, analiza propusta i nacrt specifikacije su završeni; Milica treba da ih pregleda. Nemanjina implementacija promene nije započeta.

**Naknadni napredni eksperiment:** na Milicin zahtev dodat je opcioni embedding režim u projektnom `src`. Rezultati i ograničenja su zapisani u `napredni-embedding-eksperiment.md`; obavezna M5 promena ostaje zaseban korak.
