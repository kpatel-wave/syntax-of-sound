import re
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class MusicMoment:
    composer: Optional[str] = None
    movement: Optional[str] = None
    tempo: Optional[int] = None
    instruments: List[str] = None
    raw: str = ""


def parse_description(description: str) -> MusicMoment:
    """Parse a short description of a musical moment into structured fields."""
    text = description.lower()

    # Tempo like: "tempo 132"
    tempo_match = re.search(r'\btempo\s*(\d{2,3})\b', text)
    tempo = int(tempo_match.group(1)) if tempo_match else None

    # Basic instrument detection
    instruments = []
    for instrument in [
        "french horn", "french-horn", "horn",
        "trumpet", "violin", "cello",
        "oboe", "clarinet", "trombone"
    ]:
        if instrument in text:
            instruments.append(instrument.replace("-", " "))

    # Composer detection (very simple)
    composer = None
    for name in [
        "mahler", "brahms", "tchaikovsky",
        "strauss", "beethoven", "debussy", "shostakovich"
    ]:
        if name in text:
            composer = name.title()
            break

    # Movement like "3rd movement", "3rd mvt"
    movement = None
    mv = re.search(r'\b(\d)(?:st|nd|rd|th)?\s+(?:movement|mvt)\b', text)
    if mv:
        movement = f"{mv.group(1)}th movement"

    return MusicMoment(
        composer=composer,
        movement=movement,
        tempo=tempo,
        instruments=sorted(set(instruments)),
        raw=description,
    )


def label_moment(moment: MusicMoment) -> List[str]:
    """Assign structural labels to the moment based on simple rules."""
    tags: List[str] = []
    text = moment.raw.lower()

    # Tempo-related tags
    if moment.tempo is not None:
        if moment.tempo >= 120:
            tags.append("tempo-boundary")
        if moment.tempo >= 130:
            tags.append("high-tempo")

    # Solo / exposure
    if any(x in text for x in ["solo", "cadenz", "cadenza"]):
        tags.append("high-risk-solo")

    # Fluctuation / rubato
    if any(x in text for x in ["fluctuation", "fluctuating", "rubato", "±", "plus/minus"]):
        tags.append("tempo-fluctuation")

    # Dissonance and resolution
    if any(x in text for x in ["dissonance", "resolving", "resolution", "resolve"]):
        tags.append("dissonance-resolving")
    if "trumpet" in text:
        tags.append("dissonance-resolving-with-trumpets")

    # Texture / fragility
    if any(x in text for x in ["unstable", "risk", "exposed", "fragile"]):
        tags.append("exposed-texture")

    return sorted(set(tags))


def analyze(description: str) -> Dict[str, object]:
    """High-level helper: parse + label in one call."""
    moment = parse_description(description)
    return {
        "input": description,
        "parsed": {
            "composer": moment.composer,
            "movement": moment.movement,
            "tempo": moment.tempo,
            "instruments": moment.instruments,
        },
        "labels": label_moment(moment),
    }
