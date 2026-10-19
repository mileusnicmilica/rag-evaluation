# Specifikacija jedne promene — M5: pretraga samo važećih dokumenata

**Napisano pre izmene RAG koda.** Osnova je stvarni početni rezultat [`before.json`](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/before.json) i analiza u [`pocetno-stanje.md`](pocetno-stanje.md). Ovo je specifikacija koju Milica predaje Nemanji na proveru i implementaciju.

## Propust

Na pitanju **E06** („How many days per week can I work remotely?“) očekuje se odgovor **3 days per week**, uz citat iz važećeg dokumenta `hb-03` (2026). Sistem odgovara **2 days per week** i citira samo `hb-02` (2024, `superseded`). Eval beleži `retrieval_hit=false`, `fact_in_citations=false`, `citation_precision=0.0` i `pass=false`.

Pretragom svih rangiranih delova za isto pitanje potvrđeno je da `hb-03-chunk-0` postoji i sadrži važeći podatak, ali ima skor **0.370370**; dva stara dela imaju **0.481481** i **0.400000**, pa zauzimaju oba mesta pri `TOP_K=2`.

## Hipoteza

Ako se iz pretrage uklone dokumenti sa statusom `superseded`, `hb-03-chunk-0` će ući u citate za E06 i odgovor će sadržati važeći podatak „3 days per week“. To je predviđanje, ne izmeren rezultat posle promene.

## Tačno jedna nameravana promena

Primena opcije **M5 — Current-version filter** iz `docs/improvement-menu.md` projekta:

1. U `src/config.py` postaviti `CURRENT_ONLY = True`.
2. U `src/retrieval.py`, u `searchable_chunks`, implementirati postojeću granu tako da, kada je `CURRENT_ONLY` uključeno, vrati samo delove sa `chunk.status == "current"` pre računanja skora. Kada je isključeno, zadržati postojeće ponašanje.

To su dve povezane izmene fajlova za **jednu nameru**: aktiviranje i sprovođenje filtera važeće verzije. Ne menjati chunkovanje, `TOP_K`, pragove, korpus, eval skup ni kod za metrike. Ciljani test filtera može biti deo iste izmene.

BM25 i embeddings, pomenuti na času, opisani su u početnoj analizi kao mogući **kasniji** pravci za E04/E09 i E05. Njihovo dodavanje uz M5 bi bila druga promena i onemogućilo bi jasno pripisivanje rezultata jednom uzroku.

## Očekivani efekat i rizici

- Primarni cilj: **E06** dobija `hb-03` i prolazi, uz citat iz važećeg dokumenta.
- Moguće sporedne promene: pitanja koja sada citiraju `hb-02` kao dodatni, nerelevantni izvor (npr. E01–E03) mogu dobiti druge citate i drugačiju preciznost. To se ne pretpostavlja kao uspeh dok se ne izmeri.
- Rizik regresije: upiti koji izričito traže istorijsku politiku više neće moći da koriste `superseded` dokument. Pošto eval skup nema takvo pitanje, ovo mora da bude navedeno kao ograničenje čak i ako svih 12 pitanja prođu.
- Očekivana preostala ograničenja: E04/E09 (deo s traženim rokom je četvrti odnosno peti po skoru), E05 (parafraza) i E10/E11 (neopravdani odgovori) nisu neposredna meta ove promene. Njih ipak treba proveriti u potpunom `after` rezultatu; filter može da utiče na rangiranje.

## Obavezna provera za Nemanju

1. Proveriti da je ovo jedina namera u diff-u i da je `eval/eval_set.json` ostao netaknut.
2. Pokrenuti `python -m pytest` u istom virtuelnom okruženju.
3. Pokrenuti svih 12 pitanja istom eval komandom i sačuvati `results/after.json`.
4. Pokrenuti `python -m src.eval_compare results/before.json results/after.json`; sačuvati izlaz, proveriti isti otisak eval skupa i navesti sva popravljena pitanja, regresije i metrike.
5. Ručno pokrenuti CLI za E06 sa `--show-retrieved`; proveriti tekst odgovora, citat, status i verziju dokumenta.
6. U izveštaju odvojiti izmereni ishod od ove hipoteze. Ako E06 i dalje ne prolazi, tako i napisati.

**Status u trenutku pisanja specifikacije:** implementacija nije bila započeta. Milica još treba da pregleda i potvrdi svoj deo pre zajedničke predaje.

**Naknadna beleška (19. oktobar 2026):** na Milicin poseban zahtev dodat je opcioni embedding režim u `src`. Njegov rezultat je dokumentovan [odvojeno](napredni-embedding-eksperiment.md). M5 iz ove specifikacije i dalje nije implementiran.

**Naknadni ishod M5:** Nemanja je sproveo opisani filter i izmerio rezultat. Dokazi i ograničenja su u [`nemanja-rezultati.md`](nemanja-rezultati.md).
