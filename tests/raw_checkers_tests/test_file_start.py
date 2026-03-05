from flake8_qa_style.checkers.raw_checkers import FileStartChecker
from flake8_qa_style.errors import NoBlankFileStart


def test_empty_file() -> None:
    checker = FileStartChecker(None, [])
    checker.check()
    assert len(checker.errors) == 0


def test_file_with_blank_line() -> None:
    checker = FileStartChecker(None, ["\n"])
    checker.check()
    assert len(checker.errors) == 1
    assert isinstance(checker.errors[0], NoBlankFileStart)


def test_file_without_blank_line() -> None:
    checker = FileStartChecker(None, ["print('Hello world')"])
    checker.check()
    assert len(checker.errors) == 0
