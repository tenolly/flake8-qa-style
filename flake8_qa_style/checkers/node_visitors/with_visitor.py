import ast

from flake8_qa_style.checkers.node_visitors._node_visitor import NodeVisitor
from flake8_qa_style.errors import NestedWith


class WithVisitor(NodeVisitor):

    def _check_nested_with(self, node: ast.With | ast.AsyncWith) -> None:
        is_async = isinstance(node, ast.AsyncWith)

        # Check for nested "with" of the same type (sync-in-sync or async-in-async)
        if len(node.body) == 1:
            inner = node.body[0]
            if is_async and isinstance(inner, ast.AsyncWith):
                self.error_from_node(NestedWith, node)
            elif not is_async and isinstance(inner, ast.With):
                self.error_from_node(NestedWith, node)

    def visit_With(self, node: ast.With) -> None:
        self._check_nested_with(node)
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self._check_nested_with(node)
        self.generic_visit(node)
