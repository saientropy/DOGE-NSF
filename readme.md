# NSF Research Awards Analysis Suite to detect abstract fraud.

A comprehensive toolkit for downloading and analyzing National Science Foundation (NSF) research awards data. This suite includes two main tools:
1. NSF Awards Downloader - Download award data by year
2. Red Flag Analyzer - Analyze award abstracts for specific keywords and patterns

## Features

### NSF Awards Downloader
- **Year Selection**: GUI interface for selecting years (2010-present)
- **Automated Data Retrieval**: Handles pagination and API requests automatically
- **Multi-format Export**: Saves data in both CSV and JSON formats
- **Progress Tracking**: Real-time download status and debugging information
- **Organized Storage**: Creates year-specific folders for downloaded data

### Red Flag Analyzer
- **Keyword Analysis**: Search through award abstracts using predefined or custom keywords
- **Financial Insights**: Calculate total funding for filtered results
- **Interactive UI**: Quick-add buttons for common red flag terms
- **Detailed Views**: Double-click to view full abstract text
- **CSV Import**: Compatible with NSF Awards Downloader output

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nsf-awards-analysis.git
   cd nsf-awards-analysis
   ```

2. Install required dependencies:
   ```bash
   pip install requests pandas tkinter
   ```

3. For Linux users, install Tkinter if not included:
   ```bash
   # Debian/Ubuntu
   sudo apt-get install python3-tk

   # Fedora
   sudo dnf install python3-tkinter
   ```

## Usage

### NSF Awards Downloader
1. Run the downloader:
   ```bash
   python nsf_data_extractor.py
   ```
2. Select desired years using checkboxes
3. Click "Download" to begin
4. Monitor progress in the status window
5. Find downloaded data in `awards_<year>/` folders

### Red Flag Analyzer
1. Run the analyzer:
   ```bash
   python redflag-detector.py
   ```
2. Click "Upload CSV" to load award data
3. Use predefined red flag buttons or enter custom keywords
4. View filtered results and funding totals
5. Double-click any entry to view full abstract

## Data Structure

### Downloaded Award Fields
- Award ID
- Agency
- Awardee Name
- Project Title
- Abstract Text
- Obligated Funds
- Estimated Total Amount
- PI/PD Name
- Co-PIs
- Program Officer
- Start/End Dates
- Primary Program

### File Organization
```
awards_2023/
├── 2023_awards.csv
└── 2023_awards.json

awards_2022/
├── 2022_awards.csv
└── 2022_awards.json
```

## Predefined Red Flag Terms
The analyzer includes common terms often found in grant proposals, including:
- Innovation-related: "innovative", "cutting-edge", "revolutionary"
- Impact-related: "transformative", "game-changing", "scalable"
- DEI-related: "diversity", "equity", "inclusion"
- Methodology: "framework", "empirical", "methodology"

## Limitations

### NSF Awards Downloader
- Fixed 25 records per API request (NSF limitation)
- Full-year downloads only (Jan 1 - Dec 31)
- No specified API rate limits

### Red Flag Analyzer
- CSV format must match NSF Awards Downloader output
- Text search is case-insensitive but exact match only
- Memory usage increases with larger datasets

## Requirements
- Python 3.7+
- Tkinter (GUI library)
- Pandas (data processing)
- Requests (API calls)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
