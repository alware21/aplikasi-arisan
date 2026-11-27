from django.urls import path
from . import views

urlpatterns = [
    # Layar Portal & Autentikasi Peran
    path('', views.portal_view, name='root'),
    path('portal/', views.portal_view, name='portal'),
    path('logout/', views.logout_role, name='logout'),

    # Dashboard Utama
    path('dashboard/', views.dashboard, name='dashboard'),

    # CRUD Anggota (Ketua Only)
    path('anggota/tambah/', views.anggota_create, name='anggota_create'),
    path('anggota/edit/<int:pk>/', views.anggota_update, name='anggota_update'),
    path('anggota/hapus/<int:pk>/', views.anggota_delete, name='anggota_delete'),

    # AJAX Toggle Setoran (Ketua Only)
    path('peserta/toggle-setor/<int:peserta_id>/', views.toggle_setor_api, name='toggle_setor_api'),
    path('peserta/lunas-semua/<int:kelompok_id>/', views.tandai_semua_lunas, name='tandai_semua_lunas'),
    path('buka-setoran/<int:kelompok_id>/', views.buka_setoran_baru, name='buka_setoran_baru'),

    # Kelompok & Pengundian Live
    path('kelompok/', views.kelompok_list, name='kelompok_list'),
    path('kocokan/', views.kocokan_view, name='kocokan_view'),
    path('kocokan/<int:kelompok_id>/', views.kocokan_view, name='kocokan_kelompok'),
    path('kocokan/api/proses/<int:kelompok_id>/', views.proses_kocok_api, name='proses_kocok_api'),
    path('riwayat/hapus/<int:riwayat_id>/', views.riwayat_delete, name='riwayat_delete'),
    path('riwayat/hapus-semua/<int:kelompok_id>/', views.riwayat_hapus_semua, name='riwayat_hapus_semua'),

    # Kuitansi Detail
    path('kuitansi/<int:riwayat_id>/', views.kuitansi_detail, name='kuitansi_detail'),

    # Riwayat Pemenang & Transparansi Kas (Pengganti Admin)
    path('riwayat-kas/', views.riwayat_kas_view, name='riwayat_kas'),

    # Pusat Kendali Multi-Arisan (Grup Saya)
    path('grup/', views.grup_saya_view, name='grup_saya'),
    path('grup/switch/<int:kelompok_id>/', views.switch_kelompok, name='switch_kelompok'),
    path('grup/gabung/', views.gabung_kelompok_baru, name='gabung_kelompok_baru'),
    path('grup/buat/', views.buat_kelompok_baru, name='buat_kelompok_baru'),
    path('grup/hapus/<int:kelompok_id>/', views.hapus_kelompok, name='hapus_kelompok'),
    path('grup/keluar/<int:kelompok_id>/', views.keluar_kelompok, name='keluar_kelompok'),
    path('grup/bersihkan-selesai/', views.bersihkan_kelompok_selesai, name='bersihkan_kelompok_selesai'),
    path('grup/reset-total/', views.reset_total_kelompok, name='reset_total_kelompok'),

    # Headless Django REST API v1 & Smart Delta Sync
    path('api/v1/rooms/<str:kode_room>/sync/', views.api_room_sync, name='api_room_sync'),
    path('api/v1/rooms/<str:kode_room>/warga/', views.api_room_warga, name='api_room_warga'),
    path('api/v1/rooms/<str:kode_room>/', views.api_room_detail, name='api_room_detail'),
    path('api/v1/warga/<int:peserta_id>/setor/', views.toggle_setor_api, name='api_v1_toggle_setor'),
    path('api/v1/kocokan/<int:kelompok_id>/putar/', views.proses_kocok_api, name='api_v1_proses_kocok'),
    path('api/v1/kas/riwayat/', views.api_kas_riwayat, name='api_kas_riwayat'),
]
