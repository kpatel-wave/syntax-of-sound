# Syntax of Sound

**Syntax of Sound** is a tiny Python project that tags short descriptions of orchestral moments with structural labels — things like `high-risk-solo`, `tempo-boundary`, or `dissonance-resolving-with-trumpets`.

It’s a rule-based, explainable tool: instead of using a large model, it parses text and applies simple, transparent rules about tempo, solos, dissonance, and texture. That keeps it small enough to finish while still reflecting ideas from music theory, linguistics, and neuroscience.

## Example

Input:

```text
Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%
```

Possible output (plain-text mode):

```text
Input:
  Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%

Parsed:
  composer: Mahler
  movement: 3th movement
  tempo: 132
  instruments: ['french horn', 'horn']

Labels:
  - high-risk-solo
  - high-tempo
  - tempo-boundary
  - tempo-fluctuation
```

## How to run

From the project folder:

```bash
python main.py "Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%"
```

For JSON output instead:

```bash
python main.py "Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%" --json
```

## Project idea

The goal is not to build a full music-analysis system, but to prototype a “syntax” layer for orchestral moments: a way to talk about how risk, tempo, dissonance, and texture are encoded in short descriptions. It sits at the intersection of:

- music performance (high-risk exposed lines, tempo edges),
- linguistic-style tagging (labeling spans with categories),
- and neuroscience-style thinking about tension, prediction, and resolution.

## Live demo

Try Syntax of Sound in your browser (no installation required):

https://syntax-of-sound.streamlit.app
