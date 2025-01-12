# NSF Awards Downloader

A Tkinter-based GUI application to download National Science Foundation (NSF) award data. Select specific years and download data in CSV and JSON formats, organized into year-specific folders.

## Features

- **GUI Year Selection**: Simple interface with checkboxes for years 2010-present
- **Organized Output**: Data saved in year-specific folders (`awards_<year>/`)
- **Multiple Formats**: Creates both CSV and JSON files for each year
- **Automatic Pagination**: Fetches data in chunks of 25 records
- **Progress Tracking**: Real-time progress and debug information display
- **Data Validation**: Warns if no records are found for selected years

## Requirements

- Python 3.7+ (3.6 compatible but not recommended)
- Tkinter (included with most Python installations)
  - Debian/Ubuntu: `sudo apt-get install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`
- Requests library: `pip install requests`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nsf-awards-downloader.git
   cd nsf-awards-downloader
   ```

2. Install dependencies:
   ```bash
   pip install requests
   ```

## Usage

1. Run the script:
   ```bash
   python nsf_awards_downloader.py
   ```

2. Select desired years using the checkboxes
3. Click "Download" to begin data retrieval
4. Monitor progress in the on-screen log
5. Find output files in `awards_<year>/` folders

## Data Fields

The following fields are extracted for each award:

| Field | Description |
|-------|-------------|
| `id` | Unique award identifier |
| `agency` | Awarding agency (typically "NSF") |
| `awardeeName` | Recipient institution/entity |
| `title` | Project title |
| `abstractText` | Project description |
| `fundsObligatedAmt` | Current obligated funds |
| `estimatedTotalAmt` | Estimated total award amount |
| `pdPIName` | Project Director/Principal Investigator |
| `coPDPI` | Co-Principal Investigators |
| `poName` | NSF Program Officer |
| `startDate` | Award start date |
| `expDate` | Award expiration date |
| `primaryProgram` | Primary NSF funding program |

## File Structure
Each year's data is saved in a separate folder with the following structure:
awards_2023/
├── 2023_awards.csv      # CSV file containing all awards for 2023
└── 2023_awards.json     # JSON file containing same data in JSON format

awards_2022/ 
├── 2022_awards.csv      # CSV file containing all awards for 2022  
└── 2022_awards.json     # JSON file containing same data in JSON format

etc...

## Limitations

- No specified API rate limits, but large downloads may require additional delay
- Fixed pagination of 25 records per request (NSF API maximum)
- Full-year searches only (Jan 1 - Dec 31)
- Empty files created for years with no awards
- Uses only public NSF data
- Tested primarily on Python 3.7+ (Windows)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
