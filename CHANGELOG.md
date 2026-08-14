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

