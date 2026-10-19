# Nemanjin deo — M5 promena i rezultat pre/posle

Radni zapis za zajednički izveštaj, 19. oktobar 2026. Zvanični tutorov šablon nije u repozitorijumu, pa ovaj tekst treba preneti u taj šablon kada bude dostupan. Milicin radni dnevnik još beleži da ona treba da pregleda i potvrdi svoj deo i izbor M5 pre predaje.

## Polazna osnova i jedna promena

Milicina [specifikacija](specifikacija-promene.md) cilja E06: leksička pretraga je kao dva najviše rangirana dela birala `hb-02` (2024, `superseded`), pa je odgovor navodio 2 dana rada na daljinu nedeljno. Važeći `hb-03` (2026, `current`) propisuje 3 dana. Sačuvani `results/before.json` ima 6/12 prolaznih pitanja.

Sprovedena je samo promena M5: `CURRENT_ONLY = True` u `src/config.py`, a `searchable_chunks` u `src/retrieval.py` vraća samo delove sa `status == "current"` kada je opcija uključena. Kada je isključena, funkcija zadržava ranije ponašanje. Dodat je ciljani test za oba stanja. Korpus, sečenje teksta, `TOP_K`, pragovi, eval pitanja i kod za metrike nisu menjani. Zajedničku funkciju `searchable_chunks` koristi i opcioni embedding režim; on nije predmet ovog obaveznog merenja.

## Provera i sačuvani dokazi

Komande su pokrenute iz projektnog foldera `rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint`:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.eval_runner --out results/after.json
.\.venv\Scripts\python.exe -m src.eval_compare results/before.json results/after.json
.\.venv\Scripts\python.exe -m src.cli --question "How many days per week can I work remotely?" --show-retrieved
```

- Testovi posle izmene: **20 passed** (pre izmene u ovom checkout-u 19 passed; izvorni checkpoint je imao 18 testova, a naknadni embedding eksperiment dodao je devetnaesti).
- [After rezultat](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/after.json), [tabela evaluacije](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/after-eval.txt), [poređenje](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/after-comparison.txt), [ručni CLI izlaz za E06](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/after-e06-cli.txt) i [diff koda](../rag-week-7-weak-checkpoint/rag-week-7-week-checkpoint/results/m5-code.diff) sačuvani su u projektu.
- `eval_set_sha256` je u oba JSON rezultata **`afe46db1e75a0b85bb5c9a93b6763e3b96e5cd7b289e12da6d2671e4d8650064`**. Git je na ovom Windows računaru pri prvom checkout-u pretvorio LF u CRLF, što je promenilo otisak sirovih bajtova. Pre `after` pokretanja završeci redova eval fajla vraćeni su na originalni LF. Projektni `.gitattributes` sada čuva LF i na budućim checkout-ima. Ponovljeno merenje daje isti otisak, redove i metrike kao sačuvani `after.json`; `git diff -- eval/eval_set.json` je prazan. Pitanja i njihov sadržaj nisu menjani.
- Trenutno lokalno okruženje koristi **Python 3.14.2**, dok README traži 3.12; Milicino početno merenje bilo je na 3.11.7. Pre M5 promene, ovde su konfiguracija, sažetak i svih 12 rezultata u memoriji bili identični sačuvanom `before.json`, osim otiska izazvanog CRLF konverzijom.

## Izmereni ishod

| Metrika | Pre | Posle | Promena |
| --- | ---: | ---: | ---: |
| Prošlo | 6/12 | 7/12 | +1 |
| Tačnost ponašanja | 0.8333 | 0.8333 | 0 |
| Pogodak izvora na podržanim pitanjima | 0.7778 | 0.8889 | +0.1111 |
| Srednja preciznost citata na odgovorima | 0.4545 | 0.5455 | +0.0910 |

**Popravljeno:** E06 je prešlo iz FAIL u PASS. Sada su citirana `hb-03-chunk-0` i `hb-03-chunk-1`, oba iz važećeg dokumenta iz 2026. CLI prikazuje „3 days per week“ u `hb-03-chunk-0` i ne prikazuje zastarelo pravilo o 2 dana. Preciznost citata za E06 porasla je sa 0.0 na 1.0.

**Regresije:** nijedno pitanje nije prešlo iz PASS u FAIL. Kod E01, E02 i E03 drugi, nerelevantni citat promenjen je sa zastarelog `hb-02` na važeći `hb-03`; sva tri ostaju PASS, sa preciznošću citata 0.5. Ostali redovi su ostali isti. Alat za poređenje beleži samo jednu promenjenu konfiguracionu vrednost: `CURRENT_ONLY: False -> True`.

**Ograničenja:** E04 i E09 i dalje ne citiraju ceo rok „5 business days“; E05 i dalje promašuje potreban podatak pri parafrazi; E10 i E11 i dalje daju odgovor umesto odbijanja. Filter uklanja zastarela dokumenta i za buduća pitanja koja izričito traže staru politiku, a u fiksnom skupu nema takvog pitanja. Zbog toga odsustvo regresije na ovih 12 pitanja ne dokazuje da su istorijska pitanja pokrivena.

## Doprinos i AI pomoć za proveru pre predaje

Nemanja je zatražio sprovođenje svog dela prema Milicinoj specifikaciji. AI asistent je u ovom checkout-u izmenio kod, dodao test, pokrenuo provere i pripremio ovaj zapis. Pre predaje Nemanja treba lično da pregleda diff i izlaze, potvrdi da opis odgovara stvarnom doprinosu i unese proverenu belešku o korišćenju AI-ja u zajednički izveštaj. Milicin doprinos i njena potvrda specifikacije ne mogu se pripisati Nemanji.
