import fitz

pdf_path = "/Users/why/Projects/Pdf/Papers/3746058.3759016.pdf"
doc = fitz.open(pdf_path)

print("--- MARKDOWN ---")
# print(doc[0].get_text("markdown")[:1000])

print("\n--- TEXT ---")
print(doc[0].get_text("text")[:1000])

print("\n--- BLOCKS ---")
blocks = doc[0].get_text("blocks")
for b in blocks[:5]:
    print(b)
