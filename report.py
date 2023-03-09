from fpdf import FPDF
import configparser
import os
import PyPDF2


# Parse the configuration file

dictionary = {
    'yellow': (255, 153, 0),
    'black': (64, 64, 64),
    'titlefontsize': 16,
    'antivirus': "#config antivirus profile[default]"
}

config_version = None

config = configparser.ConfigParser()
config.read('FW_1238.conf')

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_font('Calibri', '', r'C:\Windows\Fonts\Calibri.ttf')

pdf.add_page()

with open('texto.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, start=1):
        try:
            if line.startswith('(title)'):
                pdf.set_font("Arial",  size=dictionary['titlefontsize'])
                # set color to yellow
                pdf.set_text_color(*dictionary['yellow'])
                # write the line to the PDF
                pdf.write(5, line[7:])  # skip '(title)' prefix
            elif line.startswith('NEWPAGE'):
                pdf.add_page()
            elif line.startswith('IMAGEPORTADA'):
                pdf.image('Tecnocampus.png', x=130, y=40, w=70)
                pdf.set_line_width(3)  # set line width to 3
                # set draw color to yellow (255, 255, 0)
                pdf.set_draw_color(*dictionary['yellow'])
                # draw vertical line at x=10 with margin of 10
                pdf.line(10, 10, 10, pdf.h - 10)
            elif line.startswith('(portada)'):
                pdf.set_font("Helvetica",  size=26)
                pdf.set_xy(15, 130)
                # write the text using multi_cell()
                pdf.multi_cell(0, 5, line[9:], align='L')
                pdf.cell(0, 10, '')
            elif line.startswith('DISCLAIMER'):
                with open('disclaimer.txt', 'r') as file:
                    pdf.set_xy(15, 235)
                    pdf.set_font("Arial", size=9, style="B")
                    disclaimer_text = file.read()
                    line_height = 1
                    pdf.multi_cell(0, 10, disclaimer_text)
            elif "ANTIVIRUS" in line:
                value = config.get('config_antivirus_profile', 'edit')
                pdf.cell(0, 10, value)
            elif "WEBFILTER" in line:
                value = config.get('config webfilter profile', 'edit')
                pdf.cell(0, 10, value)
            elif "APP" in line:
                value = config.get('config application list', 'edit')
                pdf.cell(0, 10, value)

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
