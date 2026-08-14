# Test Materi - DevOps

## 1. Containerization

### Clone Repository

Clone repository dan masuk ke direktori project:

```bash
git clone https://github.com/cloxt01/test-devops
cd test-devops/docker
```

### Konfigurasi Environment

Salin file environment example:

```bash
cp .env.example .env
```

Sesuaikan nilai pada `.env` dengan kebutuhan environment:

```env
DB_HOST=db
DB_PORT=5432
DB_NAME=<NAMA_DATABASE>
DB_USER=<NAMA_USER>
DB_PASSWORD=<NAMA_PASSWORD>

APP_PORT=5000
```

Keterangan:

* `DB_HOST`: nama service PostgreSQL pada Docker Compose.
* `DB_PORT`: port PostgreSQL di dalam container.
* `DB_NAME`: nama database aplikasi.
* `DB_USER`: username database.
* `DB_PASSWORD`: password database.
* `APP_PORT`: port aplikasi yang digunakan baik dalam container maupun pada host.

### Build dan Menjalankan Container

Masuk ke direktori Docker:

```bash
cd docker
```

Kemudian build dan jalankan service:

```bash
docker compose up -d --build
```

Verifikasi container:

```bash
docker compose ps
```

Untuk melihat log:

```bash
docker compose logs -f
```

---

## 2. CI/CD

![CI/CD Pipeline](https://github.com/user-attachments/assets/fda12910-1587-42ba-b824-e1ee0382bdf4)

Gambar di atas menunjukkan alur CI/CD mulai dari perubahan source code hingga image berhasil dipublikasikan ke GitHub Container Registry (GHCR).

Pipeline hanya dijalankan pada branch `main`.

Secara umum, tahapan pipeline adalah:

1. Source code diambil dari repository.
2. Linting dijalankan untuk memeriksa kualitas dan format kode.
3. Testing dijalankan untuk memastikan fungsi aplikasi berjalan sesuai dengan yang diharapkan.
4. Vulnerability scanning dilakukan untuk mendeteksi kerentanan pada dependency dan pakage aplikasi.
5. Jika seluruh tahapan berhasil, Docker image aplikasi akan dibuild.
6. Image yang berhasil dibuild kemudian dipush ke GitHub Container Registry (GHCR).

Pipeline menggunakan pendekatan **fail-fast**, sehingga kegagalan pada tahap sebelumnya akan menghentikan proses sebelum image dipublikasikan.

---

## 3. Infrastructure as Code

Infrastructure as Code (IaC) menggunakan Ansible untuk melakukan provisioning, hardening, dan deployment pada server target.

### Inventory

Salin file inventory example:

```bash
cp ansible/inventory.example ansible/inventory
```

Sesuaikan inventory dengan server target:

```bash
nano ansible/inventory
```

Contoh:

```ini
[servers]
localhost ansible_host=127.0.0.1
```

> Gunakan group inventory seperti `servers` pada playbook.

### Install Ansible Collection

Install collection yang dibutuhkan:

```bash
ansible-galaxy collection install community.general
```


### Playbooks

#### `ansible/playbooks/docker.yml`

Digunakan untuk:

* Menginstal Docker Engine.
* Menginstal Docker Compose.
* Menyiapkan server target untuk menjalankan aplikasi berbasis container.

#### `ansible/playbooks/hardening.yml`

Digunakan untuk menerapkan konfigurasi hardening pada server target, termasuk user, group, firewall, dan SSH.

_Sebelum menjalankan playbook ini, pastikan SSH key (public) sudah digenerate manual, lalu salin ke `ansible/keys/<inventory-hostname>/pub`._

Generate key pair jika belum tersedia:

```bash
ssh-keygen -t ed25519
```

Struktur key pada project:

```text
ansible/
└── keys/
    └── <inventory-hostname>/
        └── pub
```

Contoh jika hostname pada inventory adalah `localhost`:

```ini
[servers]
localhost ansible_host=127.0.0.1
```
maka

```text
ansible/
└── keys/
    └── localhost/
        └── pub
```


Pastikan SSH key sudah dikonfigurasi sebelum menjalankan playbook ini.

#### `ansible/playbooks/deploy.yml`

Digunakan untuk melakukan deployment aplikasi pada server target setelah environment dan Docker sudah dipersiapkan.

---

## 4. Keputusan Teknis yang Diambil

### 4.1 Penghapusan Default Credential Database

Default credential database yang sebelumnya terdapat pada `app/app.py` dihapus.

**Alasan:**

Menyimpan credential secara langsung di source code berisiko menyebabkan kebocoran informasi sensitif, terutama saat pengembang lupa dalam membuat file konfigurasi.

Konfigurasi database kemudian dipindahkan ke environment variable.

---

### 4.2 Perubahan Scope Fungsi `init_db()`

Scope pemanggilan fungsi `init_db()` pada `app/app.py` diubah.

**Alasan:**

Memastikan proses inisialisasi database tetap dijalankan ketika aplikasi dijalankan menggunakan Gunicorn.

---

### 4.3 Sumber Konfigurasi Port dari Environment Variable

Port aplikasi pada `app/app.py` diubah agar membaca konfigurasi dari environment variable.

**Alasan:**

Memastikan konfigurasi port aplikasi memiliki satu sumber konfigurasi yang dapat digunakan secara konsisten oleh aplikasi dan Docker Compose.

Contohnya:

```env
APP_PORT=5000
```

Nilai tersebut kemudian digunakan oleh aplikasi dan konfigurasi Docker Compose.

---

### 4.4 Penggunaan `python:3.9-slim` sebagai Base Image

Docker image aplikasi menggunakan:

```dockerfile
FROM python:3.9-slim
```

**Alasan:**

Image `slim` memiliki ukuran yang lebih kecil dibandingkan image Python standar sehingga lebih sesuai untuk aplikasi API sederhana.