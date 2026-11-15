import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from PIL import Image
import win32com.client
import subprocess

# Matikan proses Word jika masih ada di background agar tidak permission lock
subprocess.run(["powershell", "-Command", "Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force"], check=False)

doc = docx.Document()

# ==========================================
# 1. PAGE SETUP (STANDAR AKADEMIK INDONESIA A4: 4-3-3-3 CM)
# ==========================================
for section in doc.sections:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(4.0)
    section.top_margin = Cm(3.0)
    section.right_margin = Cm(3.0)
    section.bottom_margin = Cm(3.0)

# Warna Teks: Hitam Murni (No AI Blue!)
COLOR_BLACK = RGBColor(0, 0, 0)
COLOR_GRAY = RGBColor(80, 80, 80)

def set_run_font(run, name="Times New Roman", size=12, bold=False, italic=False, color=COLOR_BLACK):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    # Ensure Word displays Times New Roman in eastAsia / cs fonts
    rPr = run._r.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:cs'), name)
    rPr.append(rFonts)

def add_p(text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15, bold=False, italic=False, size=12):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        set_run_font(r, name="Times New Roman", size=size, bold=bold, italic=italic, color=COLOR_BLACK)
    return p

def add_heading_1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, name="Times New Roman", size=13, bold=True, color=COLOR_BLACK)
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, name="Times New Roman", size=12, bold=True, color=COLOR_BLACK)
    return p

def set_cell_properties(cell, fill_hex=None, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, size=11):
    tcPr = cell._tc.get_or_add_tcPr()
    if fill_hex:
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)
    # Border abu-abu tipis bersih
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    for p in cell.paragraphs:
        p.alignment = align
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.0
        for r in p.runs:
            set_run_font(r, name="Times New Roman", size=size, bold=bold, color=COLOR_BLACK)

def add_image_with_caption(img_path, caption_text, width_in_inches=5.8):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        set_run_font(r_cap, name="Times New Roman", size=10.5, bold=True, italic=True, color=COLOR_GRAY)

# ==========================================
# 2. HEADER LAPORAN (STANDAR MAHASISWA)
# ==========================================
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(0)
p_title.paragraph_format.space_after = Pt(4)
r = p_title.add_run("LAPORAN PROGRESS PENGERJAAN PROYEK")
set_run_font(r, size=14, bold=True)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(16)
r = p_sub.add_run("PENGEMBANGAN SISTEM APLIKASI ARISAN DIGITAL MULTI-PLATFORM\n(DESKTOP & MOBILE RESPONSIVE)")
set_run_font(r, size=12, bold=True)

# Garis Pembatas Kop Hitam Bersih
p_line = doc.add_paragraph()
p_line.paragraph_format.space_before = Pt(0)
p_line.paragraph_format.space_after = Pt(12)
pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="000000"/></w:pBdr>')
p_line._p.get_or_add_pPr().append(pBdr)

# Identitas Mahasiswa & Tugas
p_meta = add_p(align=WD_ALIGN_PARAGRAPH.LEFT, space_after=14)
r = p_meta.add_run("Mata Kuliah\t: ")
set_run_font(r, bold=True)
r = p_meta.add_run("Pemrograman Berorientasi Objek (PBO) / Proyek Rekayasa Perangkat Lunak\n")
set_run_font(r)
r = p_meta.add_run("Dosen Pengampu\t: ")
set_run_font(r, bold=True)
r = p_meta.add_run("Zuliar Efendi, M.Kom.\n")
set_run_font(r)
r = p_meta.add_run("Topik Progres\t: ")
set_run_font(r, bold=True)
r = p_meta.add_run("Implementasi Antarmuka (Front-End & Back-End), Integrasi Basis Data, dan Finalisasi Fungsionalitas Sistem")
set_run_font(r)

# ==========================================
# 3. POIN 1: PROGRESS YANG DIKERJAKAN
# ==========================================
add_heading_1("1. PROGRESS PENGERJAAN: INTEGRASI BASIS DATA & IMPLEMENTASI ANTARMUKA")

p_intro = add_p()
r = p_intro.add_run(
    "Menindaklanjuti progres pengerjaan pada pertemuan minggu sebelumnya yang telah menyelesaikan tahapan perancangan konsep "
    "Pemrograman Berorientasi Objek (pemodelan class, encapsulation, constructor, dan relasi class) serta perancangan skema relasi basis data dasar, "
    "maka pada minggu ini progres utama difokuskan pada "
)
r1 = p_intro.add_run("implementasi penuh antarmuka sistem (Front-End dan Back-End)")
set_run_font(r1, bold=True)
r2 = p_intro.add_run(" secara responsif (mendukung layar Desktop maupun Mobile Smartphone) serta ")
r3 = p_intro.add_run("mengintegrasikan seluruh tabel basis data ke dalam antarmuka sistem nyata")
set_run_font(r3, bold=True)
r4 = p_intro.add_run(" sehingga aplikasi dapat langsung beroperasi secara utuh.")

add_heading_2("1.1. Implementasi Antarmuka Sistem (Desktop & Mobile Responsive)")
p_ui = add_p()
p_ui.add_run(
    "Antarmuka aplikasi dibangun menggunakan arsitektur antarmuka modern yang bersih, intuitif, dan responsif. "
    "Sistem dirancang adaptif untuk dua mode penggunaan pengguna, yaitu:"
)

# Bullet list fitur UI
p_b1 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
r = p_b1.add_run("a. Panel Kontrol Ketua Kelompok (Back-End / Desktop Dashboard):\n")
set_run_font(r, bold=True)
p_b1.add_run(
    "Dikhususkan untuk pengurus atau ketua arisan melalui komputer/laptop. Panel ini menampilkan informasi komprehensif grup, "
    "antara lain: nama kelompok arisan, kode room unik, nominal iuran mingguan/bulanan, total uang kas terkumpul, target pot per periode, "
    "serta menu manajemen anggota (Tambah Anggota Baru, Ruang Kocokan Live, dan Riwayat & Kas)."
)

add_image_with_caption("d:/herd/aplikasi_arisan/tampilan_desktop_dashboard.png", "Gambar 1. Tampilan Antarmuka Panel Kontrol Ketua pada Layar Desktop (Back-End)")

p_b2 = add_p(align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
r = p_b2.add_run("b. Antarmuka Peserta / Anggota (Front-End / Mobile Smartphone):\n")
set_run_font(r, bold=True)
p_b2.add_run(
    "Didesain khusus untuk smartphone anggota arisan agar dapat memantau jalannya arisan secara fleksibel. "
    "Antarmuka mobile mengusung tema bersih dengan bilah navigasi bawah (bottom navigation bar) yang memudahkan jempol pengguna, "
    "informasi putaran berjalan, tombol pintas 'Masuk Ruang Pengundian Live', 'Undang via WhatsApp', serta 'Salin Link Room' "
    "tanpa membebani memori smartphone."
)

add_image_with_caption("d:/herd/aplikasi_arisan/tampilan_mobile_dashboard.png", "Gambar 2. Tampilan Antarmuka Responsif pada Layar Smartphone Mobile (Front-End)", width_in_inches=3.0)

add_heading_2("1.2. Integrasi dan Pembuktian Relasi Basis Data pada Sistem")
p_db = add_p()
p_db.add_run(
    "Seluruh komponen pada tampilan antarmuka di atas telah terhubung secara langsung (real-time data binding) "
    "dengan skema basis data relasional. Struktur basis data terdiri atas entitas utama yang saling terhubung:"
)

p_db_list = add_p()
r = p_db_list.add_run("1. Tabel kelompok_arisan (Tabel Master Grup): ")
set_run_font(r, bold=True)
p_db_list.add_run("Menyimpan data identitas kelompok, nominal iuran (Rp 20.000), siklus setoran, putaran berikutnya, dan kode room acak (contoh: #STPKL9 atau #7A7UT9).\n")
r = p_db_list.add_run("2. Tabel anggota (Tabel Data Induk Peserta): ")
set_run_font(r, bold=True)
p_db_list.add_run("Menyimpan profil warga/anggota arisan beserta nomor kontak.\n")
r = p_db_list.add_run("3. Tabel peserta_arisan (Tabel Transaksi Relasi Many-to-Many): ")
set_run_font(r, bold=True)
p_db_list.add_run("Menghubungkan anggota dengan kelompok arisan tertentu, mencatat nomor undian lot serta status kemenangan (Belum Menang / Sudah Menang).\n")
r = p_db_list.add_run("4. Tabel riwayat_kocokan & transaksi_kas: ")
set_run_font(r, bold=True)
p_db_list.add_run("Mencatat sejarah pemenang setiap putaran secara otomatis, mengunci nomor yang sudah keluar, dan membukukan arus kas pembayaran iuran.")

add_image_with_caption("d:/herd/aplikasi_arisan/phpmyadmin_designer_relasi.png", "Gambar 3. Skema dan Relasi Antartabel Basis Data pada phpMyAdmin Designer", width_in_inches=5.8)

p_db_proof = add_p()
p_db_proof.add_run(
    "Integrasi basis data ini terbukti berjalan sempurna pada dashboard di Gambar 1, di mana sistem melakukan kalkulasi relasional otomatis:\n"
    "• Total Anggota = 1 Warga (dihitung dari relasi tabel peserta_arisan).\n"
    "• Target Pot Periode = Rp 20.000 (hasil perkalian otomatis: jumlah warga × nominal iuran per anggota).\n"
    "• Uang Kas Terkumpul = Rp 20.000 (akumulasi pembayaran yang berstatus lunas).\n"
    "• Sisa Belum Lunas = Rp 0 (validasi otomatis dari buku kas sistem)."
)

# ==========================================
# 4. POIN 2: PEKERJAAN LAIN DI LUAR DATABASE & INTERFACE
# ==========================================
add_heading_1("2. REALISASI FITUR SISTEM DAN FUNGSIONALITAS LAINNYA")

p_other = add_p()
p_other.add_run(
    "Di samping penyelesaian desain antarmuka dan pengkoneksian basis data, berikut adalah daftar pencapaian fungsionalitas sistem "
    "yang telah berhasil dibangun, diuji, dan diselesaikan hingga siap dioperasikan:"
)

# Sub-poin fitur sistem
add_heading_2("2.1. Implementasi Operasi CRUD Lengkap (Create, Read, Update, Delete)")
p_crud = add_p()
p_crud.add_run(
    "Sistem telah menerapkan operasi manipulasi data berbasis objek secara penuh:\n"
    "• Create: Penambahan kelompok arisan baru secara instan, pendaftaran warga/peserta baru, dan pembuatan nomor lot undian otomatis.\n"
    "• Read: Pelacakan daftar peserta, visualisasi riwayat undian lampau, dan pembacaan saldo kas kelompok secara transparan.\n"
    "• Update: Pembaharuan status pembayaran iuran warga (lunas/belum), pergantian status putaran, dan mutasi saldo kas.\n"
    "• Delete: Fitur pembatalan atau penghapusan data anggota yang keliru sebelum periode pengocokan dimulai."
)

add_heading_2("2.2. Mesin Pengundian Acak dengan Penguncian Status (Deterministic Randomization & State Locking)")
p_spin = add_p()
p_spin.add_run(
    "Fitur inti dari aplikasi arisan adalah pengocokan lot undian yang adil dan transparan. "
    "Sistem mengimplementasikan logika pengacakan berbasis server yang hanya mengikutsertakan peserta berstatus 'Belum Menang'. "
    "Begitu seorang pemenang terpilih melalui animasi roda roulette interaktif, sistem secara otomatis melakukan "
    "State Locking (penguncian status) pada database agar pemenang tersebut tidak dapat terpilih kembali pada putaran berikutnya "
    "sampai seluruh anggota kelompok selesai mendapatkan gilirannya."
)

add_heading_2("2.3. Generator Kuitansi Digital Otomatis")
p_receipt = add_p()
p_receipt.add_run(
    "Sebagai bukti keabsahan transaksi sosial, sistem secara otomatis menghasilkan dokumen kuitansi digital resmi setiap kali "
    "seorang pemenang keluar. Kuitansi memuat kode transaksi acak, nama pemenang, nominal uang yang berhak diterima, tanggal pengocokan, "
    "dan tanda tangan digital ketua kelompok yang dapat diunduh atau dibagikan secara langsung."
)

add_heading_2("2.4. Integrasi Pustaka HTMX Lokal (Modern & Super Ringan)")
p_htmx = add_p()
p_htmx.add_run(
    "Untuk memastikan performa aplikasi sangat mulus dan bebas lag pada smartphone anggota, sistem mengintegrasikan pustaka HTMX "
    "yang disimpan secara lokal di direktori statis (static/js/htmx.min.js, 50 KB). HTMX memungkinkan pembaruan data secara parsial "
    "tanpa perlu melakukan reload halaman browser penuh, memberikan pengalaman pengguna setara aplikasi Single Page Application (SPA) "
    "namun tetap hemat memori."
)

add_heading_2("2.5. Packaging Multi-Platform: Eksekusi Desktop (.EXE) dan Mobile Android Asli (.APK)")
p_pack = add_p()
p_pack.add_run(
    "Aplikasi tidak hanya berjalan di lingkungan kode pengembang (localhost server), melainkan telah berhasil dikompilasi menjadi dua berkas mandiri:\n"
    "1. Berkas Desktop Windows (ArisanDigital.exe, 183 MB): Paket biner mandiri yang membungkus server Django, Python Runtime, "
    "dan SQLite lokal sehingga dapat langsung dijalankan pada laptop/PC pengurus tanpa perlu instalasi Python tambahan.\n"
    "2. Berkas Android Asli (ArisanDigital.apk, 7.13 MB): Paket aplikasi resmi Android yang telah ditandatangani secara kriptografis "
    "(v1, v2, v3 Signature Scheme) dengan bilah status putih bersih (seamless borderless) dan ikon logo emas resmi."
)

add_heading_2("2.6. Arsitektur Adaptif dan Deployment Cloud Publik")
p_cloud = add_p()
p_cloud.add_run(
    "Sistem dirancang dengan fleksibilitas tinggi menggunakan arsitektur adaptif:\n"
    "• Mode Online Cloud: Aplikasi telah resmi di-deploy secara langsung pada server awan publik dan dapat diakses melalui URL: "
    "https://alware21.pythonanywhere.com/portal/ oleh dosen maupun pengguna di mana pun berada secara real-time.\n"
    "• Mode Offline Hotspot: Ketika berada di lokasi tanpa koneksi internet, aplikasi dapat beralih menggunakan jaringan Wi-Fi Hotspot lokal "
    "milik laptop/HP Ketua, sehingga anggota dapat tetap mengakses arisan dengan kuota 0 pulsa."
)

# ==========================================
# 5. TABEL REKAPITULASI PROGRES
# ==========================================
add_heading_1("3. TABEL REKAPITULASI STATUS PENGERJAAN SISTEM")

p_tbl_intro = add_p()
p_tbl_intro.add_run("Berikut adalah tabel ringkasan status implementasi seluruh modul pada proyek Aplikasi Arisan Digital:")

table = doc.add_table(rows=1, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

hdr_cells = table.rows[0].cells
headers = ["No", "Modul / Komponen Sistem", "Hasil Pengerjaan", "Status"]
widths = [Cm(1.2), Cm(5.0), Cm(5.5), Cm(2.3)]

for idx, text in enumerate(headers):
    hdr_cells[idx].text = text
    hdr_cells[idx].width = widths[idx]
    set_cell_properties(hdr_cells[idx], fill_hex="E5E7EB", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=10.5)

data = [
    ("1", "Perancangan Basis Data", "Struktur 4 tabel utama, relasi ForeignKey, & index", "Selesai 100%"),
    ("2", "Antarmuka Desktop (Back-End)", "Dashboard Ketua, Panel Kas, Ruang Kocokan", "Selesai 100%"),
    ("3", "Antarmuka Mobile (Front-End)", "Desain responsif, Bottom Tab Bar, Status Putih", "Selesai 100%"),
    ("4", "Operasi CRUD Data", "Manajemen anggota, kelompok, dan riwayat setoran", "Selesai 100%"),
    ("5", "Mesin Pengundian (Roulette)", "Algoritma acak + penguncian status pemenang", "Selesai 100%"),
    ("6", "Generator Kuitansi", "Penerbitan kuitansi digital 3D otomatis", "Selesai 100%"),
    ("7", "Optimasi HTMX Lokal", "Partial update tanpa reload halaman", "Selesai 100%"),
    ("8", "Deployment Cloud Publik", "Hosting live di alware21.pythonanywhere.com", "Selesai 100%"),
    ("9", "Build Installer Windows", "File ArisanDigital.exe mandiri (183 MB)", "Selesai 100%"),
    ("10", "Build Installer Android", "File ArisanDigital.apk resmi v3 (7.13 MB)", "Selesai 100%")
]

for row_data in data:
    row_cells = table.add_row().cells
    for c_idx, val in enumerate(row_data):
        row_cells[c_idx].text = val
        row_cells[c_idx].width = widths[c_idx]
        c_align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
        set_cell_properties(row_cells[c_idx], fill_hex=None, bold=(c_idx==3), align=c_align, size=10)

# ==========================================
# 6. PENUTUP & TANDA TANGAN LAPORAN
# ==========================================
p_close = add_p(space_before=14)
p_close.add_run(
    "Demikian laporan kemajuan ini disusun dengan sebenar-benarnya sebagai dokumentasi progres tugas besar mata kuliah Pemrograman "
    "Berorientasi Objek. Seluruh sistem telah selesai dibangun, terintegrasi, dan siap untuk dipresentasikan serta diuji coba."
)

p_sign_date = add_p(align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=16, space_after=2)
p_sign_date.add_run("Pekanbaru, 15 November 2026")

p_sign_role = add_p(align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=0, space_after=40)
p_sign_role.add_run("Mahasiswa Pengembang Sistem,")

p_sign_name = add_p(align=WD_ALIGN_PARAGRAPH.RIGHT, space_before=0, space_after=0)
r_name = p_sign_name.add_run("( Tim Pengembang Arisan Digital )")
set_run_font(r_name, bold=True)

# Save document
docx_path = r"D:\herd\aplikasi_arisan\Laporan_Progress_Arisan_Digital.docx"
pdf_path = r"D:\herd\aplikasi_arisan\Laporan_Progress_Arisan_Digital.pdf"

doc.save(docx_path)
print(f"File DOCX berhasil disimpan di: {docx_path}")

# ==========================================
# 7. EXPORT TO PDF VIA WINWORD COM
# ==========================================
try:
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word_doc = word.Documents.Open(os.path.abspath(docx_path))
    word_doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
    word_doc.Close()
    word.Quit()
    print(f"File PDF berhasil diekspor di: {pdf_path}")
except Exception as e:
    print(f"Gagal ekspor PDF otomatis: {e}")

print("SELESAI 100%!")
