import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
ax.set_xlim(0, 11)
ax.set_ylim(0, 8.2)
ax.axis("off")

# Background
fig.patch.set_facecolor("#ffffff")


# Helper function to draw rounded boxes
def draw_box(
    x,
    y,
    w,
    h,
    text,
    title=None,
    facecolor="#ffffff",
    edgecolor="#cbd5e1",
    textcolor="#0f172a",
    fontsize=9,
):
    rect = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=1.5,
        zorder=2,
    )
    ax.add_patch(rect)
    if title:
        ax.text(
            x + w / 2,
            y + h * 0.65,
            title,
            ha="center",
            va="center",
            fontsize=fontsize + 0.5,
            weight="bold",
            color=textcolor,
            zorder=3,
        )
        ax.text(
            x + w / 2,
            y + h * 0.30,
            text,
            ha="center",
            va="center",
            fontsize=fontsize - 1.2,
            color="#64748b",
            zorder=3,
        )
    else:
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",
            va="center",
            fontsize=fontsize,
            weight="bold",
            color=textcolor,
            zorder=3,
        )


# Title Header
ax.text(
    5.5,
    7.8,
    "STRUKTUR HIERARKI MENU SISTEM ARISAN DIGITAL",
    ha="center",
    va="center",
    fontsize=13,
    weight="bold",
    color="#1e293b",
)
ax.text(
    5.5,
    7.45,
    "Perancangan Menu: Berbasis Peran Ketua Kelompok (Host) vs Anggota Biasa (Peserta)",
    ha="center",
    va="center",
    fontsize=9.5,
    color="#64748b",
    style="italic",
)

# Root Node
draw_box(
    3.5,
    6.4,
    4.0,
    0.65,
    "",
    title="Sistem Aplikasi Arisan Digital",
    facecolor="#1e293b",
    edgecolor="#0f172a",
    textcolor="#ffffff",
    fontsize=10,
)

# Section Headers (FE & BE)
draw_box(
    0.5,
    5.1,
    4.6,
    0.75,
    "Dapat diakses oleh seluruh anggota peserta",
    title="FRONT END (Tampilan Anggota)",
    facecolor="#e0f2fe",
    edgecolor="#0284c7",
    textcolor="#0369a1",
    fontsize=9.5,
)
draw_box(
    5.9,
    5.1,
    4.6,
    0.75,
    "Hanya dapat diakses oleh Ketua Kelompok / Host",
    title="BACK END (Panel Ketua Kelompok)",
    facecolor="#fef3c7",
    edgecolor="#d97706",
    textcolor="#b45309",
    fontsize=9.5,
)

# Connect Root to Sections
ax.plot([5.5, 5.5], [6.4, 6.1], color="#94a3b8", lw=1.5, zorder=1)
ax.plot([2.8, 8.2], [6.1, 6.1], color="#94a3b8", lw=1.5, zorder=1)
ax.plot([2.8, 2.8], [6.1, 5.85], color="#94a3b8", lw=1.5, zorder=1)
ax.plot([8.2, 8.2], [6.1, 5.85], color="#94a3b8", lw=1.5, zorder=1)

# FE Menu Items
fe_menus = [
    ("1. Beranda & Masuk Kelompok", "Input Nama, No HP, & Kode Undangan Arisan"),
    ("2. Kartu Undian Digital", "Menampilkan Nomor Lot (#01, #02) & Status Menang"),
    ("3. Papan Transparansi Anggota", "Daftar seluruh peserta & status giliran menang"),
    (
        "4. Ruang Nonton Pengundian Live",
        "Animasi live pengocokan & pengumuman pemenang",
    ),
    ("5. Galeri Kuitansi Digital", "Arsip bukti sah & riwayat serah terima hadiah"),
]

# BE Menu Items
be_menus = [
    (
        "1. Buat & Atur Kelompok Arisan",
        "Set nama grup, nominal iuran, jadwal & kode grup",
    ),
    (
        "2. Kelola Anggota & Kunci Kuota",
        "Verifikasi anggota & kunci pendaftaran kelompok",
    ),
    ("3. Konsol Tombol Pengocokan", "Tombol picu undian acak (peserta belum menang)"),
    ("4. Pengesahan & Terbit Kuitansi", "Kunci status pemenang & cetak kuitansi resmi"),
    (
        "5. Manajemen Periode & Tutup Buku",
        "Kelola putaran berikutnya atau arsipkan grup",
    ),
]

y_start = 4.1
y_spacing = 0.8

for i, (title, desc) in enumerate(fe_menus):
    y = y_start - (i * y_spacing)
    draw_box(
        0.5,
        y,
        4.6,
        0.65,
        desc,
        title=title,
        facecolor="#f0f9ff",
        edgecolor="#bae6fd",
        textcolor="#0284c7",
        fontsize=8.5,
    )
    ax.plot([2.8, 2.8], [5.1, y + 0.32], color="#38bdf8", lw=1.2, ls="--", zorder=1)

for i, (title, desc) in enumerate(be_menus):
    y = y_start - (i * y_spacing)
    draw_box(
        5.9,
        y,
        4.6,
        0.65,
        desc,
        title=title,
        facecolor="#fffbeb",
        edgecolor="#fde68a",
        textcolor="#d97706",
        fontsize=8.5,
    )
    ax.plot([8.2, 8.2], [5.1, y + 0.32], color="#fbbf24", lw=1.2, ls="--", zorder=1)

plt.tight_layout()
plt.savefig("struktur_menu_arisan.png", bbox_inches="tight", dpi=300)
print("Diagram saved successfully to struktur_menu_arisan.png")
