"""HTML parsing utilities."""

from typing import Optional
from bs4 import Tag
import re


def clean_text(text: Optional[str]) -> Optional[str]:
    """Clean and normalize text from HTML."""
    if text is None:
        return None
    text = re.sub(r'\[\d+\]', '', text)
    text = ' '.join(text.split())
    text = text.strip()
    return text if text else None


def extract_cell_text(cell: Tag) -> Optional[str]:
    """Extract text from table cell."""
    if cell is None:
        return None
    text = cell.get_text(separator='\n', strip=True)
    return clean_text(text)


def is_remark_row(row: Tag) -> bool:
    """Check if row is a remarks row."""
    cells = row.find_all(['td', 'th'])
    if len(cells) == 1 and cells[0].has_attr('colspan'):
        return True
    return False
