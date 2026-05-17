# Syntax of Sound

A tiny Python + Streamlit tool that tags short descriptions of orchestral moments with structural labels like `high-risk-solo`, `tempo-boundary`, or `dissonance-resolving-with-trumpets`.

**Syntax of Sound** is a rule-based, explainable tool: instead of using a large model, it parses text and applies simple, transparent rules about tempo, solos, dissonance, and texture. That keeps it small enough to finish while still reflecting ideas from music theory, linguistics, and neuroscience.

## Live demo

Try Syntax of Sound in your browser (no installation required):

https://syntax-of-sound.streamlit.app

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
  movement: 3rd movement
  tempo: 132
  instruments: ['french horn', 'horn']

Labels:
  - high-risk-solo
  - high-tempo
  - tempo-boundary
  - tempo-fluctuation
```

## How to run (command-line)

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

## How it’s built

- Core logic: Python, with simple regex/keyword rules in `labeler.py`.
- Command-line interface: `main.py` using the standard `argparse` module.
- Web demo: `app.py` built with [Streamlit](https://streamlit.io/), deployed via Streamlit Community Cloud.
