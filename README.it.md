# lumen-models

Italiano | [English](README.md)

Script di conversione, quantizzazione e benchmark dei modelli per
[Lumen](https://github.com/lumen-assistive), oltre al registro delle
licenze di modelli e dataset del progetto.

## Cosa contiene

- `docs/LICENSES.md` / `docs/licenses.yaml`: il registro delle licenze,
  in forma leggibile e in forma automatizzabile, per ogni modello,
  motore di inferenza e set di simboli considerato per Lumen, inclusi i
  conflitti segnalati (AGPL-3.0 di Ultralytics YOLO, il cambio di
  licenza di Piper da MIT a GPL-3.0, la clausola non commerciale di
  ARASAAC) e come ciascuno viene gestito. **Leggere questo file per
  primo** prima di aggiungere qualsiasi nuovo modello.
- `src/lumen_models/catalog.py`: il catalogo `ModelDescriptor`, che
  rispecchia la forma del contratto `ModelDescriptor` di `lumen_sdk`.
  Oggi è vuoto; le voci vengono aggiunte solo quando esiste un vero
  artefatto on-device.
- `src/lumen_models/license_check.py`: un controllo automatico di
  conformità — la CI fallisce se una voce del catalogo fa riferimento a
  una licenza mancante dal registro o non approvata per la
  distribuzione Apache-2.0.
- `src/lumen_models/convert/`: l'interfaccia della pipeline di
  conversione dei modelli (`ModelConverter`), con un'implementazione di
  riferimento `CopyConverter` che esercita lo schema di manifest e
  checksum che ogni futuro convertitore specifico per framework
  (TFLite, ONNX, GGUF) seguirà.
- `src/lumen_models/benchmark/`: un banco di prova che misura la
  latenza e la memoria del processo per una funzione di inferenza
  fornita dal chiamante.
- `docs/benchmarks.md`: la tabella dei benchmark pubblicata (oggi
  vuota); generata da `lumen-models render-benchmarks`, mai modificata
  a mano.

## Stato attuale

Nessun modello è stato ancora convertito, quantizzato o sottoposto a
benchmark. Questa versione include l'impalcatura di governance e
strumenti — il registro delle licenze, lo schema del catalogo con il
suo controllo di conformità, l'interfaccia della pipeline di
conversione e il banco di prova per i benchmark — tutto reale e
testato. I convertitori specifici per framework vengono aggiunti man
mano che ogni modulo plugin ha bisogno di un modello concreto.

## Sviluppo

```
python -m venv .venv
.venv/Scripts/activate
pip install -e .[dev]
ruff check .
ruff format --check .
mypy .
pytest --cov
```

Installa l'hook condiviso per i messaggi di commit prima di fare commit:

```
git config core.hooksPath .githooks
```

Vedi [CONTRIBUTING.md](CONTRIBUTING.md) per il flusso di lavoro completo
(in inglese, come tutto il codice e la documentazione tecnica del
progetto).

## Licenza

Apache License 2.0, vedi [LICENSE](LICENSE), per il codice di questo
repository. Vedi [docs/LICENSES.md](docs/LICENSES.md) per le licenze
dei modelli di terze parti che questo repository converte, quantizza e
sottopone a benchmark — non sono tutte Apache-2.0, e alcune non vengono
deliberatamente incluse.
