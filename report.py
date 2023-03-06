from fpdf import FPDF
import configparser

# Parse the configuration file
config = configparser.ConfigParser()
config.read('FW_1238.conf')

# Extract relevant information
server_url = config.get('server', 'url')
db_name = config.get('database', 'name')
api_key = config.get('api', 'key')

# Generate the PDF report
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Server URL: " + server_url, ln=1)
pdf.cell(200, 10, txt="Database Name: " + db_name, ln=1)
pdf.cell(200, 10, txt="API Key: " + api_key, ln=1)
pdf.output("report.pdf")
