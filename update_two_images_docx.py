import os
import shutil
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
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
fe_img = r"C:\Users\ThinkPad\Downloads\layout_menu_frontend.png"
be_img = r"C:\Users\ThinkPad\Downloads\layout_menu_backend.png"

doc = docx.Document(docx_path)

# Verify Cover / User Modifications
print(f"Total paragraphs before: {len(doc.paragraphs)}")
cover_check = [
    doc.paragraphs[i].text for i in range(17, 28) if doc.paragraphs[i].text.strip()
]
print("Cover check:", cover_check)

# Find Section 5
p5_idx = None
for i, p in enumerate(doc.paragraphs):
    if "5. Struktur Menu" in p.text:
        p5_idx = i
        break

print(f"Section 5 found at paragraph index {p5_idx}")

# We will remove paragraphs from p5_idx + 1 up to (but not including) the last paragraph with 'TERIMA KASIH'
terima_idx = None
for i in range(p5_idx, len(doc.paragraphs)):
    if "TERIMA KASIH" in doc.paragraphs[i].text:
        terima_idx = i
        break

print(f"'TERIMA KASIH' found at paragraph index {terima_idx}")

# Update Section 5 intro (P76 or p5_idx + 1)
intro_p = doc.paragraphs[p5_idx + 1]
intro_p.text = (
    "Berikut adalah rancangan tata letak (wireframe/mockup layout) posisi menu antarmuka sistem arisan digital "
    "pada format desktop hitam-putih (monokrom), yang memisahkan secara jelas antara antarmuka pada sisi Front End "
    "(layar operasional anggota/peserta) dan sisi Back End (panel kontrol pengelolaan ketua kelompok):"
)

# Remove old paragraphs between intro_p and terima_kasih
# In python-docx, to remove a paragraph: p._element.getparent().remove(p._element)
to_remove = []
for i in range(p5_idx + 2, terima_idx):
    to_remove.append(doc.paragraphs[i])

for p in to_remove:
    p._element.getparent().remove(p._element)

# Now, find 'TERIMA KASIH' again
terima_p = None
for p in doc.paragraphs:
    if "TERIMA KASIH" in p.text:
        terima_p = p
        break


# Helper to insert paragraph before terima_p
def insert_p_before(
    ref_p,
    text="",
    bold=False,
    size=10,
    italic=False,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    color=None,
):
    new_p = ref_p._insert_paragraph_before()
    new_p.alignment = align
    if text:
        r = new_p.add_run(text)
        r.font.name = "Arial"
        r.font.bold = bold
        r.font.italic = italic
        r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
    return new_p


# 1. Front End Subheading
p_fe_sub = insert_p_before(
    terima_p,
    "5.1 Rancangan Tata Letak Menu Front End (Tampilan Layar Anggota)",
    bold=True,
    size=11,
    color=RGBColor(0, 0, 0),
)
p_fe_sub.paragraph_format.space_before = Pt(12)
p_fe_sub.paragraph_format.space_after = Pt(4)

p_fe_desc = insert_p_before(
    terima_p,
    "Menampilkan posisi 5 menu navigasi di sisi Sidebar Kiri dan area Ruang Undian Live di sisi tengah. Peserta hanya memiliki hak akses menonton dan tidak memiliki tombol pengocokan undian:",
    size=9.5,
)
p_fe_desc.paragraph_format.space_after = Pt(6)

# Front End Image
p_fe_img = insert_p_before(terima_p, align=WD_ALIGN_PARAGRAPH.CENTER)
p_fe_img.paragraph_format.space_after = Pt(4)
r_fe_img = p_fe_img.add_run()
r_fe_img.add_picture(fe_img, width=Inches(6.2))

# Front End Caption
p_fe_cap = insert_p_before(
    terima_p,
    "Gambar 1. Tata Letak Menu Sisi Front End (Tampilan Anggota/Peserta - Mode Monokrom)",
    italic=True,
    size=9,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    color=RGBColor(80, 80, 80),
)
p_fe_cap.paragraph_format.space_after = Pt(16)


# 2. Back End Subheading
p_be_sub = insert_p_before(
    terima_p,
    "5.2 Rancangan Tata Letak Menu Back End (Panel Kontrol Ketua Kelompok)",
    bold=True,
    size=11,
    color=RGBColor(0, 0, 0),
)
p_be_sub.paragraph_format.space_before = Pt(14)
p_be_sub.paragraph_format.space_after = Pt(4)

p_be_desc = insert_p_before(
    terima_p,
    "Menampilkan posisi 5 menu pengelolaan di sisi Sidebar Kiri dan area Konsol Operasional di sisi tengah. Menu ini dilengkapi tombol eksklusif '[>] TEKAN TOMBOL KOCOK' serta tombol pengesahan kuitansi resmi:",
    size=9.5,
)
p_be_desc.paragraph_format.space_after = Pt(6)

# Back End Image
p_be_img = insert_p_before(terima_p, align=WD_ALIGN_PARAGRAPH.CENTER)
p_be_img.paragraph_format.space_after = Pt(4)
r_be_img = p_be_img.add_run()
r_be_img.add_picture(be_img, width=Inches(6.2))

# Back End Caption
p_be_cap = insert_p_before(
    terima_p,
    "Gambar 2. Tata Letak Menu Sisi Back End (Panel Kontrol Ketua Kelompok / Host - Mode Monokrom)",
    italic=True,
    size=9,
    align=WD_ALIGN_PARAGRAPH.CENTER,
    color=RGBColor(80, 80, 80),
)
p_be_cap.paragraph_format.space_after = Pt(20)

# Save DOCX
doc.save(docx_path)
print(f"Saved updated DOCX to {docx_path}")

# Sync to workspace
shutil.copy2(docx_path, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.docx")

# Re-export to PDF
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word_doc = word.Documents.Open(os.path.abspath(docx_path))
word_doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # 17 = wdFormatPDF
word_doc.Close()
word.Quit()
print(f"Exported updated PDF to {pdf_path}")
shutil.copy2(pdf_path, r"D:\herd\aplikasi_arisan\Rancangan_Menu_Aplikasi_Arisan.pdf")
print("Completed successfully!")
