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