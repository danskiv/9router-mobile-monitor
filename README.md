# 9Router Mobile Monitor

> **Dashboard Pemantau Ringan 9Router LLM Gateway untuk Ponsel Android**  
> Dibuat khusus atas titah Yang Mulia Danas oleh abdi setia Darsam.

---

## 📌 Ringkasan Proyek

**9Router Mobile Monitor** adalah antarmuka web ultra-ringan (*mobile-first PWA*) yang dirancang khusus untuk memantau aktivitas, perutean (*routing*), konsumsi token, efisiensi *cache*, dan riwayat permintaan *real-time* dari gerbang 9Router di NODIX1 langsung melalui layar ponsel Android.

Aplikasi ini menggantikan dashboard desktop 9Router yang berat (@xyflow/react + Recharts) dengan visualisasi sirkuit ortogonal yang gesit, hemat memori, dan ramah sentuhan jari.

---

## ⚡ Fitur Utama

1. **Executive KPI Cards:**
   - **Total Requests**: Total panggilan API hari ini.
   - **Est. Cost**: Estimasi biaya terhemat berkat *caching*.
   - **Input vs Cached Tokens**: Dilengkapi visual bar persentase efisiensi *Cache Hit Rate*.
   - **Output Tokens**: Total token jawaban model.
2. **Topologi Aliran Dinamis (Dynamic Sliding Queue):**
   - **Simpul 9Router** bertengger kokoh di sisi kiri atas, sejajar horizontal persis dengan provider urutan pertama (#1).
   - **Perpindahan Posisi Otomatis (*Auto-Elevate & Slide*):**
     - Provider yang aktif langsung meluncur (*slide up*) ke posisi paling atas (#1), terhubung dengan garis horizontal lurus tanpa belokan (`M 90 26 H 138`).
     - Jika ada provider lain yang aktif berikutnya, provider baru mengambil posisi #1 dan mendorong provider aktif sebelumnya ke posisi #2, #3, dst.
     - Ketika sebuah provider selesai / mati, posisinya bergeser turun kembali ke kelompok *idle*, dan provider aktif di bawahnya otomatis naik menempati slot atas.
     - Seluruh pergeseran posisi menggunakan transisi CSS *hardware-accelerated* yang halus (*silky smooth*).
3. **Kawat Sirkuit Ortogonal Murni (Anti-Diagonal):**
   - Garis penghubung bersudut siku 90° murni (horizontal $\rightarrow$ bus vertikal $\rightarrow$ horizontal).
   - Status non-aktif: Kawat dan mata panah berwarna abu-abu (`#374151`).
   - Status aktif: Kawat berubah hijau zamrud terang (`#10b981`), memancarkan denyut kilat (*running beam*), dan diiringi partikel panah (`►`) yang meluncur dinamis menyusuri kawat dari 9Router menuju provider target.
4. **Recent Requests Log:**
   - Log 10 permintaan terkini yang diperbarui otomatis setiap beberapa detik dari 9Router lokal.
5. **Zero-Dependency Micro Server (`server.py`):**
   - Menggunakan pustaka standar Python 3 (tanpa perlu `pip install`).
   - Melayani berkas statis sekaligus bertindak sebagai *reverse proxy* untuk API 9Router port 20128.
   - Mengikat port `20130` di `0.0.0.0`, siap diakses aman lewat WireGuard VPN (`http://10.10.10.1:20130`).

---

## 🚀 Cara Menjalankan

### 1. Menjalankan Server
```bash
cd /home/ubuntu/Github/9router-mobile-monitor
python3 server.py
```
*Atau jalankan di latar belakang dengan PM2 / Systemd:*
```bash
pm2 start server.py --name "9router-mobile" --interpreter python3
```

### 2. Mengakses dari Ponsel Android
1. Aktifkan **WireGuard VPN** di ponsel Android Yang Mulia (koneksi ke NODIX1 `10.10.10.1`).
2. Buka peramban Chrome di Android dan tuju alamat:
   ```
   http://10.10.10.1:20130
   ```
3. Tekan menu titik tiga di Chrome $\rightarrow$ pilih **"Add to Home screen"** (Tambahkan ke Layar Utama).
4. Aplikasi akan terpasang sebagai ikon PWA mandiri di beranda ponsel, tampil layar penuh (*fullscreen*) tanpa bilah peramban.

---

## 📂 Struktur Berkas

```
9router-mobile-monitor/
├── index.html        # Antarmuka mandiri (HTML5 + CSS3 + Vanilla JS + SVG)
├── server.py         # Micro-server Python + reverse proxy API 9Router
├── manifest.json     # Konfigurasi PWA Android standalone
├── README.md         # Dokumentasi teknis proyek
└── DESIGN.md         # Spesifikasi desain, anti-slop, & token warna
```

---

## 🛡️ Standar Kualitas (Anti-Slop & Craftsmanship)

- Memenuhi standar **Anti-Slop v3.2.18** dan **Hallmark**.
- Tidak menggunakan metrik fiktif (*no fabricated data*) — seluruh angka ditarik langsung dari instans 9Router lokal.
- Rasio kontras teks memenuhi WCAG AA ($\ge 4.5:1$).
- Ukuran target sentuh tombol minimal 44px untuk kenyamanan jempol di layar HP.
