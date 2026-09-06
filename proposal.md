# Capstone Project Proposal

| Field | Response |
|---|---|
| Student name | Sai Vignesha Shesha Shyla |
| Project title | Lab/Lecture Transcript Summarizer Agent |
| Repository / notebook link | https://github.com/SViggi/SpeechtoText |
| Configuration location | README.md |

---

## Section 1. Problem Definition

The system takes a raw text transcript of a lab meeting or lecture and
produces a structured summary containing key points, decisions made, and
action items (with owner and deadline, when mentioned).

- **Intended user:** a graduate student or researcher who attends frequent
  lab meetings/lectures and needs a fast, reliable way to extract
  actionable notes without re-reading the full transcript.
- **Input:** a plain-text transcript (speaker-labeled dialogue).
- **Output:** structured JSON with three fields — `key_points`,
  `decisions`, and `action_items` (each item has `owner`, `task`,
  `deadline`).
- **Success:** every decision and action item explicitly stated in the
  transcript appears in the output, correctly attributed to the right
  speaker, with no fabricated items.
- **Failure:** the system omits a stated action item/decision,
  misattributes an owner, or hallucinates an item not present in the
  transcript.

## Section 2. Motivation and Project Scope

Lab meetings and lectures generate information that is easy to lose track
of, especially across a busy semester. A lightweight agent that reliably
converts a transcript into actionable notes saves time and reduces missed
follow-ups.

An agentic/LLM-based approach is reasonable here because the task requires
language understanding (attributing statements to speakers, distinguishing
a decision from a passing comment) that rule-based text extraction cannot
handle robustly.

**In scope this semester:**
- Single-transcript summarization (key points, decisions, action items)
- Structured, machine-readable output (JSON)
- Basic evaluation against manually-labeled ground truth for a handful of
  transcripts

**Out of scope this semester:**
- Real-time audio transcription (input is assumed to already be text)
- Multi-meeting memory or long-term tracking of open action items across
  sessions
- Speaker diarization from raw audio

## Section 3. Runnable Baseline

- **Model/tool/framework:** Google Gemini API (`gemini-3.6-flash`),
  called via the official `google-genai` Python SDK. No additional frameworks.
  (Note: Gemini model names are updated frequently by Google; if this model
  is retired, the API's error message names the current replacement.)
- **Step by step:**
  1. Read the transcript `.txt` file from disk.
  2. Send it to the Gemini API with a system instruction directing the
     model to extract key points, decisions, and action items into a fixed
     JSON schema (using Gemini's built-in JSON response mode).
  3. Parse and validate the returned JSON.
  4. Print the result to stdout (optionally save to a file).
- **Why this is a reasonable starting point:** a single well-prompted LLM
  call is the simplest possible baseline that produces a usable, structured
  output. It establishes a quality floor before adding complexity (e.g.
  retrieval over past meetings, multi-step verification, or a
  classification pass to catch hallucinated items).
- **Files:** `run_baseline.py` (implementation), `examples/test1.txt`
  (sample input).

## Section 4. Test Case and Baseline Output

**Sample input** (`examples/test1.txt`): a 4-speaker-turn lab meeting
transcript covering a calibration fix, a storage request, and a paper
deadline.

**Expected behavior:** the output should list 3 action items (calibration
test, storage request email, paper draft by Friday) each attributed to
"Sai," and one decision (revisit checkpoint after storage increase).

**Actual baseline output** (run in Google Colab, `gemini-3.6-flash`,
`GEMINI_API_KEY` set via Colab Secrets — see attached screenshot):

```json
{
  "key_points": [
    "OpenCV pose estimation pipeline on the Dobot arm showed accuracy drops under changing lighting conditions.",
    "Diffusion model training stopped at 50k steps due to SOL storage space constraints.",
    "IJRASET paper revisions are due in two weeks."
  ],
  "decisions": [
    "Address pose estimation lighting issues via a session-start calibration pass rather than getting a new camera.",
    "Request additional storage quota from IT to proceed with diffusion model training."
  ],
  "action_items": [
    {
      "owner": "Sai",
      "task": "Test session-start calibration pass for the OpenCV pose estimation pipeline",
      "deadline": "this week"
    },
    {
      "owner": "Sai",
      "task": "Email IT about expanding the SOL storage quota",
      "deadline": "not specified"
    },
    {
      "owner": "Sai",
      "task": "Send draft of IJRASET paper revisions to Advisor",
      "deadline": "Friday"
    }
  ]
}
```

**What worked / what didn't:** all three action items and both decisions
were correctly extracted, with correct owner attribution and correct
deadlines pulled from context (e.g. "this week," "Friday"). One item
("email IT") correctly used "not specified" since no deadline was given —
matching the intended schema behavior. No hallucinated items were
observed in this test case. A known remaining risk is attribution when
an owner is referenced only as "you" rather than by name.

## Section 5. Reproducibility and Run Instructions

See `README.md` for full details. Summary:

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your-key-here"
python run_baseline.py --input examples/test1.txt
```

Input: `examples/test1.txt`. Output: printed to stdout as JSON (optionally
saved via `--output`).

## Section 6. Initial Evaluation Plan

Future versions will be compared against this baseline using:
- **Completeness:** % of ground-truth action items/decisions recovered
  (manually labeled on 5–10 held-out transcripts)
- **Precision:** % of output items that are not hallucinated
- **Attribution accuracy:** % of action items with the correct owner
- **Latency and cost:** per-transcript API cost and response time

## Section 7. Limitations and Next Steps

**Known weaknesses:** no chunking for long transcripts; no schema
validation beyond JSON parsing; single LLM call has no self-check step, so
hallucinated items are possible.

**Expected failure cases:** transcripts with ambiguous pronouns ("you
should handle that") may cause misattribution; very informal or
overlapping speech may confuse the speaker-turn structure.

**Next phase plans:** add a verification pass (second LLM call or
rule-based check) that cross-references extracted items against the source
text; add transcript chunking for long meetings; begin tracking action
items across multiple meetings.

**Risks:** transcript quality (if sourced from real ASR output) may be
noisy; will need a small labeled evaluation set, which requires manual
annotation time.
