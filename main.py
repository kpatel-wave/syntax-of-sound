import argparse
import json
from labeler import analyze


def main():
    parser = argparse.ArgumentParser(
        description="Syntax of Sound: tag structural features of short orchestral moments."
    )
    parser.add_argument(
        "description",
        help="Short description of a musical moment (e.g., 'Mahler, 3rd movement, tempo 132, French-horn solo, tempo fluctuation ±10%')",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output instead of plain text.",
    )
    args = parser.parse_args()

    result = analyze(args.description)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Input:")
        print("  ", result["input"])
        print("\nParsed:")
        for k, v in result["parsed"].items():
            print(f"  {k}: {v}")
        print("\nLabels:")
        if result["labels"]:
            for tag in result["labels"]:
                print("  -", tag)
        else:
            print("  (none)")


if __name__ == "__main__":
    main()
