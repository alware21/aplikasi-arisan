"""
================================================================================
TUGAS PRAKTIK PEMROGRAMAN BERORIENTASI OBJEK (PjBL)
Topik: Encapsulation, Constructor, Getter-Setter, dan Hubungan Antarclass/Object
Studi Kasus : Aplikasi Arisan Digital Desktop (Mode Offline)
Dosen       : Zuliar Efendi, M.Kom.
================================================================================
"""

import random
from datetime import datetime


# ==============================================================================
# CLASS 1: Anggota
# Konsep: Encapsulation, Constructor (__init__), Getter-Setter (@property)
# ==============================================================================
class Anggota:
    def __init__(self, id_anggota: str, nama: str, no_hp: str):
        # Attribute internal diawali underscore (konvensi protected/private)
        self._id_anggota = id_anggota
        self._nama = ""
        self._no_hp = ""

        # Menggunakan setter agar langsung tervalidasi saat inisialisasi
        self.nama = nama
        self.no_hp = no_hp

    # --- Property Getter & Setter: Nama ---
    @property
    def id_anggota(self) -> str:
        return self._id_anggota

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, nilai: str):
        # Validasi aturan bisnis: Nama tidak boleh kosong
        if not nilai or not nilai.strip():
            raise ValueError("[Validasi Gagal] Nama anggota tidak boleh kosong!")
        self._nama = nilai.strip()

    # --- Property Getter & Setter: Nomor HP ---
    @property
    def no_hp(self) -> str:
        return self._no_hp

    @no_hp.setter
    def no_hp(self, nilai: str):
        # Validasi aturan bisnis: Nomor HP minimal 10 digit angka
        if not nilai or len(nilai.strip()) < 10:
            raise ValueError(
                "[Validasi Gagal] Nomor HP tidak valid (minimal 10 digit)!"
            )
        self._no_hp = nilai.strip()

    # Business Method
    def info(self) -> str:
        return f"[{self._id_anggota}] {self._nama} ({self._no_hp})"


# ==============================================================================
# CLASS 2: PesertaArisan
# Konsep: Association (menyimpan object Anggota sebagai attribute)
#         Status terkunci (tidak ada public setter bebas)
# ==============================================================================
class PesertaArisan:
    def __init__(self, anggota: Anggota, nomor_undian: int):
        # Association: Objek Anggota disimpan langsung sebagai attribute
        self._anggota = anggota
        self._nomor_undian = nomor_undian
        # Status transaksi/kondisi: PRIVATE (__status_menang) agar tidak dicurangi dari luar
        self.__status_menang = False

    @property
    def anggota(self) -> Anggota:
        return self._anggota

    @property
    def nomor_undian(self) -> int:
        return self._nomor_undian

    @property
    def status_menang(self) -> bool:
        return self.__status_menang

    # Business Method: Perubahan status HANYA melalui proses resmi
    def tandai_menang(self):
        if self.__status_menang:
            raise ValueError(f"Peserta {self._anggota.nama} sudah pernah menang!")
        self.__status_menang = True


# ==============================================================================
# CLASS 3: KelompokArisan
# Konsep: Aggregation (Whole-Part Lemah: Menyimpan daftar kumpulan objek peserta)
#         Business Method (kocok_pemenang, tambah_peserta)
# ==============================================================================
class KelompokArisan:
    def __init__(self, id_arisan: str, nama_kelompok: str, nominal_iuran: float):
        self._id_arisan = id_arisan
        self._nama_kelompok = nama_kelompok
        self._nominal_iuran = 0.0
        self.nominal_iuran = nominal_iuran  # Memanggil setter untuk validasi

        # Aggregation: PRIVATE (__daftar_peserta) agar list tidak dimanipulasi langsung
        self.__daftar_peserta: list[PesertaArisan] = []

    # --- Property & Setter: Nominal Iuran ---
    @property
    def id_arisan(self) -> str:
        return self._id_arisan

    @property
    def nama_kelompok(self) -> str:
        return self._nama_kelompok

    @property
    def nominal_iuran(self) -> float:
        return self._nominal_iuran

    @nominal_iuran.setter
    def nominal_iuran(self, nilai: float):
        # Validasi: Iuran harus lebih dari 0
        if nilai <= 0:
            raise ValueError("[Validasi Gagal] Nominal iuran harus lebih besar dari 0!")
        self._nominal_iuran = nilai

    @property
    def jumlah_peserta(self) -> int:
        return len(self.__daftar_peserta)

    # --- Business Method: Menambahkan Anggota ke Kelompok (Aggregation) ---
    def tambah_peserta(self, anggota: Anggota) -> PesertaArisan:
        # Cek duplikasi anggota di dalam kelompok yang sama
        for p in self.__daftar_peserta:
            if p.anggota.id_anggota == anggota.id_anggota:
                raise ValueError(
                    f"[Gagal] Anggota {anggota.nama} sudah terdaftar di kelompok ini!"
                )

        # Generate nomor undian otomatis berurutan (1, 2, 3...)
        nomor_lot = len(self.__daftar_peserta) + 1
        peserta_baru = PesertaArisan(anggota, nomor_lot)
        self.__daftar_peserta.append(peserta_baru)
        return peserta_baru

    # --- Business Method: Mengambil peserta yang BELUM menang ---
    def get_peserta_belum_menang(self) -> list[PesertaArisan]:
        return [p for p in self.__daftar_peserta if not p.status_menang]

    # --- Business Method: Menghitung total pot hadiah arisan ---
    def hitung_total_hadiah(self) -> float:
        return len(self.__daftar_peserta) * self._nominal_iuran


# ==============================================================================
# CLASS 4: KocokanArisan
# Konsep: Association Antarobject (Menghubungkan Kelompok dan Pemenang)
# ==============================================================================
class KocokanArisan:
    def __init__(self, id_kocokan: str, kelompok: KelompokArisan, periode_ke: int):
        self._id_kocokan = id_kocokan
        # Menyimpan referensi objek kelompok
        self._kelompok = kelompok
        self._periode_ke = periode_ke
        self._tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # PRIVATE (__pemenang): tidak boleh diganti manual
        self.__pemenang: PesertaArisan | None = None
        self._total_diterima: float = 0.0

    @property
    def pemenang(self) -> PesertaArisan | None:
        return self.__pemenang

    # Business Method: Proses Eksekusi Pengocokan
    def proses_kocok(self) -> bool:
        kandidat = self._kelompok.get_peserta_belum_menang()
        if not kandidat:
            return False  # Tidak ada lagi peserta yang bisa diundi

        # Algoritma Random Picker
        self.__pemenang = random.choice(kandidat)
        self.__pemenang.tandai_menang()  # Kunci status agar tidak keluar lagi
        self._total_diterima = self._kelompok.hitung_total_hadiah()
        return True

    def cetak_kuitansi(self):
        if not self.__pemenang:
            print("Belum ada pemenang yang diundi.")
            return

        print("=" * 45)
        print("     🎉 KUITANSI RESMI ARISAN DIGITAL 🎉     ")
        print("=" * 45)
        print(f"ID Transaksi : {self._id_kocokan}")
        print(f"Kelompok     : {self._kelompok.nama_kelompok}")
        print(f"Putaran      : Periode Ke-{self._periode_ke}")
        print(f"Waktu Kocok  : {self._tanggal}")
        print("-" * 45)
        print(f"Nomor Undian : #{self.__pemenang.nomor_undian:02d}")
        print(f"Nama Pemenang: {self.__pemenang.anggota.nama}")
        print(f"Kontak       : {self.__pemenang.anggota.no_hp}")
        print(f"Total Hadiah : Rp {self._total_diterima:,.0f}".replace(",", "."))
        print("Status       : SAH (Terkunci)")
        print("=" * 45)


# ==============================================================================
# PRAKTIK UJI INTERAKSI ANTAROBJECT & UJI KESALAHAN (TESTING SCRIPT)
# Mengikuti format Praktik Python Minggu ke-4
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print(" PRAKTIK PBO: UJI INTERAKSI ANTAROBJECT (ARISAN DIGITAL) ")
    print("=" * 55 + "\n")

    # --------------------------------------------------------------------------
    # UJI 1: Pembuatan Objek Anggota & Validasi
    # --------------------------------------------------------------------------
    print("[1] MEMBUAT OBJEK ANGGOTA:")
    a1 = Anggota("A001", "Ibu Siti Aminah", "081234567890")
    a2 = Anggota("A002", "Pak Budi Santoso", "081234567891")
    a3 = Anggota("A003", "Ibu Dewi Lestari", "081234567892")
    a4 = Anggota("A004", "Pak Ahmad Fauzi", "081234567893")

    print(f"  + Berhasil dibuat: {a1.info()}")
    print(f"  + Berhasil dibuat: {a2.info()}")
    print(f"  + Berhasil dibuat: {a3.info()}")
    print(f"  + Berhasil dibuat: {a4.info()}")

    # --------------------------------------------------------------------------
    # UJI 2: Pembuatan Objek Kelompok & Aggregation
    # --------------------------------------------------------------------------
    print("\n[2] MEMBUAT KELOMPOK ARISAN & MENDAFTARKAN PESERTA:")
    kelompok1 = KelompokArisan("K01", "Arisan Guyub RT 05", 200000.0)

    # Hubungkan anggota ke kelompok
    p1 = kelompok1.tambah_peserta(a1)
    p2 = kelompok1.tambah_peserta(a2)
    p3 = kelompok1.tambah_peserta(a3)
    p4 = kelompok1.tambah_peserta(a4)

    print(f"  + Kelompok '{kelompok1.nama_kelompok}' aktif.")
    print(f"  + Iuran per orang : Rp {kelompok1.nominal_iuran:,.0f}".replace(",", "."))
    print(f"  + Total peserta   : {kelompok1.jumlah_peserta} orang")
    print(
        f"  + Total Pot Hadiah: Rp {kelompok1.hitung_total_hadiah():,.0f}".replace(
            ",", "."
        )
    )

    # --------------------------------------------------------------------------
    # UJI 3: Pengocokan Periode 1
    # --------------------------------------------------------------------------
    print("\n[3] EKSEKUSI PENGOKOCAN PERIODE 1:")
    kocokan1 = KocokanArisan("TRX-001", kelompok1, periode_ke=1)
    if kocokan1.proses_kocok():
        print("  -> Pengocokan Berhasil!")
        kocokan1.cetak_kuitansi()
    else:
        print("  -> Pengocokan Gagal!")

    # --------------------------------------------------------------------------
    # UJI 4: Pengocokan Periode 2 (Peserta yang sudah menang tidak ikut lagi)
    # --------------------------------------------------------------------------
    print("\n[4] EKSEKUSI PENGOKOCAN PERIODE 2:")
    sisa_kandidat = kelompok1.get_peserta_belum_menang()
    print(f"  + Kandidat tersisa untuk diundi: {len(sisa_kandidat)} orang.")
    for p in sisa_kandidat:
        print(f"    - Lot #{p.nomor_undian:02d}: {p.anggota.nama}")

    kocokan2 = KocokanArisan("TRX-002", kelompok1, periode_ke=2)
    if kocokan2.proses_kocok():
        print("  -> Pengocokan Berhasil!")
        kocokan2.cetak_kuitansi()

    # --------------------------------------------------------------------------
    # UJI 5: Uji Kesalahan & Validasi (Negative Testing)
    # --------------------------------------------------------------------------
    print("\n[5] UJI KESALAHAN & VALIDASI (EXCEPTION HANDLING):")

    # Uji 5A: Coba input iuran negatif
    try:
        print("  -> Uji A: Mencoba set nominal iuran negatif...")
        kelompok1.nominal_iuran = -50000
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    # Uji 5B: Coba nama anggota kosong
    try:
        print("  -> Uji B: Mencoba buat anggota dengan nama kosong...")
        Anggota("A999", "", "081234567890")
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    # Uji 5C: Coba tambah anggota duplikat
    try:
        print("  -> Uji C: Mencoba daftarkan anggota yang sama 2x...")
        kelompok1.tambah_peserta(a1)
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    print("\n" + "=" * 55)
    print(" SELURUH UJI INTERAKSI & ENKAPSULASI SELESAI (SUKSES) ")
    print("=" * 55 + "\n")
