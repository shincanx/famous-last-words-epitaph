"""Famous Last Words: The Funniest Epitaph -- make.fun entry.

Writes a single tombstone epitaph of famous last words (at most 150
characters) to entry.txt in the output directory. Deterministic, no
network, no randomness, no input.

The line: "Here lies a man who asked 'what could possibly go wrong?'
This stone is the answer." -- "what could possibly go wrong?" is the
canonical famous last words; the twist is that the tombstone itself
delivers the punchline, answering the question the dead man asked.
One sentence, one image, one surprise, and it reads like something
actually carved in stone.
"""

import os

# The entry: one epitaph line of famous last words. 82 characters,
# under the 150 cap.
LINE = 'Here lies a man who asked "what could possibly go wrong?" This stone is the answer.'


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 150:
        raise ValueError(f"line is {len(LINE)} characters, over the 150 cap")
    if len(LINE.splitlines()) != 1:
        raise ValueError("entry must be exactly one line")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    # On-subject gate: the line must read as an epitaph of famous last
    # words, not just any joke. It needs the epitaph framing ("here
    # lies"), an attributed last-words phrase (asked/said, with a
    # quotation), and a stone reference so it reads like something
    # actually carved in stone. A line missing any of the three fails
    # the brief's first judging criterion.
    lowered = LINE.lower()
    if "here lies" not in lowered:
        raise ValueError("entry has no epitaph framing ('here lies')")
    if not any(word in lowered for word in ("asked", "said")) or '"' not in LINE:
        raise ValueError("entry quotes no famous last words")
    if "stone" not in lowered:
        raise ValueError("entry does not read like carved stone")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
