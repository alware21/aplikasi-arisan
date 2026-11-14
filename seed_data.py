import os
import django
from datetime import date
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from arisan.models import Anggota, KelompokArisan, PesertaArisan, RiwayatKocokan

def update_seed():
    print("Updating seed with Ketua & Setoran status...")
    kelompok = KelompokArisan.objects.first()
    if kelompok:
        kelompok.kode_room = "RT0526"
        kelompok.pin_ketua = "1234"
        kelompok.periode_kocok = "bulanan"
        kelompok.save()
        print(f"Kelompok updated: {kelompok.nama_kelompok} [Kode Room: {kelompok.kode_room}]")

    # Update Peserta 1 as Ketua
    peserta_list = list(PesertaArisan.objects.all())
    for i, p in enumerate(peserta_list):
        if i == 0:
            p.is_ketua = True
            p.status_setor = True
        elif i in [1, 2]: # Pak Budi & Ibu Dewi sudah setor
            p.is_ketua = False
            p.status_setor = True
        else: # Pak Ahmad & Ibu Rina belum setor
            p.is_ketua = False
            p.status_setor = False
        p.save()
        peran = "👑 KETUA" if p.is_ketua else "👤 ANGGOTA"
        setor = "Sudah Setor" if p.status_setor else "Belum Setor"
        print(f"  {peran}: Lot #{p.nomor_undian:02d} {p.anggota.nama} - {setor}")

    print("Seed updated successfully!")

if __name__ == '__main__':
    update_seed()
