import re

from flake8_qa_style.checkers.raw_checkers._raw_checker import RawChecker
from flake8_qa_style.errors import BackslashWith

_WITH_START_RE = re.compile(r'^(\s*)(async\s+)?with\s+')
_BACKSLASH_RE = re.compile(r'\\\s*$')
_COLON_END_RE = re.compile(r':\s*$')


class WithChecker(RawChecker):
    def check(self) -> None:
        i = 0
        while i < len(self.lines):
            line = self.lines[i].rstrip()

            match = _WITH_START_RE.match(line)
            if not match:
                i += 1
                continue

            backslashes = []
            while i < len(self.lines):
                current_line_text = self.lines[i]

                backslash_match = _BACKSLASH_RE.search(current_line_text)
                if backslash_match:
                    backslashes.append((i, backslash_match.start()))

                if _COLON_END_RE.search(current_line_text):
                    break

                i += 1

            for backslash in backslashes:
                self.errors.append(BackslashWith(lineno=backslash[0] + 1, col_offset=backslash[1]))

            i += 1
