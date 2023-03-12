from fpdf import FPDF
import configparser
import os
import PyPDF2
import regex as re


# Parse the configuration file

dictionary = {
    'yellow': (255, 153, 0),
    'black': (64, 64, 64),
    'titlefontsize': 16,
    'antivirus': "#config antivirus profile[default]"
}

dicc = {
    "INTERFACE": (5, 4, r'config system interface(.*?"modem"',
                  r'edit "([^"]+)"', r'set alias "([^"]+)"', r'set ip (\d+\.\d+\.\d+\.\d+)', r'set dhcp-relay-ip "(\d+\.\d+\.\d+\.\d+)"')
}

search_list = [
    ("(ANTIVIRUS)", r'set av-profile\s+"(\w+-?\w+)"',
     r'config firewall policy(.*?)"certificate-inspection"'),
    ("(WEBFILTER)", r'set webfilter-profile\s+"(\w+-?\w+)"',
     r'config firewall policy(.*?)"certificate-inspection"'),
    ("(APP)", r'set application-list\s+"(\w+-?\w+)"',
     r'config firewall policy(.*?)"certificate-inspection"'),
    ("(IPS)", r'set ips-sensor\s+"(\w+-?\w+)"',
     r'config firewall policy(.*?)"certificate-inspection"'),
    ("IPSLOC", r'set location\s+"(\w+-?\w+)"', r'edit "UTM-IPS"(.*?)end'),
    ("IPSSEV", r'set severity\s+(\w+)\s+(\w+)', r'edit "UTM-IPS"(.*?)end'),
    ("IPSOS", r'set os\s+(\w+)\s+(\w+)\s+(\w+)', r'edit "UTM-IPS"(.*?)end'),
    ("TABLE",  r'config-version=FG\d{3}[A-Z]-([\d.]+)-([\w-]+)-(\d{6}):',
     r'config-version=FG\d{3}[A-Z]-([\d.]+)-([\w-]+)-(\d{6}):'),

]


config_string = ""

with open('FW_1238 .conf', 'r') as f:
    for line in f:
        config_string += line

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_font('Calibri', '', r'C:\Windows\Fonts\Calibri.ttf')

pdf.add_page()
with open('texto.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, start=1):
        entrat = False
        cont = 0
        array = [None, None, None, None]
        pdf.set_font("Arial", size=12)
        pdf.set_text_color(*dictionary['black'])
        col_width, row_height, margin = 60, 6, 10

        def create_table(rows, cols, data):
            # Set header background color
            pdf.set_fill_color(255, 255, 0)

            # Calculate cell width and height
            cell_width = pdf.w / cols
            cell_height = pdf.font_size * 2

            right_margin = 10

            # Print table header
            for col in range(cols):
                pdf.cell(cell_width, cell_height,
                         f'{data[1][col+1]}', border=1, fill=True, align='C')

            pdf.ln(cell_height)

            for row in range(rows):
                for col in range(cols):
                    pdf.cell(cell_width, cell_height, f'{data[row+1][col+1]}', border=1, align='C',
                             ln=row == rows-1 and col == cols-1,  # Set line break for last cell
                             r=right_margin)  # Set right margin

                pdf.ln(cell_height)

            pdf.ln(cell_height)

        def create_data(word):
            # crear info
            values = {}
            match = re.search(dicc[word][2], config_string, re.DOTALL)
            if match:
                for i in range(3, len(dicc[word])):
                    section_string = match.group(1)
                    values[i] = re.search(dicc[word][i], section_string)
                    table_data = {}
                    for word in range(len(dicc)):
                        if dicc[word][0] > 0:
                            table_data[word+1] = {}
                            for row in range(1, dicc[word][0]+1):
                                table_data[word+1][row] = {}
                                for col in range(1, dicc[word][1]+1):
                                    if col == 1:
                                        table_data[word +
                                                   1][row][col] = dicc[word][col-1]
                                    else:
                                        try:
                                            table_data[word +
                                                       1][row][col] = values[word][col-2]
                                        except:
                                            table_data[word+1][row][col] = ''
                create_table(dicc[word][0],
                             dicc[word][1], table_data)

        try:
            for keyword, regex, section in search_list:
                if keyword in line:
                    match = re.search(section, config_string, re.DOTALL)
                    if match:
                        if keyword == "TABLE":
                            value1 = match.group(1)[1:]
                            match = re.search(regex, config_string)
                        else:
                            section_string = match.group(1)
                            match = re.search(regex, section_string)
                        if match:
                            value = match.group(1)
                            if keyword == "TABLE":
                                line = line.replace(keyword, "")
                                version = match.group(1).replace('_', '.')
                                version = version.replace('0', '', 1)
                                version = version[:2] + '0' + "." + version[2:]

                                build_match = re.search(
                                    r'build(\d+)', match.group(2))
                                build = 'build' + \
                                    build_match.group(1) if build_match else ""

                                date = match.group(3)
                                value1 = f"v{version},{build} ({date})"
                                # Define the table as a nested dictionary
                                table_data = {1: {1: 'Marca-Model', 2: f'FortiGate {value}'},
                                              2: {1: 'OS/Firmware', 2: value1},
                                              3: {1: 'S/N', 2: ''}}

                                # Set table border style
                                # Black border color
                                pdf.set_draw_color(0, 0, 0)
                                # Thin border line width
                                pdf.set_line_width(0.3)

                                # Loop over the rows and columns and add the cell contents to the PDF
                                for row_num, row_data in table_data.items():
                                    for col_num, cell_data in row_data.items():
                                        # Black text color
                                        pdf.set_text_color(0, 0, 0)
                                        pdf.cell(col_width, row_height,
                                                 cell_data, border=1)
                                    pdf.ln(row_height)
                            elif keyword == "(IPS)" or keyword == "IPSSEV":
                                array[cont] = keyword
                                array[cont+1] = value
                                cont = cont + 2
                            elif keyword == "IPSOS":
                                line = line.replace(array[0], array[1])
                                line = line.replace(array[2], array[3])
                                line = line.replace(keyword, value)
                                pdf.write(5, line)
                                entrat = True
                            else:
                                line = line.replace(keyword, value)
                                pdf.write(5, line)
                                entrat = True
            if entrat:
                continue
            elif line.startswith('BBBB'):
                create_data("INTERFACE")
            elif line.startswith('(title)'):
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
            elif line.startswith('ENCABEZADO'):
                pdf.image('Tecnocampus.png', x=160, y=15, w=35)
            elif line.startswith('(bold)'):
                pdf.set_font(
                    "Arial", 'B', size=dictionary['titlefontsize'] + 4)
                # set color to yellow
                pdf.set_text_color(*dictionary['black'])
                # write the line to the PDF
                pdf.write(5, line[6:])  # skip '(title)' prefix
            elif line.startswith('(bold1)'):
                pdf.set_font(
                    "Arial", 'B', size=dictionary['titlefontsize'])
                # set color to yellow
                pdf.set_text_color(*dictionary['black'])
                # write the line to the PDF
                pdf.write(5, line[7:])  # skip '(title)' prefix
            elif line.startswith('Migració'):
                pdf.set_font('Arial', 'B', 16)
                pdf.cell(
                    0, 10, 'Migració de la infraestructura de seguretat perimetral', 0, 1)
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
