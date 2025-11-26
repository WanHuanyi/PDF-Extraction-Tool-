from extractor import extract_content
import os
import shutil

# Setup paths
pdf_path = "/Users/why/Projects/Pdf/Papers/3746058.3759016.pdf"
output_dir = "test_output"

# Clean output dir
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Run extraction
print(f"Extracting {pdf_path}...")
try:
    files = extract_content(pdf_path, output_dir)
    print("Extraction successful!")
    print("Generated files:")
    for f in files:
        print(f" - {f}")
except Exception as e:
    print(f"Extraction failed: {e}")
    import traceback
    traceback.print_exc()
