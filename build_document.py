import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Page Margins (1 inch all around)
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Helpers for Styling
COLOR_PRIMARY = RGBColor(30, 64, 175)  # #1E40AF Navy Blue
COLOR_SECONDARY = RGBColor(15, 118, 110)  # #0F766E Teal
COLOR_DARK = RGBColor(30, 41, 59)  # #1E293B Dark Slate
COLOR_MUTED = RGBColor(100, 116, 139)  # #64748B Slate Muted


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for m, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{m}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


# Title / Header
title_p = doc.add_paragraph()
title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_title = title_p.add_run("RANCANGAN STRUKTUR & MENU SISTEM\nAPLIKASI ARISAN DIGITAL")
r_title.font.name = "Arial"
r_title.font.size = Pt(18)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY

sub_p = doc.add_paragraph()
sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_sub = sub_p.add_run(
    "Tugas Perancangan Antarmuka & Proses Bisnis Sistem - Mata Kuliah PBO\nDosen Pengampu: Zuliar Efendi, M.Kom."
)
r_sub.font.name = "Arial"
r_sub.font.size = Pt(10.5)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_MUTED

doc.add_paragraph()  # spacer

# --- Section 1 ---
h1 = doc.add_paragraph()
r = h1.add_run("1. Daftar Seluruh Menu Sistem (Front End & Back End)")
r.font.name = "Arial"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_PRIMARY

p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.15
p.add_run(
    "Sistem dirancang menggunakan arsitektur peran berbasis kelompok ("
).font.name = "Arial"
p.add_run("Group/Room-Based Role").font.bold = True
p.add_run("), di mana sistem ").font.name = "Arial"
p.add_run("tidak memerlukan superadmin terpusat").font.bold = True
p.add_run(
    ". Siapapun yang berinisiatif membuat kelompok arisan bertindak sebagai "
).font.name = "Arial"
p.add_run("Ketua Kelompok (Host/Pengocok)").font.bold = True
p.add_run(", sedangkan peserta lain bergabung sebagai ").font.name = "Arial"
p.add_run("Anggota Biasa (Peserta)").font.bold = True
p.add_run(
    ". Pemisahan sisi Front End dan Back End didefinisikan sebagai berikut:"
).font.name = "Arial"

# Front End List
p_fe = doc.add_paragraph()
r = p_fe.add_run("A. Sisi Front End (Tampilan Publik & Seluruh Anggota)")
r.font.bold = True
r.font.color.rgb = COLOR_SECONDARY
fe_items = [
    (
        "Menu Beranda & Masuk Kelompok (Join Group):",
        " Halaman utama anggota untuk mendaftar dan masuk ke grup arisan menggunakan Kode Kelompok.",
    ),
    (
        "Menu Kartu Undian Saya (My Lottery Ticket):",
        " Menampilkan nomor undian lot unik (#01, #02, dst.) dan status kemenangan anggota saat ini.",
    ),
    (
        "Menu Papan Transparansi Peserta (Live Roster):",
        " Menampilkan seluruh daftar anggota kelompok, membedakan siapa yang sudah pernah menang dan siapa yang masih mengantre.",
    ),
    (
        "Menu Ruang Nonton Pengundian (Live Draw Arena):",
        " Layar tontonan animasi siaran langsung pengocokan lot digital saat Ketua memutar undian.",
    ),
    (
        "Menu Galeri Kuitansi Digital (Official Receipts):",
        " Arsip bukti kuitansi elektronik pemenang pada setiap putaran periode yang dapat diunduh transparan.",
    ),
]
for title, desc in fe_items:
    bp = doc.add_paragraph(style="List Bullet")
    bp.paragraph_format.line_spacing = 1.15
    rt = bp.add_run(title)
    rt.font.bold = True
    bp.add_run(desc)

# Back End List
p_be = doc.add_paragraph()
r = p_be.add_run("B. Sisi Back End (Panel Kontrol Pengelolaan Ketua Kelompok / Host)")
r.font.bold = True
r.font.color.rgb = RGBColor(180, 83, 9)
be_items = [
    (
        "Menu Buat & Atur Kelompok Arisan (Group Settings):",
        " Form pembuatan kelompok arisan baru, penetapan nominal iuran, siklus undian, dan penerbitan Kode Undangan/QR.",
    ),
    (
        "Menu Kelola Anggota & Kunci Kuota (Manage Participants):",
        " Memvalidasi warga yang mendaftar, menerbitkan nomor lot otomatis, dan mengunci pendaftaran jika kuota penuh.",
    ),
    (
        "Menu Konsol Tombol Pengocokan (Host Draw Console):",
        " Tombol operasional khusus Ketua untuk memicu algoritma undian acak (hanya menyaring peserta yang belum menang).",
    ),
    (
        "Menu Terbitkan & Kunci Kuitansi (Issue & Lock Receipt):",
        " Mengesahkan pemenang, mengunci status menjadi 'Sudah Menang' agar tidak terundi ulang, dan menerbitkan kuitansi digital.",
    ),
    (
        "Menu Manajemen Periode & Tutup Buku (Group Lifecycle):",
        " Mengatur transisi ke periode berikutnya atau menutup dan mengarsipkan kelompok jika semua peserta telah menang.",
    ),
]
for title, desc in be_items:
    bp = doc.add_paragraph(style="List Bullet")
    bp.paragraph_format.line_spacing = 1.15
    rt = bp.add_run(title)
    rt.font.bold = True
    bp.add_run(desc)

# --- Section 2 ---
h2 = doc.add_paragraph()
r = h2.add_run("\n2. Fungsi dan Kegunaan Rinci Setiap Menu")
r.font.name = "Arial"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_PRIMARY

# Table of Menu Details
tbl_menu = doc.add_table(rows=1, cols=4)
tbl_menu.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_menu.autofit = False

hdr_cells = tbl_menu.rows[0].cells
headers = [
    "Sisi / Kategori",
    "Nama Menu",
    "Input Pengguna / Aksi",
    "Output / Hasil Menu",
]
widths = [Inches(1.2), Inches(1.8), Inches(1.8), Inches(1.8)]

for i, h_text in enumerate(headers):
    hdr_cells[i].width = widths[i]
    set_cell_background(hdr_cells[i], "1E40AF")
    set_cell_margins(hdr_cells[i], 120, 120, 150, 150)
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(9.5)

menu_details = [
    (
        "Front End",
        "Beranda & Masuk Kelompok",
        "Nama Lengkap, No WhatsApp, & Kode Kelompok",
        "Akses masuk ke ruang arisan & token sesi",
    ),
    (
        "Front End",
        "Kartu Undian Digital",
        "Memilih kelompok yang diikuti",
        "Tampilan kartu lot (#Lot, Nama, Status Kemenangan)",
    ),
    (
        "Front End",
        "Papan Transparansi",
        "Memilih kelompok yang aktif",
        "Daftar hadir peserta, status menang/belum, kuota",
    ),
    (
        "Front End",
        "Ruang Pengundian Live",
        "Menonton layar saat jam arisan",
        "Animasi acak lot dan pengumuman pemenang real-time",
    ),
    (
        "Front End",
        "Galeri Kuitansi Digital",
        "Filter periode kocokan",
        "Kuitansi digital sah (ID Transaksi, Total Uang, PDF)",
    ),
    (
        "Back End",
        "Buat & Atur Kelompok",
        "Nama Grup, Nominal Iuran, Jadwal Kocok",
        "ID Kelompok & Kode Undangan/QR Code aktif",
    ),
    (
        "Back End",
        "Kelola Anggota & Kuota",
        "Verifikasi pendaftar & Kunci Kuota",
        "Daftar lot terisi penuh & siap dikocok",
    ),
    (
        "Back End",
        "Konsol Pengocokan",
        "Klik tombol 'Kocok Pemenang'",
        "Trigger algoritma acak & penentuan 1 pemenang sah",
    ),
    (
        "Back End",
        "Terbitkan Kuitansi",
        "Catatan serah terima & tombol 'Sah'",
        "Kunci status '__status_menang = True' & publish bukti",
    ),
    (
        "Back End",
        "Manajemen Periode",
        "Tombol 'Mulai Periode Baru' / 'Tutup'",
        "Update counter periode dan arsip kelompok",
    ),
]

for side, name, inp, outp in menu_details:
    row_cells = tbl_menu.add_row().cells
    for i, txt in enumerate([side, name, inp, outp]):
        row_cells[i].width = widths[i]
        set_cell_margins(row_cells[i], 100, 100, 140, 140)
        p = row_cells[i].paragraphs[0]
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(txt)
        r.font.size = Pt(9)
        if i == 0:
            set_cell_background(
                row_cells[i], "F0F9FF" if side == "Front End" else "FEF3C7"
            )
            r.font.bold = True
            r.font.color.rgb = (
                COLOR_SECONDARY if side == "Front End" else RGBColor(180, 83, 9)
            )

# --- Section 3 ---
h3 = doc.add_paragraph()
r = h3.add_run("\n3. Uraian Hak Akses Pengguna (Matrix Hak Akses)")
r.font.name = "Arial"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_PRIMARY

p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.15
p.add_run(
    "Hak akses dirancang secara terdistribusi berdasarkan kepemilikan kelompok (tanpa akun admin global):"
).font.name = "Arial"

tbl_role = doc.add_table(rows=1, cols=3)
tbl_role.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_role.autofit = False

hdr_cells = tbl_role.rows[0].cells
r_headers = [
    "Fitur / Menu Sistem",
    "Anggota Biasa (Peserta)",
    "Ketua Kelompok (Host / Pengocok)",
]
r_widths = [Inches(2.8), Inches(1.8), Inches(2.0)]

for i, h_text in enumerate(r_headers):
    hdr_cells[i].width = r_widths[i]
    set_cell_background(hdr_cells[i], "0F766E")
    set_cell_margins(hdr_cells[i], 120, 120, 150, 150)
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h_text)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)
    r.font.size = Pt(9.5)

role_data = [
    ("Masuk Kelompok & Lihat Kartu Lot", "Ya (Akses Bebas)", "Ya (Akses Bebas)"),
    ("Melihat Papan Transparansi Roster", "Ya (Hanya Melihat)", "Ya (Hanya Melihat)"),
    ("Menonton Pengundian Acak (Live)", "Ya (Hanya Menonton)", "Ya (Layar Monitor)"),
    ("Mengunduh Kuitansi Sah Digital", "Ya (Unduh PDF)", "Ya (Unduh PDF)"),
    (
        "Membuat Grup & Atur Nominal Iuran",
        "Tidak Ada Akses (Terkunci)",
        "Ya (Akses Penuh)",
    ),
    ("Mengunci Pendaftaran Peserta", "Tidak Ada Akses (Terkunci)", "Ya (Akses Penuh)"),
    (
        "Mengeksekusi Tombol Kocok Pemenang",
        "Tidak Ada Akses (Terkunci)",
        "Ya (Akses Eksklusif)",
    ),
    (
        "Mengesahkan & Mengunci Status Menang",
        "Tidak Ada Akses (Terkunci)",
        "Ya (Akses Eksklusif)",
    ),
    (
        "Menutup Buku & Selesaikan Arisan",
        "Tidak Ada Akses (Terkunci)",
        "Ya (Akses Penuh)",
    ),
]

for feat, r1, r2 in role_data:
    row_cells = tbl_role.add_row().cells
    for i, txt in enumerate([feat, r1, r2]):
        row_cells[i].width = r_widths[i]
        set_cell_margins(row_cells[i], 100, 100, 140, 140)
        p = row_cells[i].paragraphs[0]
        p.paragraph_format.line_spacing = 1.1
        r = p.add_run(txt)
        r.font.size = Pt(9)
        if i == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if "Tidak" in txt:
                r.font.color.rgb = RGBColor(220, 38, 38)
            else:
                r.font.color.rgb = COLOR_SECONDARY
        elif i == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r.font.bold = True
            r.font.color.rgb = RGBColor(30, 64, 175)

# --- Section 4 ---
h4 = doc.add_paragraph()
r = h4.add_run("\n4. Keterkaitan Setiap Menu dengan Proses Bisnis")
r.font.name = "Arial"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_PRIMARY

p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.15
p.add_run(
    "Keterkaitan menu dengan alur bisnis arisan dibagi menjadi 3 tahapan utama:"
).font.name = "Arial"

phases = [
    (
        "Tahap 1: Persiapan & Registrasi Peserta",
        [
            "Ketua membuka 'Menu Buat Kelompok' untuk menetapkan aturan main dan iuran per putaran.",
            "Ketua membagikan kode undangan grup ke para warga calon peserta.",
            "Peserta membuka 'Menu Beranda & Masuk Kelompok' untuk menginput identitas.",
            "Sistem otomatis mengalokasikan nomor undian via 'Menu Kartu Undian Digital'.",
            "Ketua memverifikasi roster peserta pada 'Menu Kelola Anggota' lalu mengunci kuota agar tidak bertambah.",
        ],
    ),
    (
        "Tahap 2: Hari-H Pelaksanaan Pengundian",
        [
            "Seluruh anggota berkumpul dan membuka 'Menu Ruang Pengundian Live'.",
            "Ketua membuka 'Menu Konsol Pengocokan' dan menekan tombol 'Kocok Pemenang'.",
            "Sistem menyaring daftar kandidat peserta yang belum menang secara objektif dan acak.",
            "Hasil pengocokan langsung disiarkan secara serentak ke layar seluruh anggota secara adil.",
        ],
    ),
    (
        "Tahap 3: Pengesahan Hadiah & Rekapitulasi",
        [
            "Ketua membuka 'Menu Terbitkan Kuitansi' untuk mengesahkan penerima uang arisan periode tersebut.",
            "Sistem secara permanen mengunci status menang (__status_menang = True) di database.",
            "Kuitansi elektronik otomatis terbit ke 'Menu Galeri Kuitansi Digital' dan dapat dicetak/diunduh.",
            "Peserta yang telah menang statusnya diperbarui pada 'Menu Papan Transparansi' dan tidak akan keluar di putaran berikutnya.",
        ],
    ),
]

for ph_title, points in phases:
    p_ph = doc.add_paragraph()
    r = p_ph.add_run(ph_title)
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_SECONDARY
    for pt in points:
        bp = doc.add_paragraph(style="List Bullet")
        bp.paragraph_format.line_spacing = 1.15
        bp.add_run(pt).font.size = Pt(9.5)

# --- Section 5 ---
h5 = doc.add_paragraph()
r = h5.add_run("\n5. Struktur Menu dalam Bentuk Gambar Sederhana")
r.font.name = "Arial"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_PRIMARY

p = doc.add_paragraph()
p.paragraph_format.line_spacing = 1.15
p.add_run(
    "Berikut adalah visualisasi struktur hierarki navigasi menu pada Sistem Arisan Digital:"
).font.name = "Arial"

# Embed Image
img_path = os.path.abspath("struktur_menu_arisan.png")
if os.path.exists(img_path):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture(img_path, width=Inches(6.2))
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = caption.add_run(
        "Gambar 1. Struktur Hierarki Menu Sistem Arisan Digital (Front End & Back End)"
    )
    r_cap.font.size = Pt(9)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

# Save DOCX
out_docx = "Rancangan_Menu_Aplikasi_Arisan.docx"
doc.save(out_docx)
print(f"File {out_docx} saved successfully.")
