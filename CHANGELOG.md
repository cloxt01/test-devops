# Changelog

## *[1.0.0] CL-14-08-2026*

### Added

* Penambahan file environment `.env` untuk menyimpan informasi sensitif.

**Alasan :** Untuk meningkatkan keamanan dan memisahkan informasi sensitif dari kode sumber.

### Changed

* Penghapusan default kredensial untuk koneksi database di dalam kode.

**Alasan :** Menghapus kredensial default untuk meningkatkan keamanan dan mencegah potensi kebocoran kredensial database.

* Pemindahan blok inisialisasi database dalam kode program `app.py:80`.

**Alasan :** karena jika ingin di jalankan dengan gunicorn, harus di luar scope `__main__`

## *[1.0.1] CL-14-08-2026*

### Added

* Penambahan file `dockerfile` untuk membangun image aplikasi.
* Penambahan file `docker-compose.yml` untuk mengatur layanan aplikasi dan database.

**Alasan :** Untuk mempermudah proses build dan deployment aplikasi.

* Penambahan volume file environment & database untuk menyimpannya secara persisten.

**Alasan :** Untuk memastikan data tetap ada meskipun container dihapus atau direstart.


## *[1.0.2] CL-14-08-2026*

### Added

* modul & unit test aplikasi `pytest`

**Alasan :** Untuk memastikan bahwa perilaku aplikasi berjalan sesuai dengan yang diharapkan.

* modul & unit test aplikasi `ruff`

**Alasan :** Untuk memastikan bahwa kode aplikasi tetap berfungsi dengan baik.

## *[1.0.3] CL-14-08-2026*

### Changed

* remove unused salin file environment `.env` pada dockerfile 

**Alasan :** Sudah tidak digunakan karena sudah diatur pada docker-compose.yml

## *[1.0.4] CL-14-08-2026*

### Fixed

* Missing copy file `requirements.txt` pada dockerfile

**Alasan :** Agar dependensi aplikasi dapat diinstal dengan benar saat membangun image Docker.

## *[1.0.5] CL-14-08-2026*

### Fixed

* Downgrade pytest 9.1.1 > pytest 8.3.5

**Alasan :** Karena versi sebelumnya tidak kompatibel dengan versi python 3.9 yang digunakan dalam base image docker.

## *[1.0.6] CL-14-08-2026*

### Added

* Vulnerability scan dengan `trivy` pada base image docker

**Alasan :** Untuk memastikan bahwa base image yang digunakan aman.

## *[1.0.7] CL-14-08-2026*

### Added

* Hapus threshold/severity pada `trivy` : HIGH (testing only)

**Alasan :** Menurunkan threshold untuk mempermudah testing (hanya untuk testing).

## *[1.0.8] CL-14-08-2026*

### Added

* Update & upgrade package pada base image docker

**Alasan :** Untuk memastikan bahwa semua paket dalam base image diperbarui ke versi terbaru dan mengurangi potensi kerentanan keamanan.

## *[1.0.9] CL-14-08-2026*

### Changed

* Aktifkan opsi `ignore-unfixed` pada konfigurasi trivy

**Alasan :** Abaikan peringatan kerentanan yang tidak diperbaiki pada image docker karena tidak ada patch yang tersedia.

## *[1.1.0] CL-14-08-2026*

### Added

* Push image docker ke registry GHCR

**Alasan :** Untuk mempermudah distribusi dan penggunaan image docker di berbagai lingkungan.

## *[1.1.1] CL-14-08-2026*

### Fixed

* Perbaikan penulisan tag pada push image docker ke registry GHCR

**Alasan :** memperbaiki penulisan tag agar sesuai dengan format yang benar dan menghindari kegagalan.

## *[1.1.2] CL-14-08-2026*

### Fixed

* Penambahan izin akses `contents: read` dan `packages: write`

**Alasan :** Untuk memastikan bahwa workflow memiliki izin yang diperlukan untuk membaca konten repositori dan menulis paket ke registry GHCR.

## *[1.5.0] CL-15-08-2026*

### Added

* Penambahan playbook ansible untuk kebutuhan setup server.

**Alasan :** Untuk mempermudah proses setup server target.

### Changed

* Perubahan struktur direktori

**Alasan :** Untuk memisahkan file atau folder agar lebih terorganisir dan mudah dikelola.

## *[1.5.1] CL-15-08-2026*

### Added

* Penambahan nama container pada docker-compose.yml.

**Alasan :** Untuk mempermudah identifikasi container yang berjalan dan menghindari konflik nama container