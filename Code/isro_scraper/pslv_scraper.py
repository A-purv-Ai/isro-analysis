"""PSLV Launch Scraper Module."""

import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Optional, Dict
import logging
from time import sleep

from .config import ScraperConfig, WIKIPEDIA_URLS
from .models import PSLVLaunch
from .parsers import clean_text, extract_cell_text, is_remark_row


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PSLVScraper:
    """Scraper for PSLV launch data from Wikipedia."""
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """Initialize PSLV scraper with configuration."""
        self.config = config or ScraperConfig()
        self.launches: List[PSLVLaunch] = []
        self.url = WIKIPEDIA_URLS['pslv']
    
    def scrape(self) -> List[PSLVLaunch]:
        """Scrape PSLV launch data from Wikipedia."""
        self.launches = []
        
        for attempt in range(1, self.config.MAX_RETRIES + 1):
            try:
                logger.info(f"Fetching PSLV data (attempt {attempt}/{self.config.MAX_RETRIES})")
                response = requests.get(
                    self.url,
                    headers=self.config.HEADERS,
                    timeout=self.config.REQUEST_TIMEOUT
                )
                response.raise_for_status()
                logger.info(f"Successfully fetched page ({len(response.text):,} bytes)")
                break
            except requests.exceptions.RequestException as e:
                if attempt == self.config.MAX_RETRIES:
                    logger.error(f"Failed to fetch after {self.config.MAX_RETRIES} attempts: {e}")
                    raise
                logger.warning(f"Attempt {attempt} failed, retrying in {self.config.RETRY_DELAY}s...")
                sleep(self.config.RETRY_DELAY)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', class_='wikitable')
        logger.info(f"Found {len(tables)} launch tables")
        
        for table_idx, table in enumerate(tables):
            self._parse_table(table, table_idx)
        
        logger.info(f"Scraped {len(self.launches)} PSLV launches")
        return self.launches
    
    def _parse_table(self, table: Tag, table_idx: int) -> None:
        """Parse a single PSLV launch table."""
        rows = table.find_all('tr')
        
        for row_idx, row in enumerate(rows[2:], start=2):
            if is_remark_row(row):
                if self.launches:
                    remark_text = extract_cell_text(row.find('td'))
                    if remark_text:
                        self.launches[-1].remarks = remark_text
                continue
            
            cells = row.find_all('td')
            if len(cells) < 8:
                continue
            
            flight_th = row.find('th')
            flight_number = extract_cell_text(flight_th) if flight_th else None
            
            if not flight_number:
                continue
            
            try:
                launch = PSLVLaunch(
                    flight_number=flight_number,
                    date_time_utc=extract_cell_text(cells[0]),
                    rocket_configuration=extract_cell_text(cells[1]),
                    launch_site=extract_cell_text(cells[2]),
                    payload=extract_cell_text(cells[3]),
                    payload_mass=extract_cell_text(cells[4]),
                    orbit=extract_cell_text(cells[5]) or None,
                    user=extract_cell_text(cells[6]) or None,
                    launch_outcome=extract_cell_text(cells[7]) if len(cells) > 7 else None,
                    remarks=None
                )
                self.launches.append(launch)
            except (IndexError, ValueError) as e:
                logger.debug(f"Error parsing row {row_idx}: {e}")
                continue
    
    def get_statistics(self) -> Dict[str, int]:
        """Calculate launch outcome statistics."""
        stats = {
            'total': len(self.launches),
            'success': 0,
            'failure': 0,
            'partial_failure': 0,
            'scheduled': 0,
            'unknown': 0
        }
        
        for launch in self.launches:
            outcome = launch.launch_outcome
            if not outcome:
                stats['unknown'] += 1
            elif outcome == 'Success':
                stats['success'] += 1
            elif outcome == 'Failure':
                stats['failure'] += 1
            elif 'Partial' in outcome:
                stats['partial_failure'] += 1
            elif outcome == 'Scheduled':
                stats['scheduled'] += 1
            else:
                stats['unknown'] += 1
        
        return stats
