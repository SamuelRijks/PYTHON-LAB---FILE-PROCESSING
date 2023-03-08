from fpdf import FPDF
import configparser
import os

# Parse the configuration file


config_version = None

config = configparser.ConfigParser()
config.read('FW_1238.conf')

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_font('Arial', '', r'C:\Windows\Fonts\arial.ttf', uni=True)
pdf.add_page()

with open('texto.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, start=1):
        try:
            if line.startswith('(title)'):
                pdf.set_font
                pdf.set_font("Arial", size=16)
                pdf.set_text_color(255, 204, 0)  # set color to yellow
                # write the line to the PDF
                pdf.write(5, line[7:])  # skip '(title)' prefix
            elif line.startswith('NEWPAGE'):
                pdf.add_page()
            elif line.startswith('TABLE'):
                pdf.set_font("Arial", size=12)  # set font size to 12
                pdf.set_text_color(64, 64, 64)
                col_width = 40
                row_height = 6
                margin = 10
                # Create table header
                pdf.cell(col_width, row_height * 2, 'Header 1', border=1)
                pdf.cell(col_width, row_height * 2, 'Header 2', border=1)
                pdf.cell(col_width, row_height * 2, 'Header 3', border=1)
                pdf.ln(row_height * 2)
                # Create table rows
                for row in range(1, 4):
                    for col in range(1, 4):
                        pdf.cell(col_width, row_height,
                                 f'Row {row}, Col {col}', border=1)
                    pdf.ln(row_height)
            else:
                # set font size to 12
                pdf.set_font("Arial", size=12)
                pdf.set_text_color(64, 64, 64)  # set color to yellow
                # write the line to the PDF
                pdf.write(5, line)
                # process the line
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError in line {i}")


pdf.output("report.pdf")
