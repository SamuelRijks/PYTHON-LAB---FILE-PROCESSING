import os
from fpdf import FPDF
import configparser
import os

# Parse the configuration file


config_version = None

config = configparser.ConfigParser()
config.read('FW_1238.conf')


# Extract relevant information
# server_url = config.get('server', 'url')
# db_name = config.get('database', 'name')
# api_key = config.get('api', 'key')

# Generate the PDF report

pdf = FPDF()
pdf.add_page()

titol_color = '\033[33m'


# Add cover page image
pdf.image("Tecnocampus.png", x=0, y=0, w=100, h=40)


pdf.set_font("Arial", "B", 23)

pdf.set_text_color(64, 64, 64)

pdf.set_xy(0, pdf.h/2 + 10)


pdf.cell(0, 0, "Migració de la infraestructura de",  ln=1, align="L")
pdf.cell(0, pdf.font_size + 5, "seguretat perimetral per a", ln=1, align="L")


pdf.cell(0, pdf.font_size + 15, "TecnoCampus", ln=1, align="L")

pdf.set_font("Arial", "B", 10)


pdf.cell(0, pdf.font_size + 50, "La informació continguda en aquest document pot ser de caràcter privilegiat y/o confidencial. Qualsevol disseminació, distribució o copia d'aquest document per qualsevol altre persona diferent als receptors originals queda estrictament prohibida. Si ha rebut aquest document per error, sis plau notifiquí immediatament al emissor i esborri qualsevol copia d'aquest document.", ln=1, align="C")

# Create a new page for the table of contents
pdf.add_page()

# Set the font and font size
pdf.set_font("Arial", "B", 16)

# Set the text color to dark gray
pdf.set_text_color(64, 64, 64)

# Set the starting position of the text
pdf.set_xy(10, 20)

# Write the title of the table of contents
pdf.cell(0, 10, "Taula de continguts", ln=1)

# Set the font size for the contents
pdf.set_font_size(12)

# Write the contents of the table of contents
pdf.cell(0, 10, "1. INTRODUCCIÓ".ljust(100, '.') + "3", ln=1)
pdf.cell(0, 10, "1.1. DESCRIPCIÓ".ljust(100, '.') + "3", ln=1)
pdf.cell(0, 10, "1.2. OBJECTIUS".ljust(100, '.') + "3", ln=1)
pdf.cell(0, 10, "1.3. DESCRIPCIÓ GENERAL DE LES INFRAESTRUCTURES".ljust(
    100, '.') + "4", ln=1)
pdf.cell(0, 10, "2. CONFIGURACIÓ DEL DISPOSITIU".ljust(100, '.') + "5", ln=1)
pdf.cell(0, 10, "2.1. DISPOSITIU".ljust(100, '.') + "5", ln=1)
pdf.cell(0, 10, "2.2. CREDENCIALS D'ACCÉS".ljust(100, '.') + "5", ln=1)
pdf.cell(0, 10, "2.3. GENERAL".ljust(100, '.') + "5", ln=1)
pdf.cell(0, 10, "2.4. INTERFÍCIES".ljust(100, '.') + "5", ln=1)
pdf.cell(0, 10, "2.5. TAULA D'ENRUTAMENT".ljust(100, '.') + "6", ln=1)
pdf.cell(0, 10, "2.6. OBJECTES ADRECES DEL FIREWALL".ljust(100, '.') + "6", ln=1)
pdf.cell(0, 10, "2.7. OBJECTES SERVEIS".ljust(100, '.') + "7", ln=1)
pdf.cell(0, 10, "2.8. NATS D'ENTRADA (VIRTUAL IPS)".ljust(100, '.') + "9", ln=1)
pdf.cell(0, 10, "2.8. NATS D'ENTRADA (VIRTUAL IPS)".ljust(100, '.') + "9", ln=1)
pdf.cell(0, 10, "2.9. POLITIQUES DE FIREWALL".ljust(100, '.') + "1O", ln=1)
pdf.cell(0, 10, "2.10. SERVEI ANITVIRUS".ljust(100, '.') + "11", ln=1)
pdf.cell(0, 10, "2.11. SERVEI DE FILTRATGE WEB".ljust(100, '.') + "11", ln=1)
pdf.cell(0, 10, "2.12. SERVEI APPLICATION CONTROL".ljust(100, '.') + "11", ln=1)
pdf.cell(0, 10, "2.13. SERVEI INTRUSION PROTECTION".ljust(100, '.') + "11", ln=1)

# page 3

pdf.add_page()

# Set font style for the title
pdf.set_font("Arial", "B", 20)

# Set text color to dark grey
pdf.set_text_color(64, 64, 64)

# Add the title to the page
pdf.cell(0, 20, "1. Introducció", ln=1)

# Set font style for the section title
pdf.set_font("Arial", "B", 14)

# Add the section titles and text to the page
pdf.cell(0, 10, "1.1. Descripció", ln=1)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, "El present document descriu la configuració realitzada en el dispositiu Fortigate-80D de Fortinet a la empresa TecnoCampus resultat de la substitució de un Firewall perimetral Cisco de l'organització.", 0, "L")

pdf.set_font("Arial", "B", 14)
pdf.cell(0, 10, "1.2. Objectius", ln=1)
pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, "El objectiu d'aquest document és la de formalitzar el traspàs d'informació al equip tècnic responsable del manteniment de les infraestructures instal·lades. Aquesta informació fa referencia al disseny, instal·lació i configuració dels dispositius i sistemes afectats per la implementació.\n La present documentació inclou:", 0, "L")

pdf.set_font("Arial", "", 12)
pdf.multi_cell(0, 8, " Descripció general de les infraestructures instal·lades.\n Polítiques de filtratge de tràfic.\n Perfils de seguretat.\n Connexions Túnel.\n", 0, "L")

# page 3

pdf.add_page()

pdf.add_page()

pdf.add_page()


pdf.output("report.pdf")
