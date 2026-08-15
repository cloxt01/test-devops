# Test Materi - DevOps

Sudah diuji pada OS:
- `Ubuntu 22.04 LTS`

## Requirements

- **Ansible >= 2.21.2**

  Untuk menginstal Ansible, silakan ikuti panduan resmi pada [Ansible Installation](https://docs.ansible.com/projects/ansible/latest/installation_guide/installation_distros.html).

## Quick Start

### 1. Installation

Clone repository dan masuk ke direktori project:

```bash
git clone https://github.com/cloxt01/test-devops
cd test-devops
```

### 2. Setup

- Salin & sesuaikan file environment docker:
  ```bash
  cp docker/.env.example docker/.env
  nano docker/.env
  ```
- Install collection Ansible yang dibutuhkan:
  ```bash
  ansible-galaxy collection install community.general
  ```
- Sesuaikan konfigurasi server target pada file inventory:
  ```bash
  nano ansible/inventory
  ```

  > _Untuk informasi lebih lanjut, silakan lihat bagian [Inventory](#inventory)._

- Sesuaikan variable pada host target:

  1. Host Variable (`host_vars`)
     ```bash
     nano ansible/host_vars/<hostname>.yml
     ```
  2. Group Variable (`group_vars/all/vault.yml`)
     ```bash
     cp ansible/group_vars/all/vault.yml.example ansible/group_vars/all/vault.yml
     nano ansible/group_vars/all/vault.yml
     ```

  > _Untuk informasi lebih lanjut, silakan lihat bagian [Variable](#variable)._

### 3. Start

Jalankan playbook Ansible untuk setup server target & sesuaikan urutannya sesuai kebutuhan.

Jika server target adalah server fresh (baru), urutannya adalah:
1. `playbooks/docker.yml`
2. `playbooks/hardening.yml`
3. `playbooks/deploy.yml`

> _Untuk informasi lebih lanjut, silakan lihat bagian [Playbooks](#playbooks)._

---

## 1. Containerization

Workdir: `/docker`

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

| Variable | Deskripsi |
|---|---|
| `DB_HOST` | Nama service PostgreSQL pada Docker Compose |
| `DB_PORT` | Port PostgreSQL di dalam container |
| `DB_NAME` | Nama database aplikasi |
| `DB_USER` | Username database |
| `DB_PASSWORD` | Password database |
| `APP_PORT` | Port aplikasi yang digunakan dalam container |

### Build dan Menjalankan Container

Masuk ke direktori & jalankan dengan perintah berikut:

```bash
cd docker
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
4. Vulnerability scanning dilakukan untuk mendeteksi kerentanan pada dependency dan package aplikasi.
5. Jika seluruh tahapan berhasil, Docker image aplikasi akan dibuild.
6. Image yang berhasil dibuild kemudian di-push ke GitHub Container Registry (GHCR).

Pipeline menggunakan pendekatan **fail-fast**, sehingga kegagalan pada tahap sebelumnya akan menghentikan proses sebelum image dipublikasikan.

---

## 3. Infrastructure as Code

Infrastructure as Code (IaC) menggunakan Ansible untuk melakukan provisioning, hardening, dan deployment pada server target.

Workdir: `/ansible`

### Inventory

Sesuaikan inventory dengan server target:

```bash
nano inventory
```

Contoh untuk local server:

```ini
[servers]
localhost
```

Contoh untuk non-local server:

```ini
[servers]
server

[servers:vars]
ansible_become=true
ansible_become_method=sudo
```

> Gunakan group inventory seperti `servers` pada playbook.

### Install Ansible Collection

Install collection yang dibutuhkan:

```bash
ansible-galaxy collection install community.general
```

### Variable

Sebelum menjalankan playbook, pastikan Anda sudah mengatur koneksi SSH untuk akses ke server target. Jika belum, gunakan perintah berikut untuk menyalin file konfigurasi SSH:

#### 1. Host Vars

Untuk local:
```bash
cp host_vars/localhost.yml.example host_vars/localhost.yml
```

Untuk non-local:
```bash
cp host_vars/server.yml.example host_vars/server.yml
```

#### 2. Group Vars

Jika server target menggunakan sudo password, pastikan Anda sudah mengaturnya pada `host_vars` & `vault`. Jika belum, silakan ikuti langkah pada bagian [Vault Password](#vault-password) untuk membuat vault dan menyimpan password sudo secara aman.

`host_vars/<hostname>.yml`:
```yaml
ansible_become_password: "{{ vault_<hostname>_sudo_password }}"
```

`group_vars/all/vault.yml`:
```yaml
vault_<hostname>_sudo_password: <YOUR-SUDO-PASSWORD>
```

### Vault Password

Membuat vault:
```bash
ansible-vault create group_vars/all/vault.yml
```

Mengedit vault:
```bash
ansible-vault edit group_vars/all/vault.yml
```

### Playbooks

#### Penggunaan Playbook

```bash
ansible-playbook -i inventory playbooks/<nama-playbook>.yml
```

Contoh:

```bash
ansible-playbook -i inventory playbooks/docker.yml
```

#### `playbooks/docker.yml`

Digunakan untuk:
- Menginstal Docker Engine.
- Menginstal Docker Compose.
- Memulai dan mengaktifkan service Docker.

#### `playbooks/hardening.yml`

Digunakan untuk menerapkan konfigurasi hardening pada server target, termasuk user, group, firewall, dan SSH.

_Sebelum menjalankan playbook ini, pastikan SSH key sudah digenerate manual, lalu salin (public key) ke `ansible/keys/<inventory-hostname>.pub`._

Struktur key pada project:

```text
ansible/
└── keys/
    └── <hostname>.pub
```

**Persiapan:**

1. Generate key pair jika belum tersedia:
   ```bash
   ssh-keygen -t ed25519
   ```
2. Salin public key:
   ```bash
   cp ~/.ssh/id_ed25519.pub ansible/keys/<inventory-hostname>.pub
   ```

#### `playbooks/deploy.yml`

Digunakan untuk melakukan deployment aplikasi pada server target.

---

## 4. Keputusan Teknis yang Diambil

### 4.1 Penghapusan Default Credential Database

Default credential database yang sebelumnya terdapat pada `app/app.py` dihapus.

**Alasan:** Menyimpan credential secara langsung di source code berisiko menyebabkan kebocoran informasi sensitif.

### 4.2 Perubahan Scope Fungsi `init_db()`

Scope pemanggilan fungsi `init_db()` pada `app/app.py` diubah.

**Alasan:** Memastikan proses inisialisasi database tetap dijalankan ketika aplikasi dijalankan menggunakan Gunicorn.


### 4.3 Penggunaan `python:3.9-slim` sebagai Base Image

Docker image aplikasi menggunakan:

```dockerfile
FROM python:3.9-slim
```

**Alasan:** Image `slim` memiliki ukuran yang lebih kecil dibandingkan image Python standar sehingga lebih sesuai untuk aplikasi API sederhana.
