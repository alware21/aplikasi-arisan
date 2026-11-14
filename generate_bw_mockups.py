import matplotlib.pyplot as plt
import matplotlib.patches as patches


def draw_rounded_rect(
    ax, x, y, w, h, bg="#ffffff", border="#000000", lw=1.2, radius=0.04, shadow=False
):
    if shadow:
        sh = patches.FancyBboxPatch(
            (x + 0.04, y - 0.04),
            w,
            h,
            boxstyle=f"round,pad=0.01,rounding_size={radius}",
            facecolor="#cccccc",
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


# ==============================================================================
# 1. FRONT END WIREFRAME (BLACK & WHITE)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6.8), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.8)
ax.axis("off")
fig.patch.set_facecolor("#ffffff")

# Window frame
wx, wy, ww, wh = 0.4, 0.3, 9.2, 6.2
draw_rounded_rect(
    ax, wx, wy, ww, wh, bg="#ffffff", border="#000000", lw=2.0, radius=0.08, shadow=True
)

# Titlebar (Black with white text)
draw_rounded_rect(
    ax, wx, wy + wh - 0.5, ww, 0.5, bg="#000000", border="#000000", radius=0.04
)
ax.text(
    wx + 0.25,
    wy + wh - 0.25,
    "Arisan Digital Desktop - Mode Anggota (Front End)",
    color="#ffffff",
    weight="bold",
    fontsize=11,
    va="center",
    zorder=5,
)
ax.text(
    wx + ww - 0.3,
    wy + wh - 0.25,
    "[ _ ] [ O ] [ X ]",
    color="#ffffff",
    fontsize=9,
    weight="bold",
    va="center",
    ha="right",
    zorder=5,
)

# Header Info Bar (White with light gray border)
draw_rounded_rect(
    ax, wx, wy + wh - 1.2, ww, 0.7, bg="#f8f8f8", border="#000000", lw=1.0, radius=0
)
ax.text(
    wx + 0.25,
    wy + wh - 0.75,
    "KELOMPOK AKTIF: Arisan Warga RT 05  |  KODE GRUP: RT05-2026",
    weight="bold",
    fontsize=9.5,
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + wh - 1.02,
    "Nominal Iuran: Rp 200.000 / Bulan  |  Periode Saat Ini: Putaran Ke-2",
    fontsize=8.8,
    color="#444444",
    zorder=5,
)

# User Badge in Header
draw_rounded_rect(
    ax,
    wx + ww - 3.2,
    wy + wh - 1.1,
    3.0,
    0.5,
    bg="#ffffff",
    border="#000000",
    lw=1.2,
    radius=0.05,
)
ax.text(
    wx + ww - 1.7,
    wy + wh - 0.85,
    "Profil: Ibu Siti Aminah (Lot #01)",
    fontsize=8.8,
    weight="bold",
    color="#000000",
    ha="center",
    va="center",
    zorder=5,
)

# Sidebar Left (Navigasi Menu Front End)
sb_w = 3.0
draw_rounded_rect(
    ax, wx, wy + 0.4, sb_w, wh - 1.6, bg="#f4f4f4", border="#000000", lw=1.2, radius=0
)
ax.text(
    wx + 0.2,
    wy + wh - 1.5,
    "NAVIGASI MENU PESERTA",
    weight="bold",
    fontsize=9,
    color="#000000",
    zorder=5,
)

fe_items = [
    ("[1] Beranda & Masuk Grup", False),
    ("[2] Kartu Undian Saya", False),
    ("[3] Papan Transparansi Roster", False),
    ("[4] Ruang Pengundian Live", True),  # Active menu
    ("[5] Galeri Kuitansi Digital", False),
]

for idx, (title, is_active) in enumerate(fe_items):
    iy = wy + wh - 2.1 - (idx * 0.65)
    if is_active:
        draw_rounded_rect(
            ax,
            wx + 0.15,
            iy,
            sb_w - 0.3,
            0.52,
            bg="#000000",
            border="#000000",
            lw=1.2,
            radius=0.05,
        )
        ax.text(
            wx + 0.3,
            iy + 0.26,
            title + "  [AKTIF]",
            weight="bold",
            fontsize=8.8,
            color="#ffffff",
            va="center",
            zorder=5,
        )
    else:
        draw_rounded_rect(
            ax,
            wx + 0.15,
            iy,
            sb_w - 0.3,
            0.52,
            bg="#ffffff",
            border="#888888",
            lw=1.0,
            radius=0.05,
        )
        ax.text(
            wx + 0.3,
            iy + 0.26,
            title,
            fontsize=8.8,
            color="#000000",
            va="center",
            zorder=5,
        )

# Sidebar Info Box
draw_rounded_rect(
    ax,
    wx + 0.15,
    wy + 0.6,
    sb_w - 0.3,
    1.4,
    bg="#ffffff",
    border="#000000",
    lw=1.0,
    radius=0.05,
)
ax.text(
    wx + 0.25,
    wy + 1.75,
    "Karakteristik Menu Front End:",
    weight="bold",
    fontsize=8,
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 1.45,
    "• Terletak di Sidebar Kiri layar.",
    fontsize=7.6,
    color="#333333",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 1.20,
    "• Dapat diakses seluruh anggota.",
    fontsize=7.6,
    color="#333333",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 0.95,
    "• Tidak memiliki tombol kocok",
    fontsize=7.6,
    weight="bold",
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 0.75,
    "  (Mencegah kecurangan undian).",
    fontsize=7.6,
    color="#555555",
    zorder=5,
)

# Main Content Area (Front End: Ruang Pengundian Live)
cx = wx + sb_w
cw = ww - sb_w

# Top Live Broadcast Area
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 2.6,
    cw - 0.4,
    2.3,
    bg="#fcfcfc",
    border="#000000",
    lw=1.2,
    radius=0.06,
)
ax.text(
    cx + cw / 2,
    wy + 4.65,
    "SIARAN PENGUNDIAN PUTARAN KE-2 (LIVE)",
    weight="bold",
    fontsize=11,
    color="#000000",
    ha="center",
    zorder=5,
)
ax.text(
    cx + cw / 2,
    wy + 4.35,
    "Menampilkan animasi acak saat pengocokan dilakukan oleh Ketua...",
    fontsize=8.5,
    color="#555555",
    ha="center",
    zorder=5,
)

# Lottery Ball (Black circle with white text)
ball = patches.Circle(
    (cx + cw / 2, wy + 3.45),
    0.65,
    facecolor="#000000",
    edgecolor="#000000",
    lw=2.0,
    zorder=4,
)
ax.add_patch(ball)
ax.text(
    cx + cw / 2,
    wy + 3.55,
    "#01",
    weight="bold",
    fontsize=14,
    color="#ffffff",
    ha="center",
    va="center",
    zorder=5,
)
ax.text(
    cx + cw / 2,
    wy + 3.20,
    "Ibu Siti Aminah",
    fontsize=7.5,
    color="#ffffff",
    ha="center",
    va="center",
    zorder=5,
)

draw_rounded_rect(
    ax,
    cx + 0.8,
    wy + 2.75,
    cw - 1.6,
    0.32,
    bg="#eeeeee",
    border="#000000",
    lw=1.0,
    radius=0.04,
)
ax.text(
    cx + cw / 2,
    wy + 2.91,
    "STATUS HASIL: SAH TERKUNCI  |  Total Hadiah: Rp 1.000.000",
    weight="bold",
    fontsize=8,
    color="#000000",
    ha="center",
    va="center",
    zorder=5,
)

# Bottom Candidate Roster Area
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 0.6,
    cw - 0.4,
    1.85,
    bg="#ffffff",
    border="#000000",
    lw=1.2,
    radius=0.06,
)
ax.text(
    cx + 0.4,
    wy + 2.2,
    "Papan Transparansi Kandidat Belum Menang:",
    weight="bold",
    fontsize=9,
    color="#000000",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 1.88,
    "• Lot #02 : Pak Budi Santoso      [Status: Mengantre]",
    fontsize=8.2,
    color="#222222",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 1.60,
    "• Lot #03 : Ibu Dewi Lestari      [Status: Mengantre]",
    fontsize=8.2,
    color="#222222",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 1.32,
    "• Lot #04 : Pak Ahmad Fauzi       [Status: Mengantre]",
    fontsize=8.2,
    color="#222222",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 0.95,
    "Transparansi: Seluruh peserta melihat pergerakan pemenang secara serentak.",
    fontsize=7.8,
    style="italic",
    color="#555555",
    zorder=5,
)

# Window Footer Bar
draw_rounded_rect(ax, wx, wy, ww, 0.4, bg="#eeeeee", border="#000000", lw=1.0, radius=0)
ax.text(
    wx + ww / 2,
    wy + 0.2,
    "Aplikasi Arisan Digital Desktop (Front End) | Hak Akses: Seluruh Anggota Peserta",
    fontsize=8,
    color="#333333",
    ha="center",
    va="center",
    zorder=5,
)

plt.tight_layout()
plt.savefig(
    "d:/herd/aplikasi_arisan/layout_menu_frontend.png", bbox_inches="tight", dpi=300
)
plt.savefig(
    "C:/Users/ThinkPad/Downloads/layout_menu_frontend.png", bbox_inches="tight", dpi=300
)
plt.close()
print("Front End B&W layout generated.")


# ==============================================================================
# 2. BACK END WIREFRAME (BLACK & WHITE)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6.8), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.8)
ax.axis("off")
fig.patch.set_facecolor("#ffffff")

# Window frame
draw_rounded_rect(
    ax, wx, wy, ww, wh, bg="#ffffff", border="#000000", lw=2.0, radius=0.08, shadow=True
)

# Titlebar
draw_rounded_rect(
    ax, wx, wy + wh - 0.5, ww, 0.5, bg="#000000", border="#000000", radius=0.04
)
ax.text(
    wx + 0.25,
    wy + wh - 0.25,
    "Arisan Digital Desktop - Panel Kontrol Ketua Kelompok (Back End)",
    color="#ffffff",
    weight="bold",
    fontsize=11,
    va="center",
    zorder=5,
)
ax.text(
    wx + ww - 0.3,
    wy + wh - 0.25,
    "[ _ ] [ O ] [ X ]",
    color="#ffffff",
    fontsize=9,
    weight="bold",
    va="center",
    ha="right",
    zorder=5,
)

# Header Info Bar
draw_rounded_rect(
    ax, wx, wy + wh - 1.2, ww, 0.7, bg="#f8f8f8", border="#000000", lw=1.0, radius=0
)
ax.text(
    wx + 0.25,
    wy + wh - 0.75,
    "PENGELOLAAN GRUP: Arisan Warga RT 05  |  KODE: RT05-2026",
    weight="bold",
    fontsize=9.5,
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + wh - 1.02,
    "Total Peserta: 4 Orang  |  Total Kas Terkumpul: Rp 1.000.000",
    fontsize=8.8,
    color="#444444",
    zorder=5,
)

# Ketua Role Badge
draw_rounded_rect(
    ax,
    wx + ww - 3.2,
    wy + wh - 1.1,
    3.0,
    0.5,
    bg="#000000",
    border="#000000",
    lw=1.2,
    radius=0.05,
)
ax.text(
    wx + ww - 1.7,
    wy + wh - 0.85,
    "★ PERAN: KETUA (HOST PENGOCOK)",
    fontsize=8.5,
    weight="bold",
    color="#ffffff",
    ha="center",
    va="center",
    zorder=5,
)

# Sidebar Left (Navigasi Menu Back End)
draw_rounded_rect(
    ax, wx, wy + 0.4, sb_w, wh - 1.6, bg="#f4f4f4", border="#000000", lw=1.2, radius=0
)
ax.text(
    wx + 0.2,
    wy + wh - 1.5,
    "PANEL KONTROL KETUA",
    weight="bold",
    fontsize=9,
    color="#000000",
    zorder=5,
)

be_items = [
    ("[1] Buat & Atur Kelompok", False),
    ("[2] Kelola Anggota & Kuota", False),
    ("[3] Konsol Tombol Kocokan", True),  # Active menu
    ("[4] Pengesahan & Kuitansi", False),
    ("[5] Tutup Buku & Selesai", False),
]

for idx, (title, is_active) in enumerate(be_items):
    iy = wy + wh - 2.1 - (idx * 0.65)
    if is_active:
        draw_rounded_rect(
            ax,
            wx + 0.15,
            iy,
            sb_w - 0.3,
            0.52,
            bg="#000000",
            border="#000000",
            lw=1.2,
            radius=0.05,
        )
        ax.text(
            wx + 0.3,
            iy + 0.26,
            title + "  [AKTIF]",
            weight="bold",
            fontsize=8.8,
            color="#ffffff",
            va="center",
            zorder=5,
        )
    else:
        draw_rounded_rect(
            ax,
            wx + 0.15,
            iy,
            sb_w - 0.3,
            0.52,
            bg="#ffffff",
            border="#888888",
            lw=1.0,
            radius=0.05,
        )
        ax.text(
            wx + 0.3,
            iy + 0.26,
            title,
            fontsize=8.8,
            color="#000000",
            va="center",
            zorder=5,
        )

# Sidebar Info Box
draw_rounded_rect(
    ax,
    wx + 0.15,
    wy + 0.6,
    sb_w - 0.3,
    1.4,
    bg="#ffffff",
    border="#000000",
    lw=1.0,
    radius=0.05,
)
ax.text(
    wx + 0.25,
    wy + 1.75,
    "Karakteristik Menu Back End:",
    weight="bold",
    fontsize=8,
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 1.45,
    "• Eksklusif laptop/akun Ketua.",
    fontsize=7.6,
    color="#333333",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 1.20,
    "• Otoritas penuh pengundian.",
    fontsize=7.6,
    color="#333333",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 0.95,
    "• Tombol eksekusi & kunci",
    fontsize=7.6,
    weight="bold",
    color="#000000",
    zorder=5,
)
ax.text(
    wx + 0.25,
    wy + 0.75,
    "  status kemenangan resmi.",
    fontsize=7.6,
    color="#555555",
    zorder=5,
)

# Main Content Area (Back End: Konsol Tombol Pengocokan)
# 1. Action Button: Kocok Pemenang
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 3.8,
    cw - 0.4,
    1.15,
    bg="#000000",
    border="#000000",
    lw=1.5,
    radius=0.06,
    shadow=True,
)
ax.text(
    cx + cw / 2,
    wy + 4.55,
    "[>] TEKAN TOMBOL KOCOK PEMENANG SEKARANG",
    weight="bold",
    fontsize=11,
    color="#ffffff",
    ha="center",
    zorder=5,
)
ax.text(
    cx + cw / 2,
    wy + 4.20,
    "Algoritma acak sistem otomatis menyaring peserta yang BELUM MENANG.",
    fontsize=8.2,
    color="#cccccc",
    ha="center",
    zorder=5,
)
ax.text(
    cx + cw / 2,
    wy + 3.95,
    "Peserta yang sudah menang pada putaran sebelumnya tidak akan terpilih lagi.",
    fontsize=8.2,
    color="#cccccc",
    ha="center",
    zorder=5,
)

# 2. Candidate Status Pool Box
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 2.1,
    cw - 0.4,
    1.55,
    bg="#f8f8f8",
    border="#000000",
    lw=1.2,
    radius=0.06,
)
ax.text(
    cx + 0.4,
    wy + 3.38,
    "Validasi Kandidat Memenuhi Syarat Pengundian (3 Peserta):",
    weight="bold",
    fontsize=8.8,
    color="#000000",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 3.08,
    "[✓] Lot #02 - Pak Budi Santoso      [Status: Iuran Lunas & Siap Diundi]",
    fontsize=8.0,
    color="#000000",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 2.82,
    "[✓] Lot #03 - Ibu Dewi Lestari      [Status: Iuran Lunas & Siap Diundi]",
    fontsize=8.0,
    color="#000000",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 2.56,
    "[✓] Lot #04 - Pak Ahmad Fauzi       [Status: Iuran Lunas & Siap Diundi]",
    fontsize=8.0,
    color="#000000",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 2.28,
    "[X] Lot #01 - Ibu Siti Aminah       [TERKUNCI: Sudah Pernah Menang Periode 1]",
    fontsize=8.0,
    weight="bold",
    color="#444444",
    zorder=5,
)

# 3. Action Button: Issue & Lock Receipt
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 1.35,
    cw - 0.4,
    0.62,
    bg="#ffffff",
    border="#000000",
    lw=1.6,
    radius=0.06,
)
ax.text(
    cx + cw / 2,
    wy + 1.72,
    "[KUNCI] SAHKAN PEMENANG & TERBITKAN KUITANSI ELEKTRONIK",
    weight="bold",
    fontsize=9.2,
    color="#000000",
    ha="center",
    zorder=5,
)
ax.text(
    cx + cw / 2,
    wy + 1.48,
    "Mengunci status '__status_menang = True' permanen dan mencatat ke database.",
    fontsize=7.8,
    color="#555555",
    ha="center",
    zorder=5,
)

# 4. Audit Log Summary
draw_rounded_rect(
    ax,
    cx + 0.2,
    wy + 0.6,
    cw - 0.4,
    0.65,
    bg="#f4f4f4",
    border="#888888",
    lw=1.0,
    radius=0.04,
)
ax.text(
    cx + 0.4,
    wy + 0.98,
    "Rekap Audit Transaksi: Putaran 1 sah dimenangkan oleh Ibu Siti Aminah (Kuitansi TRX-001).",
    fontsize=7.8,
    color="#222222",
    zorder=5,
)
ax.text(
    cx + 0.4,
    wy + 0.76,
    "Semua histori pengocokan tersimpan otomatis dan tidak dapat diubah tanpa otorisasi.",
    fontsize=7.5,
    style="italic",
    color="#555555",
    zorder=5,
)

# Window Footer Bar
draw_rounded_rect(ax, wx, wy, ww, 0.4, bg="#eeeeee", border="#000000", lw=1.0, radius=0)
ax.text(
    wx + ww / 2,
    wy + 0.2,
    "Aplikasi Arisan Digital Desktop (Back End) | Otoritas Penuh Ketua / Host Kelompok",
    fontsize=8,
    color="#333333",
    ha="center",
    va="center",
    zorder=5,
)

plt.tight_layout()
plt.savefig(
    "d:/herd/aplikasi_arisan/layout_menu_backend.png", bbox_inches="tight", dpi=300
)
plt.savefig(
    "C:/Users/ThinkPad/Downloads/layout_menu_backend.png", bbox_inches="tight", dpi=300
)
plt.close()
print("Back End B&W layout generated.")
