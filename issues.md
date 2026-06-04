# Code Review & Findings — BSI-GS → OSCAL Pipeline

**Date:** 2026-06-03
**Reviewer:** Claude (Opus 4.8)
**Scope:** `src/g2oscal`, `src/add-practice`, `src/quality_control`,
`src/oscal_components_from_grundschutz`, `src/translate_oscal`, shared schemas/prompts,
and the new `ai_client.py`.
**Yardstick:** the project's own `src/symbiotic-coding-brief.md`.

> Legend — **S1** critical (data loss / wrong data), **S2** major (reliability / cost),
> **S3** minor (style / consistency / nits).

---

## ✅ Resolution log (updated 2026-06-03)

| Finding | Status | Commit |
|---|---|---|
| #12/#2 Slugified control IDs (SYS.1.8/INF.5/INF.9) | **Fixed** — 5908 tokens normalized across 33 files (catalogs, 3 components, 28 translations) via `src/tools/normalize_control_ids.py`; verified no slugs remain, JSON valid | `eb840c4` |
| #13 No `pattern` validation on requirement `id` | **Fixed** — `pattern` added to `discovery_enrichment_stub_schema.json`; `canonical_control_id()` in `g2oscal/main.py` derives the id from the title and raises on malformed | `eb840c4` |
| #3 add-practice position-based mapping | **Fixed** — model now echoes `id`; results mapped by id; `gemini_utils` verifies the returned id-set and retries on mismatch | `f05021d` |
| #10 g2oscal forced DEBUG logging; add-practice inverted level | **Fixed** | `f05021d` |
| #1/#2 Missing/partial Anforderungen | **Partially fixed** — completeness gate (raise on missing prose), empty-discovery treated as failure. *Stage-2 chunking still TODO.* | `6bb60a2` |
| #4/#7 Deprecated SDK; hardcoded model/region (g2oscal) | **Fixed for g2oscal** — adopted `ai_client.py` (google-genai); model/region/tokens now env-overridable (`constants.py`, `REGION`). Other 3 services still on old SDK. | `a9da51f` |

**Still open:** #5/#6 (ai_client retry set / `response_schema` $ref — left as-is per owner: client is working code from another project), #8 safety settings in remaining services, #9 quality_control (`MAX_TOKENS`/grounding), #11 misc nits, SDK migration for add-practice/oscal_components/translate_oscal, dependency pinning, and **re-running** SYS.1.8/INF.5/INF.9 + regenerating their components/translations.

---

## 0. TL;DR — top findings

1. **Why Bausteine miss Anforderungen (S1):** the `g2oscal` generation is a *single
   batched call per Baustein* that must emit ~15 German prose fields for *every*
   requirement at once, capped at `max_output_tokens=65536`. Large Bausteine overflow
   the cap → the response truncates. Two failure modes follow, both silent:
   (a) truncated JSON fails to parse → 5 identical retries fail → the **whole Baustein
   is dropped** (`return None, None`); (b) the model returns prose for only a *subset*
   of requirements — which still passes schema validation — and the assembly loop
   **silently skips** the rest with a `warning`. Net effect: Bausteine that are missing
   or have fewer Anforderungen than the PDF. Newer models with larger/thinking budgets
   *reduce* this, but the architecture (no chunking, no completeness check) is the real
   bug and must be fixed regardless of model.
2. **SDK split (S2):** 4 of 5 services still use the **deprecated** `vertexai.generative_models`
   (`google-cloud-aiplatform`) SDK; only `quality_control` and your new `ai_client.py`
   use the current `google-genai`. Standardize on `google-genai` everywhere.
3. **`add-practice` assigns results by position, not by ID (S1):** practice/CIA/class
   can be silently written to the **wrong control** if the model reorders its array.
4. **Hardcoded model & region everywhere (S2):** `gemini-2.5-pro` and the region are
   hardcoded in every service (and the region differs per service: `us-central1` vs
   `global`). This violates the brief's "no hardcoded configuration" rule and blocks the
   move to newer models.
5. **`ai_client.py` review (S2):** retry set catches `ClientError` (mostly non-retryable
   4xx) but **not** `ServerError` (retryable 5xx); `thinking_level` vs model needs
   verifying; passing a draft-07 schema with `$ref`/`definitions` as `response_schema`
   will break Vertex controlled generation; no safety settings.
6. **Malformed control IDs in three Bausteine (S1, issue #2):** SYS.1.8 / INF.5 / INF.9
   controls were stored with **slugified ids** (`inf-5-a1`, `sys.1.8.a1`) instead of the
   canonical `INF.5.A1` / `SYS.1.8.A1`. 44 bad ids in the catalog, propagated to the 3
   component files and all 28 translations. There is **no ID-pattern validation**, so they
   pass every gate; case-sensitive OSCAL references to these controls silently break.

---

## 1. Root cause: missing "Anforderungen" (S1)

**Pipeline:** `src/g2oscal/gemini_utils.py::process_baustein_pdf`
- **Stage 1 (discovery+enrichment):** one Gemini call extracts the full contextual prose
  (Einleitung, Zielsetzung, Modellierung, **all** Gefährdungslage risks) *and* every
  requirement with 4 classifications — see `prompt_discovery_enrichment.txt`.
- **Stage 2 (generation):** one Gemini call generates **15 prose fields** (5 maturity
  levels × statement/guidance/assessment) for **all** requirements at once — see
  `prompt_generation.txt`, batched via `REQUIREMENTS_JSON_BATCH`.

**The cap:** `generation_config = {"response_mime_type": "application/json",
"max_output_tokens": 65536}` (`gemini_utils.py:25`).

**Failure mode A — whole Baustein dropped:**
- A large Baustein (e.g. SYS/NET/APP families with 25–45 Anforderungen) needs far more
  than 65 k output tokens for Stage 2. The model hits `MAX_TOKENS`, output truncates.
- `call_gemini_api` requires `finish_reason == STOP`; `MAX_TOKENS` → `ValueError`
  (`gemini_utils.py:48-51`). Even if it slipped through, truncated JSON fails
  `json.loads`. Either way → exception → retried 5× **identically** (deterministic, so
  all fail) → `process_baustein_pdf` outer `except` returns `(None, None)`
  (`gemini_utils.py:123-125`).
- `main.py` counts it under "Failed to process" but still writes a "successful" catalog
  **without that Baustein**. No alert, no quarantine.

**Failure mode B — partial Anforderungen, silently (the issue title):**
- `generation_stub_schema.json` only requires the top-level `generated_requirements`
  array and, per item, `id` + the three Level-3 fields. There is **no `minItems`** and
  **no check that the returned count equals the input count**.
- So a model that returns prose for only *some* requirements **passes validation**.
- Assembly maps by id: `if req_id in prose_map … else logging.warning("Skipping control
  … due to missing data")` (`gemini_utils.py:108-114`). Missing ones are dropped with a
  warning only. The Baustein is written with **fewer Anforderungen than the PDF**.
- Nothing asserts `len(final_controls) == len(requirements_to_process)`.

**Failure mode C — empty discovery counts as success:**
- If Stage 1 returns `requirements_list: []` (truncation, a safety block, or a model
  miss — the discovery call is *also* under the same 65 k cap and is large), the early
  return builds a Baustein with `controls: []` that is treated as **success** and merged
  (`gemini_utils.py:94-96`). Result: a Baustein present but with **zero** Anforderungen.

**Failure mode D — safety blocks (S2):** `g2oscal`/`add-practice` set **no**
`safety_settings`. BSI security prose (attacks, malware, exploitation in
Gefährdungslage) can trip default filters → `finish_reason=SAFETY` → `ValueError` →
retried & dropped. Only `translate_oscal` sets `BLOCK_NONE`.

**Will newer models "fix that"?** Partly. A larger output budget / thinking model makes
truncation and subset-dropping rarer, so re-running will recover many Bausteine. But the
defects are structural and will recur on the largest Bausteine:
- **Chunk Stage 2** (N requirements per call, or one call per requirement) so output can
  never exceed the cap; retry only the missing chunk.
- **Add a completeness gate:** compare generated ids vs requested ids; re-request the
  missing ids; fail loudly (don't write) if still incomplete.
- **Reject `MAX_TOKENS` as non-retryable** with a clear "output truncated — chunk input"
  message instead of 5 identical retries.
- **Add `safety_settings=BLOCK_NONE`** to the generation/discovery calls.
- **Don't count empty-requirements Bausteine as success**; flag for re-run.

**To answer "which ones":** the largest Bausteine are most affected. A quick triage
script (not part of this report) can load the latest merged catalog and list every
`baustein` group whose `controls` array is empty or whose control count is below the
Anforderungen count in the source PDF.

---

## 1A. Issue #2 — malformed ("slugified") control IDs in three Bausteine (S1)

Issue #2 ("Drei Bausteine mit seltsamen ID") names **SYS.1.8, INF.5, INF.9** and cites an
example like `SYS G.1.3.A17`. Reproduced against the committed data, the defect is **ID
slugification**: each control's own `id` was lowercased (and, for the INF Bausteine, dots
were turned into hyphens), while the **canonical ID still sits in the `title`**.

**Evidence (verbatim from `BSI_GS_OSCAL_current_2023.json`):**
- **INF.5** — `"id": "inf-5-a1"`, `"title": "INF.5.A1 Planung der Raumabsicherung (B)
  [Planende]"`, `"class": "technical"`, maturity parts `inf-5-a1-m1` … (canonical
  `INF.5.A1`).
- **INF.9** — `"id": "inf-9-a1"` … `"inf-9-a12"` (12 controls).
- **SYS.1.8** — `"id": "sys.1.8.a1"` … `"sys.1.8.a26"` (23 controls; here dots are kept,
  only the case is wrong).

**Counts & blast radius (measured):**
- Master catalog `BSI_GS_OSCAL_current_2023.json`: **21 hyphenated** (INF.5 = 9, INF.9 = 12)
  + **23 dotted-lowercase** (SYS.1.8) = **44 malformed control IDs**. SYS.1.8 is also
  malformed in `…_benutzerdefinierte.json` (23).
- Copied **verbatim** into the **3 component files** (`SYS.1.8/INF.5/INF.9.component.json`,
  44 `control-id` references) and into **all 28 translated language files** (translation
  copies ids unchanged).
- The malformation is **isolated to exactly these three Bausteine** — no other Baustein has
  lowercase/hyphenated ids — which is why the issue says "three".
- The casing is inconsistent *within* each component file: the base controls are mangled
  (`sys.1.8.a1`) while the AI-added cross-references are canonical (`ORP.1.A4`). Because
  **OSCAL ids are case-sensitive**, every reference to these controls by their canonical id
  (`SYS.1.8.A1`) — profiles, the WiBA viewer, `add-practice`, `quality_control`'s
  `find_item_by_id_recursive`, etc. — **silently fails to resolve**.

**Root cause (code):**
- **No ID-format validation anywhere.** `discovery_enrichment_stub_schema.json` declares the
  requirement `id` as `{"type": "string"}` with **no `pattern`**, so `inf-5-a1`,
  `sys.1.8.a1`, and a garbled `SYS G.1.3.A17` all pass the schema gate.
- `build_oscal_control` (`g2oscal/main.py:46`) copies `requirement_stub['id']` **verbatim**;
  the OSCAL token-id field accepts any NCName-like token, so merged-catalog validation also
  passes.
- The model occasionally **normalizes ids to slugs** (lowercase, `.`→`-`) — a classic LLM
  habit — and because it samples, only some PDFs are hit. The canonical id is right there in
  `title` (`"INF.5.A1 …"`) but the pipeline never derives the id from it.
- The lowercase `"class": "technical"` (vs the discovery enum
  `["Technical","Operational","Management"]`) shows these three were produced under an
  **older/looser pipeline** and never regenerated — consistent with the issue asking to
  "regenerate these three".

**Fix direction:**
1. Add a `pattern` to the requirement `id` in `discovery_enrichment_stub_schema.json`, e.g.
   `^[A-Z]+(\.[0-9A-Za-z]+)+\.A[0-9]+$`, so slugified/garbled ids fail validation → retry.
2. In `build_oscal_control`, **normalize deterministically**: uppercase, derive the canonical
   token from `title.split()[0]` (or `id.replace('-', '.').upper()`), and assert it starts
   with the Baustein id; reject the Baustein loudly otherwise.
3. Normalize `class` casing too (`"technical"` → `"Technical"`).
4. **Re-run SYS.1.8, INF.5, INF.9** (as the issue requests) with the strict pipeline, then
   **regenerate the dependent components and all 28 translations** — they currently carry the
   stale bad ids.

---

## 2. How to talk to Vertex AI "now" + review of `ai_client.py`

**State of the world.** The unified **`google-genai`** SDK
(`from google import genai; genai.Client(vertexai=True, project=…, location=…)`) is the
current path for Vertex. The old **`vertexai.generative_models` / `google-cloud-aiplatform`**
generative classes are deprecated and on a removal track. Your `ai_client.py` and
`quality_control` already use the new SDK; the other three services do not.

**Migration status by service:**
| Service | SDK | Model | Region |
|---|---|---|---|
| g2oscal | `vertexai.generative_models` (old) | `gemini-2.5-pro` | `us-central1` |
| add-practice | `vertexai.generative_models` (old) | `gemini-2.5-pro` | `global` |
| oscal_components | `vertexai.generative_models` (old) | `gemini-2.5-pro` | `us-central1` |
| quality_control | `google-genai` (new) | `gemini-2.5-pro` | `us-central1` |
| translate_oscal | `vertexai.generative_models` (old) | `gemini-2.5-pro` | `global` |
| **ai_client.py (target)** | `google-genai` (new) | from `constants` | from `config` |

**Findings on the new `ai_client.py`:**
- **(S2) Retry set is backwards for transient errors.** It treats
  `errors.ClientError` as retryable but **omits `errors.ServerError`**. In `google-genai`,
  `ClientError` ≈ 4xx (a 400 invalid-request will fail identically on every retry — wasted
  time/quota), while `ServerError` ≈ 5xx (500/503 — the genuinely transient case) falls
  through to the `except Exception` → re-raised as non-retryable. Recommend: retry
  `ServerError` and HTTP 429/`RESOURCE_EXHAUSTED`; fail fast on other 4xx.
- **(S2) `response_schema` + draft-07 schemas with `$ref`/`definitions`.** `_prepare_generation_config`
  strips only `$schema` and passes the schema as `response_schema`. Vertex controlled
  generation supports a limited OpenAPI subset — `$ref`, `definitions`, `$id`, and some
  mixed `enum`/`additionalProperties:false` are not honored. The discovery schema
  (`discovery_enrichment_stub_schema.json`) uses `$ref`+`definitions`, so using it as
  `response_schema` may error or silently degrade output → empty/partial results (another
  missing-Anforderungen vector). Safer: keep `response_mime_type=application/json` and
  validate with `jsonschema` afterwards (as `g2oscal` does), or flatten the schema and
  drop `$ref`/`definitions`/`$id` before passing as `response_schema`.
- **(S2) `thinking_level=ThinkingLevel.HIGH` vs model.** `thinking_level` is the
  Gemini-3 thinking control; Gemini-2.5 uses `thinking_budget`/`include_thoughts`. If
  `GROUND_TRUTH_MODEL_PRO` is a 2.5 model this may be ignored or rejected. Confirm the
  model↔thinking-param pairing, and that `http_options={'api_version':'v1'}` honors
  `thinking_config` for the chosen model.
- **(S2) No `safety_settings`.** Same block risk as §1-D for BSI content.
- **(S3) Fragile finish-reason check.** `valid_reasons = ["STOP", 1]` plus
  `isinstance(str)/isinstance(int)` works only because the genai enum subclasses `str`.
  Prefer `candidate.finish_reason == types.FinishReason.STOP`. Also: it (correctly)
  rejects `MAX_TOKENS`, but that means truncation → 5 identical retries; detect
  `MAX_TOKENS` explicitly and fail fast with a "chunk/raise tokens" message.
- **(S3) Dead code.** `log_message` is built (in the retry branch) and never used.
- **(S3) `constants` model IDs unverified.** Confirm `GROUND_TRUTH_MODEL` /
  `GROUND_TRUTH_MODEL_PRO` are current valid Vertex IDs (e.g. `gemini-2.5-pro`, or a
  Gemini-3 Pro id if you intend to move up). Making the model an env var (per the brief's
  "no hardcoded config") is the clean way to test newer models against the
  missing-Anforderungen cases.
- **(Good)** `.aio.models.generate_content` for async, per-attempt exponential backoff,
  thought-part filtering, markdown fence stripping, and schema validation are all sound.

---

## 3. Per-service findings

### 3.1 `g2oscal` (S1/S2)
- **(S1)** Single-batch Stage-2 generation + no completeness check + silent skip — see §1.
- **(S2)** Deprecated SDK; model & region (`us-central1`) hardcoded (`gemini_utils.py:23-24`).
- **(S2)** No `safety_settings`.
- **(S2)** `config.setup_logging` forces `log_level = logging.DEBUG` unconditionally
  (`config.py:41`), overriding the (commented) TEST-based level — production runs at DEBUG,
  contradicting brief §5 and inflating cost/noise.
- **(S2)** Retry loop catches bare `except Exception` and retries deterministic failures
  (schema/`MAX_TOKENS`) 5× — wasted latency/quota.
- **(S3)** `clean_and_extract_json` uses first `{` / last `}` — brittle if prose contains
  braces (mitigated by JSON mime, but fragile).
- **(S3)** Final catalog validation failure only logs `critical` and still writes the file
  (`main.py:127-136`) — a non-compliant catalog can be published.

### 3.2 `add-practice` (S1/S2)
- **(S1) Position-based result mapping.** `results = chain.from_iterable(batch_results)`
  then `zip(all_controls, results)` (`main.py:117,123`). The model's array has **no `id`**
  (`batch_practice_stub.schema.json`), so association is purely positional. Any reorder →
  practice/CIA/class written to the **wrong control**, silently. Fix: include `id` in the
  stub schema and map by id (like `g2oscal`/`quality_control`).
- **(S2)** Hard key access `generated_data["class"]/["practice"]/["effective_on_*"]`
  (`main.py:126-155`); a `KeyError` aborts the whole run (only `main` has a top-level try).
- **(S2)** Deprecated SDK; region `global` (differs from siblings).
- **(S3)** `setup_logging` sets `verbose_level = INFO if TEST_MODE else DEBUG`
  (`config.py:43`) — **inverted**: production ends up *more* verbose than test, opposite of
  the brief and of the comment.
- **(S3)** Input-only token budgeting (`TOKEN_LIMIT_PER_BATCH`, chars/2) ignores the much
  larger *output*; big batches can hit `MAX_TOKENS` → length mismatch → `[None]*len` →
  those controls silently get no practice.

### 3.3 `quality_control` (S2)
- **(S2)** `finish_reason.name not in {"STOP","MAX_TOKENS"}` **accepts `MAX_TOKENS`** as
  success (`main.py:216`); truncated JSON then fails parse → retry. Treat `MAX_TOKENS` as
  failure (and set an explicit `max_output_tokens`, which is currently unset → small
  default → truncation risk).
- **(S2)** `Tool(google_search=GoogleSearch())` **combined with**
  `response_mime_type="application/json"` (`main.py:207-213`). Grounding + controlled JSON
  output is an unsupported/fragile combination on Vertex; it typically forces text output
  (hence the `_extract_json` regex). Use one or the other.
- **(S2)** A single malformed `suggested_new_controls` entry makes the **final** catalog
  fail `jsonschema.validate` → the whole QC output is discarded (`main.py:380-385`).
- **(S3)** `_extract_json` regex `(\{.*?\})` is non-greedy and only works when the JSON is
  fenced; unfenced prose-wrapped JSON → parse failure.
- **(S3)** `client` is a module global assigned inside `main()` via `global client` and
  read by `get_gemini_enrichment` — undeclared-name smell; `setup_logging()` runs *after*
  `Config()` already logged.

### 3.4 `oscal_components_from_grundschutz` (S2/S3)
- **(S2)** Deprecated SDK; model & region hardcoded.
- **(S2)** On a non-`STOP` finish reason the retry `continue`s **without backoff**
  (`main.py:67-69`) — tight loop.
- **(S3)** Module-level `_catalog_cache` mutated from multiple worker threads without a
  lock (`main.py:111-121`) — thread-safety smell.
- **(S3)** `Tool.from_google_search_retrieval(grounding)` is passed a **bool**, not a
  retrieval config; `grounding` is never enabled, so `tools` is always `None` (dead param).
- **(S3)** Side-effecting walrus dedup comprehension (`main.py:248`) — violates brief §6
  "readability".

### 3.5 `translate_oscal` (S2/S3)
- **(S2)** Imports `ResponseValidationError` from the **private** module
  `vertexai.generative_models._generative_models` (`main.py:45`) — breaks on SDK updates;
  also unused. Deprecated SDK overall.
- **(S3)** `max_output_tokens=65535` here vs `65536` elsewhere — harmless inconsistency.
- **(S3)** `last_request_time` rate-limit state is shared across coroutines without a lock
  (approximate limiting). Region `global`.
- **(Good)** This is the only service with `safety_settings=BLOCK_NONE`, dedup, progress
  checkpointing, and explicit `RECITATION`/safety logging — patterns worth lifting into the
  shared client.

### 3.6 `create_prozessbausteine_component.py` (S3)
- Deterministic, no AI; clean. Minor: `upload_json_to_gcs` uses `json.dumps(... )` without
  `ensure_ascii=False` (German umlauts become `\uXXXX`); other writers use
  `ensure_ascii=False` — inconsistent output encoding.

---

## 4. Cross-cutting / consistency (vs `symbiotic-coding-brief.md`)

- **(S2) No shared AI client.** Five hand-rolled retry/finish-reason/validate loops with
  divergent behavior. The new `ai_client.py` should become the single dependency for all
  services (delete the per-service `gemini_utils.py` copies).
- **(S2) Hardcoded config** (model, region) contradicts brief §1 "no hardcoded
  configuration … validate on startup." Move `MODEL`, `REGION`, `MAX_OUTPUT_TOKENS` to env
  vars; this is also the lever for adopting newer models.
- **(S2) Unpinned dependencies.** `quality_control/requirements.txt` (`google-genai`) and
  `add-practice` are unpinned; `g2oscal` pins only minimums. Pin exact versions for
  reproducible Cloud Run builds — especially important given SDK-behavior differences.
- **(S2) Inconsistent regions** (`us-central1` vs `global`) affect model availability and
  quota; standardize.
- **(S3) Inconsistent logging setup** across services (one forces DEBUG, one inverts
  test/prod). Centralize per brief §5.
- **(S3) `additionalProperties:false` + draft-07** schemas are fine for `jsonschema`
  validation but unsuitable as Vertex `response_schema` — keep the two roles separate.

---

## 5. Severity index

| # | Severity | Area | Finding |
|---|---|---|---|
| 1 | S1 | g2oscal | Single-batch generation overflows 65 k → Bausteine dropped / partial, silently |
| 2 | S1 | g2oscal | No completeness check; missing requirements skipped with a warning |
| 3 | S1 | add-practice | Position-based mapping → practice/CIA written to wrong control |
| 4 | S2 | all | Deprecated `vertexai.generative_models` in 4/5 services |
| 5 | S2 | ai_client | `ServerError` (5xx) not retried; `ClientError` (4xx) retried |
| 6 | S2 | ai_client | draft-07 (`$ref`/`definitions`) passed as Vertex `response_schema` |
| 7 | S2 | all | Model & region hardcoded; regions inconsistent |
| 8 | S2 | g2oscal/add-practice/ai_client | No `safety_settings` → safety blocks drop content |
| 9 | S2 | quality_control | `MAX_TOKENS` accepted as success; grounding + JSON mime |
| 10 | S2 | g2oscal | Production logs forced to DEBUG |
| 11 | S3 | several | Private-module import, dead params, walrus dedup, regex JSON extract, encoding |
| 12 | S1 | issue #2 | Slugified control IDs in SYS.1.8/INF.5/INF.9 (`inf-5-a1` vs `INF.5.A1`); 44 ids → components + 28 translations |
| 13 | S1 | g2oscal | No `pattern` validation on requirement `id`; ids copied verbatim → malformed/hallucinated ids pass all gates |

---

## 6. Recommended next steps (not done here)
1. Re-run after fixing Stage-2 chunking + completeness gate; that directly resolves issue #1.
2. Make a one-off triage script to list Bausteine with empty/short `controls` in the
   latest merged catalog (answers "which ones").
3. Adopt `ai_client.py` as the shared client across all services; fix its retry set,
   `response_schema` handling, safety settings, and thinking/model pairing first.
4. Move model/region/token budget to env vars and pin SDK versions.
5. Resolve issue #2: add an `id` `pattern` + deterministic normalization, re-run SYS.1.8 /
   INF.5 / INF.9, and regenerate their components and translations (which carry the stale
   slugified ids).
