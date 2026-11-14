from django.db import models
from django.utils import timezone
import random
import string
import datetime

def generate_room_code():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

class Anggota(models.Model):
    nama = models.CharField(max_length=100, verbose_name="Nama Anggota")
    no_telepon = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor WhatsApp/Telepon")
    alamat = models.TextField(blank=True, null=True, verbose_name="Alamat Rumah")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Registrasi")

    class Meta:
        verbose_name = "Anggota"
        verbose_name_plural = "Daftar Anggota"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.no_telepon or 'Tanpa Kontak'})"


class KelompokArisan(models.Model):
    PERIODE_CHOICES = [
        ('mingguan', 'Mingguan (Kocok Tiap Minggu)'),
        ('bulanan', 'Bulanan (Kocok Tiap Bulan)'),
        ('tahunan', 'Tahunan (Kocok Tiap Tahun)'),
    ]
    STATUS_CHOICES = [
        ('aktif', 'Aktif'),
        ('selesai', 'Selesai'),
    ]

    nama_kelompok = models.CharField(max_length=100, verbose_name="Nama Kelompok")
    kode_room = models.CharField(max_length=20, default='RT0526', verbose_name="Kode Room / Undangan")
    nominal_iuran = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Nominal Iuran (Rp)")
    periode_kocok = models.CharField(max_length=20, choices=PERIODE_CHOICES, default='bulanan', verbose_name="Periode Kocokan")
    pin_ketua = models.CharField(max_length=20, default='1234', verbose_name="PIN Pengurus Ketua")
    tanggal_mulai = models.DateField(default=timezone.now, verbose_name="Tanggal Mulai")
    status_arisan = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktif', verbose_name="Status Kelompok")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kelompok Arisan"
        verbose_name_plural = "Daftar Kelompok Arisan"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama_kelompok} [Room: {self.kode_room}]"

    @property
    def durasi_hari(self):
        """Durasi periode dalam hari"""
        if self.periode_kocok == 'mingguan':
            return 7
        elif self.periode_kocok == 'tahunan':
            return 365
        else: # bulanan
            return 30

    @property
    def frekuensi_setor(self):
        """Aturan Bisnis Relasional: Periode Kocok vs Frekuensi Setor"""
        if self.periode_kocok == 'mingguan':
            return 'Harian'
        elif self.periode_kocok == 'tahunan':
            return 'Bulanan'
        else: # bulanan
            return 'Mingguan'

    @property
    def total_peserta(self):
        return self.peserta.count()

    @property
    def total_pot_hadiah(self):
        """Target Pot Otomatis: Jumlah Anggota Aktif x Nominal Iuran"""
        return self.total_peserta * self.nominal_iuran

    @property
    def total_lunas_count(self):
        return self.peserta.filter(status_setor=True).count()

    @property
    def total_kas_terkumpul(self):
        """Uang riil yang sudah terkumpul dari anggota yang lunas"""
        return self.total_lunas_count * self.nominal_iuran

    @property
    def sisa_kekurangan_kas(self):
        """Kekurangan kas dari anggota yang belum setor"""
        return max(0, self.total_pot_hadiah - self.total_kas_terkumpul)

    @property
    def persentase_kelunasan(self):
        if self.total_pot_hadiah > 0:
            return min(100, int((self.total_kas_terkumpul / self.total_pot_hadiah) * 100))
        return 0

    @property
    def is_selesai(self):
        """
        Status Siklus Arisan: True jika seluruh peserta dalam kelompok
        sudah mendapatkan giliran menang (jumlah putaran riwayat >= total peserta aktif > 0).
        """
        total = self.peserta.count()
        if total == 0:
            return False
        return self.riwayat.count() >= total or self.peserta.filter(status_menang=True).count() >= total

    @property
    def putaran_berikutnya(self):
        return self.riwayat.count() + 1

    @property
    def deadline_kocok(self):
        """Tanggal jatuh tempo pengocokan putaran saat ini"""
        putaran = self.putaran_berikutnya
        # Mulai dari tanggal_mulai + (putaran * durasi_hari)
        delta = datetime.timedelta(days=self.durasi_hari * putaran)
        return self.tanggal_mulai + delta

    @property
    def sisa_hari_kocok(self):
        today = timezone.now().date()
        diff = (self.deadline_kocok - today).days
        return max(0, diff)

    def get_peserta_siap_undi(self):
        """
        Kandidat undian: Seluruh anggota yang BELUM PERNAH MENANG dalam siklus ini.
        Sesuai aturan arisan: Berapa pun kas yang terkumpul, kocokan tetap bisa dilakukan.
        """
        kandidat = self.peserta.filter(status_menang=False)
        # Jika semua anggota sudah menang (siklus putaran lengkap), reset siklus baru
        if not kandidat.exists() and self.peserta.exists():
            self.peserta.update(status_menang=False)
            kandidat = self.peserta.filter(status_menang=False)
        return kandidat

    @property
    def sisa_kandidat_count(self):
        return self.get_peserta_siap_undi().count()

    def check_and_trigger_auto_draw(self):
        """
        Sistem Terkocok Otomatis: Jika hari ke-30 (atau jatuh tempo) telah tiba
        dan Ketua belum mengocok, maka sistem mengeksekusi kocokan sendiri secara objektif.
        """
        today = timezone.now().date()
        if today >= self.deadline_kocok and self.peserta.exists():
            kandidat = list(self.get_peserta_siap_undi())
            if kandidat:
                pemenang = random.choice(kandidat)
                pemenang.status_menang = True
                pemenang.save()

                periode = self.putaran_berikutnya
                total_hadiah = self.total_pot_hadiah

                riwayat = RiwayatKocokan.objects.create(
                    kelompok=self,
                    peserta_menang=pemenang,
                    periode_ke=periode,
                    total_diterima=total_hadiah,
                    catatan=f"Pengocokan Otomatis Sistem (Jatuh Tempo Hari Ke-{self.durasi_hari})"
                )
                return riwayat
        return None


class PesertaArisan(models.Model):
    kelompok = models.ForeignKey(KelompokArisan, on_delete=models.CASCADE, related_name='peserta')
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE, related_name='keikutsertaan')
    nomor_undian = models.IntegerField(verbose_name="Nomor Lot Undian")
    is_ketua = models.BooleanField(default=False, verbose_name="Ketua Kelompok?")
    status_setor = models.BooleanField(default=False, verbose_name="Sudah Setor Iuran?")
    status_menang = models.BooleanField(default=False, verbose_name="Sudah Pernah Menang?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Peserta Arisan"
        verbose_name_plural = "Daftar Peserta Kelompok"
        unique_together = [['kelompok', 'anggota'], ['kelompok', 'nomor_undian']]
        ordering = ['nomor_undian']

    def __str__(self):
        peran = "👑 KETUA" if self.is_ketua else "👤 ANGGOTA"
        return f"[{peran}] Lot #{self.nomor_undian:02d} - {self.anggota.nama}"


class RiwayatKocokan(models.Model):
    kelompok = models.ForeignKey(KelompokArisan, on_delete=models.CASCADE, related_name='riwayat')
    peserta_menang = models.ForeignKey(PesertaArisan, on_delete=models.PROTECT, related_name='kemenangan')
    periode_ke = models.IntegerField(verbose_name="Putaran Periode Ke-")
    tanggal_kocok = models.DateField(default=timezone.now, verbose_name="Tanggal Pengocokan")
    total_diterima = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Hadiah (Rp)")
    catatan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Catatan Pengundian")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Riwayat Kocokan"
        verbose_name_plural = "Daftar Riwayat Kocokan"
        ordering = ['-periode_ke']

    def __str__(self):
        return f"Putaran {self.periode_ke} - Pemenang: {self.peserta_menang.anggota.nama}"
