"""
Testovi za generate_content.py i make_carousel.py.

Pokretanje:
    pip install pytest
    pytest tests/ -v
"""

import os
import sys
import tempfile
import pytest

# Dodaj root u path da možemo importati module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generate_content import get_mock_content, save_content


def test_get_mock_content_returns_three_posts():
    """get_mock_content() mora vratiti tri objave s ispravnom strukturom."""
    content = get_mock_content()
    assert "OBJAVA 1" in content
    assert "OBJAVA 2" in content
    assert "OBJAVA 3" in content
    # Svaka objava mora imati vizualni prompt, tekst i hashtagove
    assert content.count("Vizualni prompt:") == 3
    assert content.count("Tekst objave:") == 3
    assert content.count("Hashtagovi:") == 3


def test_get_mock_content_has_croatian_characters():
    """Mock sadržaj mora sadržavati hrvatske znakove i emoji."""
    content = get_mock_content()
    assert "Boža" in content
    assert "džem" in content
    assert "🍯" in content or "🧀" in content


def test_generate_with_api_signature():
    """generate_with_api mora prihvatiti sve parametre (bez poziva API-ja)."""
    from generate_content import generate_with_api
    import inspect

    sig = inspect.signature(generate_with_api)
    params = list(sig.parameters.keys())
    assert "client" in params
    assert "proizvod" in params
    assert "cilj" in params
    assert "ton" in params
    assert "publika" in params
    assert "web_stranica" in params
    assert "inspiracija" in params


def test_save_content_creates_file():
    """save_content mora spremiti datoteku u output/."""
    test_content = "TEST OBJAVA\nOvo je test."
    save_content(test_content)

    assert os.path.exists("output/generirani_sadrzaj.txt")
    with open("output/generirani_sadrzaj.txt", "r", encoding="utf-8") as f:
        saved = f.read()
    assert saved == test_content

    # Cleanup
    os.remove("output/generirani_sadrzaj.txt")


def test_make_carousel_script_exists():
    """make_carousel.py mora postojati u rootu."""
    assert os.path.exists("make_carousel.py")