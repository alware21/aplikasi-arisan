import os
import shutil
import docx
from PIL import Image
import win32com.client

docx_downloads = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.docx"
pdf_downloads = r"C:\Users\ThinkPad\Downloads\Rancangan_Menu_Aplikasi_Arisan.pdf"
png_path = r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.png"

# Kill any stray Word process first to avoid permission lock
import subprocess

subprocess.run(
    [
        "powershell",
        "-Command",
        "Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force",
    ],
    check=False,
)

doc = docx.Document(docx_downloads)

# Update Section 5 description
# Find paragraph with "5. Struktur Menu"
for i, p in enumerate(doc.paragraphs):
    if "5. Struktur Menu" in p.text:
        print(f"Found Section 5 at P{i}")
        # update next paragraphs with layout explanation
        if i + 1 < len(doc.paragraphs):
            doc.paragraphs[i + 1].text = (
                "Berikut adalah rancangan tata letak (wireframe/mockup layout) posisi menu navigasi sistem arisan digital pada layar desktop, "
                "yang membedakan secara visual letak menu pada Tampilan Anggota (Front End) di sisi kiri dan Panel Kontrol Ketua Kelompok (Back End) di sisi kanan:"
            )

# Update image in P78 (or find the paragraph containing image2.png)
for p in doc.paragraphs:
    blips = p._p.xpath(".//a:blip")
    for blip in blips:
        r_embed = blip.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
        )
        part = doc.part.related_parts[r_embed]
        if "image2" in part.partname:
            print(f"Replacing image part: {part.partname}")
            with open(png_path, "rb") as f:
                part._blob = f.read()

            # update size extent
            im = Image.open(png_path)
            ratio = im.size[0] / im.size[1]
            w_in = 6.5
            h_in = w_in / ratio
            cx = int(w_in * 914400)
            cy = int(h_in * 914400)
            for ext in p._p.xpath(".//wp:extent"):
                ext.set("cx", str(cx))
                ext.set("cy", str(cy))
            for ext in p._p.xpath(".//a:ext"):
                ext.set("cx", str(cx))
                ext.set("cy", str(cy))

doc.save(docx_downloads)
print(f"Updated {docx_downloads} successfully.")

# Also sync to workspace
shutil.copy2(
    docx_downloads, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.docx"
)

# Re-export to PDF
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word_doc = word.Documents.Open(os.path.abspath(docx_downloads))
word_doc.SaveAs(os.path.abspath(pdf_downloads), FileFormat=17)
word_doc.Close()
word.Quit()
print(f"Exported to {pdf_downloads} successfully.")
shutil.copy2(
    pdf_downloads, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.pdf"
)
print("Done!")
