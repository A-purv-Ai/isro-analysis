"""Configuration module for ISRO Launch Scraper."""

from typing import Dict
from dataclasses import dataclass


@dataclass
class ScraperConfig:
    """Main configuration for the scraper application."""
    
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5
    INTER_SCRAPER_DELAY: int = 10
    
    HEADERS: Dict[str, str] = None
    
    def __post_init__(self):
        """Initialize headers after dataclass creation."""
        if self.HEADERS is None:
            self.HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }


WIKIPEDIA_URLS = {
    'pslv': 'https://en.wikipedia.org/wiki/List_of_PSLV_launches',
    'gslv': 'https://en.wikipedia.org/wiki/List_of_GSLV_launches',
    'lvm3': 'https://en.wikipedia.org/wiki/List_of_LVM3_launches'
}

EXPECTED_COUNTS = {
    'pslv': 64,
    'gslv': 18,
    'lvm3': 9
}

VALID_OUTCOMES = {
    'Success', 'Failure', 'Partial failure', 'Partial Failure',
    'Scheduled', 'Cancelled', 'Planned'
}

OUTPUT_DIR = 'output'
LOG_DIR = 'logs'
