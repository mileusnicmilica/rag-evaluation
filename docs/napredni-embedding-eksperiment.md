# Napredni eksperiment: lokalni embeddings

Ovaj zapis je odvojen od obaveznog eksperimenta sa jednom promenom M5. Na Milicin zahtev je u postojeći projektni `src` dodat **opcioni** embedding režim; podrazumevana leksička pretraga i sačuvani `results/before.json` nisu zamenjeni. Nemanjina M5 promena još nije sprovedena.

## Implementacija i pokretanje

- Model: `BAAI/bge-small-en-v1.5` kroz FastEmbed `0.9.0`; lokalno preuzeta revizija `aa8f8b060edb00e03bfdd08813a2949946c8ba55`. [FastEmbed uputstvo za upit i dokument](https://qdrant.github.io/fastembed/qdrant/Retrieval_with_FastEmbed/) preporučuje `query_embed` i `passage_embed`, koje koristi `src/embedding_retrieval.py`.
- Dokumenti se pretvaraju u vektore jednom po skupu delova, upit u svoj vektor, a kandidati se rangiraju kosinusnom sličnošću. Vektori se čuvaju u memoriji tokom procesa; preuzeti model je u `.cache/fastembed` i taj direktorijum se ne dodaje u Git.
- Opcione zavisnosti su u `requirements-embeddings.txt`. Podrazumevana instalacija iz `requirements.txt` ostaje dovoljna za leksički režim.
- CLI: `.\.venv\Scripts\python.exe -m src.cli --question "How long until I get a new notebook computer?" --retrieval embeddings --show-retrieved`.
- Eval: `.\.venv\Scripts\python.exe -m src.embedding_eval --out results/embeddings.json`; koristi istih 12 pitanja i ne menja `eval/eval_set.json` ni funkcije za metrike.
- Poređenje: `.\.venv\Scripts\python.exe -m src.eval_compare results/before.json results/embeddings.json`.
- Početni prag odbijanja za kosinusni skor je `0.5` u `src/embedding_retrieval.py`; **nije kalibrisan**. Leksički prag `0.02` ne može direktno da se prenese na drugu skalu.

## Izmereni rezultat

| Pokazatelj | Leksički `before` | Embeddings |
| --- | ---: | ---: |
| Prošlo | 6/12 | 7/12 |
| Tačnost ponašanja | 0.8333 | 0.8333 |
| Retrieval hit na podržanim pitanjima | 0.7778 | 1.0000 |
| Srednja preciznost citata na odgovorima | 0.4545 | 0.5000 |

Sačuvani su [embedding rezultat](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/embeddings.json) i [izlaz poređenja](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/embedding-comparison.txt). Otisak eval skupa je u oba rezultata `afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064`. Poređenje navodi **E06** kao jedino pitanje koje prelazi iz FAIL u PASS i **nema novih regresija** po postojećim metrikama.

Milica je zatim sama pokrenula testove, CLI pitanje E05, celu embedding evaluaciju i poređenje. Njen sačuvani [rezultat](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/embeddings-demo.json) ima **identične redove, metrike, konfiguraciju i otisak eval skupa** kao prethodni `embeddings.json`; sačuvan je i [ponovljeni izlaz poređenja](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/embeddings-demo-comparison.txt). CLI je potvrdio da E05 citira `hb-10-chunk-0` i `hb-01-chunk-2`, ali ne daje celokupan rok „5 business days“.

Važna ručna provera: na **E06** embedding režim citira i važeći `hb-03` sa „3 days per week“ i zastareli `hb-02` sa „2 days per week“. Eval ga označava kao PASS jer očekivani podatak postoji u jednom citatu, ali tekst odgovora sadrži **protivrečne informacije**. To nije potpuno rešena korisnička greška. Na **E05** retrieval hit postaje tačan (`hb-01` ulazi u citate), ali citirani `hb-01-chunk-2` ne sadrži celu frazu „5 business days“, pa pitanje ostaje FAIL. E04, E09, E10 i E11 takođe ostaju FAIL.

Alat za poređenje upozorava da su se promenila tri zapisana podešavanja: režim, naziv modela i prag odbijanja. Ta tri polja opisuju konfiguraciju ovog odvojenog eksperimenta, ali rezultat **ne izdvaja** doprinos samih embeddings od uticaja praga. Ne treba ga predstavljati kao dokaz da je samo jedna promena rešila obavezni zadatak.

## Provera rada i ograničenja

- `python -m pytest -q` u projektnom virtuelnom okruženju: **19 passed** (18 početnih i jedan test embedding rangiranja).
- Ponovljena standardna leksička evaluacija daje iste redove, metrike, konfiguraciju i otisak skupa kao `before.json`: **6/12**.
- Evaluacija sa `HF_HUB_OFFLINE=1` po preuzimanju modela uspeva i daje identične redove i metrike kao onlajn pokretanje.
- Model traži prvo preuzimanje i dodatne lokalne zavisnosti, prostor na disku i procesorsko vreme. Nema vektorske baze, API ključa ni plaćenog servisa. Preostaju greške chunkovanja i odbijanja, kao i nerešeno pitanje citiranja zastarele verzije.

**AI pomoć:** asistent je dodao kod, instalirao opcione zavisnosti, pokrenuo eval i CLI i sastavio ovaj zapis. Milica i Nemanja treba da provere izlaze i u izveštaju navedu stvaran doprinos svakog člana.
