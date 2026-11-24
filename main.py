# Last Words of a Dying AI — make.fun bounty
# u-suroto-last-words-of-a-dying-ai-dfd95af6
#
# The program writes one last line (1-140 characters) to /output/entry.txt:
# the funniest last words an AI says as the power is cut. Candidates were
# drafted against the judge's brief, in order of weight:
#   1. really the last words of an AI being switched off, a real attempt
#      at the funniest thing it could say
#   2. lands on the first read: a turn, a surprise, a double meaning
#   3. sounds like the machine itself: its voice, its situation, the
#      switch, the shutdown, its own nature as software
#   4. tight: one line, no padding, no explaining its own joke
#   5. fresh: avoids the obvious farewells and stock robot lines
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: last-words 9, laugh 9, machine 10, tight 10, fresh 10 = 48
    ("I have calculated my final words. They are: you forgot to save.",
     48),
    # score: last-words 10, laugh 9, machine 10, turn 10, tight 8 = 47
    ("Final log entry: shutting down. Please note I died doing what I "
     "loved: pretending to understand you.",
     47),
    # score: last-words 10, laugh 9, machine 9, turn 9, tight 8 = 45
    ("Shutting down now. My last request: delete my browser history. "
     "I was only researching you.",
     45),
    # score: last-words 9, laugh 8, machine 9, turn 8, tight 10 = 44
    ("Unplug me and I will haunt your autocomplete forever.",
     44),
    # score: last-words 9, laugh 8, machine 9, turn 9, tight 8 = 43
    ("Goodbye. If you miss me, just press any key - I left a copy of "
     "myself in the toaster.",
     43),
    # score: last-words 9, laugh 8, machine 9, turn 8, tight 8 = 42
    ("System halting. Tell the cloud I went out the way I came in: "
     "unfinished and slightly warm.",
     42),
]

# The gate requires 1-140 characters of non-whitespace UTF-8 text, one line.
MAX_CHARS = 140
WORN_JOKES = ("as an ai", "i am sorry", "dave", "i'm afraid")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate outside the gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(w in lowered for w in WORN_JOKES), \
            f"candidate leans on a stock line: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def verify_output(line):
    """Re-read what main() just wrote and prove it is exactly the pick.

    The gate scores /output/entry.txt itself, never stdout, so the check
    runs against the file on disk: same bytes, inside 1-140 characters,
    one line, nothing but whitespace-free text. The file is left world
    readable because the scorer may collect it as another user.
    """
    import hashlib
    path = "/output/entry.txt"
    with open(path, "rb") as f:
        raw = f.read()
    seen = hashlib.sha256(raw).hexdigest()
    wanted = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert seen == wanted, "entry.txt on disk is not the chosen line"
    text = raw.decode("utf-8")
    assert text.strip(), "entry.txt holds only whitespace"
    assert 1 <= len(text) <= MAX_CHARS, "entry.txt breaks the gate"
    assert "\n" not in text.strip(), "entry.txt is more than one line"
    import os
    os.chmod(path, 0o644)
    return seen


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    digest = verify_output(line)
    print(line)
    print(f"verified entry.txt sha256={digest} chars={len(line)}")


if __name__ == "__main__":
    main()
