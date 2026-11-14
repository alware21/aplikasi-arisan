from .models import KelompokArisan, PesertaArisan, Anggota

def arisan_context(request):
    """
    Menyediakan data global ke seluruh template Django:
    - Informasi grup aktif (kelompok)
    - Identitas pengguna (user_nama, user_hp, user_role)
    - Kartu peserta aktif pengguna di kelompok saat ini (peserta_aktif)
    - Jumlah total kelompok arisan yang diikuti pengguna (total_grup_count)
    """
    kelompok_id = request.session.get('kelompok_id')
    user_nama = request.session.get('user_nama')
    user_role = request.session.get('user_role', 'anggota')
    user_hp = request.session.get('user_hp', '')
    
    kelompok = None
    peserta_aktif = None
    total_grup_count = 0

    if kelompok_id:
        kelompok = KelompokArisan.objects.filter(id=kelompok_id).first()

    if user_nama:
        anggota = Anggota.objects.filter(nama=user_nama).first()
        if anggota:
            total_grup_count = PesertaArisan.objects.filter(anggota=anggota).count()
            if kelompok:
                peserta_aktif = PesertaArisan.objects.filter(kelompok=kelompok, anggota=anggota).first()

    return {
        'kelompok': kelompok,
        'user_nama': user_nama,
        'user_role': user_role,
        'user_hp': user_hp,
        'peserta_aktif': peserta_aktif,
        'total_grup_count': total_grup_count,
    }
