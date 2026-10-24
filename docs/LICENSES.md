# Model and dataset licenses

This is the human-readable license ledger for every model, engine, and
symbol set considered for Lumen. `licenses.yaml` in this same directory
is the machine-readable mirror that `lumen-models check-licenses`
validates the model catalog against in CI, so a model can never be
added to the catalog with an uncleared license without CI failing.

All entries below were checked against each project's official source
on 2026-10-23. Licenses can change between releases; re-verify before
every new model version is adopted, not just once.

| Component | License (SPDX) | Compatible with Apache-2.0 distribution | Notes |
|---|---|---|---|
| OpenAI Whisper (weights, reference code) | MIT | Yes | |
| whisper.cpp (inference engine) | MIT | Yes | |
| Ultralytics YOLO (v8 and later) | AGPL-3.0-only | **No** | Dual-licensed commercially by Ultralytics. Not bundled; see "Flagged conflicts" below. |
| Google MediaPipe | Apache-2.0 | Yes | One vendored utility file carries a BSD-style notice; does not change the verdict. |
| PaddleOCR | Apache-2.0 | Yes | |
| YAMNet (tensorflow/models) | Apache-2.0 | Yes | No per-model license file; inherits the repository's root Apache-2.0 license. |
| Piper TTS engine, archived MIT release (rhasspy/piper) | MIT | Yes | Pin to the last MIT-licensed tag; see "Flagged conflicts" below for why the current fork is not used. |
| Piper TTS engine, current fork (OHF-Voice/piper1-gpl) | GPL-3.0-only | **No** | Not used. Recorded for clarity since it is the successor to the MIT release above. |
| espeak-ng (Piper phonemization dependency) | GPL-3.0-or-later | **Unresolved** | See "Flagged conflicts" below. |
| Individual Piper voice models | Varies per voice | **Depends on voice chosen** | See "Flagged conflicts" below. |
| ARASAAC pictograms | CC-BY-NC-SA-4.0 | **No** | Not used by any MVP-phase module. See "Flagged conflicts" below. |
| Microsoft Phi-3-mini-4k-instruct | MIT | Yes | Candidate small on-device LLM. |
| Google Gemma 4 (E2B / E4B) | Apache-2.0 | Yes | Candidate small on-device LLM; see note below on earlier Gemma versions. |
| Qwen2.5-1.5B-Instruct | Apache-2.0 | Yes | Candidate small on-device LLM; re-verify if a different size is chosen. |

## Flagged conflicts and how they are handled

### Ultralytics YOLO: AGPL-3.0

Current Ultralytics YOLO releases (v8 and later) are licensed AGPL-3.0,
with a separate paid Enterprise License for closed-source distribution.
Bundling an AGPL-3.0 model or its inference code inside Lumen's
Apache-2.0 app would impose copyleft obligations on the combined work.
**Decision: do not use Ultralytics YOLO.** Google MediaPipe already
ships an Apache-2.0-licensed object detection task sufficient for
Vedere's obstacle-detection use case, so this conflict is avoided by
depending on MediaPipe instead rather than needing an exception.

### Piper: engine relicensed from MIT to GPL-3.0

The original `rhasspy/piper` repository was MIT-licensed. On
2025-10-06 it was archived, and active development moved to
`OHF-Voice/piper1-gpl`, now licensed GPL-3.0. **Decision: pin to the
last MIT-licensed tag of the archived `rhasspy/piper` repository.**
That code remains MIT forever regardless of the project's later
relicensing. The cost is forgoing upstream improvements made after the
relicense; re-evaluate this trade-off periodically, and never sync
code from the GPL-3.0 fork into this project.

### espeak-ng: GPL-3.0 phonemization dependency

Piper's phonemization step has historically relied on `espeak-ng`,
which is GPL-3.0-or-later. **This is not yet resolved.** Before
shipping any Piper-based text-to-speech feature, verify whether the
pinned MIT-era Piper release links `espeak-ng` at build time (and so
would carry its GPL obligations into the binary) or only shells out to
a separately-installed copy (a different, likely more favorable,
compliance posture). If it does link at build time, evaluate process
isolation or a non-GPL phonemizer before release.

### Piper voices: per-voice licensing

Individual Piper voice models are trained on different datasets with
different licenses: the public catalog includes CC0, MIT, Apache-2.0,
and CC-BY-4.0 voices, alongside some marked non-commercial or
research-only. **No specific Italian voice has been selected yet.**
Whoever selects the production Italian (and any English) voice must
check that exact voice's own `MODEL_CARD` on
`huggingface.co/rhasspy/piper-voices` and record the result as a new,
specific entry in `licenses.yaml`. The generic `piper-voice-per-voice`
entry here is deliberately left unresolved (`compatible_with_apache_2_0:
null`) rather than assumed compatible, and `lumen-models
check-licenses` will reject a catalog entry that references it
directly for exactly that reason.

### ARASAAC pictograms: CC-BY-NC-SA-4.0

ARASAAC publishes its pictogram set under Creative Commons
Attribution-NonCommercial-ShareAlike 4.0, administered by the
Government of Aragon. The NonCommercial clause conflicts with
unrestricted redistribution. **No MVP-phase module needs this**:
Vedere, Sentire, Protezione, and Famiglia do not use AAC symbols.
Before any future communication-board module (on the long-term
roadmap, not yet built) considers bundling a symbol set: either
request explicit written permission from the rights holder, evaluate
an alternative symbol set with a verified compatible license, or
commission original icons. Do not bundle ARASAAC pictograms without
one of those resolved first.

## Small on-device LLM candidates

Three real, currently-permissively-licensed candidates exist for
features like leaflet question-answering (Vedere) or study assistance
(a future Leggere e Studiare module): Microsoft's Phi-3-mini-4k-instruct
(MIT), Google's Gemma 4 in its smaller E2B/E4B sizes (Apache-2.0, as of
its 2026-04-02 release), and Qwen2.5-1.5B-Instruct (Apache-2.0). Earlier
Gemma versions 1 through 3 used a custom, non-OSI "Gemma Terms of Use"
with a prohibited-use policy and are not candidates. None of the three
has been benchmarked yet; final selection is a `lumen-models`
benchmarking decision (latency, memory, and output quality on target
low-end hardware), not a licensing one, since all three are already
cleared.

## Process

1. Before adding any model to `src/lumen_models/catalog.py`, add or
   update its entry in `licenses.yaml` with a verified
   `compatible_with_apache_2_0` value and a dated note citing the
   source checked.
2. `lumen-models check-licenses` (and the corresponding test in
   `tests/test_license_check.py`) fails if a catalog entry references a
   license id that is missing or not marked `true`.
3. Never set `compatible_with_apache_2_0: true` from memory or
   assumption. Check the project's current, official license file or
   terms page for that specific version before recording a verdict.
