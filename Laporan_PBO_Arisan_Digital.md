# LAPORAN PRAKTIK PEMROGRAMAN BERORIENTASI OBJEK
## Project-Based Learning (PjBL) - Pertemuan 3 & 4

---

### Informasi Tugas
* **Mata Kuliah**       : Pemrograman Berorientasi Objek (PBO)
* **Dosen Pengampu**    : Zuliar Efendi, M.Kom.
* **Topik Praktik**     : Encapsulation, Constructor, Getter-Setter, dan Hubungan Antarclass/Object
* **Studi Kasus**       : Aplikasi Arisan Digital Desktop (Mode Offline / Pencatatan & Pengocokan)
* **Bahasa Pemrograman**: Python 3

---

## BAB I. PENDAHULUAN

### 1.1 Latar Belakang Studi Kasus
Arisan merupakan kegiatan sosial-finansial yang sangat populer di masyarakat Indonesia, baik di lingkungan keluarga, warga RT/RW, maupun instansi perkantoran. Selama ini, pengelolaan arisan sering dilakukan secara manual menggunakan kertas lintingan (lot undian) dan buku tulis fisik. Metode konvensional ini memiliki beberapa kelemahan, antara lain rentan terjadi kehilangan data, kecurangan dalam proses pengundian, serta kesulitan dalam melacak peserta mana saja yang sudah pernah menang dan yang belum.

Dalam proyek Project-Based Learning (PjBL) ini, dikembangkan **"Aplikasi Arisan Digital Desktop"**. Aplikasi ini dirancang secara khusus untuk bekerja secara offline (tanpa memerlukan koneksi internet, tanpa otentikasi login yang rumit, dan tanpa pembayaran gateway perbankan online). Pengurus atau bendahara arisan dapat menggunakan aplikasi ini secara mandiri di komputer desktop untuk mencatat data warga, membuat grup arisan, dan melakukan pengocokan pemenang secara adil, acak, dan terotomatisasi.

### 1.2 Rumusan Masalah
1. Bagaimana merancang arsitektur class yang mencerminkan entitas dunia nyata pada sistem arisan digital?
2. Bagaimana menerapkan konsep enkapsulasi (Public, Protected, dan Private) serta validasi data menggunakan `@property` di Python agar integritas data tetap terjaga?
3. Bagaimana menerapkan relasi antarclass (Association dan Aggregation) sehingga objek saling berinteraksi secara konsisten?
4. Bagaimana menguji alur interaksi objek dan menangani kesalahan (*exception handling*) sesuai dengan materi perkuliahan?

### 1.3 Tujuan Pembelajaran
* Memenuhi capaian pembelajaran Minggu 3: Implementasi class Python dengan enkapsulasi, constructor, getter-setter dengan validasi, dan business method.
* Memenuhi capaian pembelajaran Minggu 4: Mengimplementasikan hubungan antarclass (Association, Aggregation, dan Multiplicity) serta menguji interaksi antarobject secara sederhana.
* Menghasilkan skrip program Python yang siap diintegrasikan ke antarmuka aplikasi desktop.

---

## BAB II. PERANCANGAN SISTEM & BASIS DATA

### 2.1 Alur Sistem Arisan Digital (Mode Offline)
Sistem arisan digital ini berfokus pada kemudahan penggunaan dan pencatatan transaksi yang bersih. Alur kerja sistem dirancang sebagai berikut:
1. **Langkah 1 (Input Master Data):** Pengurus memasukkan data warga/peserta ke dalam sistem (nama lengkap dan nomor telepon).
2. **Langkah 2 (Pembuatan Kelompok Arisan):** Pengurus membuat kelompok arisan baru, menentukan nominal iuran (misal Rp 200.000), dan memilih anggota yang bergabung. Sistem secara otomatis memberikan nomor lot undian berurutan (1, 2, 3..).
3. **Langkah 3 (Hari-H Pengocokan Undian):** Pada saat acara kumpul arisan, pengurus memicu fungsi pengocokan. Sistem memfilter peserta yang berstatus BELUM MENANG, lalu memilih 1 pemenang secara acak.
4. **Langkah 4 (Penguncian Status & Kuitansi):** Peserta yang menang secara otomatis dikunci statusnya menjadi "Sudah Menang" agar pada putaran berikutnya tidak akan keluar lagi. Sistem kemudian mencetak bukti kuitansi resmi pemenang beserta total uang yang diperoleh.

### 2.2 Struktur 4 Tabel Basis Data
Struktur database dirancang sangat ramping (hanya 4 tabel utama) tanpa dependensi login atau pembayaran online:
* **Tabel `anggota`**: Menyimpan data buku induk warga (`id_anggota`, `nama`, `no_telepon`, `alamat`, `created_at`).
* **Tabel `kelompok_arisan`**: Menyimpan informasi kamar/grup arisan (`id_arisan`, `nama_kelompok`, `nominal_iuran`, `periode_kocok`, `tanggal_mulai`, `status_arisan`).
* **Tabel `peserta_arisan`**: Tabel penghubung antara anggota dan grup arisan, mencatat nomor undian lot serta status kemenangan (`id_peserta`, `id_arisan`, `id_anggota`, `nomor_undian`, `status_menang`).
* **Tabel `riwayat_kocokan`**: Mencatat rekaman sejarah pemenang pada setiap periode putaran (`id_kocokan`, `id_arisan`, `id_peserta_menang`, `periode_ke`, `tanggal_kocok`, `total_diterima`, `catatan`).

---

## BAB III. ANALISIS PEMROGRAMAN BERORIENTASI OBJEK (PBO)

### 3.1 Hubungan Antarclass (Materi Minggu 4)
Berdasarkan materi perkuliahan Minggu 4, hubungan antarclass dalam aplikasi ini diklasifikasikan menjadi:
* **Association (Objek Saling Mengenal):** Class `PesertaArisan` menyimpan referensi objek `Anggota` sebagai atribut. Begitu pula class `KocokanArisan` menyimpan referensi objek `KelompokArisan` dan `PesertaArisan` pemenang.
* **Aggregation (Whole-Part Lemah):** Class `KelompokArisan` menyimpan daftar objek `PesertaArisan` di dalam list internal. Apabila objek `KelompokArisan` dihentikan, data objek `Anggota` tetap berdiri sendiri secara mandiri.
* **Multiplicity (1 ke Banyak):** Satu kelompok arisan dapat memiliki banyak peserta (1 to Many), dan satu kelompok arisan memiliki banyak riwayat kocokan putaran.

### 3.2 Analisis Hak Akses Enkapsulasi (Materi Minggu 3)
Sesuai Slide 5 materi perkuliahan, Python menggunakan konvensi penamaan untuk membedakan tingkat akses:
* **Public:** Atribut atau method yang dapat diakses langsung secara bebas oleh pengguna atau modul antarmuka (UI).
* **Protected (Diawali 1 Underscore `_`):** Atribut internal class yang dikendalikan melalui `@property` dan setter validasi. Digunakan untuk identitas dan data yang memerlukan aturan bisnis.
* **Private (Diawali 2 Underscore `__`):** Atribut yang sangat kritis dan diamankan menggunakan teknik Name Mangling Python agar tidak dapat diubah sembarangan dari luar class.

### 3.3 Tabel Pemetaan Hak Akses Atribut ke Tabel Basis Data

| Nama Atribut | Tabel Database | Kategori Akses | Tipe Data SQL | Alasan & Keterangan Enkapsulasi |
| :--- | :--- | :--- | :--- | :--- |
| **id_anggota** | `anggota` | Protected | `INT [PK]` | ID unik anggota. Bersifat read-only via `@property`. |
| **nama** | `anggota` | Protected (Pub: Property) | `VARCHAR(100)` | Divalidasi via setter: nama tidak boleh kosong. |
| **no_telepon** | `anggota` | Protected (Pub: Property) | `VARCHAR(20)` | Divalidasi via setter: nomor HP minimal 10 digit. |
| **alamat** | `anggota` | Protected | `TEXT NULL` | Data alamat tempat tinggal anggota. |
| **id_arisan** | `kelompok_arisan` | Protected | `INT [PK]` | ID unik grup arisan. Bersifat identitas internal. |
| **nama_kelompok** | `kelompok_arisan` | Protected (Pub: Property) | `VARCHAR(100)` | Nama grup arisan yang ditampilkan di antarmuka. |
| **nominal_iuran** | `kelompok_arisan` | Protected (Pub: Property) | `DECIMAL(12,2)` | Divalidasi via setter: iuran harus lebih dari 0. |
| **daftar_peserta** | `kelompok_arisan` | **PRIVATE (`__`)** | `List of Object` | Menyimpan kumpulan peserta; dikunci dari luar. |
| **nomor_undian** | `peserta_arisan` | Protected (Pub: Property) | `INT NOT NULL` | Nomor undian lot (1, 2, 3..). Bersifat read-only. |
| **status_menang** | `peserta_arisan` | **PRIVATE (`__`)** | `BOOLEAN` | **KRITIS:** Status kemenangan dikunci agar tidak dicurangi. |
| **id_kocokan** | `riwayat_kocokan` | Protected | `INT [PK]` | ID bukti transaksi pengocokan. |
| **id_peserta_menang** | `riwayat_kocokan` | **PRIVATE (`__`)** | `INT [FK]` | **KRITIS:** Pemenang sah hasil undian acak sistem. |
| **total_diterima** | `riwayat_kocokan` | Protected (Pub: Property) | `DECIMAL(12,2)` | Total uang hadiah pemenang yang dicetak di kuitansi. |

---

## BAB IV. IMPLEMENTASI KODE PROGRAM PYTHON

Berikut adalah kode program lengkap **`arisan_digital.py`**:

```python
import random
from datetime import datetime

# ==============================================================================
# CLASS 1: Anggota
# ==============================================================================
class Anggota:
    def __init__(self, id_anggota: str, nama: str, no_hp: str):
        self._id_anggota = id_anggota
        self._nama = ""
        self._no_hp = ""
        self.nama = nama
        self.no_hp = no_hp

    @property
    def id_anggota(self) -> str:
        return self._id_anggota

    @property
    def nama(self) -> str:
        return self._nama

    @nama.setter
    def nama(self, nilai: str):
        if not nilai or not nilai.strip():
            raise ValueError("[Validasi Gagal] Nama anggota tidak boleh kosong!")
        self._nama = nilai.strip()

    @property
    def no_hp(self) -> str:
        return self._no_hp

    @no_hp.setter
    def no_hp(self, nilai: str):
        if not nilai or len(nilai.strip()) < 10:
            raise ValueError("[Validasi Gagal] Nomor HP tidak valid (minimal 10 digit)!")
        self._no_hp = nilai.strip()

    def info(self) -> str:
        return f"[{self._id_anggota}] {self._nama} ({self._no_hp})"


# ==============================================================================
# CLASS 2: PesertaArisan
# ==============================================================================
class PesertaArisan:
    def __init__(self, anggota: Anggota, nomor_undian: int):
        self._anggota = anggota
        self._nomor_undian = nomor_undian
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

    def tandai_menang(self):
        if self.__status_menang:
            raise ValueError(f"Peserta {self._anggota.nama} sudah pernah menang!")
        self.__status_menang = True


# ==============================================================================
# CLASS 3: KelompokArisan
# ==============================================================================
class KelompokArisan:
    def __init__(self, id_arisan: str, nama_kelompok: str, nominal_iuran: float):
        self._id_arisan = id_arisan
        self._nama_kelompok = nama_kelompok
        self._nominal_iuran = 0.0
        self.nominal_iuran = nominal_iuran
        self.__daftar_peserta: list[PesertaArisan] = []

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
        if nilai <= 0:
            raise ValueError("[Validasi Gagal] Nominal iuran harus lebih besar dari 0!")
        self._nominal_iuran = nilai

    @property
    def jumlah_peserta(self) -> int:
        return len(self.__daftar_peserta)

    def tambah_peserta(self, anggota: Anggota) -> PesertaArisan:
        for p in self.__daftar_peserta:
            if p.anggota.id_anggota == anggota.id_anggota:
                raise ValueError(f"[Gagal] Anggota {anggota.nama} sudah terdaftar di kelompok ini!")

        nomor_lot = len(self.__daftar_peserta) + 1
        peserta_baru = PesertaArisan(anggota, nomor_lot)
        self.__daftar_peserta.append(peserta_baru)
        return peserta_baru

    def get_peserta_belum_menang(self) -> list[PesertaArisan]:
        return [p for p in self.__daftar_peserta if not p.status_menang]

    def hitung_total_hadiah(self) -> float:
        return len(self.__daftar_peserta) * self._nominal_iuran


# ==============================================================================
# CLASS 4: KocokanArisan
# ==============================================================================
class KocokanArisan:
    def __init__(self, id_kocokan: str, kelompok: KelompokArisan, periode_ke: int):
        self._id_kocokan = id_kocokan
        self._kelompok = kelompok
        self._periode_ke = periode_ke
        self._tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__pemenang: PesertaArisan | None = None
        self._total_diterima: float = 0.0

    @property
    def pemenang(self) -> PesertaArisan | None:
        return self.__pemenang

    def proses_kocok(self) -> bool:
        kandidat = self._kelompok.get_peserta_belum_menang()
        if not kandidat:
            return False

        self.__pemenang = random.choice(kandidat)
        self.__pemenang.tandai_menang()
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
# PENGUJIAN / TESTING
# ==============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 55)
    print(" PRAKTIK PBO: UJI INTERAKSI ANTAROBJECT (ARISAN DIGITAL) ")
    print("=" * 55 + "\n")

    # UJI 1: Pembuatan Objek Anggota
    print("[1] MEMBUAT OBJEK ANGGOTA:")
    a1 = Anggota("A001", "Ibu Siti Aminah", "081234567890")
    a2 = Anggota("A002", "Pak Budi Santoso", "081234567891")
    a3 = Anggota("A003", "Ibu Dewi Lestari", "081234567892")
    a4 = Anggota("A004", "Pak Ahmad Fauzi",  "081234567893")
    print(f"  + Berhasil dibuat: {a1.info()}")
    print(f"  + Berhasil dibuat: {a2.info()}")
    print(f"  + Berhasil dibuat: {a3.info()}")
    print(f"  + Berhasil dibuat: {a4.info()}")

    # UJI 2: Pembuatan Kelompok & Aggregation
    print("\n[2] MEMBUAT KELOMPOK ARISAN & MENDAFTARKAN PESERTA:")
    kelompok1 = KelompokArisan("K01", "Arisan Guyub RT 05", 200000.0)
    p1 = kelompok1.tambah_peserta(a1)
    p2 = kelompok1.tambah_peserta(a2)
    p3 = kelompok1.tambah_peserta(a3)
    p4 = kelompok1.tambah_peserta(a4)
    print(f"  + Kelompok '{kelompok1.nama_kelompok}' aktif.")
    print(f"  + Iuran per orang : Rp {kelompok1.nominal_iuran:,.0f}".replace(",", "."))
    print(f"  + Total peserta   : {kelompok1.jumlah_peserta} orang")
    print(f"  + Total Pot Hadiah: Rp {kelompok1.hitung_total_hadiah():,.0f}".replace(",", "."))

    # UJI 3: Pengocokan Periode 1
    print("\n[3] EKSEKUSI PENGOKOCAN PERIODE 1:")
    kocokan1 = KocokanArisan("TRX-001", kelompok1, periode_ke=1)
    if kocokan1.proses_kocok():
        print("  -> Pengocokan Berhasil!")
        kocokan1.cetak_kuitansi()

    # UJI 4: Pengocokan Periode 2
    print("\n[4] EKSEKUSI PENGOKOCAN PERIODE 2:")
    sisa_kandidat = kelompok1.get_peserta_belum_menang()
    print(f"  + Kandidat tersisa untuk diundi: {len(sisa_kandidat)} orang.")
    for p in sisa_kandidat:
        print(f"    - Lot #{p.nomor_undian:02d}: {p.anggota.nama}")

    kocokan2 = KocokanArisan("TRX-002", kelompok1, periode_ke=2)
    if kocokan2.proses_kocok():
        print("  -> Pengocokan Berhasil!")
        kocokan2.cetak_kuitansi()

    # UJI 5: Uji Kesalahan (Exception Handling)
    print("\n[5] UJI KESALAHAN & VALIDASI (EXCEPTION HANDLING):")
    try:
        print("  -> Uji A: Mencoba set nominal iuran negatif...")
        kelompok1.nominal_iuran = -50000
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    try:
        print("  -> Uji B: Mencoba buat anggota dengan nama kosong...")
        Anggota("A999", "", "081234567890")
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    try:
        print("  -> Uji C: Mencoba daftarkan anggota yang sama 2x...")
        kelompok1.tambah_peserta(a1)
    except ValueError as e:
        print(f"     [TANGKAP ERROR] {e}")

    print("\n" + "=" * 55)
    print(" SELURUH UJI INTERAKSI & ENKAPSULASI SELESAI (SUKSES) ")
    print("=" * 55 + "\n")
```

---

## BAB V. HASIL PENGUJIAN DAN EKSEKUSI (TESTING)

### 5.1 Skenario Pengujian (Sesuai Slide 11 Minggu 4)
Pengujian sistem dilakukan mencakup 2 skenario utama:
* **Skenario 1 (Uji Normal & Interaksi Antarobject):** Memastikan pembentukan objek Anggota, pendaftaran ke KelompokArisan (Aggregation), eksekusi kocokan periode 1 dan 2, serta memastikan peserta yang telah menang tidak diikutsertakan kembali pada putaran selanjutnya.
* **Skenario 2 (Uji Kesalahan / Negative Testing):** Memastikan mekanisme validasi (raise ValueError) bekerja saat diberi masukan yang salah, seperti iuran bernilai negatif, nama anggota kosong, atau mendaftarkan anggota yang sama sebanyak dua kali.

### 5.2 Teks Lengkap Output Terminal Hasil Eksekusi

```text
=======================================================
 PRAKTIK PBO: UJI INTERAKSI ANTAROBJECT (ARISAN DIGITAL) 
=======================================================

[1] MEMBUAT OBJEK ANGGOTA:
  + Berhasil dibuat: [A001] Ibu Siti Aminah (081234567890)
  + Berhasil dibuat: [A002] Pak Budi Santoso (081234567891)
  + Berhasil dibuat: [A003] Ibu Dewi Lestari (081234567892)
  + Berhasil dibuat: [A004] Pak Ahmad Fauzi (081234567893)

[2] MEMBUAT KELOMPOK ARISAN & MENDAFTARKAN PESERTA:
  + Kelompok 'Arisan Guyub RT 05' aktif.
  + Iuran per orang : Rp 200.000
  + Total peserta   : 4 orang
  + Total Pot Hadiah: Rp 800.000

[3] EKSEKUSI PENGOKOCAN PERIODE 1:
  -> Pengocokan Berhasil!
=============================================
     🎉 KUITANSI RESMI ARISAN DIGITAL 🎉     
=============================================
ID Transaksi : TRX-001
Kelompok     : Arisan Guyub RT 05
Putaran      : Periode Ke-1
Waktu Kocok  : 2026-09-25 08:45:20
---------------------------------------------
Nomor Undian : #03
Nama Pemenang: Ibu Dewi Lestari
Kontak       : 081234567892
Total Hadiah : Rp 800.000
Status       : SAH (Terkunci)
=============================================

[4] EKSEKUSI PENGOKOCAN PERIODE 2:
  + Kandidat tersisa untuk diundi: 3 orang.
    - Lot #01: Ibu Siti Aminah
    - Lot #02: Pak Budi Santoso
    - Lot #04: Pak Ahmad Fauzi
  -> Pengocokan Berhasil!
=============================================
     🎉 KUITANSI RESMI ARISAN DIGITAL 🎉     
=============================================
ID Transaksi : TRX-002
Kelompok     : Arisan Guyub RT 05
Putaran      : Periode Ke-2
Waktu Kocok  : 2026-09-25 08:45:20
---------------------------------------------
Nomor Undian : #01
Nama Pemenang: Ibu Siti Aminah
Kontak       : 081234567890
Total Hadiah : Rp 800.000
Status       : SAH (Terkunci)
=============================================

[5] UJI KESALAHAN & VALIDASI (EXCEPTION HANDLING):
  -> Uji A: Mencoba set nominal iuran negatif...
     [TANGKAP ERROR] [Validasi Gagal] Nominal iuran harus lebih besar dari 0!
  -> Uji B: Mencoba buat anggota dengan nama kosong...
     [TANGKAP ERROR] [Validasi Gagal] Nama anggota tidak boleh kosong!
  -> Uji C: Mencoba daftarkan anggota yang sama 2x...
     [TANGKAP ERROR] [Gagal] Anggota Ibu Siti Aminah sudah terdaftar di kelompok ini!

=======================================================
 SELURUH UJI INTERAKSI & ENKAPSULASI SELESAI (SUKSES) 
=======================================================
```

---

## BAB VI. KESIMPULAN

1. **Penerapan Enkapsulasi Berhasil:** Atribut `status_menang` dan `daftar_peserta` berhasil dilindungi dengan hak akses Private murni (`__`), sehingga tidak dapat dimanipulasi langsung dari luar class. Modifikasi atribut publik seperti nama dan nominal_iuran terkontrol ketat melalui setter validasi (`@property`).
2. **Penerapan Relasi Antarclass Berhasil:** Konsep Association berhasil diimplementasikan di mana objek `PesertaArisan` dan `KocokanArisan` menyimpan referensi objek lain sebagai atributnya. Konsep Aggregation berhasil diterapkan di mana `KelompokArisan` memiliki kumpulan objek peserta yang tetap dapat berdiri sendiri.
3. **Sistem Siap untuk Desktop:** Arsitektur class ini telah memenuhi prinsip desain berorientasi objek yang bersih (*clean code*) di mana logika bisnis berada di level class domain dan tidak bergantung pada antarmuka, siap untuk dihubungkan ke UI Desktop.
