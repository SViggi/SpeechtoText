"""
Baseline: Lab/Lecture Transcript Summarizer Agent
Single-call LLM baseline using the Google Gemini API.

Usage:
    python run_baseline.py --input examples/test1.txt
"""

import argparse
import json
import os
import sys

from google import genai

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_PROMPT = """You are a note-taking assistant for a research lab.
Given a raw meeting or lecture transcript, extract a structured summary.
Respond ONLY with valid JSON in exactly this format, no other text,
no markdown code fences:

{
  "key_points": ["...", "..."],
  "decisions": ["...", "..."],
  "action_items": [
    {"owner": "...", "task": "...", "deadline": "..."}
  ]
}

If a field has no deadline mentioned, use "not specified".
"""


def summarize_transcript(transcript_text: str) -> dict:
    client = genai.Client()  # reads GEMINI_API_KEY from env

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=transcript_text,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
        },
    )

    raw_text = response.text.strip()

    # Strip markdown code fences if the model adds them anyway
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:].strip()

    return json.loads(raw_text)


def main():
    parser = argparse.ArgumentParser(description="Summarize a lab/lecture transcript.")
    parser.add_argument("--input", required=True, help="Path to transcript .txt file")
    parser.add_argument("--output", default=None, help="Optional path to save JSON output")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    print(f"Loaded transcript from {args.input} ({len(transcript_text)} characters)")
    print(f"Calling Gemini API ({MODEL_NAME}) for summarization...")

    try:
        result = summarize_transcript(transcript_text)
    except Exception as e:
        print(f"ERROR: baseline call failed: {e}")
        sys.exit(1)

    print("\n=== BASELINE OUTPUT ===")
    print(json.dumps(result, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved output to {args.output}")


if __name__ == "__main__":
    main()
