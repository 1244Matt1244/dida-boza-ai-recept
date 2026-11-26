
"""
Testovi za besplatni Dida Boža AI pipeline.

Pokretanje:
    pytest tests/ -v
"""

import sys
from pathlib import Path

import pytest

# Omogućuje import modula iz glavnog direktorija projekta.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from generate_content import build_prompt, load_brand_voice


def test_build_prompt_contains_three_post_requirements():
    """Prompt mora tražiti tri Instagram objave."""
    prompt = build_prompt()

    assert "OBJAVA 1" in prompt
    assert "OBJAVA 2" in prompt
    assert "OBJAVA 3" in prompt
    assert "Dida Boža" in prompt


def test_build_prompt_contains_required_sections():
    """Prompt mora definirati strukturu objava."""
    prompt = build_prompt()

    assert "Vizualni prompt" in prompt
    assert "Tekst objave" in prompt
    assert "Hashtagovi" in prompt


def test_build_prompt_supports_custom_topic():
    """Prompt mora prihvatiti zadanu temu."""
    prompt = build_prompt(topic="Mediteranski doručak")

    assert "Mediteranski doručak" in prompt


def test_build_prompt_does_not_require_api():
    """Generiranje prompta ne smije zahtijevati API ključ."""
    prompt = build_prompt()

    assert isinstance(prompt, str)
    assert len(prompt) > 100
    assert "OpenAI API ključ" not in prompt


def test_load_brand_voice_returns_string():
    """Učitavanje tona brenda mora vratiti tekst."""
    content = load_brand_voice()

    assert isinstance(content, str)


def test_load_brand_voice_missing_file(tmp_path):
    """Nepostojeća datoteka s primjerima mora vratiti prazan tekst."""
    missing_file = tmp_path / "nepostojeci_primjeri.txt"

    content = load_brand_voice(missing_file)

    assert content == ""


def test_make_carousel_script_exists():
    """Skripta za izradu carousela mora postojati."""
    assert (BASE_DIR / "make_carousel.py").exists()


def test_run_all_script_exists():
    """Glavna pipeline skripta mora postojati."""
    assert (BASE_DIR / "run_all.py").exists()
