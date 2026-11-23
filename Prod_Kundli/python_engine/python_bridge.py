"""CLI bridge that receives JSON birth details from Node.js Express, executes Swiss Ephemeris calculations, and outputs JSON."""
import sys
import os
import json

# Ensure python_engine is on PYTHONPATH
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

from kundli.astronomy.coordinates import BirthInput
from kundli.orchestrator import generate_complete_kundli
from kundli.matching.compatibility import evaluate_marriage_compatibility


def main():
    try:
        # Read JSON input from stdin
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            sys.stderr.write("Error: Empty input payload\n")
            sys.exit(1)

        payload = json.loads(raw_input)
        action = payload.get("action", "generate")

        if action == "generate":
            birth_data = payload.get("birth", payload)
            birth = BirthInput(**birth_data)
            report = generate_complete_kundli(birth)
            sys.stdout.write(json.dumps(report, ensure_ascii=False))

        elif action == "matching":
            groom_birth = BirthInput(**payload["groom"])
            bride_birth = BirthInput(**payload["bride"])
            matching = evaluate_marriage_compatibility(groom_birth, bride_birth)
            sys.stdout.write(json.dumps(matching, ensure_ascii=False))

        else:
            sys.stderr.write(f"Error: Unknown action '{action}'\n")
            sys.exit(1)

    except Exception as e:
        import traceback
        sys.stderr.write(f"Calculation Error: {str(e)}\n{traceback.format_exc()}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
