import os
import shutil
import docx
from PIL import Image
import win32com.client

docx_downloads = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.docx"
pdf_downloads = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.pdf"
drawio_src = r"D:\herd\aplikasi_arisan\struktur_menu_arisan.drawio"
png_src = r"D:\herd\aplikasi_arisan\struktur_menu_arisan.png"

# 1. Copy Draw.io files to Downloads
shutil.copy2(drawio_src, r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.drawio")
shutil.copy2(drawio_src, r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.dio")
shutil.copy2(drawio_src, r"D:\herd\aplikasi_arisan\struktur_menu_arisan.dio")
shutil.copy2(png_src, r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.png")
print("Draw.io and PNG files copied to Downloads successfully.")

# 2. Update existing DOCX in Downloads without altering other content/cover
doc = docx.Document(docx_downloads)

# Replace image2.png
p78 = doc.paragraphs[78]
blips = p78.runs[0]._r.xpath(".//a:blip")
r_embed = blips[0].get(
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
)
target_part = doc.part.related_parts[r_embed]

with open(png_src, "rb") as f:
    target_part._blob = f.read()

# Update dimensions to match aspect ratio
im = Image.open(png_src)
ratio = im.size[0] / im.size[1]
width_in = 6.4
height_in = width_in / ratio
cx = int(width_in * 914400)
cy = int(height_in * 914400)

for ext in p78.runs[0]._r.xpath(".//wp:extent"):
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))

for ext in p78.runs[0]._r.xpath(".//a:ext"):
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))

doc.save(docx_downloads)
print(f"Updated {docx_downloads} in-place successfully.")

# Also sync to workspace
shutil.copy2(
    docx_downloads, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.docx"
)

# 3. Export to PDF via Word COM
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word_doc = word.Documents.Open(os.path.abspath(docx_downloads))
word_doc.SaveAs(os.path.abspath(pdf_downloads), FileFormat=17)  # 17 = wdFormatPDF
word_doc.Close()
word.Quit()
print(f"Exported updated PDF to {pdf_downloads} successfully.")

# Also sync PDF to workspace
shutil.copy2(
    pdf_downloads, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.pdf"
)
print("All files updated and synchronized successfully.")
