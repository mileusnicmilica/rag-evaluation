# Milicin deo — radni dnevnik i dokazi

## Status

**Status 19. oktobra 2026:** Početna provera, analiza propusta i predlog specifikacije su završeni. RAG kod tada nije menjan. Detaljni nalazi su u [`pocetno-stanje.md`](pocetno-stanje.md), a predlog izmene u [`specifikacija-promene.md`](specifikacija-promene.md). Milica treba da pregleda zaključke i potvrdi da su to njeni stvarni doprinosi pre predaje.

**Ažuriranje 22. oktobra 2026:** Nemanjin deo M5 i merenje obavezne jedne promene zabeleženi su u [`nemanja-rezultati.md`](nemanja-rezultati.md), uključujući AI pomoć pri izmeni koda. Dodatna poboljšanja su u odvojenom [`advanced-experiment`](../advanced-experiment/README.md). Ovaj dnevnik ispod beleži raniji tok Milicinog rada.

## Izvor zahteva

- Tutorov zadatak: [`zadatak-nedelja-7.md`](zadatak-nedelja-7.md), kopija datoteke koju je korisnica priložila.
- Usvojena podela: [`PLAN.md`](PLAN.md).
- Cilj Milicinog dela: početni testovi, `before` rezultat na fiksnih 12 pitanja, najmanje dva dokumentovana propusta, pa pisana specifikacija **jedne** promene pre bilo kakve implementacije.

## Provere obavljene 19. oktobra 2026.

1. Radni folder je `C:\Users\HP\Desktop\AI Bootcamp\week7-rag`. Pre početka obrade sadržao je samo `PLAN.md`.
2. Prva pretraga naziva `*checkpoint*.zip`, `eval_set.json`, `improvement-menu.md` i naziva sličnih „pre/posle“ na Desktopu i u Downloads nije našla checkpoint, eval skup ni šablon. Posle te provere Milica je dodala checkpoint; nađen je i ZIP u Downloads. Zvanični šablon pre/posle i dalje nije pronađen.
3. `python --version` → `Python 3.11.7`.
4. `python -m pytest --version` → `No module named pytest` u podrazumevanom Python okruženju. Zatim je napravljeno projektno virtuelno okruženje i instaliran `pytest==8.3.3` prema `requirements.txt`.
5. `git --version` → `git version 2.53.0.windows.1`.
6. Originalni ZIP je privremeno kopiran u radni folder bez izmene; sada se nalazi u Downloads. SHA-256 je `31607f2f0de57f6b454b4c7e33a07e47efce7986525dd968999e717e4d98f333`. Svih 22 fajlova iz arhive byte-for-byte odgovara raspakovanoj kopiji pre izmene koda.
7. Projektni README traži Python 3.12. Dostupan je 3.11.7; pod njim su početni testovi prošli: **18/18**. Sačuvan je izlaz u `results/baseline-tests.txt`.
8. Prvi pokušaj instalacije zavisnosti bio je blokiran mrežnim ograničenjem (`WinError 10013`). Ponovljena instalacija uz odobren pristup mreži je uspela.
9. Potpuna početna evaluacija pokrenuta je komandom `.\.venv\Scripts\python.exe -m src.eval_runner --out results/before.json`. Sačuvani su `results/before.json` i `results/baseline-eval.txt`. Rezultat je **6/12**, a otisak eval skupa `afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064`.
10. CLI sa `--show-retrieved` je pokrenut za svih šest neuspešnih pitanja E04, E05, E06, E09, E10 i E11. Za E04 i E06 dodatno su pregledani svi rangirani delovi da se proveri gde se nalazi očekivani podatak. Nalazi i tip svakog propusta zapisani su u `pocetno-stanje.md`.
11. Pre izmene koda napisana je specifikacija opcije M5, filtera važećih dokumenata, kao jedne nameravane promene. Nemanjin deo još nije započet.
12. Posle Milicinog zahteva pregledani su slajdovi 14 i 26 prezentacije za Sesiju 1. U `pocetno-stanje.md` dodato je objašnjenje BM25, embeddings i hibridne pretrage, vezano za stvarne propuste. Nije menjana specifikovana promena M5 niti RAG kod.
13. U zasebnom naknadnom zahtevu Milica je tražila embeddings u postojećem `src`. Dodat je opcioni režim, sprovedena evaluacija i rezultat zapisan u [`napredni-embedding-eksperiment.md`](napredni-embedding-eksperiment.md). Ova izmena je odvojena od prethodno napisanog Milicinog početnog stanja i M5 specifikacije.
14. Milica je u sopstvenom PowerShell-u pokrenula testove, CLI sa embedding pretragom za E05, celu embedding evaluaciju i poređenje sa `before.json`. Sačuvani `results/embeddings-demo.json` je proveren i podudara se sa prethodnim embedding merenjem po svim redovima, metrikama, konfiguraciji i otisku eval skupa. Poređenje i ručni nalaz zabeleženi su u naprednom eksperimentu.

## Plan predaje Nemanji zapisan 19. oktobra

Nemanja dobija [`specifikacija-promene.md`](specifikacija-promene.md), [`pocetno-stanje.md`](pocetno-stanje.md), `results/before.json` i početne izlaze testova/evaluacije u projektnoj fascikli. Tek po proveri specifikacije primenjuje jednu promenu i pokreće `after` merenje. Zvanični šablon izveštaja pre/posle treba pribaviti pre sastavljanja zajedničkog završnog izveštaja.

## Beleška o AI pomoći

AI asistent je pročitao tutorov zadatak i projektni README, podesio lokalno okruženje, pokrenuo početne testove i evaluaciju, pregledao CLI izlaze i korpus, dokumentovao propuste i sastavio predlog specifikacije. RAG kod nije menjan. Dokaz su sačuvani izlazi komandi i `before.json`; Milica treba da ih pregleda i svojim rečima potvrdi zaključke pre predaje. U zajedničkom izveštaju doprinos treba pripisati stvarnom izvršiocu i jasno navesti ovu AI pomoć.
