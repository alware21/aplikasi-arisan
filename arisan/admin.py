from django.contrib import admin
from .models import Anggota, KelompokArisan, PesertaArisan, RiwayatKocokan

@admin.register(Anggota)
class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'no_telepon', 'alamat', 'created_at')
    search_fields = ('nama', 'no_telepon', 'alamat')
    list_filter = ('created_at',)
    ordering = ('nama',)


class PesertaInline(admin.TabularInline):
    model = PesertaArisan
    extra = 1
    autocomplete_fields = ['anggota']
    readonly_fields = ['status_menang']


@admin.register(KelompokArisan)
class KelompokArisanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama_kelompok', 'nominal_iuran', 'periode_kocok', 'tanggal_mulai', 'status_arisan', 'total_peserta', 'total_pot_hadiah')
    search_fields = ('nama_kelompok',)
    list_filter = ('status_arisan', 'periode_kocok')
    inlines = [PesertaInline]


@admin.register(PesertaArisan)
class PesertaArisanAdmin(admin.ModelAdmin):
    list_display = ('id', 'kelompok', 'nomor_undian', 'anggota', 'status_menang', 'created_at')
    list_filter = ('kelompok', 'status_menang')
    search_fields = ('anggota__nama', 'nomor_undian')
    ordering = ('kelompok', 'nomor_undian')


@admin.register(RiwayatKocokan)
class RiwayatKocokanAdmin(admin.ModelAdmin):
    list_display = ('id', 'kelompok', 'periode_ke', 'peserta_menang', 'tanggal_kocok', 'total_diterima', 'catatan')
    list_filter = ('kelompok', 'tanggal_kocok')
    search_fields = ('peserta_menang__anggota__nama', 'catatan')
    ordering = ('-tanggal_kocok', '-periode_ke')
