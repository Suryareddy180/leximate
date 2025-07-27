import google.generativeai as genai
from fpdf import FPDF
import os
import urllib.request
from dotenv import load_dotenv
from datetime import datetime

# Load .env file
load_dotenv()

# Get API key from .env
genai_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=genai_api_key)

LEGAL_TEMPLATES = {
    "Rental Agreement": "Generate a rental agreement between {party1} (tenant) and {party2} (landlord) for {duration} months.",
    "Employment Contract": "Generate an employment contract between {party1} (employee) and {party2} (employer) with a salary of {salary} per year.",
    "Business Partnership Agreement": "Draft a business partnership agreement between {party1} and {party2}, defining responsibilities and profit-sharing terms.",
    "NDA": "Generate a non-disclosure agreement (NDA) between {party1} and {party2} to protect confidential business information.",
    "MOU": "Create a Memorandum of Understanding (MOU) between {party1} and {party2} outlining the mutual intentions and responsibilities of both parties.",
    "Contractor Agreement": "Draft a contractor agreement between {party1} (contractor) and {party2} (client), outlining services, timelines, and payment terms.",
    "Loan Agreement": "Generate a loan agreement where {party1} lends money to {party2}, specifying repayment terms and interest rate.",
    "SLA": "Create a Service Level Agreement (SLA) between {party1} (provider) and {party2} (client), defining service expectations and penalties."
}

def generate_document(doc_type, party1, party2, duration="", salary=""):
    if doc_type not in LEGAL_TEMPLATES:
        return "Invalid document type."

    prompt = LEGAL_TEMPLATES[doc_type].format(
        party1=party1, party2=party2, duration=duration, salary=salary
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text if hasattr(response, 'text') else "No response text found."
    except Exception as e:
        return f"Error generating document: {e}"

def save_to_pdf(content, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_document_{timestamp}.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    font_path = os.path.join(font_dir, "LiberationSerif-Regular.ttf")
    font_url = "https://raw.githubusercontent.com/liberationfonts/liberation-fonts/master/LiberationSerif-Regular.ttf"

    try:
        if not os.path.exists(font_path):
            urllib.request.urlretrieve(font_url, font_path)

        pdf.add_font("LiberationSerif", "", font_path, uni=True)
        pdf.set_font("LiberationSerif", size=12)
    except Exception as e:
        pdf.set_font("Arial", size=12)
        content = f"Font could not be loaded. Default font used.\n\n{content}"

    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)

    try:
        pdf.output(filename)
        return filename
    except Exception as e:
        return f"Error saving PDF: {e}"
