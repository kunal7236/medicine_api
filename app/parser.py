import pdfplumber
from typing import List, Dict

def parse_pdf_to_data(pdf_path: str) -> List[Dict]:
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue
            for row in table:
                if len(row) >= 5 and row[0].strip().isdigit():
                    data.append({
                        "Sr.No": row[0].strip(),
                        "Drug Code": row[1].strip(),
                        "Generic Name": row[2].strip(),
                        "Unit Size": row[3].strip(),
                        "MRP(in Rs.)": row[4].strip()
                    })
    return data
