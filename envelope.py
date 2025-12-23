#!/usr/bin/python

from fpdf import FPDF
import csv
from tkinter import filedialog
import tkinter as tk
import os
import sys


INCHES_TO_POINTS = 72

# --- Configurable constants ---
PAGE_WIDTH_IN = 7.2
PAGE_HEIGHT_IN = 5.25
FONT_FACE = 'Times'
FONT_FACE_RETURN_NAME = 'Times'
FONT_SIZE_RETURN_NAME = 11
FONT_SIZE_OTHER = 11
MARGIN_IN = 0.25
LINE_HEIGHT_PT = 12

# I/O and default from-address (moved here so they're easy to edit)
# Used File From: 
INFILE = 'address.csv'
OUTFILE = 'Processed_Addresses.pdf'
FROM_ADDR = ('The Franzen Family',
             '[elided]',
             'San Francisco, CA 94110')


def write_envelopes(out, from_addr, to_addrs):
    pdf = FPDF(
        format=(PAGE_WIDTH_IN, PAGE_HEIGHT_IN),
        unit='in',
        orientation='P'
    )
    
    for to_addr in to_addrs:
        pdf.add_page()
        
        # from address (left-aligned at margin)
        for i, line in enumerate(from_addr):
            if i == 0:
                pdf.set_font(FONT_FACE_RETURN_NAME, size=FONT_SIZE_RETURN_NAME)
            else:
                pdf.set_font(FONT_FACE, size=FONT_SIZE_OTHER)
            
            y_pos = MARGIN_IN + (LINE_HEIGHT_PT / 72) * i
            pdf.set_y(y_pos)
            pdf.set_x(MARGIN_IN)
            pdf.cell(0, 0, line)
        
        # to address (centered horizontally and vertically)
        pdf.set_font(FONT_FACE, size=FONT_SIZE_OTHER)
        
        # Calculate vertical centering: center of page minus half the height of all address lines
        address_height = len(to_addr) * (LINE_HEIGHT_PT / 72)
        center_y = (PAGE_HEIGHT_IN / 2) - (address_height / 2)
        
        for i, line in enumerate(to_addr):
            y_pos = center_y + (LINE_HEIGHT_PT / 72) * i
            pdf.set_y(y_pos)
            pdf.cell(PAGE_WIDTH_IN, 0, line, align='C')
    
    pdf.output(out)


def load_csv(filename):
    # Parse CSV with columns: Name, Street Address Line 1, Street Address Line 2, City, State, Code
    # Returns formatted address lines: [Name, Street Line 1, Street Line 2 (if present), City State Code]
    with open(filename) as f:
        for i, row in enumerate(csv.reader(f)):
            if i == 0:  # Skip header row
                continue

            if len(row) < 6:
                continue  # Skip incomplete rows

            name = row[0].strip()
            street1 = row[1].strip()
            street2 = row[2].strip()
            city = row[3].strip()
            state = row[4].strip()
            code = row[5].strip()

            # Build address lines, excluding empty street2
            addr_lines = [name, street1]
            if street2:
                addr_lines.append(street2)
            
            # Add city, state, code line only if city is not empty
            if city:
                addr_lines.append(f"{city}, {state} {code}".strip())

            yield addr_lines


def select_csv_file(default_file=None):
    """
    Open a file picker dialog to select a CSV file.
    Returns the selected file path, or default_file if the user cancels.
    """
    # Suppress macOS tkinter warnings about NSOpenPanel
    stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        file_path = filedialog.askopenfilename(
            title="Select Address CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=default_file
        )
        
        root.destroy()
    finally:
        sys.stderr.close()
        sys.stderr = stderr
    
    return file_path if file_path else default_file


def load_from_address(filename='Home.csv'):
    """
    Load the from-address from Home.csv.
    Expects columns: Name, Street Address Line 1, Street Address Line 2, City, State, Code
    Returns a tuple of address lines.
    """
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            
            row = next(reader)  # Get first data row
            
            if len(row) < 6:
                print(f'Warning: {filename} does not have enough columns. Using default FROM_ADDR.')
                return FROM_ADDR
            
            name = row[0].strip()
            street1 = row[1].strip()
            street2 = row[2].strip()
            city = row[3].strip()
            state = row[4].strip()
            code = row[5].strip()
            
            # Build address tuple, excluding empty street2
            addr_lines = [name, street1]
            if street2:
                addr_lines.append(street2)
            
            # Add city, state, code line only if city is not empty
            if city:
                addr_lines.append(f"{city}, {state} {code}".strip())
            
            return tuple(addr_lines)
    except FileNotFoundError:
        print(f'Warning: {filename} not found. Using default FROM_ADDR.')
        return FROM_ADDR
    except (StopIteration, IndexError):
        print(f'Warning: {filename} is empty or invalid. Using default FROM_ADDR.')
        return FROM_ADDR


if __name__ == '__main__':
    # Load from-address from Home.csv
    from_address = load_from_address('Home.csv')
    
    # Prompt user to select CSV file
    selected_file = select_csv_file(default_file=INFILE)
    
    if not selected_file:
        print('No file selected. Exiting.')
        exit(1)
    
    # Open PDF in binary mode; some platforms require binary write for PDFs
    with open(OUTFILE, 'wb') as f:
        write_envelopes(f, from_address, list(load_csv(selected_file)))
    print('wrote %s.' % OUTFILE)
