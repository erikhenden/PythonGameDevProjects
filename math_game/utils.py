import random
import json
import os
from settings import LEVELS

SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")


# ---------------------------------------------------------------------------
# Save / Load
# ---------------------------------------------------------------------------

def load_save() -> dict:
    """Return save data dict. Creates a fresh one if file doesn't exist."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return _fresh_save()


def save_data(data: dict) -> None:
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _fresh_save() -> dict:
    return {
        "coins": 0,
        "total_correct": 0,
        "total_answered": 0,
    }


# ---------------------------------------------------------------------------
# Question generation
# ---------------------------------------------------------------------------

def generate_question(level: int) -> dict:
    """
    Generate a math question for the given level.
    Returns a dict with keys: 'text', 'answer', 'op'
    """
    cfg = LEVELS[level]
    ops = cfg["ops"]
    op  = random.choice(ops)

    if op == "+":
        a = random.randint(1, cfg["max_num"])
        b = random.randint(1, cfg["max_num"])
        answer = a + b
        text = f"{a} + {b}"

    elif op == "-":
        a = random.randint(1, cfg["max_num"])
        b = random.randint(1, a)        # b <= a so answer >= 0
        answer = a - b
        text = f"{a} - {b}"

    elif op == "*":
        table_max = cfg.get("tables_max", 5)
        a = random.randint(1, table_max)
        b = random.randint(1, table_max)
        answer = a * b
        text = f"{a} x {b}"

    elif op == "/":
        table_max = cfg.get("tables_max", 10)
        b = random.randint(1, table_max)
        answer = random.randint(1, table_max)
        a = answer * b                  # ensure clean integer division
        text = f"{a} / {b}"

    else:
        raise ValueError(f"Unknown op: {op}")

    return {"text": text, "answer": answer, "op": op}


def check_answer(question: dict, raw_input: str) -> bool:
    """Return True if raw_input matches the question's answer."""
    try:
        return int(raw_input.strip()) == question["answer"]
    except ValueError:
        return False
