import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from arisan.models import KelompokArisan, PesertaArisan, Anggota

c = Client()

# 1. Test Portal GET
r = c.get('/')
assert r.status_code == 200, f'Portal GET failed: {r.status_code}'
print('[PASS] Portal GET / returned 200 OK')

# 2. Test Ketua Login / Group Init
r = c.post('/portal/', {
    'peran': 'ketua',
    'nama': 'Ibu Siti Nurhaliza',
    'no_telepon': '081234567890',
    'alamat': 'Jl. Melati No. 12',
    'pin': '1234',
    'nama_kelompok': 'Arisan Warga RT 05',
    'nominal_iuran': '200000',
    'periode_kocok': 'bulanan'
}, follow=True)
assert r.status_code == 200, f'Ketua login failed: {r.status_code}'
assert c.session['user_role'] == 'ketua', 'Session user_role not ketua'
print('[PASS] Ketua portal login & session verified')

# 3. Test Dashboard as Ketua
r = c.get('/dashboard/')
assert r.status_code == 200
kelompok = KelompokArisan.objects.get(pk=c.session['kelompok_id'])
print(f'[PASS] Dashboard loaded. Kelompok: {kelompok.nama_kelompok}, Room: {kelompok.kode_room}, Periode: {kelompok.periode_kocok}, Frekuensi: {kelompok.frekuensi_setor}')

# 4. Test Toggle Setor
peserta_2 = kelompok.peserta.filter(is_ketua=False).first()
if peserta_2:
    old_status = peserta_2.status_setor
    r = c.post(f'/peserta/toggle-setor/{peserta_2.id}/')
    assert r.status_code == 200
    peserta_2.refresh_from_db()
    assert peserta_2.status_setor != old_status
    print(f'[PASS] Toggle setor AJAX passed: {peserta_2.anggota.nama} status changed to {peserta_2.status_setor}')

# Ensure we have candidates ready for draw
for p in kelompok.peserta.filter(status_menang=False)[:2]:
    p.status_setor = True
    p.save()

# 5. Test Pengocokan Live API
r = c.post(f'/kocokan/api/proses/{kelompok.id}/')
assert r.status_code == 200
data = r.json()
print(f"[PASS] Pengocokan Live API passed: Status={data.get('status')}, Pemenang={data.get('pemenang_nama')}, Lot={data.get('nomor_undian')}, Hadiah={data.get('total_hadiah')}")

# 6. Test Anggota Joining via Room Code
c2 = Client()
r = c2.post('/portal/', {
    'peran': 'anggota',
    'nama': 'Doni Kusuma (Warga Baru)',
    'no_telepon': '089876543210',
    'alamat': 'RT 05 Blok E',
    'kode_room': kelompok.kode_room
}, follow=True)
assert r.status_code == 200
assert c2.session['user_role'] == 'anggota'
print(f"[PASS] Anggota join with Room Code passed, verified in session as {c2.session['user_role']}")
