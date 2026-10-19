# Početno stanje RAG sistema — Milicin deo

## Dokazi i način pokretanja

- Izvorni checkpoint: `C:\Users\HP\Downloads\rag-week-7-weak-checkpoint.zip`, SHA-256 `31607f2f0de57f6b454b4c7e33a07e47efce7986525dd968999e717e4d98f333`.
- Svih **22 izvornih fajlova** iz arhive odgovara raspakovanim fajlovima pre bilo kakve izmene RAG koda.
- Projektni folder: [`rag-week-7-week-checkpoint`](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/README.md). README traži Python 3.12, a u dostupnom okruženju je Python **3.11.7**; projekat i svih 18 testova rade pod 3.11.7. To odstupanje treba pomenuti pri predaji.
- Okruženje je kreirano komandom `python -m venv .venv`, zatim instalirano `pytest==8.3.3` komandom `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- Početni testovi: `.\.venv\Scripts\python.exe -m pytest` → **18 passed in 0.67s**. Sačuvan [izlaz testova](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/baseline-tests.txt).
- Početni eval: `.\.venv\Scripts\python.exe -m src.eval_runner --out results/before.json`. Sačuvani [before.json](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/before.json) i [tekstualni izlaz](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/baseline-eval.txt).
- Za šest neuspešnih pitanja sačuvan je [CLI izlaz sa dohvaćenim delovima i skorovima](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/baseline-cli-failures.txt).
- SHA-256 eval skupa, jednak otisku u `before.json`: `afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064`.
- SHA-256 sačuvanog `before.json`: `02ad667f9c17363c6b543df7780698d4c4dccd55a6e3d20ddce502b912b306a3`.
- Početna konfiguracija: `CHUNK_STRATEGY=chars`, `CHUNK_SIZE=140`, `CHUNK_OVERLAP=30`, `TOP_K=2`, `RETRIEVAL_MIN_SCORE=0.01`, `STOPWORDS_ENABLED=False`, `CURRENT_ONLY=False`, `REFUSAL_THRESHOLD=0.02`, `CITATION_MIN_SCORE=None`.

## Rezultat svih 12 pitanja

| ID | Očekivano → dobijeno | Hit | Podatak u citatima | Preciznost citata | Ishod |
| --- | --- | --- | --- | ---: | --- |
| E01 | answer → answer | da | da | 0.50 | PASS |
| E02 | answer → answer | da | da | 0.50 | PASS |
| E03 | answer → answer | da | da | 0.50 | PASS |
| E04 | answer → answer | da | ne | 1.00 | FAIL |
| E05 | answer → answer | ne | ne | 0.00 | FAIL |
| E06 | answer → answer | ne | ne | 0.00 | FAIL |
| E07 | answer → answer | da | da | 1.00 | PASS |
| E08 | answer → answer | da | da | 0.50 | PASS |
| E09 | answer → answer | da | ne | 1.00 | FAIL |
| E10 | refuse → answer | — | — | 0.00 | FAIL |
| E11 | refuse → answer | — | — | 0.00 | FAIL |
| E12 | refuse → refuse | — | — | — | PASS |

Ukupno **6/12** prolazi. `behaviour_accuracy=0.8333`, `retrieval_hit_rate=0.7778` na pitanjima sa očekivanim odgovorom i `mean_citation_precision=0.4545` na odgovorima. Ove metrike mere ponašanje opisano u README-u; ne treba ih tumačiti kao dokaz da su svi odgovori semantički tačni.

## Dokumentovani propusti

**E04 — izostao dokaz za rok zamene laptopa.** Očekuje se „5 business days“ iz `hb-01`. Sistem vraća odgovor, ali citira `hb-01-chunk-0` (skor 0.217391) i `hb-01-chunk-2` (0.173913), koji ne sadrže ceo traženi podatak. `hb-01-chunk-1` ga sadrži, ali je četvrti među svim delovima sa 0.107143 i ne ulazi u `TOP_K=2`. Tip: rangiranje/dohvatanje i posledično nepotpun citat; način sečenja teksta doprinosi jer relevantna rečenica završava u odvojenom delu. Nije tačno reći da podatak ne postoji u korpusu.

**E09 — mesto zahteva je citirano, rok nije.** Očekuju se zahtev u IT portalu i „5 business days“ iz `hb-01`. Sistem citira opet `hb-01-chunk-0` i `hb-01-chunk-2`, pa se vidi „IT portal under Hardware“, ali nema celog roka. Deo sa rokom, `hb-01-chunk-1`, peti je među svim delovima sa skorom 0.142857. Tip: rangiranje/dohvatanje i nepotpun citat. To je ista mehanička slabost kao E04 na drugom eval pitanju.

**E05 — parafraza promašuje pravi dokument.** Pitanje koristi „new notebook computer“, a očekivani izvor `hb-01` govori o „replacement laptop“. Sistem citira `hb-06-chunk-0` (onboarding, skor 0.153846) i `hb-07-chunk-1` (annual leave, 0.083333); `hb-01` nije u prva dva. Tip: promašaj retrieval-a zbog leksičkog nepoklapanja; očekivani podatak „5 business days“ nije citiran.

**E06 — zastarela verzija potiskuje važeću.** Očekuje se „3 days per week“ iz `hb-03` (2026, `current`). Sistem citira dva dela `hb-02` (2024, `superseded`) sa skorovima 0.481481 i 0.400000 i odgovara „2 days per week“. Važeći `hb-03-chunk-0` sadrži „3 days per week“, ali je treći sa 0.370370. Tip: izbor zastarele verzije / pogrešan odgovor i citat. Ovo je cilj izabrane specifikacije.

**E10 — izostalo odbijanje nepodržanog pitanja.** Za trenutnu cenu akcije kompanije priručnik nema podatak, pa se očekuje odbijanje. Sistem ipak odgovara citatima iz parkinga (`hb-09-chunk-1`, 0.058824) i bezbednosti naloga (`hb-05-chunk-1`, 0.052632). Oba skora prelaze početni prag odbijanja 0.02. Tip: pogrešan odgovor umesto odbijanja.

**E11 — izostalo odbijanje pitanja s bliskim rečima.** Za roditeljsko odsustvo priručnik nema politiku, ali sistem citira delove politike godišnjeg odmora `hb-07-chunk-1` (0.166667) i `hb-07-chunk-0` (0.160000). Podudaranje reči „leave“ i „policy“ nije dokaz za parental leave. Tip: pogrešan odgovor umesto odbijanja i nerelevantan citat.

## Veza sa gradivom: BM25 i embeddings

Na času su pomenuti BM25 i embeddings (prezentacija „Kvalitet RAG-a“, slajdovi 14 i 26). To su korisne ideje za razumevanje propusta, ali **nisu deo ovog početnog sistema**. Funkcija `lexical_score` u `src/retrieval.py` trenutno broji poklapanja reči iz pitanja u delu dokumenta i deli ih brojem reči u tom delu. To nije BM25: BM25 dodatno uzima u obzir koliko je reč retka u zbirci i normalizuje dužinu dokumenta.

| Pristup | Veza sa uočenim propustom | Šta tek treba proveriti |
| --- | --- | --- |
| BM25, leksička pretraga | Mogao bi drugačije rangirati delove za E04/E09 jer razlikuje informativnije od čestih reči. | Da li deo sa „5 business days“ ulazi u citate bez regresija na ostalih 11 pitanja. BM25 sam po sebi ne rešava sinonime „notebook“ i „laptop“. |
| Embeddings, semantička pretraga | Mogla bi povezati parafrazu „new notebook computer“ iz E05 sa tekstom o zameni laptopa. | Da li se zaista dohvaća `hb-01`, koliko košta lokalni model ili servis i da li se pogoršavaju citati i odbijanja. |
| Hibridna pretraga, BM25 + embeddings | Spaja kandidate po rečima i po značenju, što je na slajdu 26 navedeno kao napredna tehnika. | Potrebno je posebno merenje na istih 12 pitanja posle obaveznog minimuma. |

Izabrani filter važećih dokumenata **M5** rešava drugi problem: za E06 stara politika ima veći skor od važeće. Zamena formule skorovanja ili dodavanje semantičke pretrage ne garantuju izbor važeće verzije. Na Milicin naknadni zahtev embeddings su dodati kao opcioni režim i izmereni u [zasebnom naprednom zapisu](napredni-embedding-eksperiment.md); taj rezultat ne zamenjuje obavezno merenje M5.

## Predlog jedne promene

Izabrana je opcija **M5 — filter važećih dokumenata**, jer E06 ima jasan uzrok i postoji važeći izvor sa traženim podatkom. Predlog, rizici i provera su napisani u [`specifikacija-promene.md`](specifikacija-promene.md) **pre izmene koda**. E04/E09, E05 i E10/E11 ostaju zasebni propusti; ova promena ne pretenduje da ih sve reši.

## Granice zaključka

Ovo je samo početno stanje. Nisu pokrenuti `after` eval niti poređenje, nije primenjena izmena i ne može se tvrditi da je M5 bilo šta popravio dok Nemanja ne sprovede i izmeri promenu. Zvanični „Šablon za izveštaj pre/posle“ nije pronađen u dostupnim fajlovima.
