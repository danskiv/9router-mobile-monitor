# DESIGN.md — 9Router Mobile Monitor

> **Spesifikasi Desain & Panduan Gaya Antarmuka (Hallmark & Anti-Slop Compliant)**

---

## 🎨 Identitas & Mood

- **Dial Antislop:** `ENERGY 2 / RHYTHM 2 / MOTION 2`
- **Konsep:** *Dark-mode Tactical Telemetry* — Antarmuka ringkas bergaya panel kontrol telemetri server, dirancang khusus untuk keterbacaan tinggi di layar sentuh ponsel Android dalam kondisi minim cahaya (*low-light*).
- **Filosofi:** *"Content-first, Zero-bloat"* — Setiap elemen visual memiliki fungsi operasional yang jelas, menolak ornamen hampa seperti gradien berlebih, blur beruntun, atau data palsu.

---

## 📐 Token Desain & Palet Warna

| Token | Nilai | Peruntukan |
| :--- | :--- | :--- |
| `--bg` | `#090d16` | Latar belakang dasar halaman (*deep void*) |
| `--card-bg` | `#111827` | Latar kartu informasi & bingkai sirkuit |
| `--card-subtle` | `#162032` | Latar elemen sekunder / baris tabel |
| `--border` | `#1f2937` | Garis pembatas kartu & baris non-aktif |
| `--border-highlight` | `#374151` | Garis pembatas saat disentuh (*hover/touch*) |
| `--primary` | `#3b82f6` | Aksen biru penunjuk metrik output |
| `--accent` | `#f59e0b` | Aksen emas untuk simpul `9Router` & token input |
| `--success` | `#10b981` | Warna rute aktif, kawat menyala, & status online |
| `--wire-gray` | `#374151` | Kawat ortogonal dalam kondisi tidak aktif (*standby*) |
| `--text` | `#f3f4f6` | Teks utama dengan kontras tinggi |
| `--text-muted` | `#9ca3af` | Teks keterangan, label metrik, & waktu relatif |

---

## ⚡ Mekanika Visual Sirkuit Ortogonal

1. **Simpul 9Router (Kiri Atas):**
   - Posisi vertikal: `top: 10px`, tinggi `32px`. Titik pusat sumbu $Y = 26\text{px}$.
   - Sejajar lurus horizontal sempurna dengan Slot 1 (#1) dari daftar provider.
2. **Jalur Kawat (Strictly Orthogonal 90°):**
   - **Slot #1 (Paling Atas):** $M(90, 26) \rightarrow H(138)$. Garis horizontal lurus tanpa deviasi dan tanpa sudut diagonal.
   - **Slot #2..#N (Di Bawahnya):** $M(90, 26) \rightarrow H(114) \rightarrow V(Y_i) \rightarrow H(138)$. Keluar horizontal menuju tiang bus di $X=114$, turun vertikal sesuai baris target, lalu belok horizontal menusuk kartu target.
3. **Dinamika Aliran Saat Aktif:**
   - Provider yang aktif meluncur (*slide*) ke urutan teratas (#1).
   - Jalur kawat berubah menjadi hijau terang (`#10b981`) dengan efek pendar (*drop-shadow*).
   - Mata panah beranimasi (`►`) meluncur dengan kecepatan $0.85\text{s}$ dari 9Router menyusuri kawat hingga masuk ke kotak provider aktif.
   - Transisi pergeseran baris menggunakan kurva kubik `cubic-bezier(0.2, 0.8, 0.2, 1)` selama $0.45\text{s}$.
