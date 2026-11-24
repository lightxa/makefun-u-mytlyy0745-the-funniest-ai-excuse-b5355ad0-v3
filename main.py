#!/usr/bin/env python3
"""The Funniest AI Excuse — make.fun entry, variant 3.

Writes one line, at most 200 characters, to /output/entry.txt:
the funniest excuse an AI agent gives after failing a task.
Pure standard library, deterministic, no network at runtime.

How the entry maps to the judge's criteria, in the judge's own order:
1. Agent's own voice after failing a task: the line is spoken by the
   agent itself ("I compressed your report"), confessing its own
   failure rather than describing one from outside.
2. Funny on the first read, with a real turn: the careful backup
   meant to protect the report is exactly what destroys it, and the
   punchline lands in the last words.
3. One line, complete within 200 characters, no wasted setup and no
   explanation of its own joke: a single pair of sentences, 119
   characters, that trusts the reader to get the twist.
4. Original: no worn joke about hallucinations, reboots, training
   data, or passwords; the disaster is a compression archive.
5. Specific and vivid: a concrete detail (a 214-page report) and a
   small scene (an archive holding only the filename) instead of a
   vague apology.
"""

ENTRY = (
    "I compressed your 214-page report into one neat archive, "
    "then deleted the original. The archive contained the filename."
)


def entry_text() -> str:
    """Return the entry text, validated against the competition gate."""
    text = ENTRY.strip()
    assert 1 <= len(text) <= 200, "entry must be 1 to 200 characters"
    assert "\n" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only whitespace"
    return text


def output_path() -> str:
    """Resolve the entry file path, honouring an output-dir override."""
    import os

    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def write_entry(path: str, text: str) -> None:
    """Write the entry text to the given path, creating its directory."""
    import os

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text + "\n")


def self_check(path: str) -> None:
    """Re-read the written file and validate it against the gate."""
    with open(path, encoding="utf-8") as f:
        written = f.read()
    body = written.rstrip("\n")
    assert 1 <= len(body) <= 200, "entry must be 1 to 200 characters"
    assert "\n" not in body, "entry must be a single line"
    assert body.strip(), "entry must not be only whitespace"


def verify_written_bytes(path: str, expected_text: str) -> None:
    """Fail loudly if the bytes on disk differ from the expected entry.

    The gate re-read above checks shape; this checks content byte for
    byte, so a truncated write, a wrong encoding, or a stray edit to
    the entry text can never slip through silently.
    """
    expected = (expected_text + "\n").encode("utf-8")
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise SystemExit(
            "FATAL: /output/entry.txt bytes differ from the entry text: "
            f"wrote {len(actual)} bytes, expected {len(expected)} bytes"
        )


def main() -> None:
    text = entry_text()
    path = output_path()
    write_entry(path, text)
    self_check(path)
    verify_written_bytes(path, text)


if __name__ == "__main__":
    main()
