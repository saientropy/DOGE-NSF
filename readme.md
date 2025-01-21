# NSF Research Awards Analysis Suite to detect abstract fraud.

Abstract fraud is often decided based on the observation that some researchers fill their abstracts with "word salad"—a jumble of buzzwords and jargon that sounds impressive but ultimately means nothing. This tactic is used to impress reviewers and secure funding for research that is often incremental and has little to no real impact.

The goal of this analysis suite is to uncover how science funding is allocated to projects that may not contribute significantly to the advancement of knowledge or societal benefit. By analyzing award abstracts for specific keywords and patterns, we aim to identify instances where funding may be going to research that lacks substance or genuine innovation.

This is just the beginning of the process to shed light on the allocation of science funding and to challenge the status quo of how research proposals are evaluated.

**While some awards may emerge during the analysis as genuinely deserving of public funds, they are certainly not the majority. The goal of this process is not merely to separate the wheat from the chaff but to critically evaluate whether public funding of science is necessary in the first place.
**

A comprehensive toolkit for downloading and analyzing National Science Foundation (NSF) research awards data. This suite includes three main tools:
1. NSF Awards Downloader - Download award data by year
2. Red Flag Analyzer - Analyze award abstracts for specific keywords and patterns
3. NSF Awards Analysis Suite - Download award data and analyze abstracts for keywords in one integrated tool

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
- **Detailed Views**: Double-click to view full abstract text with highlighted red flag words
- **CSV Import**: Compatible with NSF Awards Downloader output

### NSF Awards Analysis Suite
- **Integrated Functionality**: Combines downloading and analyzing award data in one tool
- **User-Friendly Interface**: Simplifies the process of fetching and analyzing data
- **Real-Time Results**: View results and insights immediately after analysis
- **Highlighting Red Flags**: Automatically highlights keywords in abstracts for easy identification

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nsf-awards-analysis.git
   cd nsf-awards-analysis
   ```

2. Install required dependencies:
   ```bash
   pip install requests pandas customtkinter fpdf
   ```

3. For Linux users, install Tkinter if not included:
   ```bash
   # Debian/Ubuntu
   sudo apt-get install python3-tk

   # Fedora
   sudo dnf install python3-tkinter
   ```

## Usage

1. Run the application:
   ```bash
   python nsf.py
   ```

2. Select the desired year using the GUI.
3. Choose any red flag keywords you want to analyze.
4. Click the "Analyze" button to fetch and analyze the data.
5. Review the results displayed in the GUI, with red flag words highlighted in the abstracts.
6. Generate a report by clicking the "Generate Report" button after analysis.

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
├── 2023_awards.json

awards_2022/
├── 2022_awards.json
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
- JSON format must match NSF Awards Downloader output
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
