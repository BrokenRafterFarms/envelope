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
INFILE = 'address.csv'
OUTFILE = 'out.pdf'
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
    # This logic is necessarily use case specific, but for
    # our list we just have three columns of addresses and an optional
    # fourth column that says "yes" for addresses we wanted printed.
    with open(filename) as f:
        for i, row in enumerate(csv.reader(f)):
            if i == 0:
                continue

            type = ''
            if len(row) > 3:
                type = row[3].strip()
            if type != 'yes':
                continue
            yield row[0:3]


if __name__ == '__main__':
    # Open PDF in binary mode; some platforms require binary write for PDFs
    with open(OUTFILE, 'wb') as f:
        write_envelopes(f, FROM_ADDR, list(load_csv(INFILE)))
    print('wrote %s.' % OUTFILE)
