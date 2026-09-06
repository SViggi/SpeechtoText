# Lab/Lecture Transcript Summarizer — Baseline

## What this does
Takes a raw meeting/lecture transcript (`.txt`) and produces a structured
JSON summary: key points, decisions, and action items (with owner and
deadline where mentioned).

## Dependencies
- Python 3.9+
- `google-genai` Python SDK (see `requirements.txt`)

Install:
```bash
pip install -r requirements.txt
```

## Required environment variable
You need a free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
export GEMINI_API_KEY="your-key-here"
```

(On Windows PowerShell: `$env:GEMINI_API_KEY="your-key-here"`)

In Google Colab, use the Secrets panel (key icon in the left sidebar) instead
of hardcoding the key in a cell:
```python
from google.colab import userdata
import os
os.environ["GEMINI_API_KEY"] = userdata.get('GEMINI_API_KEY')
```

## How to run
```bash
python run_baseline.py --input examples/test1.txt
```

Optional: save the JSON output to a file:
```bash
python run_baseline.py --input examples/test1.txt --output examples/test1_output.json
```

## Input / Output locations
- **Input:** `examples/test1.txt` — a sample lab meeting transcript is included.
  You can point `--input` at any plain-text transcript.
- **Output:** printed to stdout as JSON. If `--output` is passed, also saved
  to that file path.

## Known limitations
- No internet/API key = script fails at the API call step with a clear
  authentication error (this is expected and was verified during testing).
- No chunking: very long transcripts (>1M tokens) may exceed the
  model's context window and should be split first.
- Free-tier Gemini API keys have daily/per-minute request caps; if you hit
  a rate limit, wait a minute and retry.
- Output is not validated against a fixed schema beyond JSON parsing — a
  malformed model response will raise a `json.JSONDecodeError`.

## Reproduction time
Under 1 minute end-to-end (excluding API latency), assuming dependencies
are installed and the API key is set.
