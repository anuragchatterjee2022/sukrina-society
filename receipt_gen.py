from fpdf2 import FPDF

def generate_receipt(name, flat, amount, month):
    pdf = FPDF()
    pdf.add_page()
    # Header
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 15, txt="SUKRINA COOPERATIVE HOUSING LTD.", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Official Maintenance Receipt", ln=True, align='C')
    pdf.ln(10)
    
    # Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Billing Month: {month}", ln=True)
    pdf.line(10, 45, 200, 45)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Member Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Flat Number: {flat}", ln=True)
    pdf.cell(200, 10, txt=f"Amount Received: Rs. {amount}/-", ln=True)
    pdf.cell(200, 10, txt=f"Payment Status: SUCCESSFUL", ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="This is a computer-generated receipt.", ln=True, align='C')
    import os

# Define the filename path based on the environment
    if os.path.exists("/tmp"):
     filename = f"/tmp/Receipt_{flat}.pdf"
    else:
    # Local path for Windows testing in your 'co society' folder
     filename = os.path.join(os.getcwd(), f"Receipt_{flat}.pdf")

# Move this OUTSIDE the if/else so it always runs
    pdf.output(filename)
    return filename