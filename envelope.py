#!/usr/bin/python

import cairo
import csv


INCHES_TO_POINTS = 72

# --- Configurable constants ---
PAGE_WIDTH_IN = 7.2
PAGE_HEIGHT_IN = 5.25
FONT_FACE = 'serif'
MARGIN_IN = 0.25
TO_X_IN = 2.5
TO_Y_START_IN = 2.25
LINE_HEIGHT_PT = 12

# I/O and default from-address (moved here so they're easy to edit)
# Used File From: 
INFILE = 'address.csv'
OUTFILE = 'Processed_Addresses.pdf'
FROM_ADDR = ('The Franzen Family',
             '[elided]',
             'San Francisco, CA 94110')


def write_envelopes(out, from_addr, to_addrs):
    surface = cairo.PDFSurface(out,
                               PAGE_WIDTH_IN * INCHES_TO_POINTS,
                               PAGE_HEIGHT_IN * INCHES_TO_POINTS)
    cr = cairo.Context(surface)
    cr.select_font_face(FONT_FACE)

    for to_addr in to_addrs:
        # from address
        for i, line in enumerate(from_addr):
            cr.move_to(MARGIN_IN * INCHES_TO_POINTS,
                       (MARGIN_IN * INCHES_TO_POINTS) + LINE_HEIGHT_PT + (LINE_HEIGHT_PT * i))
            cr.show_text(line)

        # to address
        for i, line in enumerate(to_addr):
            cr.move_to(TO_X_IN * INCHES_TO_POINTS,
                       (TO_Y_START_IN * INCHES_TO_POINTS) + LINE_HEIGHT_PT + (LINE_HEIGHT_PT * i))
            cr.show_text(line)
        cr.show_page()

    surface.flush()
    surface.finish()


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
            addr_lines.append(f"{city} {state} {code}")

            yield addr_lines


if __name__ == '__main__':
    # Open PDF in binary mode; some platforms require binary write for PDFs
    with open(OUTFILE, 'wb') as f:
        write_envelopes(f, FROM_ADDR, list(load_csv(INFILE)))
    print('wrote %s.' % OUTFILE)
