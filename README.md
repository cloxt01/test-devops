# Test Materi - DevOps

## Quick Start

**1. Containerization**
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

**2. CI / CD**

**3. Infrastructure as Code**

**4. Keputusan teknis yang diambil**

- Penghapusan default kredensial database pada program aplikasi `app/app.py`
  
  **Alasan :** Karena berisiko menimbulkan masalah kebocoran informasi sensitif.
  
- Penambahan module python `dotenv` ke dalam `requirements.txt` untuk kebutuhan pemanggilan file environment secara terpisah.
  
  **Alasan :** Agar dapat memisahkan konfigurasi environment variable dari source code.
  
- Perubahan scope pada fungsi inisiasi database `init_db()` pada program aplikasi `app/app.py`.

  **Alasan :** Agar fungsi terpanggil walaupun dijalankan melalui gunicorn.
  
- Perubahan sumber konfigurasi port pada program aplikasi `app/app.py`.

  **Alasan :** Agar port sama dengan yang diexpose oleh docker karena dari satu sumber yang sama.
