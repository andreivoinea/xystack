import pytest

from paginate import get_page, page_count


def test_page_count_rounds_up():
    assert page_count(11, 5) == 3


def test_page_count_exact_fit():
    assert page_count(10, 5) == 2


def test_get_page_rejects_page_zero():
    with pytest.raises(ValueError):
        get_page([1, 2, 3], 0, 2)
