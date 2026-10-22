# Week 7: odvojeni napredni eksperiment

Ovaj folder je zasebna kopija projekta. Obavezna promena M5 (filter važećih dokumenata) i njen `before`/`after` rezultat ostaju u originalnom projektu. Ovde su dodatne promene merene redom na istom eval skupu.

| Korak | Promena u odnosu na prethodni korak | Prolaznost |
| --- | --- | ---: |
| Početni rezultat | Slab checkpoint | 6/12 |
| M5 | Samo `current` dokumenti | 7/12 |
| M1 | Sečenje po celim rečenicama | 9/12 |
| M3 | Leksički prag odbijanja `0.02` → `0.08` | 10/12 |
| Opcioni embedding režim | Lokalni `BAAI/bge-small-en-v1.5`, početni prag `0.5` | 10/12 |
| Kalibracija embedding praga | `0.5` → `0.75` | **12/12** |

M1 rešava E04 i E09 jer citati čuvaju celu frazu „5 business days“. Prelazak na embedding režim popravlja E05, ali pri početnom pragu ponovo kvari E10; zbir ostaje 10/12. Prag `0.75` zatim odbija E10 i E11. Ručna provera E05, E06, E10 i E11 je uključena u `run_demo.py`.

Iz korena ovog foldera u PowerShell-u:

```powershell
& '..\rag-week-7-weak-checkpoint\rag-week-7-week-checkpoint\.venv\Scripts\python.exe' .\run_demo.py
& '..\rag-week-7-weak-checkpoint\rag-week-7-week-checkpoint\.venv\Scripts\python.exe' -m pytest -q
```

Skripta koristi već preuzeti lokalni model iz originalnog projekta. Prva komanda prikazuje tabelu, upisuje `results/live-demo.json` i ispisuje četiri odgovora za ručnu proveru. Sačuvani rezultati pojedinačnih koraka su u `results/`.

**Granica zaključka:** 12/12 važi za ovih dvanaest poznatih pitanja. Prag `0.75` izabran je posle pregleda njihovih skorova, pa ovaj rezultat nije nezavisna provera rada na novim pitanjima. Završna verzija sadrži više promena i ne predstavlja jednu obaveznu izmenu iz zadatka. Za obavezni deo koristite samo originalni `results/before.json` i `results/after.json` (6/12 → 7/12).

Kratka provera na četiri nova pitanja potvrđuje to ograničenje. Sistem tačno pronalazi politiku rada od kuće i odbija pitanje o porodiljskom odsustvu za koje nema izvor. Međutim, **pogrešno odbija** „What is the training budget for courses?“ (skor `0.725`) i „Where do I report a lost badge?“ (skor `0.723`), iako odgovori postoje u priručniku. Zato `12/12` ne treba predstavljati kao dokaz da sistem pouzdano radi na novim formulacijama.
