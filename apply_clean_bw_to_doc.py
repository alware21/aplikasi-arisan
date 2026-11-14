import os
import shutil
import subprocess
import docx
from PIL import Image
import win32com.client

# Stop Word to avoid file locking
subprocess.run(
    [
        "powershell",
        "-Command",
        "Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force",
    ],
    check=False,
)

docx_path = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.docx"
pdf_path = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.pdf"
fe_img_path = r"C:\Users\ThinkPad\Downloads\layout_menu_frontend.png"
be_img_path = r"C:\Users\ThinkPad\Downloads\layout_menu_backend.png"

doc = docx.Document(docx_path)

# Verify Cover
print(
    "Cover check:",
    [doc.paragraphs[i].text for i in range(17, 28) if doc.paragraphs[i].text.strip()],
)

# 1. Update text for Section 5 to be concise and minimal
doc.paragraphs[76].text = (
    "Berikut adalah rancangan tata letak (wireframe) posisi menu antarmuka sistem arisan digital "
    "secara terpisah antara sisi Front End dan Back End dalam bentuk diagram monokrom sederhana:"
)
doc.paragraphs[78].text = (
    "Menampilkan posisi navigasi menu peserta di sisi kiri (Sidebar) dan area siaran pengundian langsung di sisi utama."
)
doc.paragraphs[80].text = "Gambar 1. Tata Letak Menu Front End (Tampilan Anggota)"
doc.paragraphs[82].text = (
    "Menampilkan posisi menu pengelolaan di sisi kiri (Sidebar) serta konsol tombol operasional pengundian di sisi utama."
)
doc.paragraphs[84].text = "Gambar 2. Tata Letak Menu Back End (Panel Ketua Kelompok)"

# 2. Update Image 1 (Front End) at P79
p79 = doc.paragraphs[79]
blips_fe = p79.runs[0]._r.xpath(".//a:blip")
r_embed_fe = blips_fe[0].get(
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
)
part_fe = doc.part.related_parts[r_embed_fe]
with open(fe_img_path, "rb") as f:
    part_fe._blob = f.read()

# Update dimensions for Image 1
im_fe = Image.open(fe_img_path)
ratio_fe = im_fe.size[0] / im_fe.size[1]
w_in = 6.2
h_in = w_in / ratio_fe
cx = int(w_in * 914400)
cy = int(h_in * 914400)

for ext in p79.runs[0]._r.xpath(".//wp:extent"):
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))
for ext in p79.runs[0]._r.xpath(".//a:ext"):
    ext.set("cx", str(cx))
    ext.set("cy", str(cy))

print(
    f"Updated Image 1 (FE) blob: {len(part_fe._blob)} bytes, size {w_in}x{h_in:.2f} inches"
)

# 3. Update Image 2 (Back End) at P83
p83 = doc.paragraphs[83]
blips_be = p83.runs[0]._r.xpath(".//a:blip")
r_embed_be = blips_be[0].get(
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
)
part_be = doc.part.related_parts[r_embed_be]
with open(be_img_path, "rb") as f:
    part_be._blob = f.read()

# Update dimensions for Image 2
im_be = Image.open(be_img_path)
ratio_be = im_be.size[0] / im_be.size[1]
h_in_be = w_in / ratio_be
cx_be = int(w_in * 914400)
cy_be = int(h_in_be * 914400)

for ext in p83.runs[0]._r.xpath(".//wp:extent"):
    ext.set("cx", str(cx_be))
    ext.set("cy", str(cy_be))
for ext in p83.runs[0]._r.xpath(".//a:ext"):
    ext.set("cx", str(cx_be))
    ext.set("cy", str(cy_be))

print(
    f"Updated Image 2 (BE) blob: {len(part_be._blob)} bytes, size {w_in}x{h_in_be:.2f} inches"
)

# Save DOCX
doc.save(docx_path)
print(f"Saved updated docx to {docx_path}")

# Sync to workspace
shutil.copy2(docx_path, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.docx")

# Re-export to PDF via Word COM
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word_doc = word.Documents.Open(os.path.abspath(docx_path))
word_doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # 17 = wdFormatPDF
word_doc.Close()
word.Quit()
print(f"Exported updated PDF to {pdf_path}")

# Sync PDF to workspace
shutil.copy2(pdf_path, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.pdf")
print("Clean Black & White update completed successfully!")
