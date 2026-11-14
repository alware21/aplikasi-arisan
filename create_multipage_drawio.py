import os

drawio_multi_page = """<mxfile host="65bd71144e">
    <diagram name="1. Layout Front End (Anggota)" id="fe-layout-bw">
        <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="750" background="#ffffff" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- Header Title -->
                <mxCell id="fe_h_title" value="Rancangan Tata Letak Menu Front End (Tampilan Layar Anggota)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;fontColor=#000000;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="25" width="700" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="fe_h_sub" value="Sisi Front End: Menampilkan Posisi Menu Navigasi di Sidebar Kiri &amp; Ruang Undian Live (Akses Seluruh Anggota)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontColor=#555555;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="55" width="800" height="20" as="geometry"/>
                </mxCell>

                <!-- Window Frame -->
                <mxCell id="fe_win" value="" style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" parent="1" vertex="1">
                    <mxGeometry x="50" y="90" width="1000" height="620" as="geometry"/>
                </mxCell>

                <!-- Titlebar -->
                <mxCell id="fe_tb" value="&lt;b&gt;Arisan Digital Desktop - Mode Anggota (Front End)&lt;/b&gt;" style="rounded=1;arcSize=0;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;align=left;spacingLeft=15;fontSize=12;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="90" width="1000" height="35" as="geometry"/>
                </mxCell>
                <mxCell id="fe_tb_ctrl" value="[ _ ] [ O ] [ X ]" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontSize=10;fontColor=#ffffff;fontStyle=1;spacingRight=15;" parent="1" vertex="1">
                    <mxGeometry x="920" y="95" width="120" height="25" as="geometry"/>
                </mxCell>

                <!-- Top Info Bar -->
                <mxCell id="fe_top" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8f8f8;strokeColor=#000000;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="50" y="125" width="1000" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="fe_top_txt" value="&lt;b&gt;KELOMPOK AKTIF: Arisan Warga RT 05&lt;/b&gt; | Kode Grup: &lt;b&gt;RT05-2026&lt;/b&gt;&lt;br&gt;Nominal Iuran: Rp 200.000 / Bulan | Putaran: Periode Ke-2" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#000000;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="50" y="130" width="500" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="fe_badge" value="&lt;b&gt;Profil: Ibu Siti Aminah (Lot #01)&lt;/b&gt;&lt;br&gt;Status: Terdaftar di Grup" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;fontSize=10.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="810" y="132" width="220" height="36" as="geometry"/>
                </mxCell>

                <!-- Left Sidebar -->
                <mxCell id="fe_sb" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f4f4f4;strokeColor=#000000;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="50" y="175" width="300" height="495" as="geometry"/>
                </mxCell>
                <mxCell id="fe_sb_title" value="&lt;b&gt;NAVIGASI MENU PESERTA&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#000000;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="50" y="185" width="300" height="25" as="geometry"/>
                </mxCell>

                <!-- FE Menu Buttons -->
                <mxCell id="fe_m1" value="🏠 1. Beranda &amp;amp; Masuk Grup" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="215" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m2" value="🎟️ 2. Kartu Undian Saya" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="267" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m3" value="👥 3. Papan Transparansi Roster" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="319" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m4" value="🎰 4. Ruang Pengundian Live [AKTIF]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;align=left;spacingLeft=12;fontSize=11;fontStyle=1;fontColor=#ffffff;" parent="1" vertex="1">
                    <mxGeometry x="65" y="371" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="fe_m5" value="📄 5. Galeri Kuitansi Digital" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="423" width="270" height="42" as="geometry"/>
                </mxCell>

                <!-- FE Sidebar Note -->
                <mxCell id="fe_note" value="&lt;b&gt;Karakteristik Menu Front End:&lt;/b&gt;&lt;br&gt;• Terletak di Sidebar Kiri layar.&lt;br&gt;• Dapat diakses oleh seluruh anggota.&lt;br&gt;• &lt;b&gt;Tidak memiliki tombol kocokan&lt;/b&gt;&lt;br&gt;  (Mencegah manipulasi/kecurangan)." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;align=left;spacingLeft=10;fontSize=10.5;lineHeight=1.3;" parent="1" vertex="1">
                    <mxGeometry x="65" y="555" width="270" height="95" as="geometry"/>
                </mxCell>

                <!-- Content Area -->
                <mxCell id="fe_content" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=none;" parent="1" vertex="1">
                    <mxGeometry x="350" y="175" width="700" height="495" as="geometry"/>
                </mxCell>

                <!-- Live Area Box -->
                <mxCell id="fe_live_box" value="" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#fcfcfc;strokeColor=#000000;strokeWidth=1.5;" parent="1" vertex="1">
                    <mxGeometry x="380" y="195" width="640" height="230" as="geometry"/>
                </mxCell>
                <mxCell id="fe_live_t" value="&lt;b style=&quot;font-size:13px;&quot;&gt;SIARAN PENGUNDIAN PUTARAN KE-2 (LIVE)&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#555555&quot;&gt;Menampilkan animasi putaran acak saat pengocokan dipicu oleh Ketua...&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;" parent="1" vertex="1">
                    <mxGeometry x="380" y="205" width="640" height="35" as="geometry"/>
                </mxCell>
                <mxCell id="fe_ball" value="&lt;b style=&quot;font-size:18px; color:#ffffff;&quot;&gt;#01&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:10px; color:#ffffff;&quot;&gt;Ibu Siti Aminah&lt;/font&gt;" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#000000;strokeColor=#000000;strokeWidth=2;" parent="1" vertex="1">
                    <mxGeometry x="645" y="245" width="110" height="110" as="geometry"/>
                </mxCell>
                <mxCell id="fe_res_badge" value="&lt;b&gt;STATUS HASIL: SAH TERKUNCI | Total Hadiah: Rp 1.000.000&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eeeeee;strokeColor=#000000;fontSize=10.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="460" y="375" width="480" height="32" as="geometry"/>
                </mxCell>

                <!-- Candidate List Box -->
                <mxCell id="fe_cand_box" value="&lt;b&gt;Papan Transparansi Kandidat Belum Menang:&lt;/b&gt;&lt;br&gt;• Lot #02 : Pak Budi Santoso [Status: Mengantre]&lt;br&gt;• Lot #03 : Ibu Dewi Lestari [Status: Mengantre]&lt;br&gt;• Lot #04 : Pak Ahmad Fauzi [Status: Mengantre]&lt;br&gt;&lt;font color=&quot;#555555&quot; style=&quot;font-size:9.5px;&quot;&gt;&lt;i&gt;Transparansi: Seluruh peserta melihat pergerakan pemenang secara serentak.&lt;/i&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;align=left;spacingLeft=15;fontSize=11;lineHeight=1.4;" parent="1" vertex="1">
                    <mxGeometry x="380" y="445" width="640" height="120" as="geometry"/>
                </mxCell>

                <!-- Footer Bar -->
                <mxCell id="fe_ft" value="Aplikasi Arisan Digital Desktop (Front End) | Hak Akses: Seluruh Anggota Peserta" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#eeeeee;strokeColor=#000000;fontColor=#333333;fontSize=10;align=center;" parent="1" vertex="1">
                    <mxGeometry x="50" y="670" width="1000" height="40" as="geometry"/>
                </mxCell>

            </root>
        </mxGraphModel>
    </diagram>

    <diagram name="2. Layout Back End (Ketua)" id="be-layout-bw">
        <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="750" background="#ffffff" math="0" shadow="0">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- Header Title -->
                <mxCell id="be_h_title" value="Rancangan Tata Letak Menu Back End (Panel Kontrol Ketua Kelompok)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontStyle=1;fontColor=#000000;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="25" width="700" height="30" as="geometry"/>
                </mxCell>
                <mxCell id="be_h_sub" value="Sisi Back End: Menampilkan Posisi Menu Pengelolaan di Sidebar Kiri &amp; Tombol Operasional Pengocokan (Akses Eksklusif Ketua)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=11;fontColor=#555555;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="55" width="850" height="20" as="geometry"/>
                </mxCell>

                <!-- Window Frame -->
                <mxCell id="be_win" value="" style="rounded=1;arcSize=3;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;" parent="1" vertex="1">
                    <mxGeometry x="50" y="90" width="1000" height="620" as="geometry"/>
                </mxCell>

                <!-- Titlebar -->
                <mxCell id="be_tb" value="&lt;b&gt;Arisan Digital Desktop - Panel Kontrol Ketua Kelompok (Back End)&lt;/b&gt;" style="rounded=1;arcSize=0;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;align=left;spacingLeft=15;fontSize=12;fontFamily=Helvetica;" parent="1" vertex="1">
                    <mxGeometry x="50" y="90" width="1000" height="35" as="geometry"/>
                </mxCell>
                <mxCell id="be_tb_ctrl" value="[ _ ] [ O ] [ X ]" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontSize=10;fontColor=#ffffff;fontStyle=1;spacingRight=15;" parent="1" vertex="1">
                    <mxGeometry x="920" y="95" width="120" height="25" as="geometry"/>
                </mxCell>

                <!-- Top Info Bar -->
                <mxCell id="be_top" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8f8f8;strokeColor=#000000;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="50" y="125" width="1000" height="50" as="geometry"/>
                </mxCell>
                <mxCell id="be_top_txt" value="&lt;b&gt;PENGELOLAAN GRUP: Arisan Warga RT 05&lt;/b&gt; | Kode Grup: &lt;b&gt;RT05-2026&lt;/b&gt;&lt;br&gt;Total Peserta: 4 Orang | Total Kas Terkumpul: Rp 1.000.000" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#000000;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="50" y="130" width="500" height="40" as="geometry"/>
                </mxCell>
                <mxCell id="be_badge" value="&lt;b&gt;★ PERAN: KETUA (HOST PENGOCOK)&lt;/b&gt;&lt;br&gt;Otoritas Eksekusi &amp;amp; Penguncian Penuh" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;fontColor=#ffffff;fontSize=10.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="780" y="132" width="250" height="36" as="geometry"/>
                </mxCell>

                <!-- Left Sidebar -->
                <mxCell id="be_sb" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f4f4f4;strokeColor=#000000;strokeWidth=1;" parent="1" vertex="1">
                    <mxGeometry x="50" y="175" width="300" height="495" as="geometry"/>
                </mxCell>
                <mxCell id="be_sb_title" value="&lt;b&gt;PANEL KONTROL KETUA&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#000000;spacingLeft=15;" parent="1" vertex="1">
                    <mxGeometry x="50" y="185" width="300" height="25" as="geometry"/>
                </mxCell>

                <!-- BE Menu Buttons -->
                <mxCell id="be_m1" value="⚙️ 1. Buat &amp;amp; Atur Kelompok" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="215" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="be_m2" value="📋 2. Kelola Anggota &amp;amp; Kuota" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="267" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="be_m3" value="🎲 3. Konsol Tombol Kocokan [AKTIF]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;align=left;spacingLeft=12;fontSize=11;fontStyle=1;fontColor=#ffffff;" parent="1" vertex="1">
                    <mxGeometry x="65" y="371" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="be_m4" value="📝 4. Pengesahan &amp;amp; Kuitansi" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="423" width="270" height="42" as="geometry"/>
                </mxCell>
                <mxCell id="be_m5" value="🏁 5. Tutup Buku &amp;amp; Selesai" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#888888;align=left;spacingLeft=12;fontSize=11;fontColor=#000000;" parent="1" vertex="1">
                    <mxGeometry x="65" y="475" width="270" height="42" as="geometry"/>
                </mxCell>

                <!-- BE Sidebar Note -->
                <mxCell id="be_note" value="&lt;b&gt;Karakteristik Menu Back End:&lt;/b&gt;&lt;br&gt;• Eksklusif di laptop/akun Ketua.&lt;br&gt;• Otoritas penuh tombol pengundian.&lt;br&gt;• &lt;b&gt;Eksekusi &amp;amp; kunci status&lt;/b&gt; pemenang&lt;br&gt;  resmi tersimpan ke basis data." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;align=left;spacingLeft=10;fontSize=10.5;lineHeight=1.3;" parent="1" vertex="1">
                    <mxGeometry x="65" y="555" width="270" height="95" as="geometry"/>
                </mxCell>

                <!-- Content Area -->
                <mxCell id="be_content" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=none;" parent="1" vertex="1">
                    <mxGeometry x="350" y="175" width="700" height="495" as="geometry"/>
                </mxCell>

                <!-- Main Action Button: Kocok -->
                <mxCell id="be_btn_draw" value="&lt;b style=&quot;font-size:13px; color:#ffffff;&quot;&gt;[ &amp;gt; ] TEKAN TOMBOL KOCOK PEMENANG SEKARANG&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:10px; color:#cccccc;&quot;&gt;Algoritma acak sistem otomatis menyaring peserta yang BELUM MENANG.&lt;br&gt;Peserta yang sudah menang pada putaran sebelumnya tidak akan terpilih lagi.&lt;/font&gt;" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;align=center;" parent="1" vertex="1">
                    <mxGeometry x="380" y="195" width="640" height="75" as="geometry"/>
                </mxCell>

                <!-- Candidate Status Pool -->
                <mxCell id="be_pool" value="&lt;b&gt;Validasi Kandidat Memenuhi Syarat Pengundian (3 Peserta):&lt;/b&gt;&lt;br&gt;[✓] Lot #02 - Pak Budi Santoso [Status: Iuran Lunas &amp;amp; Siap Diundi]&lt;br&gt;[✓] Lot #03 - Ibu Dewi Lestari [Status: Iuran Lunas &amp;amp; Siap Diundi]&lt;br&gt;[✓] Lot #04 - Pak Ahmad Fauzi [Status: Iuran Lunas &amp;amp; Siap Diundi]&lt;br&gt;&lt;b&gt;[X] Lot #01 - Ibu Siti Aminah [TERKUNCI: Sudah Pernah Menang Periode 1]&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f8f8;strokeColor=#000000;align=left;spacingLeft=15;fontSize=10.5;lineHeight=1.4;" parent="1" vertex="1">
                    <mxGeometry x="380" y="285" width="640" height="110" as="geometry"/>
                </mxCell>

                <!-- Second Action Button: Issue Receipt -->
                <mxCell id="be_btn_lock" value="&lt;b&gt;[KUNCI] SAHKAN PEMENANG &amp;amp; TERBITKAN KUITANSI ELEKTRONIK&lt;/b&gt;&lt;br&gt;&lt;font color=&quot;#555555&quot; style=&quot;font-size:10px;&quot;&gt;Mengunci status '__status_menang = True' permanen dan mencatat ke database.&lt;/font&gt;" style="rounded=1;arcSize=4;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1.5;align=center;" parent="1" vertex="1">
                    <mxGeometry x="380" y="410" width="640" height="50" as="geometry"/>
                </mxCell>

                <!-- Audit Log -->
                <mxCell id="be_audit" value="&lt;b&gt;Rekap Audit Transaksi:&lt;/b&gt; Putaran 1 sah dimenangkan oleh Ibu Siti Aminah (Kuitansi TRX-001).&lt;br&gt;&lt;font color=&quot;#555555&quot;&gt;&lt;i&gt;Semua histori pengocokan tersimpan otomatis dan tidak dapat diubah tanpa otorisasi.&lt;/i&gt;&lt;/font&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f4f4f4;strokeColor=#888888;align=left;spacingLeft=15;fontSize=10.5;lineHeight=1.3;" parent="1" vertex="1">
                    <mxGeometry x="380" y="475" width="640" height="70" as="geometry"/>
                </mxCell>

                <!-- Footer Bar -->
                <mxCell id="be_ft" value="Aplikasi Arisan Digital Desktop (Back End) | Otoritas Penuh Ketua / Host Kelompok" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#eeeeee;strokeColor=#000000;fontColor=#333333;fontSize=10;align=center;" parent="1" vertex="1">
                    <mxGeometry x="50" y="670" width="1000" height="40" as="geometry"/>
                </mxCell>

            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
"""

with open(
    r"d:\herd\aplikasi_arisan\struktur_menu_arisan.drawio", "w", encoding="utf-8"
) as f:
    f.write(drawio_multi_page)

with open(
    r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.drawio", "w", encoding="utf-8"
) as f:
    f.write(drawio_multi_page)

with open(
    r"C:\Users\ThinkPad\Downloads\struktur_menu_arisan.dio", "w", encoding="utf-8"
) as f:
    f.write(drawio_multi_page)

print("Saved multi-page Draw.io diagrams successfully.")
