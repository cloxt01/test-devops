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

## *[1.5.5] CL-15-08-2026*

### Added

* Penambahan stage pada playbook `docker.yml` mengikuti dokumentasi resmi.

**Alasan :** Agar proses instalasi Docker lebih sesuai dengan dokumentasi resmi dan mengurangi potensi masalah saat instalasi.


## *[1.6.0] CL-15-08-2026*

### Added

* Penambahan opsi `shell: /bin/bash` pada pembuatan user baru di playbook `hardening.yml`.

**Alasan :** Agar user baru yang dibuat memiliki shell default yang sesuai.

## *[1.6.5] CL-15-08-2026*

### Added

* Penambahan vault, guna menyimpan infomasi sensitif.

**Alasan :** Untuk meningkatkan keamanan dengan menyimpan informasi sensitif seperti password dalam bentuk terenkripsi.

## *[1.7.0] CL-15-08-2026*

### Added

* Penambahan endpoint `/metrics` pada program aplikasi.
* Penambahan requirement `prometheus-client` pada file `requirements.txt`.

**Alasan :** Untuk memungkinkan aplikasi mengekspor metrik.

## *[1.7.1] CL-15-08-2026*

### Added

* Penambahan prometheus & grafana pada stack.

**Alasan :** Untuk mempermudah kebutuhan monitoring aplikasi.

## *[1.8.0] CL-15-08-2026*

### Added

* Penambahan dashboard grafana untuk menampilkan metrik aplikasi.

**Alasan :** Untuk mempermudah visualisasi metrik aplikasi dan memantau kinerja aplikasi secara real-time.

## *[1.8.5] CL-15-08-2026*

### Added

* Penambahan stack pada deploy file & folder service pada playbook `deploy.yml`.

**Alasan :** Memungkinkan untuk memulai stack monitoring (prometheus & grafana).

## *[1.8.7] CL-15-08-2026*

### Fixed

* Perbaikan penulisan path pada loop playbook `deploy.yml` untuk stack monitoring.

**Alasan :** Memperbaiki path yang digunakan dalam loop playbook `deploy.yml` sesuai dengan struktur direktori yang benar.

## *[1.9.0] CL-15-08-2026*

### Fixed

* Perbaikan targets pada config prometheus (host.docker.internal -> localhost).

**Alasan :** Memperbaiki konfigurasi target pada Prometheus agar support di lingkungan linux

## *[1.9.1] CL-15-08-2026*

### Fixed

* Penambahan opsi `extra_hosts` pada service prometheus di docker-compose.yml.

**Alasan :** Memperbaiki konfigurasi prometheus pada `docker/compose.yml` dapat mengakses host internal Docker dengan benar.

## *[1.9.5] CL-15-08-2026*

### Added

* Pastikan db service sehat sebelum lanjut ke aplikasi

**Alasan :** Untuk memastikan bahwa service database sudah siap sebelum aplikasi dijalankan, menghindari error koneksi database.

## *[1.9.10] CL-15-08-2026*

### Added

* Penambahan collection `community.docker` pada playbook deploy `deploy.yml`.

**Alasan :** Untuk mempermudah pengelolaan docker compose.

## *[1.9.15] CL-15-08-2026*

### Added

* Penambahan alert rules pada prometheus untuk memantau aplikasi.

**Alasan :** Untuk mempermudah pemantauan status aplikasi dan memberikan peringatan jika terjadi masalah, seperti aplikasi down, error rate tinggi, atau latency tinggi.

## *[1.9.20] CL-15-08-2026*

### Removed

* Port expose pada service db di docker-compose.yml.

**Alasan :** Untuk meningkatkan keamanan, port database tidak diekspos ke host, sehingga hanya dapat diakses oleh service lain dalam jaringan Docker internal.