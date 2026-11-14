import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
ax.set_xlim(0, 15)
ax.set_ylim(0, 9.5)
ax.axis("off")
fig.patch.set_facecolor("#f1f5f9")


def draw_rect(
    x, y, w, h, bg="#ffffff", border="#cbd5e1", lw=1.2, radius=0.08, shadow=False
):
    if shadow:
        sh = patches.FancyBboxPatch(
            (x + 0.04, y - 0.04),
            w,
            h,
            boxstyle=f"round,pad=0.01,rounding_size={radius}",
            facecolor="#000000",
            alpha=0.07,
            edgecolor="none",
            zorder=2,
        )
        ax.add_patch(sh)
    rect = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.01,rounding_size={radius}",
        facecolor=bg,
        edgecolor=border,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(rect)


# Main Title & Subtitle
ax.text(
    0.5,
    9.15,
    "Rancangan Tata Letak (Layout) Posisi Menu Antarmuka",
    fontsize=15,
    weight="bold",
    color="#0f172a",
    zorder=5,
)
ax.text(
    0.5,
    8.85,
    "Posisi Menu Navigasi: Tampilan Anggota (Front End) vs Panel Kontrol Ketua Kelompok (Back End)",
    fontsize=10,
    color="#64748b",
    style="italic",
    zorder=5,
)

# ==============================================================================
# WINDOW 1: FRONT END (LEFT)
# ==============================================================================
wx1, wy1, ww, wh = 0.5, 0.4, 6.8, 8.2
draw_rect(
    wx1, wy1, ww, wh, bg="#ffffff", border="#0284c7", lw=1.8, radius=0.1, shadow=True
)

# Titlebar
draw_rect(wx1, wy1 + wh - 0.45, ww, 0.45, bg="#0284c7", border="#0284c7", radius=0.05)
ax.text(
    wx1 + 0.2,
    wy1 + wh - 0.23,
    "Arisan Digital - Mode Anggota (Front End)",
    color="#ffffff",
    weight="bold",
    fontsize=10.5,
    va="center",
    zorder=5,
)
ax.text(
    wx1 + ww - 0.3,
    wy1 + wh - 0.23,
    "[ _ ] [ O ] [ X ]",
    color="#ffffff",
    fontsize=8.5,
    weight="bold",
    va="center",
    ha="right",
    zorder=5,
)

# Top Info Bar
draw_rect(wx1, wy1 + wh - 1.05, ww, 0.6, bg="#f0f9ff", border="#bae6fd", radius=0)
ax.text(
    wx1 + 0.2,
    wy1 + wh - 0.65,
    "Grup: Arisan Warga RT 05  |  Kode Undangan: RT05-2026",
    weight="bold",
    fontsize=9.2,
    color="#0f172a",
    zorder=5,
)
ax.text(
    wx1 + 0.2,
    wy1 + wh - 0.90,
    "Nominal Iuran: Rp 200.000 / Bulan (Status: Aktif)",
    fontsize=8.2,
    color="#0369a1",
    zorder=5,
)
draw_rect(
    wx1 + ww - 2.4,
    wy1 + wh - 0.95,
    2.2,
    0.42,
    bg="#ffffff",
    border="#0284c7",
    radius=0.06,
)
ax.text(
    wx1 + ww - 1.3,
    wy1 + wh - 0.74,
    "Profil: Ibu Siti Aminah (Lot #01)",
    fontsize=8.2,
    weight="bold",
    color="#0284c7",
    ha="center",
    va="center",
    zorder=5,
)

# Sidebar Front End (Left Column)
sb_w = 2.4
draw_rect(wx1, wy1 + 0.4, sb_w, wh - 1.45, bg="#f8fafc", border="#e2e8f0", radius=0)
ax.text(
    wx1 + 0.15,
    wy1 + wh - 1.3,
    "NAVIGASI MENU PESERTA",
    weight="bold",
    fontsize=8.5,
    color="#0369a1",
    zorder=5,
)

fe_navs = [
    ("[1] Beranda & Masuk", False),
    ("[2] Kartu Undian Saya", False),
    ("[3] Papan Transparansi", False),
    ("[4] Ruang Pengundian Live", True),  # Active
    ("[5] Galeri Kuitansi Digital", False),
]

for idx, (lbl, active) in enumerate(fe_navs):
    ny = wy1 + wh - 1.85 - (idx * 0.58)
    if active:
        draw_rect(
            wx1 + 0.12,
            ny,
            sb_w - 0.24,
            0.46,
            bg="#e0f2fe",
            border="#0284c7",
            lw=1.5,
            radius=0.06,
        )
        ax.text(
            wx1 + 0.22,
            ny + 0.23,
            lbl + "  (AKTIF)",
            weight="bold",
            fontsize=8.2,
            color="#0284c7",
            va="center",
            zorder=5,
        )
    else:
        draw_rect(
            wx1 + 0.12,
            ny,
            sb_w - 0.24,
            0.46,
            bg="#ffffff",
            border="#cbd5e1",
            lw=1,
            radius=0.06,
        )
        ax.text(
            wx1 + 0.22,
            ny + 0.23,
            lbl,
            fontsize=8.2,
            color="#334155",
            va="center",
            zorder=5,
        )

# Sidebar Note Box
draw_rect(
    wx1 + 0.12, wy1 + 0.6, sb_w - 0.24, 1.4, bg="#ffffff", border="#e2e8f0", radius=0.06
)
ax.text(
    wx1 + 0.2,
    wy1 + 1.7,
    "Keterangan Posisi Menu:",
    weight="bold",
    fontsize=7.8,
    color="#0f172a",
    zorder=5,
)
ax.text(
    wx1 + 0.2,
    wy1 + 1.45,
    "- Menu terletak di Sidebar Kiri.",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)
ax.text(
    wx1 + 0.2,
    wy1 + 1.22,
    "- Memberikan navigasi cepat.",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)
ax.text(
    wx1 + 0.2,
    wy1 + 0.99,
    "- Peserta tidak memiliki tombol",
    fontsize=7.2,
    color="#dc2626",
    zorder=5,
)
ax.text(
    wx1 + 0.2,
    wy1 + 0.78,
    "  pengocokan (Aman/Terkunci).",
    fontsize=7.2,
    color="#dc2626",
    zorder=5,
)

# Main Content Area (Front End Active View: Ruang Pengundian Live)
cx1 = wx1 + sb_w
cw = ww - sb_w
draw_rect(
    cx1 + 0.15, wy1 + 3.7, cw - 0.3, 3.3, bg="#f0f9ff", border="#bae6fd", radius=0.08
)
ax.text(
    cx1 + cw / 2,
    wy1 + 6.7,
    "SIARAN PENGUNDIAN PUTARAN KE-2",
    weight="bold",
    fontsize=11,
    color="#0369a1",
    ha="center",
    zorder=5,
)
ax.text(
    cx1 + cw / 2,
    wy1 + 6.4,
    "Sedang dikocok secara live oleh Ketua Kelompok...",
    fontsize=8,
    color="#64748b",
    ha="center",
    zorder=5,
)

# Lottery Ball Animation Graphic
circle = patches.Circle(
    (cx1 + cw / 2, wy1 + 5.2),
    0.85,
    facecolor="#0284c7",
    edgecolor="#0369a1",
    lw=2.5,
    zorder=4,
)
ax.add_patch(circle)
ax.text(
    cx1 + cw / 2,
    wy1 + 5.35,
    "#01",
    weight="bold",
    fontsize=16,
    color="#ffffff",
    ha="center",
    va="center",
    zorder=5,
)
ax.text(
    cx1 + cw / 2,
    wy1 + 4.85,
    "Ibu Siti Aminah",
    fontsize=8.2,
    color="#ffffff",
    ha="center",
    va="center",
    zorder=5,
)

draw_rect(
    cx1 + 0.6, wy1 + 3.9, cw - 1.2, 0.35, bg="#dcfce7", border="#16a34a", radius=0.05
)
ax.text(
    cx1 + cw / 2,
    wy1 + 4.07,
    "STATUS: PEMENANG SAH  |  Hadiah: Rp 1.000.000",
    weight="bold",
    fontsize=7.8,
    color="#15803d",
    ha="center",
    va="center",
    zorder=5,
)

# Candidate Roster Box in Content
draw_rect(
    cx1 + 0.15, wy1 + 0.6, cw - 0.3, 2.9, bg="#f8fafc", border="#cbd5e1", radius=0.08
)
ax.text(
    cx1 + 0.35,
    wy1 + 3.2,
    "Papan Ringkasan Kandidat Mengantre:",
    weight="bold",
    fontsize=8.5,
    color="#0f172a",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 2.85,
    "- Lot #02 : Pak Budi Santoso   (Status: Menunggu Kocokan)",
    fontsize=7.8,
    color="#334155",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 2.55,
    "- Lot #03 : Ibu Dewi Lestari   (Status: Menunggu Kocokan)",
    fontsize=7.8,
    color="#334155",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 2.25,
    "- Lot #04 : Pak Ahmad Fauzi    (Status: Menunggu Kocokan)",
    fontsize=7.8,
    color="#334155",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 1.85,
    "Catatan Keterbukaan:",
    weight="bold",
    fontsize=7.8,
    color="#0284c7",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 1.55,
    "Seluruh anggota dapat menyaksikan animasi secara real-time,",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)
ax.text(
    cx1 + 0.35,
    wy1 + 1.35,
    "namun otorisasi pengocokan sepenuhnya berada di layar Ketua.",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)

# Bottom Status Footer (FE)
draw_rect(wx1, wy1, ww, 0.4, bg="#f1f5f9", border="#e2e8f0", radius=0)
ax.text(
    wx1 + ww / 2,
    wy1 + 0.2,
    "Aplikasi Arisan Digital Desktop (Front End) | Terhubung ke Ruang Acara",
    fontsize=7.5,
    color="#64748b",
    ha="center",
    va="center",
    zorder=5,
)


# ==============================================================================
# WINDOW 2: BACK END (RIGHT)
# ==============================================================================
wx2 = 7.7
draw_rect(
    wx2, wy1, ww, wh, bg="#ffffff", border="#d97706", lw=1.8, radius=0.1, shadow=True
)

# Titlebar
draw_rect(wx2, wy1 + wh - 0.45, ww, 0.45, bg="#d97706", border="#d97706", radius=0.05)
ax.text(
    wx2 + 0.2,
    wy1 + wh - 0.23,
    "Arisan Digital - Panel Kontrol Ketua Kelompok (Back End)",
    color="#ffffff",
    weight="bold",
    fontsize=10.5,
    va="center",
    zorder=5,
)
ax.text(
    wx2 + ww - 0.3,
    wy1 + wh - 0.23,
    "[ _ ] [ O ] [ X ]",
    color="#ffffff",
    fontsize=8.5,
    weight="bold",
    va="center",
    ha="right",
    zorder=5,
)

# Top Info Bar
draw_rect(wx2, wy1 + wh - 1.05, ww, 0.6, bg="#fffbeb", border="#fde68a", radius=0)
ax.text(
    wx2 + 0.2,
    wy1 + wh - 0.65,
    "KONTROL GRUP: Arisan Warga RT 05",
    weight="bold",
    fontsize=9.2,
    color="#0f172a",
    zorder=5,
)
ax.text(
    wx2 + 0.2,
    wy1 + wh - 0.90,
    "Putaran: Periode Ke-2  |  Total Kas Hadiah: Rp 1.000.000",
    fontsize=8.2,
    color="#b45309",
    zorder=5,
)
draw_rect(
    wx2 + ww - 2.4,
    wy1 + wh - 0.95,
    2.2,
    0.42,
    bg="#ffffff",
    border="#d97706",
    radius=0.06,
)
ax.text(
    wx2 + ww - 1.3,
    wy1 + wh - 0.74,
    "Peran: Ketua (Host Pengocok)",
    fontsize=8.2,
    weight="bold",
    color="#d97706",
    ha="center",
    va="center",
    zorder=5,
)

# Sidebar Back End (Left Column of Window 2)
draw_rect(wx2, wy1 + 0.4, sb_w, wh - 1.45, bg="#f8fafc", border="#e2e8f0", radius=0)
ax.text(
    wx2 + 0.15,
    wy1 + wh - 1.3,
    "PANEL KONTROL KETUA",
    weight="bold",
    fontsize=8.5,
    color="#b45309",
    zorder=5,
)

be_navs = [
    ("[1] Buat & Atur Kelompok", False),
    ("[2] Kelola Anggota & Kuota", False),
    ("[3] Konsol Tombol Kocokan", True),  # Active
    ("[4] Pengesahan & Kuitansi", False),
    ("[5] Tutup Buku & Selesai", False),
]

for idx, (lbl, active) in enumerate(be_navs):
    ny = wy1 + wh - 1.85 - (idx * 0.58)
    if active:
        draw_rect(
            wx2 + 0.12,
            ny,
            sb_w - 0.24,
            0.46,
            bg="#fef3c7",
            border="#d97706",
            lw=1.5,
            radius=0.06,
        )
        ax.text(
            wx2 + 0.22,
            ny + 0.23,
            lbl + "  (AKTIF)",
            weight="bold",
            fontsize=8.2,
            color="#d97706",
            va="center",
            zorder=5,
        )
    else:
        draw_rect(
            wx2 + 0.12,
            ny,
            sb_w - 0.24,
            0.46,
            bg="#ffffff",
            border="#cbd5e1",
            lw=1,
            radius=0.06,
        )
        ax.text(
            wx2 + 0.22,
            ny + 0.23,
            lbl,
            fontsize=8.2,
            color="#334155",
            va="center",
            zorder=5,
        )

# Sidebar Note Box (BE)
draw_rect(
    wx2 + 0.12, wy1 + 0.6, sb_w - 0.24, 1.4, bg="#ffffff", border="#e2e8f0", radius=0.06
)
ax.text(
    wx2 + 0.2,
    wy1 + 1.7,
    "Keterangan Posisi Menu:",
    weight="bold",
    fontsize=7.8,
    color="#0f172a",
    zorder=5,
)
ax.text(
    wx2 + 0.2,
    wy1 + 1.45,
    "- Menu terletak di Sidebar Kiri.",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)
ax.text(
    wx2 + 0.2,
    wy1 + 1.22,
    "- Eksklusif untuk Ketua Grup.",
    fontsize=7.2,
    color="#64748b",
    zorder=5,
)
ax.text(
    wx2 + 0.2,
    wy1 + 0.99,
    "- Berisi tombol operasional",
    fontsize=7.2,
    color="#d97706",
    zorder=5,
)
ax.text(
    wx2 + 0.2,
    wy1 + 0.78,
    "  pengocokan & kunci status.",
    fontsize=7.2,
    color="#d97706",
    zorder=5,
)

# Main Content Area (Back End Active View: Konsol Tombol Pengocokan)
cx2 = wx2 + sb_w
draw_rect(
    cx2 + 0.15,
    wy1 + 5.6,
    cw - 0.3,
    1.4,
    bg="#d97706",
    border="#b45309",
    radius=0.08,
    shadow=True,
)
ax.text(
    cx2 + cw / 2,
    wy1 + 6.5,
    "[>] TEKAN TOMBOL KOCOK PEMENANG SEKARANG",
    weight="bold",
    fontsize=10.5,
    color="#ffffff",
    ha="center",
    zorder=5,
)
ax.text(
    cx2 + cw / 2,
    wy1 + 6.1,
    "Sistem secara otomatis memilih 1 pemenang acak",
    fontsize=8.5,
    color="#fffbeb",
    ha="center",
    zorder=5,
)
ax.text(
    cx2 + cw / 2,
    wy1 + 5.8,
    "dari daftar peserta yang berstatus BELUM MENANG.",
    fontsize=8.5,
    color="#fffbeb",
    ha="center",
    zorder=5,
)

# Candidate Pool Status Box
draw_rect(
    cx2 + 0.15, wy1 + 3.4, cw - 0.3, 2.0, bg="#fffbeb", border="#fde68a", radius=0.08
)
ax.text(
    cx2 + 0.35,
    wy1 + 5.1,
    "Panel Validasi Kandidat Siap Diundi (3 Orang):",
    weight="bold",
    fontsize=8.5,
    color="#0f172a",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 4.75,
    "[V] Lot #02 - Pak Budi Santoso   (Iuran Lunas - Memenuhi Syarat)",
    fontsize=7.8,
    color="#16a34a",
    weight="bold",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 4.45,
    "[V] Lot #03 - Ibu Dewi Lestari   (Iuran Lunas - Memenuhi Syarat)",
    fontsize=7.8,
    color="#16a34a",
    weight="bold",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 4.15,
    "[V] Lot #04 - Pak Ahmad Fauzi    (Iuran Lunas - Memenuhi Syarat)",
    fontsize=7.8,
    color="#16a34a",
    weight="bold",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 3.75,
    "[X] Lot #01 - Ibu Siti Aminah    (TERKUNCI: Sudah Pernah Menang)",
    fontsize=7.8,
    color="#dc2626",
    weight="bold",
    zorder=5,
)

# Second Action Button: Issue Receipt
draw_rect(
    cx2 + 0.15,
    wy1 + 2.5,
    cw - 0.3,
    0.75,
    bg="#1e293b",
    border="#0f172a",
    radius=0.08,
    shadow=True,
)
ax.text(
    cx2 + cw / 2,
    wy1 + 3.0,
    "[KUNCI] SAHKAN PEMENANG & TERBITKAN KUITANSI DIGITAL",
    weight="bold",
    fontsize=8.8,
    color="#ffffff",
    ha="center",
    zorder=5,
)
ax.text(
    cx2 + cw / 2,
    wy1 + 2.7,
    "Kunci status '__status_menang = True' permanen ke database lokal",
    fontsize=7.8,
    color="#94a3b8",
    ha="center",
    zorder=5,
)

# Audit Log Box
draw_rect(
    cx2 + 0.15, wy1 + 0.6, cw - 0.3, 1.75, bg="#f8fafc", border="#cbd5e1", radius=0.08
)
ax.text(
    cx2 + 0.35,
    wy1 + 2.05,
    "Catatan Rekap Riwayat Transaksi:",
    weight="bold",
    fontsize=8.2,
    color="#0f172a",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 1.75,
    "- Putaran 1: Dimenangkan oleh Ibu Siti Aminah (Kuitansi #TRX-001)",
    fontsize=7.5,
    color="#334155",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 1.45,
    "- Putaran 2: Sedang siap dieksekusi pengocokannya hari ini",
    fontsize=7.5,
    color="#334155",
    zorder=5,
)
ax.text(
    cx2 + 0.35,
    wy1 + 1.15,
    "- Semua transaksi otomatis tersimpan di tabel riwayat_kocokan",
    fontsize=7.5,
    color="#64748b",
    zorder=5,
)

# Bottom Status Footer (BE)
draw_rect(wx2, wy1, ww, 0.4, bg="#f1f5f9", border="#e2e8f0", radius=0)
ax.text(
    wx2 + ww / 2,
    wy1 + 0.2,
    "Aplikasi Arisan Digital Desktop (Back End) | Otoritas Penuh Ketua / Host Kelompok",
    fontsize=7.5,
    color="#64748b",
    ha="center",
    va="center",
    zorder=5,
)

plt.tight_layout()
plt.savefig(
    "d:/herd/aplikasi_arisan/struktur_menu_arisan.png", bbox_inches="tight", dpi=300
)
plt.savefig(
    "C:/Users/ThinkPad/Downloads/struktur_menu_arisan.png", bbox_inches="tight", dpi=300
)
print("Rendered clean UI layout mockup diagram successfully.")
