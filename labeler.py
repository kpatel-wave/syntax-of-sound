import re

# Known composers (you can add more)
COMPOSERS = [
    "mahler", "brahms", "tchaikovsky", "strauss",
    "beethoven", "debussy", "shostakovich", "holst",
    "stravinsky", "ravel", "rachmaninoff", "prokofiev",
    "schoenberg", "berlioz", "dvorak", "sibelius",
    "mozart", "haydn", "bach", "handel"
]

# Instrument patterns: handle plurals and common variants
INSTRUMENT_PATTERNS = {
    "trumpet": ["trumpet", "trumpets"],
    "french horn": ["french horn", "french-horn", "horn", "horns"],
    "trombone": ["trombone", "trombones"],
    "tuba": ["tuba", "tubas"],
    "flute": ["flute", "flutes"],
    "oboe": ["oboe", "oboes"],
    "clarinet": ["clarinet", "clarinets"],
    "bassoon": ["bassoon", "bassoons"],
    "violin": ["violin", "violins"],
    "viola": ["viola", "violas"],
    "cello": ["cello", "cellos"],
    "double bass": ["double bass", "double-bass", "bass", "basses"],
    "timpani": ["timpani", "kettle drum", "kettle drums"],
    "percussion": ["percussion", "snare", "bass drum", "cymbals"],
}


def parse_description(text: str):
    """
    Take the raw text description and pull out:
    - composer (string, or 'Unknown')
    - tempo (int bpm, or None)
    - instruments (list of canonical names)
    - raw_text (echo the input)
    """
    lower = text.lower()

    # Composer detection
    composer = "Unknown"
    for name in COMPOSERS:
        if name in lower:
            composer = name.title()
            break

    # Instrument detection (handles plurals and variants)
    instruments = set()
    for canonical, variants in INSTRUMENT_PATTERNS.items():
        for v in variants:
            if v in lower:
                instruments.add(canonical)
                break
    instruments = sorted(instruments)

    # Tempo detection using several common patterns
    tempo = None
    tempo_patterns = [
        r'\btempo\s*(\d{2,3})\b',      # "tempo 132"
        r'(\d{2,3})\s*bpm',            # "132 bpm"
        r'=\s*(\d{2,3})',              # "q = 132"
    ]
    for pattern in tempo_patterns:
        m = re.search(pattern, lower)
        if m:
            try:
                tempo = int(m.group(1))
            except ValueError:
                tempo = None
            break

    return {
        "composer": composer,
        "tempo": tempo,
        "instruments": instruments,
        "raw_text": text,
    }


def label_moment(parsed: dict):
    """
    Rule-based labels that use tempo, instruments, and language.
    """
    labels = []
    tempo = parsed.get("tempo")
    instruments = parsed.get("instruments", [])
    text = parsed.get("raw_text", "").lower()

    # High-tempo risk
    if tempo is not None and tempo >= 132:
        labels.append("high-tempo")

    # Slow exposed strings
    if tempo is not None and 56 <= tempo <= 80:
        if any(inst in instruments for inst in ["violin", "viola", "cello"]):
            if any(word in text for word in ["pp", "pianissimo", "soft", "cantabile", "dolce", "solo"]):
                labels.append("slow-exposed-strings")

    # Exposed brass solo
    if any(inst in instruments for inst in ["trumpet", "french horn", "trombone"]):
        if any(word in text for word in ["solo", "soli", "exposed", "on their own"]):
            labels.append("exposed-brass-solo")

    # Ostinato / motor rhythm
    if any(word in text for word in ["ostinato", "repeated pattern", "motor rhythm", "driving rhythm"]):
        labels.append("rhythmic-ostinato-backdrop")

    # Structural boundary / transition
    if any(word in text for word in ["suddenly", "subito", "cuts off", "drops into silence", "new section", "transition"]):
        labels.append("structural-boundary")

    # Sustained dissonance / tension
    if any(word in text for word in ["dissonant", "cluster", "clashing", "biting harmony"]):
        labels.append("sustained-dissonance")

    # Chorale-style brass entry
    if any(inst in instruments for inst in ["trumpet", "french horn", "trombone", "tuba"]):
        if any(word in text for word in ["chorale", "block chords", "homophonic"]):
            labels.append("chorale-brass-entry")

    # Generic fallback if nothing matched
    if not labels:
        labels.append("unclassified-pattern")

    return labels


def practice_tips(labels: list[str]) -> list[str]:
    """
    Map labels to concrete practice / rehearsal suggestions.
    """
    tips = []

    if "high-tempo" in labels:
        tips.append(
            "High tempo: Practice at a much slower tempo with a metronome, then raise by 4–6 bpm only after you can play it three times in a row without mistakes."
        )

    if "slow-exposed-strings" in labels:
        tips.append(
            "Slow, exposed strings: Treat this like chamber music—tune chords slowly, listen for beats, and start without vibrato so intonation is really clear."
        )

    if "exposed-brass-solo" in labels:
        tips.append(
            "Exposed brass solo: Practice entries from silence, focusing on breath, soft attacks, and secure intonation before adding the full ensemble."
        )

    if "rhythmic-ostinato-backdrop" in labels:
        tips.append(
            "Ostinato / motor rhythm: Lock the repeating pattern with a metronome and subdivide carefully so it stays steady under changing textures."
        )

    if "structural-boundary" in labels:
        tips.append(
            "Structural boundary: Decide clear cues into and out of this spot; rehearse the transition several times so the change feels coordinated."
        )

    if "sustained-dissonance" in labels:
        tips.append(
            "Sustained dissonance: Tune intervals slowly and listen for beats; aim for steady tone so the tension sounds intentional, not just out of tune."
        )

    if "chorale-brass-entry" in labels:
        tips.append(
            "Chorale brass entry: Balance inner voices and match articulation; rehearse at softer dynamics first to focus on blend and intonation."
        )

    if not tips:
        tips.append(
            "No specific practice tips triggered yet—start with rhythm, intonation, and balance, then focus on any spots that feel exposed or unstable."
        )

    return tips


def summarize(parsed: dict, labels: list[str]) -> str:
    """
    Turn the labels + parsed info into a short explanation string.
    """
    parts = []
    tempo = parsed.get("tempo")
    instruments = parsed.get("instruments", [])
    composer = parsed.get("composer", "Unknown")

    # Composer / context sentence
    if composer != "Unknown":
        parts.append(f"This moment is described in a passage by {composer}.")
    else:
        parts.append("The description doesn’t name a specific piece or composer.")

    # Tempo commentary
    if "high-tempo" in labels and tempo is not None:
        parts.append(f"The tempo around {tempo} bpm pushes the music toward the edge of comfortable control.")
    elif tempo is not None:
        parts.append(f"The tempo is around {tempo} bpm, so the technical pressure is moderate here.")

    # Instrument / risk commentary
    if "exposed-brass-solo" in labels:
        parts.append("An exposed brass solo makes small issues in attack, intonation, and tone very noticeable.")
    if "slow-exposed-strings" in labels:
        parts.append("Slow, soft string writing demands very precise intonation and blend from the section.")
    if "rhythmic-ostinato-backdrop" in labels:
        parts.append("A repeating ostinato or motor rhythm keeps underlying tension and momentum going.")
    if "structural-boundary" in labels:
        parts.append("The language suggests a structural boundary or sudden transition in the form.")
    if "sustained-dissonance" in labels:
        parts.append("Sustained dissonance or clustered harmony creates ongoing tension that can feel unstable.")
    if "chorale-brass-entry" in labels:
        parts.append("A chorale-style brass entry can sound powerful but is demanding for balance and tuning.")

    # Instrument list, if we have one
    if instruments:
        inst_str = ", ".join(instruments)
        parts.append(f"The description explicitly mentions: {inst_str}.")

    return " ".join(parts)


def analyze(text: str) -> dict:
    """
    Main entry point: parse the description, assign labels, and build a summary.
    """
    parsed = parse_description(text)
    labels = label_moment(parsed)
    summary = summarize(parsed, labels)
    tips = practice_tips(labels)

    return {
        "input": text,
        "parsed": parsed,
        "labels": labels,
        "summary": summary,
        "tips": tips,
    }
