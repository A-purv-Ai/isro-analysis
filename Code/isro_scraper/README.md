# ISRO Launch Scraper

Python package for scraping ISRO rocket launch history data from Wikipedia.

## 1. Author
Apurva Upadhyay - IIT Ropar, Minor in AI

## 2. Overview
This package scrapes historical launch data for three ISRO launch vehicles:
- PSLV (Polar Satellite Launch Vehicle) - 64 launches
- GSLV (Geosynchronous Satellite Launch Vehicle) - 18 launches  
- LVM3 (Launch Vehicle Mark-3) - 9 launches

Total dataset: 91 missions from 1993 to 2025

## 3. Installation

```bash
pip install -r requirements.txt
```
## 4. Usage
### 4.1 Basic Scraping

```python
from isro_scraper import PSLVScraper, GSLVScraper, LVM3Scraper
from isro_scraper.exporters import export_to_csv

# Scrape PSLV launches
scraper = PSLVScraper()
launches = scraper.scrape()

# Export to CSV
export_to_csv(launches, 'pslv_launches.csv')

# Get statistics
stats = scraper.get_statistics()
print(f"Success rate: {stats['success']/stats['total']*100:.1f}%")
```
### 4.2 Scrape All Rockets

```python
from isro_scraper import PSLVScraper, GSLVScraper, LVM3Scraper
from isro_scraper.exporters import export_to_csv

scrapers = {
    'pslv': PSLVScraper(),
    'gslv': GSLVScraper(),
    'lvm3': LVM3Scraper()
}

for rocket_name, scraper in scrapers.items():
    launches = scraper.scrape()
    export_to_csv(launches, f'{rocket_name}_launches.csv')
    print(f"{rocket_name.upper()}: {len(launches)} launches")
```
## 5. Package Structure
```
isro_scraper/
├── __init__.py          - Package initialization
├── config.py            - Configuration and HTTP headers
├── models.py            - Pydantic data models
├── parsers.py           - HTML parsing utilities
├── exporters.py         - CSV/JSON export functions
├── pslv_scraper.py      - PSLV scraper
├── gslv_scraper.py      - GSLV scraper
├── lvm3_scraper.py      - LVM3 scraper (hierarchical tables)
├── requirements.txt     - Dependencies
└── README.md            - This file
```

## 6. Data Models
### 6.1 PSLV/GSLV Launch
- flight_number
- date_time_utc
- rocket_configuration
- launch_site
- payload
- payload_mass
- orbit
- user
- launch_outcome
- remarks

### 6.2 LVM3 Launch
- flight_number
- date_time_utc
- launch_site
- payload
- payload_mass
- regime (orbital regime)
- operator
- function
- status
- remarks

## 7. Features
- Automatic retry with exponential backoff
- Wikipedia-compliant HTTP headers
- HTML table parsing with rowspan/colspan handling
- Flat table support (PSLV/GSLV)
- Hierarchical multi-row table support (LVM3)
- Citation removal from Wikipedia text
- Data validation with Pydantic
- CSV and JSON export

## 8. Notes
- Respects Wikipedia's robot policy with delays
- Uses proper User-Agent headers
- Handles multi-payload missions
- Filters out planned/scheduled missions (LVM3)
- Extracts flight numbers from rowheader elements

## 9. Data Sources
- PSLV: https://en.wikipedia.org/wiki/List_of_PSLV_launches
- GSLV: https://en.wikipedia.org/wiki/List_of_GSLV_launches
- LVM3: https://en.wikipedia.org/wiki/List_of_LVM3_launches

## 10. License
For academic use - IIT Ropar Minor in AI Final Project

## 11. Project Context
This scraper is part of a larger machine learning project to predict ISRO launch success probability using Random Forest classification.

## 12. Acknowledgements
- Wikipedia contributors for launch data
