import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
ax.set_xlim(0, 13)
ax.set_ylim(0, 9)
ax.axis("off")

# Draw.io background canvas color
fig.patch.set_facecolor("#f8fafc")


def draw_drawio_box(
    x,
    y,
    w,
    h,
    title,
    subtitle=None,
    bg_color="#ffffff",
    border_color="#cbd5e1",
    title_color="#0f172a",
    sub_color="#64748b",
    is_header=False,
    align="left",
):
    # Subtle drop shadow
    shadow = patches.FancyBboxPatch(
        (x + 0.04, y - 0.04),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor="#000000",
        alpha=0.06,
        edgecolor="none",
        zorder=2,
    )
    ax.add_patch(shadow)

    # Main box
    rect = patches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.6,
        zorder=3,
    )
    ax.add_patch(rect)

    if is_header:
        ax.text(
            x + w / 2,
            y + h * 0.62,
            title,
            ha="center",
            va="center",
            fontsize=11,
            weight="bold",
            color=title_color,
            zorder=4,
        )
        if subtitle:
            ax.text(
                x + w / 2,
                y + h * 0.28,
                subtitle,
                ha="center",
                va="center",
                fontsize=9,
                color=sub_color,
                zorder=4,
            )
    else:
        if align == "center":
            ax.text(
                x + w / 2,
                y + h * 0.62,
                title,
                ha="center",
                va="center",
                fontsize=10,
                weight="bold",
                color=title_color,
                zorder=4,
            )
            if subtitle:
                ax.text(
                    x + w / 2,
                    y + h * 0.28,
                    subtitle,
                    ha="center",
                    va="center",
                    fontsize=8.5,
                    color=sub_color,
                    zorder=4,
                )
        else:
            ax.text(
                x + 0.25,
                y + h * 0.64,
                title,
                ha="left",
                va="center",
                fontsize=9.8,
                weight="bold",
                color=title_color,
                zorder=4,
            )
            if subtitle:
                ax.text(
                    x + 0.25,
                    y + h * 0.30,
                    subtitle,
                    ha="left",
                    va="center",
                    fontsize=8.2,
                    color=sub_color,
                    zorder=4,
                )


# Top Title & Subtitle (Draw.io canvas style)
ax.text(
    0.6,
    8.45,
    "Struktur Hierarki Menu: Sistem Aplikasi Arisan Digital",
    fontsize=15,
    weight="bold",
    color="#0f172a",
    zorder=5,
)
ax.text(
    0.6,
    8.12,
    "Perancangan Menu: Berbasis Peran Ketua Kelompok (Host) vs Anggota Biasa (Peserta) Tanpa Superadmin",
    fontsize=9.8,
    color="#64748b",
    style="italic",
    zorder=5,
)

# Top Right Legend Box
draw_drawio_box(
    9.2,
    7.85,
    3.2,
    0.75,
    "■ Front End: Akses Seluruh Peserta",
    "■ Back End: Akses Eksklusif Ketua (Host)",
    bg_color="#ffffff",
    border_color="#cbd5e1",
    title_color="#0284c7",
    sub_color="#d97706",
    align="center",
)

# ROOT NODE (Dark Theme)
draw_drawio_box(
    4.2,
    6.85,
    4.6,
    0.8,
    "Sistem Aplikasi Arisan Digital",
    "Arsitektur Navigasi Berbasis Kelompok (Group/Room Role)",
    bg_color="#1e293b",
    border_color="#0f172a",
    title_color="#ffffff",
    sub_color="#94a3b8",
    is_header=True,
)

# Connectors: Root to FE & BE
ax.plot(
    [5.2, 5.2, 2.9, 2.9], [6.85, 6.45, 6.45, 6.2], color="#64748b", lw=1.8, zorder=1
)
ax.plot(
    [7.8, 7.8, 10.1, 10.1], [6.85, 6.45, 6.45, 6.2], color="#64748b", lw=1.8, zorder=1
)

# FRONT END Parent Node (Blue)
draw_drawio_box(
    0.6,
    5.45,
    4.6,
    0.75,
    "FRONT END (Tampilan Anggota)",
    "Dapat Diakses Bebas oleh Seluruh Peserta Arisan",
    bg_color="#0284c7",
    border_color="#0369a1",
    title_color="#ffffff",
    sub_color="#e0f2fe",
    is_header=True,
)

# BACK END Parent Node (Amber)
draw_drawio_box(
    7.8,
    5.45,
    4.6,
    0.75,
    "BACK END (Panel Ketua Kelompok)",
    "Hak Akses Khusus Ketua Kelompok (Host / Pengocok)",
    bg_color="#d97706",
    border_color="#b45309",
    title_color="#ffffff",
    sub_color="#fef3c7",
    is_header=True,
)

# FE Items
fe_items = [
    (
        "1. Beranda & Masuk Kelompok (Join Group)",
        "Input Nama, No. WhatsApp, dan Kode Undangan / QR Grup",
    ),
    (
        "2. Kartu Undian Digital (My Lottery Ticket)",
        "Menampilkan Nomor Undian Lot Unik (#01, #02) & Status Menang",
    ),
    (
        "3. Papan Transparansi Peserta (Live Roster)",
        "Daftar seluruh peserta: membedakan yang sudah menang & belum",
    ),
    (
        "4. Ruang Nonton Pengundian (Live Draw Arena)",
        "Layar tontonan animasi live saat Ketua memutar undian lot digital",
    ),
    (
        "5. Galeri Kuitansi Digital (Official Receipts)",
        "Arsip kuitansi resmi pemenang tiap periode & unduh bukti PDF sah",
    ),
]

# BE Items
be_items = [
    (
        "1. Buat & Atur Kelompok Arisan (Group Settings)",
        "Form buat kelompok baru, nominal iuran, jadwal, & kode undangan",
    ),
    (
        "2. Kelola Anggota & Kunci Kuota (Manage Participants)",
        "Verifikasi pendaftar, alokasi nomor lot, & kunci kuota grup",
    ),
    (
        "3. Konsol Tombol Pengocokan (Host Draw Console)",
        "Tombol picu undian acak (hanya menyaring peserta belum menang)",
    ),
    (
        "4. Pengesahan & Penerbitan Kuitansi (Issue Receipt)",
        "Kunci status __status_menang = True & terbitkan kuitansi digital",
    ),
    (
        "5. Manajemen Periode & Tutup Buku (Lifecycle)",
        "Pindah putaran berikutnya (Periode 2, 3) atau tutup & arsipkan grup",
    ),
]

y_start = 4.45
y_gap = 0.85

for i, (title, subtitle) in enumerate(fe_items):
    y = y_start - (i * y_gap)
    draw_drawio_box(
        0.6,
        y,
        4.6,
        0.68,
        title,
        subtitle,
        bg_color="#f0f9ff",
        border_color="#0284c7",
        title_color="#0369a1",
        sub_color="#64748b",
    )
    # Connector line from FE
    ax.plot([2.9, 2.9], [5.45, y + 0.34], color="#0284c7", lw=1.2, ls="--", zorder=1)

for i, (title, subtitle) in enumerate(be_items):
    y = y_start - (i * y_gap)
    draw_drawio_box(
        7.8,
        y,
        4.6,
        0.68,
        title,
        subtitle,
        bg_color="#fffbeb",
        border_color="#d97706",
        title_color="#b45309",
        sub_color="#64748b",
    )
    # Connector line from BE
    ax.plot([10.1, 10.1], [5.45, y + 0.34], color="#d97706", lw=1.2, ls="--", zorder=1)

# Draw.io Watermark Footer
ax.text(
    6.5,
    0.35,
    "Diagram dibuat dengan Draw.io (Diagrams.net) | Format: .drawio XML",
    ha="center",
    va="center",
    fontsize=8.5,
    color="#94a3b8",
    style="italic",
)

plt.tight_layout()
plt.savefig(
    "d:/herd/aplikasi_arisan/struktur_menu_arisan.png", bbox_inches="tight", dpi=300
)
print("Image rendered successfully.")
