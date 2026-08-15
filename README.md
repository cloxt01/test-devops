# Test Materi - DevOps

Sudah diuji pada OS:
- `Ubuntu 22.04 LTS`

## Requirements

- **Ansible >= 2.21.2**

  Untuk menginstal Ansible, silakan ikuti panduan resmi pada [Ansible Installation](https://docs.ansible.com/projects/ansible/latest/installation_guide/installation_distros.html).

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/cloxt01/test-devops
cd test-devops
```

### 2. Setup Docker Environment

```bash
cp docker/.env.example docker/.env
nano docker/.env
```

> _Detail variable, lihat [Konfigurasi Environment](#konfigurasi-environment)._

### 3. Setup Ansible

- Install collection yang dibutuhkan, sesuaikan inventory, host_vars, dan vault. Lihat [Infrastructure as Code](#3-infrastructure-as-code) untuk langkah lengkapnya.

### 4. Jalankan Playbook

Jika server target adalah server fresh (baru), jalankan playbook berikut secara berurutan dari direktori `ansible/`:

1. `docker.yml` — install Docker
2. `hardening.yml` — hardening server (perlu SSH key, lihat [detail](#playbookshardeningyml))
3. `deploy.yml` — deploy aplikasi

```bash
cd ansible
ansible-playbook -i inventory playbooks/<nama-playbook>.yml --vault-password-file .vault_pass
```

Ganti `<nama-playbook>` sesuai urutan di atas (`docker`, `hardening`, `deploy`).

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

Pipeline hanya dijalankan pada branch `main`, dengan pendekatan **fail-fast** — kegagalan pada satu tahap menghentikan proses sebelum image dipublikasikan.

Tahapan pipeline:

1. Source code diambil dari repository.
2. Linting dijalankan untuk memeriksa kualitas dan format kode.
3. Testing dijalankan untuk memastikan fungsi aplikasi berjalan sesuai dengan yang diharapkan.
4. Vulnerability scanning dilakukan untuk mendeteksi kerentanan pada dependency dan package aplikasi.
5. Jika seluruh tahapan berhasil, Docker image aplikasi akan dibuild dan di-push ke GHCR.

---

## 3. Infrastructure as Code

Infrastructure as Code (IaC) menggunakan Ansible untuk melakukan provisioning, hardening, dan deployment pada server target.

Workdir: `/ansible`

### Install Ansible Collection

```bash
ansible-galaxy collection install community.general community.docker
```

### Inventory

Sesuaikan inventory dengan server target:

```bash
nano inventory
```

Contoh untuk local server:

```ini
[servers]
localhost

[servers:vars]
ansible_become=true
ansible_become_method=sudo
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

### Variable

Sebelum menjalankan playbook, pastikan koneksi SSH ke server target sudah diatur.

#### Host Vars

Untuk local:
```bash
cp host_vars/localhost.yml.example host_vars/localhost.yml
```

Untuk non-local:
```bash
cp host_vars/server.yml.example host_vars/server.yml
```

Cek host variable:
```bash
cat host_vars/<inventory-hostname>.yml
```

_Pastikan ada baris seperti_

```yaml
ansible_become_password: "{{ vault_<inventory-hostname>_sudo_password }}"
```

#### Group Vars & Vault

Salin template vault:
```bash
cp group_vars/all/vault.yml.example group_vars/all/vault.yml
nano group_vars/all/vault.yml
```

Isi dengan password sudo:
```yaml
vault_<inventory-hostname>_sudo_password: <YOUR-SUDO-PASSWORD>
```

Encrypt vault file:
```bash
ansible-vault encrypt group_vars/all/vault.yml
```

Simpan vault password:
```bash
echo <YOUR-VAULT-PASSWORD> > .vault_pass
```

Untuk mengedit vault yang sudah di-encrypt, gunakan:
```bash
ansible-vault edit group_vars/all/vault.yml
```

> Catatan: `ansible-vault create` hanya dipakai jika membuat vault baru dari nol (tanpa file example). Untuk project ini, alurnya selalu **copy dari `.example` → encrypt**, bukan `create`.

### Playbooks

Jalankan dengan:

```bash
ansible-playbook -i inventory playbooks/<nama-playbook>.yml --vault-password-file .vault_pass
```

#### `playbooks/docker.yml`

Digunakan untuk:
- Menginstal Docker Engine.
- Menginstal Docker Compose.
- Memulai dan mengaktifkan service Docker.

#### `playbooks/hardening.yml`

Digunakan untuk menerapkan konfigurasi hardening pada server target, termasuk user, group, firewall, dan SSH.

**Persiapan (wajib sebelum menjalankan playbook ini):**

1. Generate SSH key pair jika belum tersedia:
   ```bash
   ssh-keygen -t ed25519
   ```
2. Salin public key ke direktori project:
   ```bash
   cp ~/.ssh/id_ed25519.pub keys/<inventory-hostname>.pub
   ```

Struktur key pada project:

```text
ansible/
└── keys/
    └── <inventory-hostname>.pub
```

#### `playbooks/deploy.yml`

Digunakan untuk melakukan deployment aplikasi pada server target.

---

## 4. Keputusan Teknis yang Diambil


### 4.1 Perubahan Scope Fungsi `init_db()`

Scope pemanggilan fungsi `init_db()` pada `app/app.py` diubah.

**Alasan:** Memastikan proses inisialisasi database tetap dijalankan ketika aplikasi dijalankan menggunakan Gunicorn.

### 4.2 Penggunaan `python:3.9-slim` sebagai Base Image

Docker image aplikasi menggunakan:

```dockerfile
FROM python:3.9-slim
```

**Alasan:** Image `slim` memiliki ukuran yang lebih kecil dibandingkan image Python standar sehingga lebih sesuai untuk aplikasi API sederhana.

### 4.3 Versi untuk setiap image docker

Semua image docker menggunakan versi yang statis

**Alasan:** Menggunakan versi statis memastikan konsistensi dalam deployment, serta menghindari masalah yang mungkin timbul akibat perubahan versi.

### 4.4 Penonaktifan login & password autentikasi `root` user pada target server

**Alasan:** Meminimalisir akses `root` untuk mengurangi risiko penyalahgunaan akses root dan meningkatkan keamanan server.

## 5. Pertimbangan Keamanan

### 5.1 Penggunaan `docker/.env` untuk Menyimpan Credential

Semua credential sensitif seperti database username dan password, port aplikasi dalam file `docker/.env` yang tidak di-commit ke repository.

### 5.2 Penghapusan Default Credential Database

Default credential database yang sebelumnya terdapat pada `app/app.py` dihapus.

**Alasan:** Menyimpan credential secara langsung di source code berisiko menyebabkan kebocoran informasi sensitif.

### 5.3 Penghapusan Port Database dari host

Port database yang sebelumnya di expose ke host dihapus dari file `docker/compose.yaml`.

**Alasan:** Meningkatkan keamanan dengan membatasi akses ke database hanya dari dalam jaringan Docker, sehingga mengurangi risiko akses tidak sah dari luar.

### 5.4 Penggunaan vault untuk menyimpan password sudo

Password sudo disimpan dalam file vault yang dienkripsi dan tidak di-commit ke repository.

Alasan: Meningkatkan keamanan dengan melindungi password sudo dari akses tidak sah.

### 5.5 Monitoring Connection via Grafana Proxy

Monitoring menggunakan grafana sebagai proxy pada datasource prometheus, gambarannya seperti berikut:

```text
Browser <----> Grafana <----> Prometheus <----> Aplikasi
   |                            |
   <------------PROXY----------->
```

Dnngan begitu grafana tidak langsung mengakses prometheus, tetapi melalui grafana terlebih dahulu, sehingga akses prometheus dapat dibatasi.