import ast
import textwrap
from typing import Any, Optional, Type

from flake8_plugin_utils.plugin import Error, TConfig, Visitor


def _errors_from_src(
    visitor_cls: Type[Visitor[TConfig]],
    src: str,
    config: Optional[TConfig] = None
) -> Optional[list[Error]]:
    visitor = visitor_cls(config=config)
    tree = ast.parse(textwrap.dedent(src))
    visitor.visit(tree)

    if not visitor.errors:
        return None

    return visitor.errors


def assert_errors(
    visitor_cls: Type[Visitor[TConfig]],
    src: str,
    expected: list[Type[Error]],
    config: Optional[TConfig] = None,
    **kwargs: Any,
) -> None:
    errors = _errors_from_src(visitor_cls, src, config=config)
    assert errors, f'Errors "{errors}" not found in\n{src}'
    assert len(errors) == len(expected)

    for error, expected_error in zip(errors, expected):
        assert isinstance(error, expected_error)

        expected_message = expected_error.formatted_message(**kwargs)
        assert expected_message == error.message, (
            f'Expected error with message "{expected_message}", got "{error.message}"'
        )
