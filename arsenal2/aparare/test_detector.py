from collections import Counter

from detector import suspecti
import pytest


def test_pragul_taie():

    c = Counter({
        "a": 13,
        "b": 2
    })

    assert suspecti(c, 10) == [("a", 13)]


def test_prag_invalid():


    with pytest.raises(ValueError):
        suspecti({}, 0)