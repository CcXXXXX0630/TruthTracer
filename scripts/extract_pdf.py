import sys, os
pdf = r"D:\论文写作\.hermes\desktop-attachments\NS-甲烷基SCP代替鱼粉.pdf"
out = r"D:\论文写作\academic-data-forensics\investigations\scp_paper\extracted_text.txt"
os.makedirs(os.path.dirname(out), exist_ok=True)

text = ""
for lib in ["fitz", "pdfplumber", "PyPDF2"]:
    try:
        if lib == "fitz":
            import fitz
            doc = fitz.open(pdf)
            for page in doc:
                text += page.get_text()
            doc.close()
        elif lib == "pdfplumber":
            import pdfplumber
            with pdfplumber.open(pdf) as p:
                for page in p.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
        elif lib == "PyPDF2":
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if text.strip():
            print("SUCCESS: " + lib + " - " + str(len(text)) + " chars")
            break
    except Exception as e:
        print("FAILED: " + lib + " - " + str(e))

if text.strip():
    with open(out, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SAVED: " + out)
else:
    print("ALL BACKENDS FAILED")
