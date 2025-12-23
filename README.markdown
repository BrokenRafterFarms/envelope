# Envelope Generator

## Overview

This script generates PDF envelopes with a return address and recipient addresses. It reads recipient addresses from a CSV file and creates a centered layout suitable for printing on standard envelope stock.

## Features

- **Return Address**: Loaded from `Home.csv`, positioned in the top-left corner
- **Recipient Address**: Centered both horizontally and vertically on the page
- **Flexible CSV Format**: Supports addresses with optional second street line
- **File Picker UI**: Interactive file selection dialog for choosing the recipient CSV file
- **Customizable Fonts & Sizing**: Configurable via top-level constants
- **No External Dependencies**: Uses only pure Python libraries (fpdf2, csv, tkinter)

## Setup

### Requirements

- Python 3.6+
- fpdf2
- tkinter (usually included with Python)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/BrokenRafterFarms/envelope.git
cd envelope
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install fpdf2
```

## Usage

### Create Input Files

#### Home.csv (Return Address)
Create a file named `Home.csv` with your return address in the following format:
```
Name,Street Address Line 1,Street Address Line 2,City,State,Code
The Franzen Family,123 Main St,,San Francisco,CA,94110
```

#### address.csv (Recipient Addresses)
Create a file named `address.csv` with recipient addresses:
```
Name,Street Address Line 1,Street Address Line 2,City,State,Code
John Doe,456 Oak Ave,Apt 2B,Springfield,IL,62701
```

### Run the Script

```bash
python envelope.py
```

A file picker dialog will appear. Select your `address.csv` file containing recipient addresses. The script will generate `Processed_Addresses.pdf` with one envelope per address.

## Configuration

All configurable constants are at the top of `envelope.py`:

```python
# Page dimensions (in inches)
PAGE_WIDTH_IN = 7.2
PAGE_HEIGHT_IN = 5.25

# Fonts
FONT_FACE = 'Times'                    # Recipient address font
FONT_FACE_RETURN_NAME = 'Times'        # Return address name font
FONT_SIZE_RETURN_NAME = 11
FONT_SIZE_OTHER = 11

# Positioning
MARGIN_IN = 0.25                       # Return address left margin
LINE_HEIGHT_PT = 12                    # Line height in points

# I/O
INFILE = 'address.csv'                 # Default recipient file
OUTFILE = 'Processed_Addresses.pdf'    # Output PDF filename
```

## CSV Format Notes

- **Street Address Line 2** can be left empty (will not appear on envelope)
- **City, State, Code**: If the city field is empty, this entire line is omitted
- The script skips the header row automatically
- Rows with fewer than 6 columns are skipped

## Output

The generated PDF will have:
- One page per recipient address
- Standard envelope dimensions (7.2" × 5.25")
- Return address in top-left corner
- Recipient address centered on the page



