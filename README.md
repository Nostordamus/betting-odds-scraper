# betting-odds-scrapper

This Python program scrapes football match odds from a Pinnacle website and stores them in a text file. It is solely for demonstration purposes unless someone wants to transform it into full solution.

## Features

- **Web Scraping:** The program utilizes web scraping (reverse engineeringr) techniques to extract football match odds from a target website (Pinnacle).
- **Data Extraction:** It extracts data such as match details, team names, and corresponding odds (e.g., home team win, draw, away team win, etc).
- **Text File Storage:** The program saves the scraped odds data in a text file for further analysis or usage.

## Requirements

- Python 3.x
- Requests library: To make HTTP requests and fetch web page data. (Install via 'pip install requests')

## Usage

1. Clone this repository: `git clone https://github.com/your-username/football-odds-scraper.git`
2. Install the required dependencies: `pip install requests`
4. Run the program: `python pinnacle.py`
5. The program will scrape the football match odds and store them in a text file. (Root directory -> folder: Scraped)
6. Open the generated text file to view the scraped odds data.

## Customize and Extend

You can customize and extend the program according to your specific needs:

- Modify the web scraping code to target a different website or extract additional data.
- Implement data processing or analysis functions on the scraped odds data.
- Integrate the program into a larger system or pipeline for further automation.

## Disclaimer

Please note that web scraping may have legal and ethical considerations. Ensure that you comply with the website's terms of service and data usage policies. Additionally, be respectful of the website's resources and do not overwhelm their servers with excessive requests.
