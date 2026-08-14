# Test Materi - DevOps


## 1. Containerization
- Clone repository
```bash
git clone https://github.com/cloxt01/test-devops
cd test-devops
```

- Salin & sesuaikan environment variables

```bash
cp .env.example .env
nano .env
```

- _Contoh konfigurasi database postgresql_
```bash
DB_HOST=db # nama service database 
DB_PORT=5432 # port default postgresql
DB_NAME=<NAMA_DATABASE>
DB_USER=<NAMA_USER>
DB_PASSWORD=<NAMA_PASSWORD>

APP_PORT=5000 # port default aplikasi
```

- Build & Run Docker Compose
```bash
docker-compose up --build
```

## 2. CI / CD

<img width="8192" height="1783" alt="IP Pool Request Flow-2026-08-14-155755" src="https://github.com/user-attachments/assets/fda12910-1587-42ba-b824-e1ee0382bdf4" />

  Gambar diatas menunjukan alur kerja (step by step) mulai dari push/pull request hingga push registry. Pipeline hanya akan dijalankan pada branch main. Setelah source code diambil sistem menjalankan linting, testing & vulnerablity scann. Jika seluruh tahap berhasil, base image akan di build dan di push ke registry GHCR.

## 3. Infrastructure as Code

## 4. Keputusan teknis yang diambil**

- Penghapusan default kredensial database pada program aplikasi `app/app.py`
  
  **Alasan :** Karena berisiko menimbulkan masalah kebocoran informasi sensitif.
  
- Penambahan module python `dotenv` ke dalam `requirements.txt` untuk kebutuhan pemanggilan file environment secara terpisah.
  
  **Alasan :** Agar dapat memisahkan konfigurasi environment variable dari source code.
  
- Perubahan scope pada fungsi inisiasi database `init_db()` pada program aplikasi `app/app.py`.

  **Alasan :** Agar fungsi terpanggil walaupun dijalankan melalui gunicorn.
  
- Perubahan sumber konfigurasi port pada program aplikasi `app/app.py`.

  **Alasan :** Agar port sama dengan yang diexpose oleh docker karena dari satu sumber yang sama.

- Penggunakan image `python3.9-slim` sebagai base image aplikasi docker.
  
  **Alasan :** Karena diversi ini ringan dan cocok jika hanya untuk Task API kecil.
