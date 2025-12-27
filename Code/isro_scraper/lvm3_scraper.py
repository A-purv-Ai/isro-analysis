"""LVM3 Launch Scraper Module."""

import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Optional, Dict
import logging
from time import sleep

from .config import ScraperConfig, WIKIPEDIA_URLS
from .models import LVM3Launch
from .parsers import clean_text, extract_cell_text


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LVM3Scraper:
    """Scraper for LVM3 launch data from Wikipedia."""
    
    def __init__(self, config: Optional[ScraperConfig] = None):
        """Initialize LVM3 scraper with configuration."""
        self.config = config or ScraperConfig()
        self.launches: List[LVM3Launch] = []
        self.url = WIKIPEDIA_URLS['lvm3']
    
    def scrape(self) -> List[LVM3Launch]:
        """Scrape LVM3 launch data from Wikipedia."""
        self.launches = []
        
        for attempt in range(1, self.config.MAX_RETRIES + 1):
            try:
                logger.info(f"Fetching LVM3 data (attempt {attempt}/{self.config.MAX_RETRIES})")
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
        logger.info(f"Found {len(tables)} tables")
        
        for table_idx in [1, 2]:
            if table_idx < len(tables):
                self._parse_hierarchical_table(tables[table_idx], table_idx)
        
        logger.info(f"Scraped {len(self.launches)} LVM3 launches")
        return self.launches
    
    def _parse_hierarchical_table(self, table: Tag, table_idx: int) -> None:
        """Parse LVM3 hierarchical multi-row table structure."""
        rows = table.find_all('tr')
        current_launch = {}
        
        for row_idx, row in enumerate(rows[4:], start=4):
            cells = row.find_all('td')
            
            if len(cells) == 0:
                continue
            
            if len(cells) == 1 and cells[0].get('colspan'):
                if current_launch and current_launch.get('flight_number'):
                    status = current_launch.get('status', '')
                    if status == 'Success':
                        current_launch['remarks'] = extract_cell_text(cells[0])
                        try:
                            launch = LVM3Launch(**current_launch)
                            self.launches.append(launch)
                        except Exception as e:
                            logger.debug(f"Error creating launch: {e}")
                current_launch = {}
                continue
            
            if len(cells) == 5:
                if current_launch and current_launch.get('flight_number'):
                    status = current_launch.get('status', '')
                    if status == 'Success':
                        try:
                            launch = LVM3Launch(**current_launch)
                            self.launches.append(launch)
                        except Exception as e:
                            logger.debug(f"Error creating launch: {e}")
                current_launch = {}
                
                date_text = extract_cell_text(cells[0])
                payload_raw = extract_cell_text(cells[1])
                
                payload_name = payload_raw
                payload_mass = None
                
                if payload_raw and '\n' in payload_raw:
                    parts = payload_raw.split('\n')
                    payload_name = parts[0].strip()
                    if len(parts) > 1:
                        payload_mass = parts[1].strip()
                
                current_launch = {
                    'date_time_utc': date_text,
                    'payload': payload_name,
                    'payload_mass': payload_mass,
                    'launch_site': extract_cell_text(cells[2]),
                    'regime': extract_cell_text(cells[3]),
                    'status': extract_cell_text(cells[4]),
                    'flight_number': None,
                    'operator': None,
                    'function': None,
                    'remarks': None
                }
            
            elif len(cells) == 3 and current_launch:
                current_launch['flight_number'] = extract_cell_text(cells[0])
                current_launch['operator'] = extract_cell_text(cells[1])
                current_launch['function'] = extract_cell_text(cells[2])
        
        if current_launch and current_launch.get('flight_number'):
            status = current_launch.get('status', '')
            if status == 'Success':
                try:
                    launch = LVM3Launch(**current_launch)
                    self.launches.append(launch)
                except Exception as e:
                    logger.debug(f"Error creating final launch: {e}")
    
    def get_statistics(self) -> Dict[str, int]:
        """Calculate launch status statistics."""
        stats = {
            'total': len(self.launches),
            'success': 0,
            'failure': 0,
            'partial_failure': 0,
            'scheduled': 0,
            'unknown': 0
        }
        
        for launch in self.launches:
            status = launch.status
            if not status:
                stats['unknown'] += 1
            elif status == 'Success':
                stats['success'] += 1
            elif status == 'Failure':
                stats['failure'] += 1
            elif 'Partial' in status:
                stats['partial_failure'] += 1
            elif status in ['Scheduled', 'Planned']:
                stats['scheduled'] += 1
            else:
                stats['unknown'] += 1
        
        return stats
