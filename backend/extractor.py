import pdfplumber
import fitz  # PyMuPDF
import os
from pathlib import Path
import pandas as pd

def extract_content(pdf_path: str, output_dir: str):
    """
    Extracts text, tables, and images from a PDF.
    Returns a tuple: (list of generated files, extracted title).
    """
    output_path = Path(output_dir)
    md_content = []
    generated_files = []
    
    # Open with both libraries
    doc = fitz.open(pdf_path)
    image_count = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            md_content.append(f"## Page {i+1}\n")
            
            # 1. Extract Tables using pdfplumber
            tables = page.extract_tables()
            if tables:
                md_content.append("### Tables\n")
                for table in tables:
                    # Filter out empty rows/cols if needed, or just convert
                    # Handle cases where table might be None or empty
                    if table:
                        try:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            md_content.append(df.to_markdown(index=False))
                            md_content.append("\n\n")
                        except Exception:
                            pass # Skip malformed tables

            # 2. Extract Text using PyMuPDF (fitz) - Better layout preservation
            fitz_page = doc[i]
            text = fitz_page.get_text("text")
            if text:
                md_content.append("### Text\n")
                md_content.append(text)
                md_content.append("\n\n")

            # 3. Extract Images using PyMuPDF (fitz)
            image_list = fitz_page.get_images(full=True)
            
            # Get text blocks to find captions
            text_blocks = fitz_page.get_text("blocks")
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Get image bbox to find nearest text
                    rects = fitz_page.get_image_rects(xref)
                    caption = ""
                    if rects:
                        img_rect = rects[0]
                        
                        # Search for "Figure" or "Fig" below the image
                        candidates = []
                        for block in text_blocks:
                            b_x0, b_y0, b_x1, b_y1, b_text, _, _ = block
                            if b_y0 >= img_rect.y1 and b_y0 < img_rect.y1 + 100:
                                clean_text = b_text.strip()
                                if clean_text.lower().startswith("figure") or clean_text.lower().startswith("fig"):
                                    candidates.append((b_y0, clean_text))
                        
                        candidates.sort(key=lambda x: x[0])
                        if candidates:
                            caption = candidates[0][1].split('\n')[0]
                            import re
                            match = re.match(r"(Figure\s*[\d\.]+)", caption, re.IGNORECASE)
                            if match:
                                caption = match.group(1).replace(" ", "_").replace(".", "_")
                            else:
                                caption = ""

                    if caption:
                        image_name = f"{caption}.{image_ext}"
                    else:
                        image_name = f"Figure_{image_count + 1}.{image_ext}"
                    
                    if image_name in generated_files:
                         image_name = f"{Path(image_name).stem}_{image_count + 1}.{image_ext}"

                    image_path = output_path / image_name
                    
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    
                    generated_files.append(image_name)
                    md_content.append(f"![{image_name}]({image_name})\n\n")
                    image_count += 1
                except Exception as e:
                    print(f"Error extracting image {img_index} on page {i}: {e}")
                    continue

    # Extract Title (First text block of first page)
    title = "Untitled"
    try:
        first_page = doc[0]
        blocks = first_page.get_text("blocks")
        if blocks:
            # blocks[0][4] is the text content
            raw_title = blocks[0][4].strip()
            # Take first line or join lines, sanitize
            title = raw_title.split('\n')[0].strip()
            if len(title) > 50:
                title = title[:50]
    except Exception:
        pass

    # Write Markdown file
    md_file_name = "extracted_content.md"
    with open(output_path / md_file_name, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    
    generated_files.append(md_file_name)
    
    return generated_files, title
