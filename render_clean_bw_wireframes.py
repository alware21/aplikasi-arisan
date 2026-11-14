import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set clean default font
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]


def draw_wireframe(
    title_window,
    header_left,
    header_right,
    sidebar_title,
    menu_list,
    active_idx,
    content_type,
    filename,
):
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 620)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    # 1. Main Window Border (Desktop Frame)
    rect_main = patches.Rectangle(
        (30, 20), 940, 580, linewidth=2, edgecolor="#000000", facecolor="#ffffff"
    )
    ax.add_patch(rect_main)

    # 2. Window Titlebar
    rect_tb = patches.Rectangle(
        (30, 565), 940, 35, linewidth=1.5, edgecolor="#000000", facecolor="#000000"
    )
    ax.add_patch(rect_tb)
    ax.text(
        50, 582, title_window, color="#ffffff", fontsize=11, weight="bold", va="center"
    )
    ax.text(
        945,
        582,
        "[ - ]  [ # ]  [ X ]",
        color="#ffffff",
        fontsize=10,
        weight="bold",
        va="center",
        ha="right",
    )

    # 3. Top Info Bar (Under Titlebar)
    rect_top = patches.Rectangle(
        (30, 515), 940, 50, linewidth=1, edgecolor="#000000", facecolor="#f5f5f5"
    )
    ax.add_patch(rect_top)
    ax.text(
        50, 540, header_left, color="#000000", fontsize=10, weight="bold", va="center"
    )

    # User / Role Badge
    rect_badge = patches.Rectangle(
        (710, 523), 240, 34, linewidth=1, edgecolor="#000000", facecolor="#ffffff"
    )
    ax.add_patch(rect_badge)
    ax.text(
        830,
        540,
        header_right,
        color="#000000",
        fontsize=9.5,
        weight="bold",
        va="center",
        ha="center",
    )

    # 4. Left Sidebar (Menu Navigation)
    rect_sb = patches.Rectangle(
        (30, 20), 250, 495, linewidth=1, edgecolor="#000000", facecolor="#fafafa"
    )
    ax.add_patch(rect_sb)

    # Sidebar Header
    ax.text(
        50, 485, sidebar_title, color="#000000", fontsize=10, weight="bold", va="center"
    )
    line_sb = patches.ConnectionPatch(
        (45, 470), (265, 470), "data", "data", linewidth=1, edgecolor="#000000"
    )
    ax.add_patch(line_sb)

    # Menu items
    y_start = 420
    y_gap = 52
    for i, m_name in enumerate(menu_list):
        y_pos = y_start - (i * y_gap)
        is_active = i == active_idx

        # Menu box
        if is_active:
            m_box = patches.Rectangle(
                (45, y_pos),
                220,
                40,
                linewidth=2,
                edgecolor="#000000",
                facecolor="#e5e5e5",
            )
            ax.add_patch(m_box)
            ax.text(
                60,
                y_pos + 20,
                m_name,
                color="#000000",
                fontsize=9.5,
                weight="bold",
                va="center",
            )
            ax.text(
                250,
                y_pos + 20,
                ">",
                color="#000000",
                fontsize=11,
                weight="bold",
                va="center",
                ha="right",
            )
        else:
            m_box = patches.Rectangle(
                (45, y_pos),
                220,
                40,
                linewidth=1,
                edgecolor="#888888",
                facecolor="#ffffff",
            )
            ax.add_patch(m_box)
            ax.text(60, y_pos + 20, m_name, color="#333333", fontsize=9.5, va="center")

    # Sidebar Bottom Info Box
    rect_note = patches.Rectangle(
        (45, 40), 220, 85, linewidth=1, edgecolor="#000000", facecolor="#ffffff"
    )
    ax.add_patch(rect_note)
    ax.text(
        55,
        105,
        "Keterangan Posisi:",
        fontsize=8.5,
        weight="bold",
        color="#000000",
        va="center",
    )
    ax.text(55, 85, "- Menu di Sidebar Kiri.", fontsize=8, color="#333333", va="center")
    if content_type == "fe":
        ax.text(
            55, 68, "- Akses seluruh anggota.", fontsize=8, color="#333333", va="center"
        )
        ax.text(
            55,
            52,
            "- Mode tampilan tontonan.",
            fontsize=8,
            color="#333333",
            va="center",
        )
    else:
        ax.text(
            55, 68, "- Khusus akun Ketua.", fontsize=8, color="#333333", va="center"
        )
        ax.text(
            55,
            52,
            "- Memiliki tombol undian.",
            fontsize=8,
            color="#333333",
            va="center",
        )

    # 5. Right Content Area (Main Panel)
    if content_type == "fe":
        # --- FRONT END CONTENT ---
        # Area Box: Live Draw Animation
        rect_c1 = patches.Rectangle(
            (305, 230),
            645,
            265,
            linewidth=1.5,
            edgecolor="#000000",
            facecolor="#ffffff",
        )
        ax.add_patch(rect_c1)
        ax.text(
            627,
            465,
            "SIARAN PENGUNDIAN (PUTARAN KE-2)",
            color="#000000",
            fontsize=11,
            weight="bold",
            va="center",
            ha="center",
        )
        ax.text(
            627,
            442,
            "Menampilkan hasil putaran undian secara real-time",
            color="#555555",
            fontsize=9,
            va="center",
            ha="center",
        )

        # Circle Lot Result
        circle = patches.Circle(
            (627, 345), 52, linewidth=2, edgecolor="#000000", facecolor="#f0f0f0"
        )
        ax.add_patch(circle)
        ax.text(
            627,
            355,
            "Lot #01",
            color="#000000",
            fontsize=14,
            weight="bold",
            va="center",
            ha="center",
        )
        ax.text(
            627,
            330,
            "Ibu Siti",
            color="#000000",
            fontsize=9.5,
            va="center",
            ha="center",
        )

        # Status badge below circle
        rect_st = patches.Rectangle(
            (477, 250), 300, 28, linewidth=1, edgecolor="#000000", facecolor="#e5e5e5"
        )
        ax.add_patch(rect_st)
        ax.text(
            627,
            264,
            "Status: Pemenang Sah (Terkunci)",
            color="#000000",
            fontsize=9,
            weight="bold",
            va="center",
            ha="center",
        )

        # Area Box: Candidate Queue Roster
        rect_c2 = patches.Rectangle(
            (305, 40), 645, 175, linewidth=1.5, edgecolor="#000000", facecolor="#ffffff"
        )
        ax.add_patch(rect_c2)
        ax.text(
            325,
            190,
            "Daftar Peserta Belum Menang (Mengantre):",
            color="#000000",
            fontsize=9.5,
            weight="bold",
            va="center",
        )

        # Simple clean table rows
        candidates = [
            ("Lot #02", "Pak Budi Santoso", "Status: Menunggu Putaran Berikutnya"),
            ("Lot #03", "Ibu Dewi Lestari", "Status: Menunggu Putaran Berikutnya"),
            ("Lot #04", "Pak Ahmad Fauzi", "Status: Menunggu Putaran Berikutnya"),
        ]
        for idx, (c_lot, c_name, c_st) in enumerate(candidates):
            ry = 145 - (idx * 35)
            row_rect = patches.Rectangle(
                (325, ry),
                605,
                26,
                linewidth=1,
                edgecolor="#cccccc",
                facecolor="#fdfdfd",
            )
            ax.add_patch(row_rect)
            ax.text(
                340,
                ry + 13,
                c_lot,
                color="#000000",
                fontsize=9,
                weight="bold",
                va="center",
            )
            ax.text(430, ry + 13, c_name, color="#000000", fontsize=9, va="center")
            ax.text(700, ry + 13, c_st, color="#555555", fontsize=8.5, va="center")

        ax.text(
            325,
            55,
            "* Layar ini tidak menyediakan tombol kocokan demi menjaga integritas data.",
            color="#555555",
            fontsize=8,
            style="italic",
            va="center",
        )

    else:
        # --- BACK END CONTENT ---
        # Area 1: Primary Action Button (Big Clean Button)
        rect_btn = patches.Rectangle(
            (305, 410), 645, 85, linewidth=2, edgecolor="#000000", facecolor="#000000"
        )
        ax.add_patch(rect_btn)
        ax.text(
            627,
            462,
            "[ TEKAN TOMBOL KOCOK UNDIAN ]",
            color="#ffffff",
            fontsize=12,
            weight="bold",
            va="center",
            ha="center",
        )
        ax.text(
            627,
            432,
            "Sistem memilih 1 pemenang acak dari daftar peserta yang belum menang",
            color="#e0e0e0",
            fontsize=9,
            va="center",
            ha="center",
        )

        # Area 2: Candidate Validation Box
        rect_pool = patches.Rectangle(
            (305, 200),
            645,
            195,
            linewidth=1.5,
            edgecolor="#000000",
            facecolor="#ffffff",
        )
        ax.add_patch(rect_pool)
        ax.text(
            325,
            370,
            "Validasi Peserta Siap Diundi (Putaran Ke-2):",
            color="#000000",
            fontsize=9.5,
            weight="bold",
            va="center",
        )

        rows_be = [
            ("[ V ]", "Lot #02 - Pak Budi Santoso", "Iuran Lunas - Memenuhi Syarat"),
            ("[ V ]", "Lot #03 - Ibu Dewi Lestari", "Iuran Lunas - Memenuhi Syarat"),
            ("[ V ]", "Lot #04 - Pak Ahmad Fauzi", "Iuran Lunas - Memenuhi Syarat"),
            ("[ X ]", "Lot #01 - Ibu Siti Aminah", "Terkunci: Sudah Pernah Menang"),
        ]
        for idx, (tag, name, status) in enumerate(rows_be):
            ry = 325 - (idx * 30)
            row_bg = "#f5f5f5" if idx == 3 else "#ffffff"
            row_rect = patches.Rectangle(
                (325, ry), 605, 24, linewidth=1, edgecolor="#cccccc", facecolor=row_bg
            )
            ax.add_patch(row_rect)
            ax.text(
                340,
                ry + 12,
                tag,
                color="#000000",
                fontsize=9,
                weight="bold",
                va="center",
            )
            ax.text(390, ry + 12, name, color="#000000", fontsize=9, va="center")
            ax.text(680, ry + 12, status, color="#555555", fontsize=8.5, va="center")

        # Area 3: Secondary Action Button: Kunci & Kuitansi
        rect_btn2 = patches.Rectangle(
            (305, 115), 645, 65, linewidth=1.5, edgecolor="#000000", facecolor="#f0f0f0"
        )
        ax.add_patch(rect_btn2)
        ax.text(
            627,
            155,
            "[ KUNCI PEMENANG & TERBITKAN KUITANSI ]",
            color="#000000",
            fontsize=10.5,
            weight="bold",
            va="center",
            ha="center",
        )
        ax.text(
            627,
            132,
            "Kunci status '__status_menang = True' secara permanen di database",
            color="#555555",
            fontsize=8.5,
            va="center",
            ha="center",
        )

        # Area 4: Audit summary note
        rect_audit = patches.Rectangle(
            (305, 40), 645, 60, linewidth=1, edgecolor="#888888", facecolor="#fafafa"
        )
        ax.add_patch(rect_audit)
        ax.text(
            325,
            80,
            "Riwayat Transaksi:",
            color="#000000",
            fontsize=8.5,
            weight="bold",
            va="center",
        )
        ax.text(
            325,
            60,
            "Putaran 1 telah selesai (Pemenang: Ibu Siti Aminah - Kuitansi #TRX-001).",
            color="#555555",
            fontsize=8,
            va="center",
        )

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Generated {filename}")


# Generate Front End
fe_menus = [
    "1. Beranda Kelompok",
    "2. Kartu Undian Saya",
    "3. Papan Transparansi",
    "4. Ruang Pengundian Live",
    "5. Galeri Kuitansi",
]
draw_wireframe(
    title_window="Aplikasi Arisan Digital - Layar Anggota (Front End)",
    header_left="Kelompok: Arisan Warga RT 05  |  Iuran: Rp 200.000",
    header_right="Profil: Ibu Siti (Anggota)",
    sidebar_title="MENU PESERTA",
    menu_list=fe_menus,
    active_idx=3,
    content_type="fe",
    filename="d:/herd/aplikasi_arisan/layout_menu_frontend.png",
)

# Generate Back End
be_menus = [
    "1. Atur Kelompok",
    "2. Kelola Anggota",
    "3. Konsol Pengocokan",
    "4. Pengesahan Kuitansi",
    "5. Tutup Periode",
]
draw_wireframe(
    title_window="Aplikasi Arisan Digital - Panel Ketua Kelompok (Back End)",
    header_left="Kelompok: Arisan Warga RT 05  |  Total Kas: Rp 1.000.000",
    header_right="Peran: Ketua (Host)",
    sidebar_title="MENU KETUA",
    menu_list=be_menus,
    active_idx=2,
    content_type="be",
    filename="d:/herd/aplikasi_arisan/layout_menu_backend.png",
)

import shutil

shutil.copy2(
    "d:/herd\aplikasi_arisan/layout_menu_frontend.png",
    "C:/Users/ThinkPad/Downloads/layout_menu_frontend.png",
)
shutil.copy2(
    "d:/herd\aplikasi_arisan/layout_menu_backend.png",
    "C:/Users/ThinkPad/Downloads/layout_menu_backend.png",
)
print("Copied cleanly to Downloads.")
