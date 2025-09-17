from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class QuickstartReport:
    success: bool
    sections: List[str]
    total_checks: int


class QuickstartValidator:
    def __init__(self, markdown: str) -> None:
        self.markdown = markdown

    @classmethod
    def from_markdown(cls, markdown: str) -> "QuickstartValidator":
        return cls(markdown=markdown)

    def validate(self) -> QuickstartReport:
        raw_sections = re.findall(r"^###\s+([^\n]+)", self.markdown, flags=re.MULTILINE)
        sections = [re.sub(r"^\d+\.\s*", "", section) for section in raw_sections]
        total_checks = sum(1 for line in self.markdown.splitlines() if line.strip().startswith("- ✅"))
        success = bool(sections) and total_checks >= 3
        return QuickstartReport(success=success, sections=sections, total_checks=total_checks)


__all__ = ["QuickstartValidator", "QuickstartReport"]
