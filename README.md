## Description
One part of this project contains code to scrape SSSB.se queue data every 
few minutes and save it to a csv files.
The programme automatically creates a new directory for every SSSB round (who begin/end every Monday and Thursday). 
New data, that is a new .csv file will only be created if the data has changed.
The name of the file will be an encoded timestamp.

The other part of this project contains code to analyze any (scraped) data sequence.
It will generate a new csv file with the estimated data queue structure. 

### Factors that affect accuracy
- Integrity: The snapshots provided to the analyzer covers the whole SSSB round (lasting either 3 or 4 days)
- Resolution: The snapshots provided to the analyzer are taken with minimal interval. Usually a few minutes are optimal 


### Data collected by Scraper
- Max Queue days
- Number of applicants
- Address of object
- Type of housing
- Moving in date
- Apartment/room size
- Rent

## Usage
### Scraper
1. Install dependencies with `pip3 install -r requirements.txt`
2. Run `python3 main.py <output_directory>` in terminal 

The scraper will run indefinedly, scraping data every x minutes. Run the analyzer after the next SSSB round has ended.

### Analyzer
1. Install dependencies with `pip3 install -r requirements.txt`
2. Run `python3 analyzer.py <input_directory>` in terminal 

The analyzer will generate a new csv file in the same directory as the input directory. 
The name of the file will be the same as the input directory, but with the suffix `_analyzed`