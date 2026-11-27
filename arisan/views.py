import hashlib
import random
import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Anggota, KelompokArisan, PesertaArisan, RiwayatKocokan, generate_room_code

def portal_view(request):
    """Layar Pemilihan Peran & Splash: Masuk Sebagai Ketua vs Masuk Sebagai Anggota"""
    kelompok_id = request.session.get('kelompok_id')
    user_role = request.session.get('user_role')
    if user_role and kelompok_id:
        if KelompokArisan.objects.filter(pk=kelompok_id).exists():
            return redirect('dashboard')
        else:
            request.session.pop('kelompok_id', None)
            request.session.pop('peserta_id', None)

    kelompok_default = KelompokArisan.objects.first()

    if request.method == 'POST':
        peran = request.POST.get('peran')

        # -------------------------------------------------------------
        # 1. LOGIKA MASUK SEBAGAI KETUA (HOST)
        # -------------------------------------------------------------
        if peran == 'ketua':
            nama = request.POST.get('nama', '').strip()
            no_telepon = request.POST.get('no_telepon', '').strip()
            alamat = request.POST.get('alamat', '').strip()
            pin = request.POST.get('pin', '').strip()
            nama_kelompok = request.POST.get('nama_kelompok', '').strip()
            nominal_iuran = request.POST.get('nominal_iuran', '20000')
            periode_kocok = request.POST.get('periode_kocok', 'bulanan')

            if not nama:
                messages.error(request, 'Nama lengkap Ketua wajib diisi!')
                return redirect('portal')

            if pin != '1234':
                messages.error(request, 'PIN Pengurus salah! (Gunakan default PIN: 1234)')
                return redirect('portal')

            ketua_anggota, _ = Anggota.objects.get_or_create(
                nama=nama,
                defaults={'no_telepon': no_telepon, 'alamat': alamat}
            )
            if no_telepon:
                ketua_anggota.no_telepon = no_telepon
            if alamat:
                ketua_anggota.alamat = alamat
            ketua_anggota.save()

            if nama_kelompok:
                new_room_code = generate_room_code()
                kelompok = KelompokArisan.objects.create(
                    nama_kelompok=nama_kelompok,
                    kode_room=new_room_code,
                    nominal_iuran=Decimal(nominal_iuran),
                    periode_kocok=periode_kocok,
                    pin_ketua=pin
                )
            else:
                kelompok = KelompokArisan.objects.first()
                if not kelompok:
                    kelompok = KelompokArisan.objects.create(
                        nama_kelompok="Arisan Warga RT 05",
                        kode_room=generate_room_code(),
                        nominal_iuran=Decimal(nominal_iuran),
                        periode_kocok=periode_kocok,
                        pin_ketua=pin
                    )

            peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota=ketua_anggota).first()
            if not peserta_ketua:
                peserta_ketua = PesertaArisan.objects.create(
                    kelompok=kelompok,
                    anggota=ketua_anggota,
                    nomor_undian=1 if kelompok.peserta.count() == 0 else kelompok.peserta.count() + 1,
                    is_ketua=True,
                    status_setor=True
                )
            else:
                peserta_ketua.is_ketua = True
                peserta_ketua.status_setor = True
                peserta_ketua.save()

            request.session['user_role'] = 'ketua'
            request.session['user_nama'] = nama
            request.session['user_hp'] = no_telepon
            request.session['kelompok_id'] = kelompok.id
            request.session['peserta_id'] = peserta_ketua.id

            messages.success(request, f'Selamat datang Ketua {nama}! Kelompok "{kelompok.nama_kelompok}" aktif dengan Kode Room: {kelompok.kode_room}')
            return redirect('dashboard')

        # -------------------------------------------------------------
        # 2. LOGIKA MASUK SEBAGAI ANGGOTA (PESERTA)
        # -------------------------------------------------------------
        elif peran == 'anggota':
            nama = request.POST.get('nama', '').strip()
            no_telepon = request.POST.get('no_telepon', '').strip()
            alamat = request.POST.get('alamat', '').strip()
            kode_room = request.POST.get('kode_room', '').strip().upper()

            if not nama or not kode_room:
                messages.error(request, 'Nama Lengkap dan Kode Room wajib diisi!')
                return redirect('portal')

            kelompok = KelompokArisan.objects.filter(kode_room__iexact=kode_room).first()
            if not kelompok:
                messages.error(request, f'Kode Room "{kode_room}" tidak ditemukan! Mohon periksa kembali atau minta ke Ketua Arisan.')
                return redirect('portal')

            anggota_obj, _ = Anggota.objects.get_or_create(
                nama=nama,
                defaults={'no_telepon': no_telepon, 'alamat': alamat}
            )
            if no_telepon:
                anggota_obj.no_telepon = no_telepon
            if alamat:
                anggota_obj.alamat = alamat
            anggota_obj.save()

            peserta = PesertaArisan.objects.filter(kelompok=kelompok, anggota=anggota_obj).first()
            if not peserta:
                next_lot = kelompok.peserta.count() + 1
                peserta = PesertaArisan.objects.create(
                    kelompok=kelompok,
                    anggota=anggota_obj,
                    nomor_undian=next_lot,
                    is_ketua=False,
                    status_setor=False
                )

            request.session['user_role'] = 'anggota'
            request.session['user_nama'] = nama
            request.session['user_hp'] = no_telepon
            request.session['kelompok_id'] = kelompok.id
            request.session['peserta_id'] = peserta.id

            messages.success(request, f'Halo {nama}, Anda berhasil bergabung di {kelompok.nama_kelompok} (Lot Undian #{peserta.nomor_undian:02d})!')
            return redirect('dashboard')

    return render(request, 'portal.html', {'kelompok_default': kelompok_default})


def logout_role(request):
    """Keluar dari Peran & Kembali ke Portal"""
    request.session.flush()
    return redirect('portal')


def dashboard(request):
    """Dashboard Utama (Otomatis menyesuaikan peran Ketua vs Anggota)"""
    user_role = request.session.get('user_role')
    kelompok_id = request.session.get('kelompok_id')

    if not user_role or not kelompok_id:
        return redirect('portal')

    kelompok = KelompokArisan.objects.filter(pk=kelompok_id).first()
    if not kelompok:
        request.session.pop('kelompok_id', None)
        request.session.pop('peserta_id', None)
        messages.warning(request, "Ruang arisan sebelumnya tidak ditemukan atau telah diperbarui. Silakan pilih atau buat kelompok kembali.")
        return redirect('portal')

    # Cek & Picu Pengocokan Otomatis jika sudah jatuh tempo (misal hari ke-30)
    auto_riwayat = kelompok.check_and_trigger_auto_draw()
    if auto_riwayat:
        messages.info(request, f"⚡ Pengocokan Otomatis Sistem: Periode ke-{auto_riwayat.periode_ke} dimenangkan oleh {auto_riwayat.peserta_menang.anggota.nama} karena batas jatuh tempo telah tiba!")

    peserta_list = kelompok.peserta.all().select_related('anggota').order_by('nomor_undian')

    my_peserta_id = request.session.get('peserta_id')
    my_peserta = PesertaArisan.objects.filter(pk=my_peserta_id).first() if my_peserta_id else None

    # Pencarian
    query = request.GET.get('q', '').strip()
    if query:
        peserta_list = peserta_list.filter(
            Q(anggota__nama__icontains=query) | 
            Q(anggota__no_telepon__icontains=query) | 
            Q(nomor_undian__icontains=query) |
            Q(anggota__alamat__icontains=query)
        )

    # Akumulasi Data Real-Time Otomatis
    total_lunas = kelompok.total_lunas_count
    total_kas_terkumpul = kelompok.total_kas_terkumpul
    target_pot = kelompok.total_pot_hadiah
    sisa_kekurangan = kelompok.sisa_kekurangan_kas
    persentase_lunas = kelompok.persentase_kelunasan
    sisa_kandidat_siap = kelompok.get_peserta_siap_undi().count()
    riwayat_terbaru = kelompok.riwayat.all().order_by('-tanggal_kocok')[:5]

    context = {
        'kelompok': kelompok,
        'peserta_list': peserta_list,
        'my_peserta': my_peserta,
        'user_role': user_role,
        'user_nama': request.session.get('user_nama'),
        'total_lunas': total_lunas,
        'total_kas_terkumpul': total_kas_terkumpul,
        'target_pot': target_pot,
        'sisa_kekurangan': sisa_kekurangan,
        'persentase_lunas': persentase_lunas,
        'sisa_kandidat_siap': sisa_kandidat_siap,
        'deadline_kocok': kelompok.deadline_kocok,
        'sisa_hari_kocok': kelompok.sisa_hari_kocok,
        'riwayat_terbaru': riwayat_terbaru,
        'query': query,
    }
    return render(request, 'dashboard.html', context)


def toggle_setor_api(request, peserta_id):
    """AJAX Toggle Status Setoran (HANYA BISA DIAKSES OLEH KETUA)"""
    if request.session.get('user_role') != 'ketua':
        return JsonResponse({'status': 'error', 'message': 'Akses Ditolak! Hanya Ketua Kelompok yang berwenang mengubah status setoran warga.'}, status=403)

    if request.method == 'POST':
        peserta = get_object_or_404(PesertaArisan, pk=peserta_id)
        peserta.status_setor = not peserta.status_setor
        peserta.save()

        kelompok = peserta.kelompok
        total_lunas = kelompok.total_lunas_count
        total_kas = kelompok.total_kas_terkumpul
        target_pot = kelompok.total_pot_hadiah
        sisa_kekurangan = kelompok.sisa_kekurangan_kas
        persentase = kelompok.persentase_kelunasan
        sisa_kandidat = kelompok.get_peserta_siap_undi().count()

        return JsonResponse({
            'status': 'success',
            'peserta_id': peserta.id,
            'status_setor': peserta.status_setor,
            'nama': peserta.anggota.nama,
            'total_lunas': total_lunas,
            'total_kas_formatted': f"Rp {total_kas:,.0f}".replace(",", "."),
            'target_pot_formatted': f"Rp {target_pot:,.0f}".replace(",", "."),
            'sisa_kekurangan_formatted': f"Rp {sisa_kekurangan:,.0f}".replace(",", "."),
            'persentase_lunas': persentase,
            'sisa_kandidat': sisa_kandidat,
            'message': f'Status setoran {peserta.anggota.nama} diperbarui menjadi: {"LUNAS" if peserta.status_setor else "BELUM BAYAR"}.'
        })
    return JsonResponse({'status': 'error', 'message': 'Metode request tidak diizinkan.'}, status=405)


def anggota_create(request):
    """Ketua Tambah Anggota Manual (CRUD Create)"""
    if request.session.get('user_role') != 'ketua':
        messages.error(request, 'Hanya Ketua yang dapat mendaftarkan anggota manual!')
        return redirect('dashboard')

    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        no_telepon = request.POST.get('no_telepon', '').strip()
        alamat = request.POST.get('alamat', '').strip()
        kelompok_id = request.session.get('kelompok_id')
        kelompok = KelompokArisan.objects.filter(pk=kelompok_id).first()
        if not kelompok:
            messages.error(request, 'Kelompok arisan tidak ditemukan!')
            return redirect('portal')

        if not nama:
            messages.error(request, 'Nama anggota wajib diisi!')
            return redirect('dashboard')

        anggota_obj, _ = Anggota.objects.get_or_create(
            nama=nama,
            defaults={'no_telepon': no_telepon, 'alamat': alamat}
        )
        if no_telepon:
            anggota_obj.no_telepon = no_telepon
        if alamat:
            anggota_obj.alamat = alamat
        anggota_obj.save()

        nomor_lot = kelompok.peserta.count() + 1
        PesertaArisan.objects.create(
            kelompok=kelompok,
            anggota=anggota_obj,
            nomor_undian=nomor_lot,
            is_ketua=False,
            status_setor=False
        )
        # Target pot otomatis ter-update karena total_peserta bertambah!
        messages.success(request, f'Anggota "{nama}" berhasil didaftarkan sebagai Lot #{nomor_lot:02d}! Target pot otomatis menjadi Rp {kelompok.total_pot_hadiah:,.0f}.'.replace(',', '.'))
        return redirect('dashboard')

    return redirect('dashboard')


def anggota_update(request, pk):
    """Ketua Edit Data Anggota (CRUD Update)"""
    if request.session.get('user_role') != 'ketua':
        messages.error(request, 'Hanya Ketua yang berwenang mengubah data anggota!')
        return redirect('dashboard')

    peserta = get_object_or_404(PesertaArisan, pk=pk)
    anggota = peserta.anggota

    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        no_telepon = request.POST.get('no_telepon', '').strip()
        alamat = request.POST.get('alamat', '').strip()

        if not nama:
            messages.error(request, 'Nama anggota tidak boleh kosong!')
            return redirect('dashboard')

        anggota.nama = nama
        anggota.no_telepon = no_telepon
        anggota.alamat = alamat
        anggota.save()

        messages.success(request, f'Data anggota "{nama}" (Lot #{peserta.nomor_undian:02d}) berhasil diperbarui!')
        return redirect('dashboard')

    return redirect('dashboard')


def anggota_delete(request, pk):
    """Ketua Hapus Anggota dari Kelompok (CRUD Delete)"""
    if request.session.get('user_role') != 'ketua':
        messages.error(request, 'Hanya Ketua yang berhak menghapus peserta!')
        return redirect('dashboard')

    peserta = get_object_or_404(PesertaArisan, pk=pk)
    if peserta.is_ketua:
        messages.error(request, 'Ketua kelompok tidak dapat dihapus dari daftar arisan!')
        return redirect('dashboard')

    nama = peserta.anggota.nama
    nomor = peserta.nomor_undian

    # Cegah ProtectedError jika peserta sudah memenangkan undian
    if peserta.status_menang or peserta.kemenangan.exists():
        messages.error(request, f'Warga "{nama}" sudah tercatat memenangkan arisan pada putaran sebelumnya. Hapus riwayat kemenangannya terlebih dahulu jika ingin menghapus warga ini.')
        return redirect('dashboard')

    anggota_obj = peserta.anggota
    peserta.delete()

    # Bersihkan master Anggota jika tidak lagi mengikuti kelompok lain (bebas orphan record)
    if anggota_obj.keikutsertaan.count() == 0:
        anggota_obj.delete()

    messages.success(request, f'Peserta "{nama}" (Lot #{nomor:02d}) berhasil dihapus permanen dari database.')
    return redirect('dashboard')


def kelompok_list(request):
    """Halaman Info Kelompok (atau langsung redirect ke dashboard)"""
    return redirect('dashboard')


def kocokan_view(request, kelompok_id=None):
    """Ruang Pengundian Live (Ketua sebagai Pemutar Otoritatif, Anggota sebagai Penonton)"""
    session_kelompok_id = request.session.get('kelompok_id')
    active_id = kelompok_id or session_kelompok_id

    if not active_id:
        return redirect('portal')

    kelompok = KelompokArisan.objects.filter(pk=active_id).first()
    if not kelompok:
        request.session.pop('kelompok_id', None)
        request.session.pop('peserta_id', None)
        messages.warning(request, "Ruang arisan tidak ditemukan atau telah dihapus.")
        return redirect('portal')

    user_role = request.session.get('user_role', 'anggota')

    # Cek & Picu Pengocokan Otomatis jika sudah jatuh tempo
    auto_riwayat = kelompok.check_and_trigger_auto_draw()
    if auto_riwayat:
        messages.info(request, f"⚡ Pengocokan Otomatis Sistem: Periode ke-{auto_riwayat.periode_ke} dimenangkan oleh {auto_riwayat.peserta_menang.anggota.nama} karena telah melewati batas hari!")

    # Aturan Arisan: Kandidat undian adalah seluruh anggota yang BELUM MENANG dalam siklus ini
    kandidat_siap = list(kelompok.get_peserta_siap_undi())
    semua_peserta = kelompok.peserta.all().order_by('nomor_undian')
    riwayat_list = kelompok.riwayat.all().order_by('-tanggal_kocok')

    context = {
        'kelompok': kelompok,
        'user_role': user_role,
        'user_nama': request.session.get('user_nama'),
        'kandidat_siap': kandidat_siap,
        'semua_peserta': semua_peserta,
        'riwayat_list': riwayat_list,
        'sisa_kandidat_count': len(kandidat_siap),
        'deadline_kocok': kelompok.deadline_kocok,
        'sisa_hari_kocok': kelompok.sisa_hari_kocok,
    }
    return render(request, 'kocokan.html', context)


def proses_kocok_api(request, kelompok_id):
    """
    API Eksekusi Pengocokan (HANYA BISA DIAKSES OLEH KETUA)
    Aturan: Berapa pun nominal yang terkumpul, tetap bisa dikocok.
    Pemenang yang sudah keluar tidak akan keluar lagi 2x dalam satu siklus!
    """
    if request.session.get('user_role') != 'ketua':
        return JsonResponse({
            'status': 'error', 
            'message': 'Akses Ditolak! Hanya Ketua Kelompok yang memiliki otoritas memutar roda undian.'
        }, status=403)

    if request.method == 'POST':
        kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
        kandidat = list(kelompok.get_peserta_siap_undi())

        if not kandidat:
            return JsonResponse({
                'status': 'error', 
                'message': 'Seluruh anggota kelompok ini sudah pernah menang dalam siklus ini! Siklus akan di-reset untuk putaran baru.'
            })

        # Algoritma Acak Pemenang Objektif (Hanya yang belum pernah menang)
        pemenang = random.choice(kandidat)
        pemenang.status_menang = True
        pemenang.save()

        # Rekam Transaksi Riwayat
        periode = kelompok.riwayat.count() + 1
        total_hadiah = kelompok.total_pot_hadiah
        catatan = request.POST.get('catatan', f'Pengocokan Putaran Periode Ke-{periode}')

        riwayat = RiwayatKocokan.objects.create(
            kelompok=kelompok,
            peserta_menang=pemenang,
            periode_ke=periode,
            total_diterima=total_hadiah,
            catatan=catatan
        )

        sisa_belum_menang = kelompok.peserta.filter(status_menang=False).count()
        cycle_note = ""
        if sisa_belum_menang == 0:
            cycle_note = " (Siklus lengkap! Semua anggota telah memenangkan arisan)"

        return JsonResponse({
            'status': 'success',
            'pemenang_nama': pemenang.anggota.nama,
            'nomor_undian': pemenang.nomor_undian,
            'kontak': pemenang.anggota.no_telepon or '-',
            'alamat': pemenang.anggota.alamat or '-',
            'total_hadiah': f"Rp {total_hadiah:,.0f}".replace(",", "."),
            'periode_ke': periode,
            'kuitansi_id': riwayat.id,
            'message': f'Selamat kepada {pemenang.anggota.nama} (Lot #{pemenang.nomor_undian:02d}) yang memenangkan undian periode ke-{periode}!{cycle_note}'
        })

    return JsonResponse({'status': 'error', 'message': 'Metode request tidak diizinkan.'}, status=405)


def kuitansi_detail(request, riwayat_id):
    """Tampilan Cetak Kuitansi Resmi Pemenang"""
    riwayat = get_object_or_404(RiwayatKocokan, pk=riwayat_id)
    return render(request, 'kuitansi.html', {'riwayat': riwayat})


def riwayat_kas_view(request):
    """
    Fitur Revolusioner Transparansi Kas & Hall of Fame Pemenang
    (Menggantikan Django Admin di Sidebar & Mobile Tab Bar)
    Menampilkan:
    1. Hall of Fame Arsip Pemenang & Kuitansi Digital
    2. Transparansi Kas (Total Masuk, Keluar, Saldo Cadangan)
    3. Generator 1-Klik Broadcast Laporan ke WhatsApp
    4. Aturan & Kebijakan Kelompok Arisan
    """
    kelompok_id = request.session.get('kelompok_id')
    if not kelompok_id:
        return redirect('portal')

    kelompok = KelompokArisan.objects.filter(pk=kelompok_id).first()
    if not kelompok:
        request.session.pop('kelompok_id', None)
        request.session.pop('peserta_id', None)
        messages.warning(request, "Ruang arisan tidak ditemukan atau telah dihapus.")
        return redirect('portal')

    user_role = request.session.get('user_role', 'anggota')
    user_nama = request.session.get('user_nama', '')

    riwayat_list = kelompok.riwayat.all().order_by('-tanggal_kocok')
    total_hadiah_keluar = sum(r.total_diterima for r in riwayat_list)
    total_kas_terkumpul = kelompok.total_kas_terkumpul
    total_pot_hadiah = kelompok.total_pot_hadiah
    sisa_kekurangan = kelompok.sisa_kekurangan_kas

    peserta_lunas = kelompok.peserta.filter(status_setor=True).select_related('anggota')
    peserta_belum = kelompok.peserta.filter(status_setor=False).select_related('anggota')

    # Buat format teks WhatsApp broadcast otomatis untuk pengurus / warga
    wa_broadcast_text = (
        f"📢 *LAPORAN TRANSPARANSI KAS ARISAN*\n"
        f"Kelompok: *{kelompok.nama_kelompok}* (Room: `{kelompok.kode_room}`)\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 Target Kas Putaran: Rp {total_pot_hadiah:,.0f}\n"
        f"✅ Kas Terkumpul: Rp {total_kas_terkumpul:,.0f} ({kelompok.total_lunas_count}/{kelompok.total_peserta} warga lunas)\n"
        f"⏳ Kekurangan Iuran: Rp {sisa_kekurangan:,.0f}\n"
        f"🏆 Putaran Berikutnya: Ke-{kelompok.putaran_berikutnya}\n"
        f"📅 Batas Kocokan: {kelompok.deadline_kocok.strftime('%d %B %Y')}\n\n"
        f"Bagi warga yang belum melunasi iuran sebesar Rp {kelompok.nominal_iuran:,.0f}, mohon segera setor ke Ketua/Pengurus. Terima kasih! 🙏"
    ).replace(',', '.')

    wa_broadcast_encoded = urllib.parse.quote(wa_broadcast_text)

    context = {
        'kelompok': kelompok,
        'user_role': user_role,
        'user_nama': user_nama,
        'riwayat_list': riwayat_list,
        'total_hadiah_keluar': total_hadiah_keluar,
        'total_kas_terkumpul': total_kas_terkumpul,
        'total_pot_hadiah': total_pot_hadiah,
        'sisa_kekurangan': sisa_kekurangan,
        'peserta_lunas': peserta_lunas,
        'peserta_belum': peserta_belum,
        'wa_broadcast_text': wa_broadcast_text,
        'wa_broadcast_encoded': wa_broadcast_encoded,
    }
    return render(request, 'riwayat_kas.html', context)


def grup_saya_view(request):
    """
    Pusat Kendali Multi-Arisan (Grup Saya) & Tombol Keluar Resmi
    Menampilkan seluruh kelompok arisan yang diikuti pengguna (1 warga bisa ikut banyak arisan).
    Bisa berpindah kelompok secara instan, gabung kelompok baru dengan kode room, atau buat kelompok baru.
    """
    user_nama = request.session.get('user_nama')
    user_hp = request.session.get('user_hp', '')
    current_kelompok_id = request.session.get('kelompok_id')
    user_role = request.session.get('user_role', 'anggota')

    if not user_nama or not current_kelompok_id:
        return redirect('portal')

    kelompok_aktif = KelompokArisan.objects.filter(pk=current_kelompok_id).first()
    if not kelompok_aktif:
        anggota_obj = Anggota.objects.filter(nama=user_nama).first()
        fallback_peserta = PesertaArisan.objects.filter(anggota=anggota_obj).first() if anggota_obj else None
        if fallback_peserta:
            request.session['kelompok_id'] = fallback_peserta.kelompok.id
            kelompok_aktif = fallback_peserta.kelompok
        else:
            request.session.pop('kelompok_id', None)
            request.session.pop('peserta_id', None)
            messages.warning(request, "Ruang arisan aktif tidak ditemukan. Silakan bergabung ke kelompok arisan.")
            return redirect('portal')

    # Temukan semua keanggotaan pengguna ini di berbagai kelompok
    anggota_obj = Anggota.objects.filter(nama=user_nama).first()
    if anggota_obj:
        daftar_keanggotaan = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok').order_by('-is_ketua', 'kelompok__nama_kelompok')
    else:
        daftar_keanggotaan = PesertaArisan.objects.filter(kelompok=kelompok_aktif).select_related('kelompok')

    peserta_aktif = PesertaArisan.objects.filter(kelompok=kelompok_aktif, anggota__nama=user_nama).first()

    context = {
        'user_nama': user_nama,
        'user_hp': user_hp,
        'user_role': user_role,
        'kelompok': kelompok_aktif,
        'peserta_aktif': peserta_aktif,
        'daftar_keanggotaan': daftar_keanggotaan,
        'total_grup_diikuti': daftar_keanggotaan.count() if hasattr(daftar_keanggotaan, 'count') else 1,
    }
    return render(request, 'grup_saya.html', context)


def switch_kelompok(request, kelompok_id):
    """Beralih ke kelompok arisan lain yang sudah diikuti pengguna"""
    user_nama = request.session.get('user_nama')
    if not user_nama:
        return redirect('portal')

    target_kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta = PesertaArisan.objects.filter(kelompok=target_kelompok, anggota__nama=user_nama).first()

    if not peserta:
        messages.error(request, f"Anda belum terdaftar di kelompok '{target_kelompok.nama_kelompok}'. Masukkan kode room untuk bergabung!")
        return redirect('grup_saya')

    request.session['kelompok_id'] = target_kelompok.id
    request.session['user_role'] = 'ketua' if peserta.is_ketua else 'anggota'
    request.session['peserta_id'] = peserta.id

    messages.success(request, f"Beralih ke '{target_kelompok.nama_kelompok}' sebagai {'👑 KETUA' if peserta.is_ketua else '👤 ANGGOTA'}!")
    return redirect('dashboard')


def gabung_kelompok_baru(request):
    """Anggota bergabung ke kelompok arisan lain menggunakan Kode Room"""
    user_nama = request.session.get('user_nama')
    user_hp = request.session.get('user_hp', '')

    if not user_nama:
        return redirect('portal')

    if request.method == 'POST' or request.GET.get('kode_room'):
        kode_room = (request.POST.get('kode_room') or request.GET.get('kode_room', '')).strip().upper()
        if not kode_room:
            messages.error(request, "Silakan masukkan Kode Room yang valid!")
            return redirect('grup_saya')

        target_kelompok = KelompokArisan.objects.filter(kode_room__iexact=kode_room).first()
        if not target_kelompok:
            messages.error(request, f"Kode Room '{kode_room}' tidak ditemukan! Pastikan kode room benar.")
            return redirect('grup_saya')

        anggota_obj, _ = Anggota.objects.get_or_create(
            nama=user_nama,
            defaults={'no_telepon': user_hp}
        )

        peserta, created = PesertaArisan.objects.get_or_create(
            kelompok=target_kelompok,
            anggota=anggota_obj,
            defaults={
                'nomor_undian': target_kelompok.peserta.count() + 1,
                'is_ketua': False,
                'status_setor': False
            }
        )

        request.session['kelompok_id'] = target_kelompok.id
        request.session['user_role'] = 'ketua' if peserta.is_ketua else 'anggota'
        request.session['peserta_id'] = peserta.id

        if created:
            messages.success(request, f"Selamat! Anda berhasil bergabung di '{target_kelompok.nama_kelompok}' sebagai Lot #{peserta.nomor_undian:02d}!")
        else:
            messages.info(request, f"Anda sudah terdaftar di '{target_kelompok.nama_kelompok}'. Berhasil beralih ke ruang ini!")

        return redirect('dashboard')

    return redirect('grup_saya')


def buat_kelompok_baru(request):
    """Pengguna membuat program arisan baru (Otomatis menjadi Ketua di kelompok baru)"""
    user_nama = request.session.get('user_nama')
    user_hp = request.session.get('user_hp', '')

    if not user_nama:
        return redirect('portal')

    if request.method == 'POST':
        nama_kelompok = request.POST.get('nama_kelompok', '').strip()
        nominal_iuran = request.POST.get('nominal_iuran', '20000')
        periode_kocok = request.POST.get('periode_kocok', 'bulanan')

        if not nama_kelompok:
            messages.error(request, "Nama kelompok arisan wajib diisi!")
            return redirect('grup_saya')

        kode_room = generate_room_code()
        kelompok_baru = KelompokArisan.objects.create(
            nama_kelompok=nama_kelompok,
            kode_room=kode_room,
            nominal_iuran=Decimal(nominal_iuran),
            periode_kocok=periode_kocok
        )

        anggota_obj, _ = Anggota.objects.get_or_create(
            nama=user_nama,
            defaults={'no_telepon': user_hp}
        )

        peserta = PesertaArisan.objects.create(
            kelompok=kelompok_baru,
            anggota=anggota_obj,
            nomor_undian=1,
            is_ketua=True,
            status_setor=True
        )

        request.session['kelompok_id'] = kelompok_baru.id
        request.session['user_role'] = 'ketua'
        request.session['peserta_id'] = peserta.id

        messages.success(request, f"Kelompok '{nama_kelompok}' berhasil dibuat dengan Kode Room #{kode_room}! Anda adalah Ketua kelompok ini.")
        return redirect('dashboard')

    return redirect('grup_saya')


def hapus_kelompok(request, kelompok_id):
    """
    Ketua Menghapus Ruang Arisan:
    - Hanya user yang berstatus Ketua di kelompok ini yang berhak menghapus.
    - Jika kelompok MASIH BERJALAN (belum selesai), verifikasi PIN Ketua (default: 1234 atau kelompok.pin_ketua).
    - Jika kelompok SUDAH SELESAI, dapat langsung dihapus dengan konfirmasi biasa.
    """
    user_nama = request.session.get('user_nama')
    if not user_nama:
        return redirect('portal')

    kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama, is_ketua=True).first()

    if not peserta_ketua:
        messages.error(request, "Akses ditolak! Anda bukan Ketua di kelompok arisan ini.")
        return redirect('grup_saya')

    if request.method == 'POST':
        pin_input = request.POST.get('pin', '').strip()
        expected_pin = kelompok.pin_ketua or '1234'

        # Jika arisan masih berjalan, wajib verifikasi PIN
        if not kelompok.is_selesai:
            if pin_input != expected_pin and pin_input != '1234':
                messages.error(request, "PIN Pengurus salah! Gagal menghapus ruang arisan yang sedang aktif.")
                return redirect('grup_saya')

        nama_kelompok = kelompok.nama_kelompok
        # Hapus riwayat kocokan terlebih dahulu agar bebas dari ProtectedError
        kelompok.riwayat.all().delete()
        kelompok.delete()

        # Update sesi aktif jika kelompok yang dihapus adalah kelompok aktif saat ini
        if request.session.get('kelompok_id') == kelompok_id:
            anggota_obj = Anggota.objects.filter(nama=user_nama).first()
            sisa_peserta = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok').first() if anggota_obj else None
            if sisa_peserta:
                request.session['kelompok_id'] = sisa_peserta.kelompok.id
                request.session['user_role'] = 'ketua' if sisa_peserta.is_ketua else 'anggota'
                request.session['peserta_id'] = sisa_peserta.id
            else:
                # Tidak ada kelompok tersisa
                request.session.pop('kelompok_id', None)
                request.session.pop('user_role', None)
                request.session.pop('peserta_id', None)
                messages.success(request, f"Ruang arisan '{nama_kelompok}' telah berhasil dihapus. Anda tidak memiliki kelompok tersisa.")
                return redirect('portal')

        messages.success(request, f"Ruang arisan '{nama_kelompok}' berhasil dihapus secara tuntas.")
        return redirect('grup_saya')

    return redirect('grup_saya')


def keluar_kelompok(request, kelompok_id):
    """
    Anggota Keluar dari Ruang Arisan:
    - Melepas keanggotaan PesertaArisan milik pengguna ini tanpa menghapus ruang arisan bagi anggota lain.
    - Aturan Arisan: Jika anggota SUDAH PERNAH MENANG dalam periode berjalan dan arisan BELUM SELESAI, dilarang keluar!
    """
    user_nama = request.session.get('user_nama')
    if not user_nama:
        return redirect('portal')

    kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama).first()

    if not peserta:
        messages.error(request, "Anda tidak terdaftar di kelompok arisan ini.")
        return redirect('grup_saya')

    if peserta.is_ketua:
        messages.error(request, "Sebagai Ketua pengelola, Anda tidak bisa 'Keluar'. Gunakan tombol 'Hapus Ruang' jika arisan sudah tuntas.")
        return redirect('grup_saya')

    if request.method == 'POST':
        # Validasi: Jika sudah pernah menang dan arisan belum tuntas
        if peserta.status_menang and not kelompok.is_selesai:
            messages.error(request, f"Perhatian: Anda sudah menerima uang tarikan arisan pada putaran sebelumnya. Sesuai aturan gotong royong warga, Anda tidak dapat keluar sampai seluruh putaran arisan tuntas!")
            return redirect('grup_saya')

        nama_kelompok = kelompok.nama_kelompok
        # Hapus catatan kemenangan jika ada atau update peserta
        if peserta.kemenangan.exists():
            peserta.kemenangan.all().delete()
        peserta.delete()

        # Update sesi aktif jika kelompok yang ditinggalkan adalah yang sedang dibuka
        if request.session.get('kelompok_id') == kelompok_id:
            anggota_obj = Anggota.objects.filter(nama=user_nama).first()
            sisa_peserta = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok').first() if anggota_obj else None
            if sisa_peserta:
                request.session['kelompok_id'] = sisa_peserta.kelompok.id
                request.session['user_role'] = 'ketua' if sisa_peserta.is_ketua else 'anggota'
                request.session['peserta_id'] = sisa_peserta.id
            else:
                request.session.pop('kelompok_id', None)
                request.session.pop('user_role', None)
                request.session.pop('peserta_id', None)
                messages.success(request, f"Anda telah keluar dari '{nama_kelompok}'. Anda tidak memiliki kelompok aktif lainnya.")
                return redirect('portal')

        messages.success(request, f"Anda telah berhasil keluar dari kelompok '{nama_kelompok}'.")
        return redirect('grup_saya')

    return redirect('grup_saya')


def bersihkan_kelompok_selesai(request):
    """
    Shortcut Bersihkan Semua Ruang yang Sudah Selesai (FOOLPROOF):
    - HANYA menghapus / keluar dari kelompok yang statusnya SUDAH SELESAI (is_selesai == True).
    - Ruang yang sedang AKTIF/BERJALAN dijamin 100% aman dan TIDAK AKAN DISENTUH!
    - Membutuhkan konfirmasi PIN Pengurus (1234) sebagai gembok pengaman tambahan.
    """
    user_nama = request.session.get('user_nama')
    if not user_nama:
        return redirect('portal')

    if request.method == 'POST':
        pin_input = request.POST.get('pin', '').strip()
        if pin_input != '1234':
            messages.error(request, "PIN Pengurus salah! Gembok pengaman aktif untuk mencegah salah pencet.")
            return redirect('grup_saya')

        anggota_obj = Anggota.objects.filter(nama=user_nama).first()
        if not anggota_obj:
            messages.info(request, "Tidak ada data anggota ditemukan.")
            return redirect('grup_saya')

        daftar_keanggotaan = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok')
        cleaned_count = 0

        for p in list(daftar_keanggotaan):
            k = p.kelompok
            if k.is_selesai:
                if p.is_ketua:
                    k.riwayat.all().delete()
                    k.delete()
                else:
                    p.kemenangan.all().delete()
                    p.delete()
                cleaned_count += 1

        # Cek apakah sesi aktif terkena pembersihan
        curr_k_id = request.session.get('kelompok_id')
        if not KelompokArisan.objects.filter(pk=curr_k_id).exists():
            sisa_peserta = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok').first()
            if sisa_peserta:
                request.session['kelompok_id'] = sisa_peserta.kelompok.id
                request.session['user_role'] = 'ketua' if sisa_peserta.is_ketua else 'anggota'
                request.session['peserta_id'] = sisa_peserta.id
            else:
                request.session.pop('kelompok_id', None)
                request.session.pop('user_role', None)
                request.session.pop('peserta_id', None)
                messages.success(request, f"Berhasil membersihkan {cleaned_count} ruang arisan tuntas. Tidak ada ruang tersisa.")
                return redirect('portal')

        if cleaned_count > 0:
            messages.success(request, f"✨ Berhasil membersihkan {cleaned_count} ruang arisan yang telah tuntas! Seluruh ruang aktif tetap aman tersimpan.")
        else:
            messages.info(request, "Tidak ada ruang arisan berstatus 'Selesai' untuk dibersihkan. Seluruh ruang aktif tetap terjaga aman.")

        return redirect('grup_saya')

    return redirect('grup_saya')


def reset_total_kelompok(request):
    """
    Master Reset / Zona Bahaya (Pembersihan Total Aplikasi):
    - Diletakkan di Zona Bahaya paling bawah.
    - Memerlukan PIN 1234 DAN ketikan teks konfirmasi 'RESET' atau 'HAPUS'.
    - 0% risiko salah pencet tidak sengaja oleh pengguna.
    """
    user_nama = request.session.get('user_nama')
    if not user_nama:
        return redirect('portal')

    if request.method == 'POST':
        pin_input = request.POST.get('pin', '').strip()
        konfirmasi_teks = request.POST.get('konfirmasi', '').strip().upper()

        if pin_input != '1234' or konfirmasi_teks not in ['RESET', 'HAPUS']:
            messages.error(request, "Konfirmasi Reset Ditolak! Anda harus memasukkan PIN '1234' dan mengetik kata 'RESET' untuk mengeksekusi.")
            return redirect('grup_saya')

        anggota_obj = Anggota.objects.filter(nama=user_nama).first()
        if anggota_obj:
            daftar_keanggotaan = PesertaArisan.objects.filter(anggota=anggota_obj).select_related('kelompok')
            for p in list(daftar_keanggotaan):
                k = p.kelompok
                if p.is_ketua:
                    k.riwayat.all().delete()
                    k.delete()
                else:
                    p.kemenangan.all().delete()
                    p.delete()

        # Bersihkan sesi
        request.session.flush()
        messages.success(request, "Pembersihan total berhasil! Seluruh program arisan telah di-reset bersih.")
        return redirect('portal')

    return redirect('grup_saya')


def buka_setoran_baru(request, kelompok_id):
    """
    Fitur Buka Setoran Putaran Baru (Khusus Ketua):
    - Mengatur ulang (reset) status setoran seluruh anggota menjadi BELUM SETOR (False)
      untuk memulai penarikan iuran pada putaran berikutnya.
    - Status kemenangan (status_menang) dan riwayat putaran sebelumnya tetap aman tersimpan 100%.
    - Wajib POST dan verifikasi otoritas Ketua.
    """
    user_nama = request.session.get('user_nama')
    user_role = request.session.get('user_role')

    if not user_nama or user_role != 'ketua':
        messages.error(request, "Akses ditolak! Hanya Ketua yang berwenang membuka siklus setoran putaran baru.")
        return redirect('dashboard')

    kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama, is_ketua=True).first()

    if not peserta_ketua:
        messages.error(request, "Akses ditolak! Anda bukan Ketua di kelompok arisan ini.")
        return redirect('dashboard')

    if request.method == 'POST':
        total_peserta = kelompok.peserta.count()
        kelompok.peserta.all().update(status_setor=False)
        putaran_ke = kelompok.putaran_berikutnya

        messages.success(
            request, 
            f"🎉 Pengumpulan iuran untuk Putaran Ke-{putaran_ke} resmi dibuka! Status setoran {total_peserta} warga telah disetel kembali untuk periode baru. Riwayat pemenang sebelumnya tetap aman tersimpan."
        )
        return redirect('dashboard')

    return redirect('dashboard')


def riwayat_delete(request, riwayat_id):
    """
    Fitur Hapus / Batalkan Riwayat Pengundian (Khusus Ketua):
    - Mengembalikan status_menang pemenang menjadi False (masuk kembali ke daftar siap undi).
    - Menghapus rekaman RiwayatKocokan.
    - Putaran berikutnya otomatis mundur ke nomor putaran yang dibatalkan.
    """
    user_nama = request.session.get('user_nama')
    user_role = request.session.get('user_role')

    if not user_nama or user_role != 'ketua':
        messages.error(request, "Akses ditolak! Hanya Ketua yang berwenang membatalkan pengundian.")
        return redirect('riwayat_kas')

    riwayat = get_object_or_404(RiwayatKocokan, pk=riwayat_id)
    kelompok = riwayat.kelompok

    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama, is_ketua=True).first()
    if not peserta_ketua:
        messages.error(request, "Akses ditolak! Anda bukan Ketua di kelompok arisan ini.")
        return redirect('riwayat_kas')

    if request.method == 'POST':
        pemenang = riwayat.peserta_menang
        periode = riwayat.periode_ke
        nama_pemenang = pemenang.anggota.nama

        # Kembalikan status pemenang agar bisa diundi lagi
        pemenang.status_menang = False
        pemenang.save()

        # Hapus riwayat
        riwayat.delete()

        messages.success(
            request, 
            f"✨ Pengundian Putaran Ke-{periode} atas nama {nama_pemenang} berhasil dibatalkan. Warga telah dikembalikan ke daftar siap undi."
        )
        referer = request.META.get('HTTP_REFERER', '')
        if 'kocokan' in referer:
            return redirect('kocokan_view')
        return redirect('riwayat_kas')

    return redirect('riwayat_kas')


def riwayat_hapus_semua(request, kelompok_id):
    """
    Hapus / Reset Seluruh Riwayat Pemenang (Khusus Ketua):
    - Mengembalikan status_menang seluruh peserta di kelompok menjadi False.
    - Menghapus seluruh rekaman RiwayatKocokan di kelompok ini.
    - Putaran berikutnya otomatis kembali ke Putaran Ke-1.
    """
    user_nama = request.session.get('user_nama')
    user_role = request.session.get('user_role')

    if not user_nama or user_role != 'ketua':
        messages.error(request, "Akses ditolak! Hanya Ketua yang berwenang menghapus semua riwayat.")
        return redirect('riwayat_kas')

    kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama, is_ketua=True).first()

    if not peserta_ketua:
        messages.error(request, "Akses ditolak! Anda bukan Ketua di kelompok arisan ini.")
        return redirect('riwayat_kas')

    if request.method == 'POST':
        total_riwayat = kelompok.riwayat.count()
        kelompok.peserta.all().update(status_menang=False)
        kelompok.riwayat.all().delete()

        messages.success(
            request, 
            f"🗑️ Sukses! Seluruh {total_riwayat} riwayat pengundian berhasil dihapus bersih. Semua warga telah dikembalikan ke daftar siap undi dari putaran ke-1."
        )
        referer = request.META.get('HTTP_REFERER', '')
        if 'kocokan' in referer:
            return redirect('kocokan_view')
        return redirect('riwayat_kas')

    return redirect('riwayat_kas')


def tandai_semua_lunas(request, kelompok_id):
    """
    Fitur 1-Klik Tandai Semua Warga Lunas (Khusus Hari Pertemuan Arisan):
    - Mempermudah Ketua/Bendahara saat seluruh warga menyetor uang tunai serentak di hari-H arisan.
    - Mengubah status_setor seluruh peserta di kelompok menjadi True dalam 1 kali sentuhan.
    """
    user_nama = request.session.get('user_nama')
    user_role = request.session.get('user_role')

    if not user_nama or user_role != 'ketua':
        messages.error(request, "Akses ditolak! Hanya Ketua yang berwenang menandai kelunasan massal.")
        return redirect('dashboard')

    kelompok = get_object_or_404(KelompokArisan, pk=kelompok_id)
    peserta_ketua = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama, is_ketua=True).first()

    if not peserta_ketua:
        messages.error(request, "Akses ditolak! Anda bukan Ketua di kelompok arisan ini.")
        return redirect('dashboard')

    if request.method == 'POST':
        total = kelompok.peserta.count()
        kelompok.peserta.all().update(status_setor=True)

        messages.success(
            request, 
            f"✅ Sukses! Seluruh {total} warga di kelompok '{kelompok.nama_kelompok}' telah ditandai LUNAS SETOR untuk putaran ini."
        )
        return redirect('dashboard')

    return redirect('dashboard')


# ==============================================================================
# TAHAP 4: HEADLESS DJANGO REST API V1 & SMART DELTA HEARTBEAT POLLER
# ==============================================================================

def _format_rupiah(value):
    """Memformat nilai desimal/angka menjadi string Rupiah bertitik."""
    return f"Rp {int(value):,}".replace(",", ".")


def _get_authorized_room(request, kode_room):
    """Memvalidasi sesi aktif dan mengembalikan instance KelompokArisan yang berhak diakses."""
    session_kelompok_id = request.session.get('kelompok_id')
    if not session_kelompok_id:
        return None, JsonResponse({'status': 'error', 'message': 'Sesi tidak aktif.'}, status=401)

    kelompok = KelompokArisan.objects.filter(kode_room__iexact=kode_room).first()
    if not kelompok:
        return None, JsonResponse({'status': 'error', 'message': 'Room tidak ditemukan.'}, status=404)

    if kelompok.id != session_kelompok_id:
        user_nama = request.session.get('user_nama', '')
        is_member = PesertaArisan.objects.filter(kelompok=kelompok, anggota__nama=user_nama).exists()
        if not is_member:
            return None, JsonResponse({'status': 'error', 'message': 'Akses room ditolak.'}, status=403)

    return kelompok, None


def _compute_room_version(kelompok):
    """Menghitung hash sidik jari status room secara cepat tanpa migrasi skema DB."""
    peserta_rows = list(
        kelompok.peserta.values_list(
            'id', 'nomor_undian', 'is_ketua', 'status_setor', 'status_menang', 'anggota__nama'
        ).order_by('nomor_undian')
    )
    latest_riwayat = kelompok.riwayat.values_list('id', 'periode_ke').first()
    riwayat_count = kelompok.riwayat.count()
    raw = f"{kelompok.nama_kelompok}|{kelompok.nominal_iuran}|{kelompok.periode_kocok}|{riwayat_count}|{latest_riwayat}|{peserta_rows}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()[:12], peserta_rows


def _build_room_snapshot(kelompok, version, peserta_rows=None):
    """Menyusun payload JSON ringkas untuk detail room, statistik finansial, dan peserta."""
    if peserta_rows is None:
        peserta_rows = list(
            kelompok.peserta.values_list(
                'id', 'nomor_undian', 'is_ketua', 'status_setor', 'status_menang', 'anggota__nama'
            ).order_by('nomor_undian')
        )

    total_peserta = len(peserta_rows)
    total_lunas = sum(1 for row in peserta_rows if row[3])
    nominal = kelompok.nominal_iuran
    target_pot = total_peserta * nominal
    total_kas = total_lunas * nominal
    sisa_kas = max(Decimal('0'), target_pot - total_kas)
    persentase = min(100, int((total_kas / target_pot) * 100)) if target_pot > 0 else 0
    latest_riwayat = kelompok.riwayat.select_related('peserta_menang__anggota').first()

    return {
        'has_update': True,
        'version': version,
        'room': {
            'id': kelompok.id,
            'nama_kelompok': kelompok.nama_kelompok,
            'kode_room': kelompok.kode_room,
            'putaran_berikutnya': kelompok.putaran_berikutnya,
            'nominal_iuran': int(nominal),
            'nominal_iuran_formatted': _format_rupiah(nominal),
            'frekuensi_setor': kelompok.frekuensi_setor,
            'sisa_hari_kocok': kelompok.sisa_hari_kocok,
        },
        'stats': {
            'total_peserta': total_peserta,
            'total_lunas': total_lunas,
            'target_pot_formatted': _format_rupiah(target_pot),
            'total_kas_formatted': _format_rupiah(total_kas),
            'sisa_kekurangan_formatted': _format_rupiah(sisa_kas),
            'persentase_lunas': persentase,
        },
        'members': [
            {
                'id': r[0],
                'nomor_undian': r[1],
                'is_ketua': r[2],
                'status_setor': r[3],
                'status_menang': r[4],
                'nama': r[5],
            }
            for r in peserta_rows
        ],
        'latest_winner': {
            'id': latest_riwayat.id,
            'periode_ke': latest_riwayat.periode_ke,
            'nama': latest_riwayat.peserta_menang.anggota.nama,
            'nomor_undian': latest_riwayat.peserta_menang.nomor_undian,
        } if latest_riwayat else None,
    }


def api_room_sync(request, kode_room):
    """Smart Delta Heartbeat Poller: mengembalikan ~40 byte JSON jika belum ada mutasi."""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    kelompok, err_resp = _get_authorized_room(request, kode_room)
    if err_resp:
        return err_resp

    current_version, peserta_rows = _compute_room_version(kelompok)
    client_version = request.GET.get('version') or request.GET.get('v') or ''

    if client_version and client_version == current_version:
        return JsonResponse({'has_update': False, 'version': current_version})

    return JsonResponse(_build_room_snapshot(kelompok, current_version, peserta_rows))


def api_room_detail(request, kode_room):
    """Endpoint REST untuk mengambil metadata lengkap & KPI finansial sebuah room."""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    kelompok, err_resp = _get_authorized_room(request, kode_room)
    if err_resp:
        return err_resp

    version, peserta_rows = _compute_room_version(kelompok)
    payload = _build_room_snapshot(kelompok, version, peserta_rows)
    payload.pop('has_update', None)
    payload['status'] = 'success'
    return JsonResponse(payload)


def api_room_warga(request, kode_room):
    """Endpoint REST untuk mengambil daftar anggota & status iuran pada sebuah room."""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    kelompok, err_resp = _get_authorized_room(request, kode_room)
    if err_resp:
        return err_resp

    peserta_list = kelompok.peserta.select_related('anggota').order_by('nomor_undian')
    return JsonResponse({
        'status': 'success',
        'kode_room': kelompok.kode_room,
        'total': peserta_list.count(),
        'warga': [
            {
                'id': p.id,
                'nama': p.anggota.nama,
                'no_telepon': p.anggota.no_telepon or '',
                'nomor_undian': p.nomor_undian,
                'is_ketua': p.is_ketua,
                'status_setor': p.status_setor,
                'status_menang': p.status_menang,
            }
            for p in peserta_list
        ],
    })


def api_kas_riwayat(request):
    """Endpoint REST ringkasan transparansi kas & riwayat pemenang room aktif."""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    kelompok_id = request.session.get('kelompok_id')
    if not kelompok_id:
        return JsonResponse({'status': 'error', 'message': 'Sesi tidak aktif.'}, status=401)

    kelompok = KelompokArisan.objects.filter(pk=kelompok_id).first()
    if not kelompok:
        return JsonResponse({'status': 'error', 'message': 'Room tidak ditemukan.'}, status=404)

    riwayat_list = kelompok.riwayat.select_related('peserta_menang__anggota').order_by('-periode_ke')
    total_hadiah_keluar = sum(r.total_diterima for r in riwayat_list)

    return JsonResponse({
        'status': 'success',
        'kode_room': kelompok.kode_room,
        'total_pot_formatted': _format_rupiah(kelompok.total_pot_hadiah),
        'total_kas_terkumpul_formatted': _format_rupiah(kelompok.total_kas_terkumpul),
        'sisa_kekurangan_formatted': _format_rupiah(kelompok.sisa_kekurangan_kas),
        'total_hadiah_keluar_formatted': _format_rupiah(total_hadiah_keluar),
        'riwayat': [
            {
                'id': r.id,
                'periode_ke': r.periode_ke,
                'pemenang': r.peserta_menang.anggota.nama,
                'nomor_undian': r.peserta_menang.nomor_undian,
                'tanggal_kocok': r.tanggal_kocok.isoformat(),
                'total_diterima': int(r.total_diterima),
                'total_diterima_formatted': _format_rupiah(r.total_diterima),
            }
            for r in riwayat_list
        ],
    })






