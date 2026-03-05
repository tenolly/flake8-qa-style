import textwrap

from flake8_qa_style.checkers.raw_checkers import WithChecker
from flake8_qa_style.errors import BackslashWith


def _perform_with_checker(code: str) -> WithChecker:
    lines = textwrap.dedent(code).splitlines(True)
    checker = WithChecker(lines=lines)
    checker.check()
    return checker


def test_backslash_with():
    code = """\
    with open('a'),\\
        open('b'):
        pass
    """
    checker = _perform_with_checker(code)
    assert len(checker.errors) == 1
    assert isinstance(checker.errors[0], BackslashWith)


def test_empty_line_between_backslash_with():
    code = """\
    with open('a'),\\
    
        open('b'):
        pass
    """
    checker = _perform_with_checker(code)
    assert len(checker.errors) == 1
    assert isinstance(checker.errors[0], BackslashWith)


def test_another_line_backslash_with():
    code = """\
    with open(
        'a'),\\
        open('b'):
        pass
    """
    checker = _perform_with_checker(code)
    assert len(checker.errors) == 1
    assert isinstance(checker.errors[0], BackslashWith)


def test_no_backslash_with_parenthesized():
    code = """\
    with (
        open('a'),
        open('b'),
    ):
        pass
    """
    checker = _perform_with_checker(code)
    assert len(checker.errors) == 0


def test_single_line_with_no_backslash():
    code = """\
    with open('a'):
        pass
    """
    checker = _perform_with_checker(code)
    assert len(checker.errors) == 0
