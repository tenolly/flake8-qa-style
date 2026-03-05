from flake8_qa_style.checkers.raw_checkers._raw_checker import RawChecker
from flake8_qa_style.errors import NoBlankFileStart


class FileStartChecker(RawChecker):
    def check(self) -> None:
        if not self.lines:
            return

        if not self.lines[0].strip():
            self.errors.append(NoBlankFileStart(lineno=1, col_offset=0))
