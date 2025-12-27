"""Export utilities for launch data."""

import csv
import json
from typing import List, Union
from pathlib import Path
import logging

from .models import PSLVLaunch, GSLVLaunch, LVM3Launch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_to_csv(launches: List[Union[PSLVLaunch, GSLVLaunch, LVM3Launch]], filepath: str) -> None:
    """Export launch data to CSV file."""
    if not launches:
        logger.warning("No data to export")
        return
    
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(launches[0].model_dump().keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for launch in launches:
            writer.writerow(launch.model_dump())
    
    logger.info(f"Exported {len(launches)} records to {filepath}")


def export_to_json(launches: List[Union[PSLVLaunch, GSLVLaunch, LVM3Launch]], filepath: str) -> None:
    """Export launch data to JSON file."""
    if not launches:
        logger.warning("No data to export")
        return
    
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    outcomes = {}
    for launch in launches:
        if hasattr(launch, 'launch_outcome'):
            outcome = launch.launch_outcome or 'Unknown'
        elif hasattr(launch, 'status'):
            outcome = launch.status or 'Unknown'
        else:
            outcome = 'Unknown'
        
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    
    data = {
        'metadata': {
            'total_launches': len(launches),
            'outcomes': outcomes
        },
        'launches': [launch.model_dump() for launch in launches]
    }
    
    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    logger.info(f"Exported {len(launches)} records to {filepath}")
