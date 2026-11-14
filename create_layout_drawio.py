import os

drawio_content = """<mxfile host="65bd71144e">
    <diagram name="Rancangan Layout Menu Arisan" id="layout-menu-arisan">
        <mxGraphModel dx="1400" dy="950" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="1000" background="#f1f5f9" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- TITLE HEADER -->
                <mxCell id="title" value="Rancangan Layout Posisi Menu Antarmuka (Front End &amp; Back End)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=20;fontStyle=1;fontColor=#0f172a;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="40" y="20" width="800" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="subtitle" value="Tata Letak Komponen Navigasi Sistem Arisan Digital: Tampilan Anggota (Front End) vs Panel Ketua Kelompok (Back End)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=12;fontColor=#64748b;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="40" y="50" width="850" height="20" as="geometry"/>
                </mxCell>

                <!-- ============================================================ -->
                <!-- WINDOW 1: FRONT END (TAMPILAN PESERTA / ANGGOTA)              -->
                <!-- ============================================================ -->
                <mxCell id="fe_win" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0284c7;strokeWidth=2;shadow=1;" parent="1" vertex="1">
                    <mxGeometry x="40" y="90" width="680" height="840" as="geometry"/>
                </mxCell>

                <!-- Window 1 Title Bar -->
                <mxCell id="fe_titlebar" value="&lt;b&gt;Arisan Digital - Mode Anggota (Front End)&lt;/b&gt;" style="rounded=1;arcSize=0;whiteSpace=wrap;html=1;fillColor=#0284c7;strokeColor=#0284c7;fontColor=#ffffff;align=left;spacingLeft=15;fontSize=12;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="40" y="90" width="680" height="35" as="geometry"/>
                </mxCell>
                <!-- Window Controls -->
                <mxCell id="fe_ctrl" value="⚪ ⚪ ⚪" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#ffffff;spacingRight=10;" parent="1" vertex="1">
                    <mxGeometry x="640" y="95" width="70" height="25" as="geometry"/>
                </mxCell>

                <!-- Window 1 Topbar / Header Info -->
                <mxCell id="fe_topbar" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f0f9ff;strokeColor=#bae6fd;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="40" y="125" width="680" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="fe_grp_info" value="&lt;b&gt;Grup: Arisan Warga RT 05&lt;/b&gt; | Kode: &lt;b&gt;RT05-2026&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#0369a1&quot;&gt;Nominal Iuran: Rp 200.000 / Bulan&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#0f172a;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="40" y="130" width="350" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_user_badge" value="&lt;b&gt;Profil Saya: Ibu Siti Aminah&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#16a34a&quot;&gt;● Terdaftar (Lot #01)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0284c7;fontSize=10.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="510" y="132" width="190" height="36" as="geometry"/>
                </mxCell>

                <!-- Window 1 Left Sidebar (Menu Front End) -->
                <mxCell id="fe_sidebar" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#e2e8f0;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="40" y="175" width="220" height="715" as="geometry"/>
                </mxCell>
                <mxCell id="fe_menu_header" value="&lt;b style=&quot;color:#0369a1;&quot;&gt;NAVIGASI MENU PESERTA&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="40" y="185" width="220" height="25" as="geometry"/>
                </mxCell>

                <!-- FE Menu Items -->
                <mxCell id="fe_m1" value="🏠 1. Beranda / Masuk Kelompok" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="50" y="215" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m2" value="🎟️ 2. Kartu Undian Saya" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="50" y="265" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m3" value="👥 3. Papan Transparansi Roster" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="50" y="315" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m4" value="🎰 4. Ruang Pengundian Live (AKTIF)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e0f2fe;strokeColor=#0284c7;strokeWidth=2;align=left;spacingLeft=12;fontSize=11;fontStyle=1;fontColor=#0284c7;" parent="1" vertex="1">
                    <mxGeometry x="50" y="365" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m5" value="📄 5. Galeri Kuitansi Digital" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="50" y="415" width="200" height="40" as="geometry"/>
                </mxCell>

                <mxCell id="fe_sidebar_note" value="&lt;font color=&quot;#64748b&quot; style=&quot;font-size:10px;&quot;&gt;Sidebar di sisi kiri layar memudahkan peserta berpindah halaman dengan 1 klik.&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e2e8f0;align=center;spacing=8;" parent="1" vertex="1">
                    <mxGeometry x="50" y="780" width="200" height="90" as="geometry"/>
                </mxCell>

                <!-- FE Main Content Area (Layar Aktif Ruang Kocokan) -->
                <mxCell id="fe_content" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=none;" parent="1" vertex="1">
                    <mxGeometry x="260" y="175" width="460" height="715" as="geometry"/>
                </mxCell>
                <!-- Simulation of Active Screen Content -->
                <mxCell id="fe_arena_box" value="" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#f0f9ff;strokeColor=#bae6fd;strokeWidth=1.5;" parent="1" vertex="1">
                    <mxGeometry x="280" y="200" width="420" height="280" as="geometry"/>
                </mxCell>
                <mxCell id="fe_arena_title" value="&lt;b style=&quot;font-size:14px; color:#0369a1;&quot;&gt;🎉 SIARAN PENGUNDIAN PUTARAN KE-2 🎉&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#64748b&quot;&gt;Sedang dikocok oleh Ketua Kelompok...&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;" parent="1" vertex="1">
                    <mxGeometry x="280" y="215" width="420" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_ball" value="&lt;b style=&quot;font-size:24px; color:#ffffff;&quot;&gt;#01&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:12px; color:#ffffff;&quot;&gt;Ibu Siti Aminah&lt;/font&gt;" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#0284c7;strokeColor=#0369a1;strokeWidth=3;shadow=1;" parent="1" vertex="1">
                    <mxGeometry x="415" y="270" width="150" height="150" as="geometry"/>
                </mxCell>
                <mxCell id="fe_status_lock" value="&lt;b&gt;STATUS PEMENANG: TERKONFIRMASI SAH&lt;/b&gt;&lt;br&gt;Nominal Hadiah: Rp 1.000.000" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dcfce7;strokeColor=#16a34a;fontColor=#15803d;fontSize=11;align=center;" parent="1" vertex="1">
                    <mxGeometry x="340" y="430" width="300" height="35" as="geometry"/>
                </mxCell>

                <!-- FE Table of Candidates -->
                <mxCell id="fe_tbl_box" value="&lt;b&gt;Papan Ringkasan Kandidat Belum Menang:&lt;/b&gt;&lt;br&gt;• Lot #02 : Pak Budi Santoso (Mengantre)&lt;br&gt;• Lot #03 : Ibu Dewi Lestari (Mengantre)&lt;br&gt;• Lot #04 : Pak Ahmad Fauzi (Mengantre)&lt;br&gt;&lt;font color=&quot;#0369a1&quot;&gt;&lt;b&gt;Peserta tidak memiliki tombol kocok (Hanya Mode Tonton)&lt;/b&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;align=left;spacingLeft=15;fontSize=11;lineHeight=1.4;" parent="1" vertex="1">
                    <mxGeometry x="280" y="500" width="420" height="130" as="geometry"/>
                </mxCell>

                <!-- FE Footer Bar -->
                <mxCell id="fe_footer" value="Aplikasi Arisan Digital Desktop (Front End) | Sistem Terkoneksi Lokal" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#e2e8f0;fontColor=#64748b;fontSize=10;align=center;" parent="1" vertex="1">
                    <mxGeometry x="40" y="890" width="680" height="40" as="geometry"/>
                </mxCell>


                <!-- ============================================================ -->
                <!-- WINDOW 2: BACK END (PANEL KONTROL KETUA KELOMPOK / HOST)      -->
                <!-- ============================================================ -->
                <mxCell id="be_win" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d97706;strokeWidth=2;shadow=1;" parent="1" vertex="1">
                    <mxGeometry x="760" y="90" width="680" height="840" as="geometry"/>
                </mxCell>

                <!-- Window 2 Title Bar -->
                <mxCell id="be_titlebar" value="&lt;b&gt;Arisan Digital - Panel Kontrol Ketua Kelompok (Back End)&lt;/b&gt;" style="rounded=1;arcSize=0;whiteSpace=wrap;html=1;fillColor=#d97706;strokeColor=#d97706;fontColor=#ffffff;align=left;spacingLeft=15;fontSize=12;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="760" y="90" width="680" height="35" as="geometry"/>
                </mxCell>
                <!-- Window Controls -->
                <mxCell id="be_ctrl" value="⚪ ⚪ ⚪" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=10;fontColor=#ffffff;spacingRight=10;" parent="1" vertex="1">
                    <mxGeometry x="1360" y="95" width="70" height="25" as="geometry"/>
                </mxCell>

                <!-- Window 2 Topbar / Header Info -->
                <mxCell id="be_topbar" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#fde68a;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="760" y="125" width="680" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="be_grp_info" value="&lt;b&gt;KONTROL GRUP: Arisan Warga RT 05&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#b45309&quot;&gt;Putaran: Periode Ke-2 | Kas Hadiah: Rp 1.000.000&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#0f172a;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="760" y="130" width="350" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_role_badge" value="&lt;b&gt;Peran: Ketua / Host Kelompok&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#d97706&quot;&gt;★ Hak Akses Pengocokan Penuh&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d97706;fontSize=10.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="1230" y="132" width="190" height="36" as="geometry"/>
                </mxCell>

                <!-- Window 2 Left Sidebar (Menu Back End) -->
                <mxCell id="be_sidebar" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#e2e8f0;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="760" y="175" width="220" height="715" as="geometry"/>
                </mxCell>
                <mxCell id="be_menu_header" value="&lt;b style=&quot;color:#b45309;&quot;&gt;PANEL KONTROL KETUA&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="760" y="185" width="220" height="25" as="geometry"/>
                </mxCell>

                <!-- BE Menu Items -->
                <mxCell id="be_m1" value="⚙️ 1. Buat &amp; Atur Kelompok" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="770" y="215" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_m2" value="📋 2. Kelola Anggota &amp; Kuota" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="770" y="265" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_m3" value="🎲 3. Konsol Tombol Kocokan (AKTIF)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;strokeWidth=2;align=left;spacingLeft=12;fontSize=11;fontStyle=1;fontColor=#d97706;" parent="1" vertex="1">
                    <mxGeometry x="770" y="315" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_m4" value="📝 4. Pengesahan &amp; Kuitansi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="770" y="365" width="200" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_m5" value="🏁 5. Tutup Buku &amp; Periode Baru" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cbd5e1;align=left;spacingLeft=12;fontSize=11;fontColor=#334155;" parent="1" vertex="1">
                    <mxGeometry x="770" y="415" width="200" height="40" as="geometry"/>
                </mxCell>

                <mxCell id="be_sidebar_note" value="&lt;font color=&quot;#64748b&quot; style=&quot;font-size:10px;&quot;&gt;Menu Back End hanya terlihat di aplikasi laptop Ketua Kelompok (Host).&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#e2e8f0;align=center;spacing=8;" parent="1" vertex="1">
                    <mxGeometry x="770" y="780" width="200" height="90" as="geometry"/>
                </mxCell>

                <!-- BE Main Content Area (Konsol Pengocokan & Aksi Tombol) -->
                <mxCell id="be_content" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=none;" parent="1" vertex="1">
                    <mxGeometry x="980" y="175" width="460" height="715" as="geometry"/>
                </mxCell>

                <!-- Action Button in BE Console -->
                <mxCell id="be_btn_draw" value="&lt;b style=&quot;font-size:14px;&quot;&gt;🎲 TEKAN TOMBOL KOCOK PEMENANG&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:10.5px;&quot;&gt;Sistem memilih 1 peserta secara acak dari sisa kandidat&lt;/font&gt;" style="rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor=#d97706;strokeColor=#b45309;fontColor=#ffffff;align=center;shadow=1;" parent="1" vertex="1">
                    <mxGeometry x="1000" y="200" width="420" height="65" as="geometry"/>
                </mxCell>

                <!-- Active Candidate Pool Status -->
                <mxCell id="be_pool_box" value="&lt;b&gt;Panel Status Kandidat Siap Dikocok (3 Orang):&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#16a34a&quot;&gt;[✓] Lot #02 - Pak Budi Santoso (Iuran Lunas)&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#16a34a&quot;&gt;[✓] Lot #03 - Ibu Dewi Lestari (Iuran Lunas)&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#16a34a&quot;&gt;[✓] Lot #04 - Pak Ahmad Fauzi (Iuran Lunas)&lt;/font&gt;&lt;br&gt;&lt;font color=&quot;#dc2626&quot;&gt;[X] Lot #01 - Ibu Siti Aminah (Terkunci: Sudah Pernah Menang)&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fffbeb;strokeColor=#fde68a;align=left;spacingLeft=15;fontSize=11;lineHeight=1.4;" parent="1" vertex="1">
                    <mxGeometry x="1000" y="280" width="420" height="110" as="geometry"/>
                </mxCell>

                <!-- Issue Receipt Button -->
                <mxCell id="be_btn_lock" value="&lt;b&gt;🔒 Sahkan Pemenang &amp;amp; Kunci Status Menang&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:10px;&quot;&gt;Otomatis terbitkan Kuitansi Sah ke layar seluruh peserta&lt;/font&gt;" style="rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor=#1e293b;strokeColor=#0f172a;fontColor=#ffffff;align=center;shadow=1;" parent="1" vertex="1">
                    <mxGeometry x="1000" y="405" width="420" height="50" as="geometry"/>
                </mxCell>

                <!-- Audit Log Box -->
                <mxCell id="be_audit_box" value="&lt;b&gt;Catatan Audit Transaksi Arisan:&lt;/b&gt;&lt;br&gt;• Periode 1: Menang oleh Ibu Siti Aminah (Rp 1.000.000) [Kuitansi #TRX-001]&lt;br&gt;• Periode 2: Sedang Berlangsung di Ruang Acara&lt;br&gt;• Seluruh aksi pengocokan tersimpan permanen di basis data lokal." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor=#cbd5e1;align=left;spacingLeft=15;fontSize=10.5;lineHeight=1.4;" parent="1" vertex="1">
                    <mxGeometry x="1000" y="470" width="420" height="100" as="geometry"/>
                </mxCell>

                <!-- BE Footer Bar -->
                <mxCell id="be_footer" value="Aplikasi Arisan Digital Desktop (Back End) | Otoritas Penuh Ketua Kelompok" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f1f5f9;strokeColor=#e2e8f0;fontColor=#64748b;fontSize=10;align=center;" parent="1" vertex="1">
                    <mxGeometry x="760" y="890" width="680" height="40" as="geometry"/>
                </mxCell>

            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
"""

with open(
    r"d:\herd\aplikasi_arisan\struktur_menu_arisan.drawio", "w", encoding="utf-8"
) as f:
    f.write(drawio_content)

with open(
    r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.drawio", "w", encoding="utf-8"
) as f:
    f.write(drawio_content)

with open(
    r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.dio", "w", encoding="utf-8"
) as f:
    f.write(drawio_content)

print("Draw.io XML layout files saved successfully.")
