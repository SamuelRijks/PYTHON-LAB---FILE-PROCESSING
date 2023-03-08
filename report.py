from fpdf import FPDF
import configparser
import os

# Parse the configuration file


config_version = None

config = configparser.ConfigParser()
config.read('FW_1238.conf')

pdf = FPDF()
pdf.add_page()

with open('texto.txt', 'r') as f:
    for i, line in enumerate(f, start=1):
        try:
            if line.startswith('(title)'):
                pdf.set_font
                pdf.set_font("Arial", size=16)
                 # write the line to the PDF
                pdf.write(5, line[7:])  # skip '(title)' prefix
             else:
                 # set font size to 12
                pdf.set_font("Arial", size=12)
                # write the line to the PDF
                pdf.write(5, line)
                # process the line
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError in line {i}")


pdf.output("report.pdf")
