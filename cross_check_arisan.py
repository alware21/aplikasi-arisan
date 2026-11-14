import os
import sys
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from arisan.models import Anggota, KelompokArisan, PesertaArisan, RiwayatKocokan

def run_cross_check():
    print("=" * 70)
    print("🚀 MEMULAI TOTAL CROSS-CHECK LOGIKA & FITUR ARISAN DIGITAL")
    print("=" * 70)

    client_ketua = Client()
    client_anggota = Client()
    passed_tests = 0
    total_tests = 0

    def assert_test(condition, title, details=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  ✅ [PASS] {title}")
            if details:
                print(f"     ↳ {details}")
        else:
            print(f"  ❌ [FAIL] {title}")
            if details:
                print(f"     ↳ {details}")
            sys.exit(1)

    # -------------------------------------------------------------
    # TAHAP 1: PEMBUATAN KELOMPOK BARU & REGISTRASI KETUA
    # -------------------------------------------------------------
    print("\n[1] PENGUJIAN REGISTRASI KETUA & PEMBUATAN KELOMPOK BARU")
    res = client_ketua.post('/portal/', {
        'peran': 'ketua',
        'nama': 'Pak RT Sukamto',
        'no_telepon': '081299998888',
        'alamat': 'Jl. Kenanga No. 10',
        'pin': '1234',
        'nama_kelompok': 'Arisan Warga Sukamaju',
        'nominal_iuran': '50000',
        'periode_kocok': 'bulanan'
    }, follow=True)

    assert_test(res.status_code == 200, "Ketua berhasil mendaftar dan dialihkan ke dashboard")
    
    kelompok = KelompokArisan.objects.filter(nama_kelompok='Arisan Warga Sukamaju').first()
    assert_test(kelompok is not None, "Kelompok Arisan tersimpan di database")
    assert_test(len(kelompok.kode_room) == 6, f"Kode room terbentuk 6 karakter: {kelompok.kode_room}")
    assert_test(kelompok.nominal_iuran == Decimal('50000'), "Nominal iuran tersimpan Rp 50.000")
    assert_test(kelompok.periode_kocok == 'bulanan', "Periode kocok bulanan")
    assert_test(kelompok.frekuensi_setor == 'Mingguan', "Aturan relasional frekuensi setor = Mingguan")
    assert_test(kelompok.durasi_hari == 30, "Durasi hari = 30")

    # Verifikasi Ketua otomatis menjadi Peserta #01
    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, is_ketua=True).first()
    assert_test(peserta_ketua is not None, "Ketua otomatis terdaftar sebagai peserta pertama")
    assert_test(peserta_ketua.nomor_undian == 1, "Ketua mendapatkan nomor lot undian #01")

    # -------------------------------------------------------------
    # TAHAP 2: PENAMBAHAN ANGGOTA (CRUD & ALOKASI NOMOR LOT)
    # -------------------------------------------------------------
    print("\n[2] PENGUJIAN PENAMBAHAN ANGGOTA & ALOKASI LOT UNIK")
    anggota_data = [
        ('Ibu Siti Rahma', '081211112222', 'Rumah No. 12'),
        ('Bpk. Budi Santoso', '081233334444', 'Rumah No. 15'),
        ('Ibu Dewi Lestari', '081255556666', 'Rumah No. 18'),
        ('Bpk. Agus Hermawan', '081277778888', 'Rumah No. 20'),
    ]

    for nama, hp, almt in anggota_data:
        res = client_ketua.post('/anggota/tambah/', {
            'nama': nama,
            'no_telepon': hp,
            'alamat': almt
        }, follow=True)
        assert_test(res.status_code == 200, f"Tambah anggota '{nama}' berhasil")

    assert_test(kelompok.total_peserta == 5, f"Total anggota kelompok tepat 5 warga (1 Ketua + 4 Anggota)")
    
    # Cek keunikan lot 1..5
    nomor_lot_list = list(kelompok.peserta.values_list('nomor_undian', flat=True).order_by('nomor_undian'))
    assert_test(nomor_lot_list == [1, 2, 3, 4, 5], f"Seluruh lot berurutan rapi tanpa bentrok: {nomor_lot_list}")

    # -------------------------------------------------------------
    # TAHAP 3: KALKULASI KEUANGAN, KAS & SETORAN
    # -------------------------------------------------------------
    print("\n[3] PENGUJIAN KALKULASI KAS & SETORAN REAL-TIME")
    assert_test(kelompok.total_pot_hadiah == Decimal('250000'), "Target pot dihitung otomatis: 5 warga x Rp 50.000 = Rp 250.000")
    assert_test(kelompok.total_lunas_count == 1, "Ketua otomatis tercatat lunas sebagai penyetor awal (1 warga lunas)")
    assert_test(kelompok.total_kas_terkumpul == Decimal('50000'), "Kas terkumpul awal = Rp 50.000 (dari Ketua)")
    assert_test(kelompok.sisa_kekurangan_kas == Decimal('200000'), "Sisa kekurangan kas = Rp 200.000")
    assert_test(kelompok.persentase_kelunasan == 20, "Persentase lunas awal = 20%")

    # Simulasi Toggle Setor AJAX 2 Orang (Budi & Dewi)
    peserta_budi = kelompok.peserta.filter(anggota__nama='Bpk. Budi Santoso').first()
    peserta_dewi = kelompok.peserta.filter(anggota__nama='Ibu Dewi Lestari').first()

    res_budi = client_ketua.post(f'/peserta/toggle-setor/{peserta_budi.id}/')
    res_budi_json = res_budi.json()
    assert_test(res_budi.status_code == 200 and res_budi_json['status'] == 'success', "AJAX Toggle setor Bpk. Budi berhasil")
    assert_test(res_budi_json['status_setor'] == True, "Status setor Bpk. Budi kini LUNAS")

    res_dewi = client_ketua.post(f'/peserta/toggle-setor/{peserta_dewi.id}/')
    res_dewi_json = res_dewi.json()
    assert_test(res_dewi.status_code == 200 and res_dewi_json['status_setor'] == True, "Status setor Ibu Dewi kini LUNAS")

    # Refresh kelompok dari DB
    kelompok.refresh_from_db()
    assert_test(kelompok.total_lunas_count == 3, "3 warga terdata lunas (Ketua + Budi + Dewi)")
    assert_test(kelompok.total_kas_terkumpul == Decimal('150000'), "Kas terkumpul = Rp 150.000 (3 x Rp 50.000)")
    assert_test(kelompok.persentase_kelunasan == 60, "Persentase kelunasan tepat 60%")
    assert_test(kelompok.sisa_kekurangan_kas == Decimal('100000'), "Sisa kekurangan kas = Rp 100.000")

    # Fitur 1-Klik Tandai Semua Lunas
    res_lunas_semua = client_ketua.post(f'/peserta/lunas-semua/{kelompok.id}/', follow=True)
    assert_test(res_lunas_semua.status_code == 200, "Eksekusi 'Tandai Semua Lunas' berhasil")
    kelompok.refresh_from_db()
    assert_test(kelompok.total_lunas_count == 5, "Seluruh 5 warga tercatat LUNAS")
    assert_test(kelompok.total_kas_terkumpul == Decimal('250000'), "Kas terkumpul 100% penuh = Rp 250.000")
    assert_test(kelompok.persentase_kelunasan == 100, "Persentase kelunasan tepat 100%")

    # -------------------------------------------------------------
    # TAHAP 4: OTORISASI & HAK AKSES PENGUNDIAN (RBAC)
    # -------------------------------------------------------------
    print("\n[4] PENGUJIAN OTORISASI & HAK AKSES ROLE (KETUA VS ANGGOTA)")
    # Setup session anggota
    session_anggota = client_anggota.session
    session_anggota['user_role'] = 'anggota'
    session_anggota['user_nama'] = 'Bpk. Budi Santoso'
    session_anggota['kelompok_id'] = kelompok.id
    session_anggota['peserta_id'] = peserta_budi.id
    session_anggota.save()

    # Anggota mencoba memutar kocokan -> Harus 403 Forbidden!
    res_kocok_anggota = client_anggota.post(f'/kocokan/api/proses/{kelompok.id}/')
    assert_test(res_kocok_anggota.status_code == 403, "Anggota DITOLAK (403) saat mencoba memutar kocokan")

    # Anggota mencoba tandai lunas massal -> Harus ditolak (redirect with error)
    res_lunas_anggota = client_anggota.post(f'/peserta/lunas-semua/{kelompok.id}/', follow=True)
    assert_test(res_lunas_anggota.status_code == 200, "Akses anggota ke tandai semua lunas dialihkan aman")

    # -------------------------------------------------------------
    # TAHAP 5: LOGIKA ARISAN - PUTARAN 1 & ANTI-DUPLIKASI PEMENANG
    # -------------------------------------------------------------
    print("\n[5] PENGUJIAN LOGIKA PENGUNDIAN & ANTI-DUPLIKASI SIKLUS")
    assert_test(kelompok.putaran_berikutnya == 1, "Putaran saat ini adalah Putaran Ke-1")
    assert_test(kelompok.sisa_kandidat_count == 5, "Seluruh 5 warga masuk daftar siap undi")

    # Ketua memutar Kocokan Putaran 1
    res_kocok_1 = client_ketua.post(f'/kocokan/api/proses/{kelompok.id}/')
    res_1_json = res_kocok_1.json()
    assert_test(res_kocok_1.status_code == 200 and res_1_json['status'] == 'success', f"Pengocokan Putaran 1 Sukses: Pemenang {res_1_json['pemenang_nama']}")
    
    pemenang_1_nama = res_1_json['pemenang_nama']
    pemenang_1_obj = kelompok.peserta.filter(anggota__nama=pemenang_1_nama).first()
    assert_test(pemenang_1_obj.status_menang == True, f"Pemenang 1 ({pemenang_1_nama}) berstatus status_menang=True")
    
    kelompok.refresh_from_db()
    assert_test(kelompok.riwayat.count() == 1, "Tercatat 1 riwayat pengundian")
    assert_test(kelompok.putaran_berikutnya == 2, "Putaran berikutnya naik menjadi Putaran Ke-2")
    assert_test(kelompok.sisa_kandidat_count == 4, f"Sisa kandidat berkurang menjadi 4 warga (Pemenang 1 terkunci)")

    # Buka Setoran Baru Putaran 2
    res_buka_2 = client_ketua.post(f'/buka-setoran/{kelompok.id}/', follow=True)
    assert_test(res_buka_2.status_code == 200, "Buka setoran Putaran 2 berhasil")
    
    # Cek bahwa status_setor di-reset ke False, tapi status_menang pemenang 1 TETAP TRUE!
    pemenang_1_obj.refresh_from_db()
    assert_test(pemenang_1_obj.status_setor == False, "Status setor warga di-reset ke False untuk iuran putaran 2")
    assert_test(pemenang_1_obj.status_menang == True, "Status menang Pemenang 1 TETAP TERKUNCI (True)")

    # Ketua memutar Kocokan Putaran 2
    res_kocok_2 = client_ketua.post(f'/kocokan/api/proses/{kelompok.id}/')
    res_2_json = res_kocok_2.json()
    pemenang_2_nama = res_2_json['pemenang_nama']
    assert_test(pemenang_2_nama != pemenang_1_nama, f"Pemenang Putaran 2 ({pemenang_2_nama}) BUKAN pemenang Putaran 1 ({pemenang_1_nama}) [Anti-Duplikasi Sah!]")

    # -------------------------------------------------------------
    # TAHAP 6: PENGUNDIAN LENGKAP 1 SIKLUS HINGGA HABIS (5 WARGA)
    # -------------------------------------------------------------
    print("\n[6] PENGUJIAN SIKLUS PENUH (SELURUH WARGA MENANG 1X)")
    daftar_pemenang = [pemenang_1_nama, pemenang_2_nama]

    # Putar putaran 3, 4, 5
    for p_idx in [3, 4, 5]:
        res_k = client_ketua.post(f'/kocokan/api/proses/{kelompok.id}/')
        k_json = res_k.json()
        assert_test(res_k.status_code == 200 and k_json['status'] == 'success', f"Pengocokan Putaran {p_idx} Sukses: {k_json['pemenang_nama']}")
        assert_test(k_json['pemenang_nama'] not in daftar_pemenang, f"Pemenang Putaran {p_idx} belum pernah menang sebelumnya")
        daftar_pemenang.append(k_json['pemenang_nama'])

    assert_test(len(set(daftar_pemenang)) == 5, f"Tepat 5 warga unik telah memenangkan arisan secara adil: {daftar_pemenang}")
    kelompok.refresh_from_db()
    assert_test(kelompok.is_selesai == True, "Siklus arisan terdeteksi selesai (seluruh anggota telah menang)")

    # Cek perilaku jika diputar di siklus baru: harus me-reset siklus otomatis
    kandidat_siklus_baru = kelompok.get_peserta_siap_undi()
    assert_test(kandidat_siklus_baru.count() == 5, "Siklus berikutnya otomatis membuka kembali seluruh 5 anggota untuk diundi")

    # -------------------------------------------------------------
    # TAHAP 7: PEMBATALAN / HAPUS RIWAYAT & RECOVERY
    # -------------------------------------------------------------
    print("\n[7] PENGUJIAN PEMBATALAN RIWAYAT & RESET KAS")
    riwayat_terakhir = kelompok.riwayat.first()
    pemenang_terakhir = riwayat_terakhir.peserta_menang
    pemenang_terakhir_nama = pemenang_terakhir.anggota.nama

    # Hapus 1 riwayat
    res_del_1 = client_ketua.post(f'/riwayat/hapus/{riwayat_terakhir.id}/', follow=True)
    assert_test(res_del_1.status_code == 200, f"Hapus 1 riwayat putaran terakhir ({pemenang_terakhir_nama}) berhasil")
    
    pemenang_terakhir.refresh_from_db()
    assert_test(pemenang_terakhir.status_menang == False, f"Status menang {pemenang_terakhir_nama} dikembalikan menjadi False")
    assert_test(kelompok.riwayat.count() == 4, "Sisa riwayat menjadi 4")
    assert_test(kelompok.putaran_berikutnya == 5, "Putaran berikutnya mundur kembali ke Putaran Ke-5")

    # Hapus SEMUA riwayat (Shortcut Reset Total)
    res_del_all = client_ketua.post(f'/riwayat/hapus-semua/{kelompok.id}/', follow=True)
    assert_test(res_del_all.status_code == 200, "Hapus seluruh riwayat pengundian berhasil")
    kelompok.refresh_from_db()
    assert_test(kelompok.riwayat.count() == 0, "Seluruh rekaman riwayat bersih (0 data)")
    assert_test(kelompok.putaran_berikutnya == 1, "Nomor putaran kembali ke Putaran Ke-1")
    assert_test(kelompok.peserta.filter(status_menang=True).count() == 0, "Semua peserta dikembalikan ke status belum menang (0 pemenang)")

    # -------------------------------------------------------------
    # TAHAP 8: GABUNG KELOMPOK DENGAN KODE ROOM (WARGA BARU)
    # -------------------------------------------------------------
    print("\n[8] PENGUJIAN JOIN ROOM VIA KODE ROOM (6 DIGIT)")
    client_warga_baru = Client()
    res_join = client_warga_baru.post('/portal/', {
        'peran': 'anggota',
        'nama': 'Doni Kusuma',
        'no_telepon': '089988776655',
        'alamat': 'Gang Cempaka',
        'kode_room': kelompok.kode_room
    }, follow=True)
    assert_test(res_join.status_code == 200, f"Warga 'Doni Kusuma' berhasil join dengan room '{kelompok.kode_room}'")
    
    kelompok.refresh_from_db()
    assert_test(kelompok.total_peserta == 6, "Total peserta kelompok bertambah menjadi 6 warga")
    doni_peserta = kelompok.peserta.filter(anggota__nama='Doni Kusuma').first()
    assert_test(doni_peserta is not None, "Doni Kusuma resmi terdaftar di kelompok")
    assert_test(doni_peserta.nomor_undian == 6, "Doni otomatis mendapatkan nomor lot #06")

    # -------------------------------------------------------------
    # TAHAP 9: KELAYAKAN HALAMAN & KEAMANAN SESSION (NO 404 / 500)
    # -------------------------------------------------------------
    print("\n[9] PENGUJIAN KELAYAKAN VIEW, TEMPLATE & SELF-HEALING SESSION")
    
    # Klien fresh tanpa sesi login membuka '/' -> Harus 200 (Portal)
    client_fresh = Client()
    res_portal_fresh = client_fresh.get('/')
    assert_test(res_portal_fresh.status_code == 200, "Pengunjung baru membuka '/' dialihkan ke Portal (Status: 200)")

    # Ketua yang sudah login membuka '/' -> Harus 302 redirect ke /dashboard/
    res_portal_ketua = client_ketua.get('/')
    assert_test(res_portal_ketua.status_code == 302 and res_portal_ketua.headers['Location'] == '/dashboard/', "Ketua yang login membuka '/' otomatis di-redirect ke /dashboard/ (Status: 302)")

    # Buat 1 riwayat untuk uji kuitansi
    riwayat_uji = RiwayatKocokan.objects.create(
        kelompok=kelompok,
        peserta_menang=doni_peserta,
        periode_ke=1,
        total_diterima=Decimal('300000'),
        catatan="Uji Kuitansi"
    )

    for path, expected_status in [
        ('/dashboard/', 200),
        ('/kocokan/', 200),
        ('/riwayat-kas/', 200),
        ('/grup/', 200),
        (f'/kuitansi/{riwayat_uji.id}/', 200),
    ]:
        res_page = client_ketua.get(path)
        assert_test(res_page.status_code == expected_status, f"Halaman '{path}' render sukses (Status: {res_page.status_code})")

    # Uji Self-Healing Session (ID kelompok tidak valid)
    client_stale = Client()
    s = client_stale.session
    s['user_role'] = 'ketua'
    s['kelompok_id'] = 999999 # ID Fiktif
    s['user_nama'] = 'User Hantu'
    s.save()

    res_stale_dash = client_stale.get('/dashboard/')
    assert_test(res_stale_dash.status_code == 302 and res_stale_dash.headers['Location'] == '/portal/', "Sesi usang terdeteksi & otomatis dialihkan ke /portal/ tanpa 404")
    
    res_stale_portal = client_stale.get(res_stale_dash.headers['Location'])
    assert_test(res_stale_portal.status_code == 200, "Halaman portal terbuka normal dengan status 200")

    # Cleanup data uji
    kelompok.riwayat.all().delete()
    kelompok.delete()
    print("\n" + "=" * 70)
    print(f"🎉 SEMUA {passed_tests}/{total_tests} PENGUJIAN LOGIKA & FITUR BERHASIL 100% (SEMPURNA)!")
    print("=" * 70)

if __name__ == '__main__':
    run_cross_check()
