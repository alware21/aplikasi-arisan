import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from arisan.models import Anggota, KelompokArisan, PesertaArisan, RiwayatKocokan

cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'arisan_%';")
tables = cursor.fetchall()
print("=== TABEL-TABEL ARISAN DI DATABASE ===")
for t in tables:
    table_name = t[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    cols = cursor.fetchall()
    col_str = ", ".join([f"{c[1]} ({c[2]})" for c in cols])
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]
    print(f"\n[TABLE] {table_name} ({row_count} records)")
    print(f"  Columns: {col_str}")

print("\n=== PEMERIKSAAN RELASI & DATA ===")
for k in KelompokArisan.objects.all():
    print(f"\nKelompok: {k.nama_kelompok} (Room: {k.kode_room})")
    print(f"  Nominal: Rp {k.nominal_iuran:,.0f} | Periode: {k.periode_kocok} ({k.durasi_hari} hari)")
    print(f"  Target Pot Real-time: Rp {k.total_pot_hadiah:,.0f} ({k.total_peserta} peserta)")
    print(f"  Kas Terkumpul: Rp {k.total_kas_terkumpul:,.0f} ({k.total_lunas_count} lunas)")
    print(f"  Kekurangan: Rp {k.sisa_kekurangan_kas:,.0f} ({k.persentase_kelunasan}%)")
    print(f"  Jatuh Tempo: {k.deadline_kocok} (Sisa {k.sisa_hari_kocok} hari)")
    print(f"  Daftar Peserta:")
    for p in k.peserta.all():
        role = "👑 KETUA" if p.is_ketua else "👤 ANGGOTA"
        setor = "LUNAS" if p.status_setor else "BELUM"
        menang = "MENANG" if p.status_menang else "ANTRE"
        print(f"    - Lot #{p.nomor_undian:02d}: {p.anggota.nama} [{role}] Setor={setor}, Status={menang}")
    print(f"  Riwayat Kocokan ({k.riwayat.count()} putaran):")
    for r in k.riwayat.all():
        print(f"    - Periode #{r.periode_ke}: {r.peserta_menang.anggota.nama} | Hadiah: Rp {r.total_diterima:,.0f} | Tgl: {r.tanggal_kocok}")
