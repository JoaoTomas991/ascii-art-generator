"""
Persistence for words the user has taught the ENCommandParser at runtime
(e.g. new mood synonyms), so they survive across sessions.
"""

import json
from pathlib import Path
from typing import Dict

LEARNED_WORDS_PATH = Path.home() / ".config" / "ascii_generator" / "learned_words.json"


def _read() -> dict:
    try:
        return json.loads(LEARNED_WORDS_PATH.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def load_learned_moods() -> Dict[str, str]:
    """Return {synonym: canonical_mood} taught by the user in past sessions."""
    moods = _read().get('moods', {})
    if not isinstance(moods, dict):
        return {}
    return {k: v for k, v in moods.items() if isinstance(k, str) and isinstance(v, str)}


def save_learned_mood(word: str, canonical: str) -> None:
    """Persist a new word -> canonical mood mapping, merging with existing entries."""
    LEARNED_WORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = _read()
    data.setdefault('moods', {})[word] = canonical
    LEARNED_WORDS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
