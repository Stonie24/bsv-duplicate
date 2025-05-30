import pytest
from unittest.mock import patch
from src.util.detector import detect_duplicates, Article

@pytest.fixture
def sut():
    with patch("src.util.detector.parse", autospec=True) as mock_parse:
        yield mock_parse

@pytest.mark.unit
class TestDetectDuplicates:

    def test_duplicate_key_and_doi_returns_one_result(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc"),
            Article(key="ref1", doi="10.1000/abc")
        ]

        result = detect_duplicates("mocked input")

        assert len(result) == 1

    def test_duplicate_key_and_doi_content(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc"),
            Article(key="ref1", doi="10.1000/abc")
        ]

        result = detect_duplicates("mocked input")

        assert result[0] == Article(key="ref1", doi="10.1000/abc")

    def test_same_key_no_doi_detects_duplicate(self, sut):
        sut.return_value = [
            Article(key="ref1", doi=None),
            Article(key="ref1", doi=None)
        ]

        result = detect_duplicates("mocked input")

        assert len(result) == 1

    def test_different_key_same_doi_not_duplicate(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc"),
            Article(key="ref2", doi="10.1000/abc")
        ]

        result = detect_duplicates("mocked input")

        assert result == []

    def test_different_key_and_doi_not_duplicate(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc"),
            Article(key="ref2", doi="10.1000/xyz")
        ]

        result = detect_duplicates("mocked input")

        assert result == []

    def test_one_missing_doi_same_key_detects_duplicate(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc"),
            Article(key="ref1", doi=None)
        ]

        result = detect_duplicates("mocked input")

        assert len(result) == 1

    def test_less_than_two_articles_raises_error(self, sut):
        sut.return_value = [
            Article(key="ref1", doi="10.1000/abc")
        ]

        with pytest.raises(ValueError):
            detect_duplicates("mocked input")
