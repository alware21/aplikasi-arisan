-- ==========================================================
-- SKEMA BASIS DATA: APLIKASI ARISAN DIGITAL (OFFLINE / DESKTOP)
-- Sifat: Pencatatan & Pengocokan Digital (Tanpa Login & Tanpa Pembayaran Online)
-- DBMS: MySQL / MariaDB (InnoDB Engine) / SQLite Compatible
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `arisan_digital`
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `arisan_digital`;

-- Nonaktifkan pengecekan foreign key sementara saat inisialisasi tabel
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------
-- 1. TABEL: anggota (Buku Tamu / Master Anggota)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `anggota`;
CREATE TABLE `anggota` (
    `id_anggota` INT AUTO_INCREMENT PRIMARY KEY,
    `nama` VARCHAR(100) NOT NULL,
    `no_telepon` VARCHAR(20) NULL,
    `alamat` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 2. TABEL: kelompok_arisan (Daftar Kelompok / Grup Arisan)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `kelompok_arisan`;
CREATE TABLE `kelompok_arisan` (
    `id_arisan` INT AUTO_INCREMENT PRIMARY KEY,
    `nama_kelompok` VARCHAR(100) NOT NULL,
    `nominal_iuran` DECIMAL(12, 2) NOT NULL,
    `periode_kocok` ENUM('mingguan', 'bulanan') NOT NULL DEFAULT 'bulanan',
    `tanggal_mulai` DATE NOT NULL,
    `status_arisan` ENUM('aktif', 'selesai') NOT NULL DEFAULT 'aktif',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 3. TABEL: peserta_arisan (Anggota yang Ikut di Kelompok Tertentu)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `peserta_arisan`;
CREATE TABLE `peserta_arisan` (
    `id_peserta` INT AUTO_INCREMENT PRIMARY KEY,
    `id_arisan` INT NOT NULL,
    `id_anggota` INT NOT NULL,
    `nomor_undian` INT NOT NULL,
    `status_menang` BOOLEAN NOT NULL DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uq_arisan_anggota` (`id_arisan`, `id_anggota`),
    UNIQUE KEY `uq_arisan_nomor` (`id_arisan`, `nomor_undian`),
    CONSTRAINT `fk_peserta_kelompok` 
        FOREIGN KEY (`id_arisan`) REFERENCES `kelompok_arisan` (`id_arisan`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_peserta_anggota` 
        FOREIGN KEY (`id_anggota`) REFERENCES `anggota` (`id_anggota`) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ----------------------------------------------------------
-- 4. TABEL: riwayat_kocokan (Catatan Pemenang Tiap Putaran)
-- ----------------------------------------------------------
DROP TABLE IF EXISTS `riwayat_kocokan`;
CREATE TABLE `riwayat_kocokan` (
    `id_kocokan` INT AUTO_INCREMENT PRIMARY KEY,
    `id_arisan` INT NOT NULL,
    `id_peserta_menang` INT NOT NULL,
    `periode_ke` INT NOT NULL,
    `tanggal_kocok` DATE NOT NULL,
    `total_diterima` DECIMAL(12, 2) NOT NULL,
    `catatan` VARCHAR(255) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY `uq_arisan_periode` (`id_arisan`, `periode_ke`),
    CONSTRAINT `fk_kocokan_kelompok` 
        FOREIGN KEY (`id_arisan`) REFERENCES `kelompok_arisan` (`id_arisan`) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_kocokan_peserta` 
        FOREIGN KEY (`id_peserta_menang`) REFERENCES `peserta_arisan` (`id_peserta`) 
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Aktifkan kembali pengecekan foreign key
SET FOREIGN_KEY_CHECKS = 1;


-- ==========================================================
-- DATA CONTOH (SAMPLE DUMMY DATA / SEEDER)
-- ==========================================================

-- 1. Insert Data Master Anggota
INSERT INTO `anggota` (`id_anggota`, `nama`, `no_telepon`, `alamat`) VALUES
(1, 'Ibu Siti Aminah', '081234567801', 'Blok A No. 12'),
(2, 'Pak Budi Santoso', '081234567802', 'Blok A No. 15'),
(3, 'Ibu Dewi Lestari', '081234567803', 'Blok B No. 04'),
(4, 'Pak Ahmad Fauzi', '081234567804', 'Blok B No. 09'),
(5, 'Ibu Rina Anggraini', '081234567805', 'Blok C No. 01');

-- 2. Insert Data Kelompok Arisan
INSERT INTO `kelompok_arisan` (`id_arisan`, `nama_kelompok`, `nominal_iuran`, `periode_kocok`, `tanggal_mulai`, `status_arisan`) VALUES
(1, 'Arisan Warga RT 05', 200000.00, 'bulanan', '2026-01-10', 'aktif');

-- 3. Hubungkan Anggota ke Kelompok (5 Peserta, masing-masing dapat nomor undian)
INSERT INTO `peserta_arisan` (`id_peserta`, `id_arisan`, `id_anggota`, `nomor_undian`, `status_menang`) VALUES
(1, 1, 1, 1, TRUE),   -- Ibu Siti menang di periode 1
(2, 1, 2, 2, FALSE),  -- Belum menang
(3, 1, 3, 3, FALSE),  -- Belum menang
(4, 1, 4, 4, FALSE),  -- Belum menang
(5, 1, 5, 5, FALSE);  -- Belum menang

-- 4. Catat Riwayat Pemenang Periode 1 (Total dapat = 5 x 200.000 = Rp 1.000.000)
INSERT INTO `riwayat_kocokan` (`id_kocokan`, `id_arisan`, `id_peserta_menang`, `periode_ke`, `tanggal_kocok`, `total_diterima`, `catatan`) VALUES
(1, 1, 1, 1, '2026-01-10', 1000000.00, 'Kocokan perdana di rumah Bu RW');


-- ==========================================================
-- CONTOH QUERY PENTING PADA APLIKASI OFFLINE
-- ==========================================================

-- A. Query untuk Mengambil Peserta yang BELUM MENANG (Siap Dikocok)
-- SELECT pa.id_peserta, pa.nomor_undian, a.nama, a.no_telepon 
-- FROM peserta_arisan pa
-- JOIN anggota a ON pa.id_anggota = a.id_anggota
-- WHERE pa.id_arisan = 1 AND pa.status_menang = FALSE
-- ORDER BY RAND(); -- Sistem memilih 1 pemenang acak

-- B. Query Rekap Riwayat Pemenang
-- SELECT rk.periode_ke, rk.tanggal_kocok, a.nama AS nama_pemenang, pa.nomor_undian, rk.total_diterima, rk.catatan
-- FROM riwayat_kocokan rk
-- JOIN peserta_arisan pa ON rk.id_peserta_menang = pa.id_peserta
-- JOIN anggota a ON pa.id_anggota = a.id_anggota
-- WHERE rk.id_arisan = 1
-- ORDER BY rk.periode_ke ASC;
