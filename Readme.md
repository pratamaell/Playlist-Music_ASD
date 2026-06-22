# 🎵 Aplikasi Pengelola Playlist Musik (Music Playlist Manager)

Proyek ini merupakan aplikasi manajemen playlist musik berbasis CLI (Command Line Interface) yang dibuat untuk memenuhi tugas mata kuliah **Struktur Data dan Algoritma (ASD)**. Aplikasi ini mengimplementasikan berbagai konsep struktur data fundamental untuk menyimulasikan pemutar musik digital secara efisien.

---

## 👥 Anggota Kelompok 13

**Program Studi Teknologi Rekayasa Perangkat Lunak (TPL B) - Sekolah Vokasi IPB University**

- **Rony Wijaya** - `J0403251047`
- **Pratama Fahriel Sanjaya** - `J0403251053`
- **Muhammad Haris** - `J0403251141`

🎥 **[Tonton Video Demonstrasi Aplikasi di YouTube](https://www.youtube.com/watch?v=BDK6caP0vY4)**

---

## 🛠️ Arsitektur Sistem & Struktur Data

Aplikasi ini memanfaatkan kombinasi struktur data untuk menangani alur kerja pemutaran musik:

1.  **Double Linked List (DLL)**
    - **Kegunaan:** Digunakan sebagai struktur utama penyimpanan playlist lagu.
    - **Alasan:** Mempermudah navigasi lagu berikutnya (`next`) dan lagu sebelumnya (`previous`) berkat pointer ganda pada setiap _node_.
2.  **Stack (Tumpukan)**
    - **Kegunaan:** Digunakan untuk mencatat riwayat (_history_) pemutaran lagu.
    - **Alasan:** Menggunakan prinsip **LIFO (Last In, First Out)**, sehingga lagu yang terakhir kali diputar akan muncul di urutan paling atas riwayat. Batas maksimal riwayat dikonfigurasi hingga 100 lagu.
3.  **Linear Search**
    - **Kegunaan:** Digunakan pada fitur pencarian lagu berdasarkan judul atau nama musisi (_artist_). Pencarian bersifat _case-insensitive_.
4.  **Bubble Sort**
    - **Kegunaan:** Digunakan untuk mengurutkan daftar playlist berdasarkan alfabet (A-Z) dan berdasarkan durasi lagu (dari terpendek ke terpanjang).

---

## 🚀 Fitur Utama Aplikasi

Aplikasi dibagi menjadi 3 menu utama yang memiliki fungsionalitas komprehensif:

### 1. Menu Playlist (Operasi CRUD)

- **Tambah Lagu:** Mengintegrasikan pustaka `Mutagen` untuk membaca metadata file `.mp3` secara otomatis (judul, artis, durasi) dan melakukan validasi ID unik agar tidak duplikat saat dimasukkan ke _node_ baru.
- **Lihat Playlist:** Melakukan _traversal_ dari komponen _head_ hingga _tail_ pada Linked List untuk menampilkan informasi seluruh lagu.
- **Hapus Lagu:** Menghapus lagu berdasarkan ID dengan menangani 3 kondisi struktural: jika lagu berada di _head_, di _tail_, atau di tengah-tengah playlist.
- **Edit Lagu:** Mengubah informasi lagu secara opsional (judul, artis, durasi, atau memperbarui file `.mp3`).

### 2. Menu Lagu (Music Player Control)

- Menggunakan pustaka `Pygame` untuk memproses _audio rendering_.
- **Play Lagu:** Memutar lagu aktif serta otomatis memasukkan data lagu ke dalam _Stack_ riwayat.
- **Next & Previous:** Navigasi maju-mundur antar lagu memanfaatkan pointer ganda Linked List, lengkap dengan fitur **Shuffle (Acak)** menggunakan bantuan _library_ `random`.
- **Media Control:** Fungsi dasar audio seperti _Pause_, _Resume_, dan _Stop_.

### 3. Menu Utilities (Fitur Pendukung)

- **Lihat Riwayat:** Menampilkan daftar lagu yang telah diputar dari _Stack_.
- **Cari Lagu:** Menemukan lagu secara spesifik berdasarkan kriteria Judul atau Artis menggunakan _Linear Search_.
- **Urutkan Playlist:** Menata ulang posisi _node_ Linked List berdasarkan Alfabet atau Durasi melalui algoritma _Bubble Sort_.
- **Simpan ke CSV:** Fitur _Data Handler_ untuk mengeksplorasi dan mencadangkan data playlist ke dalam file `.csv` menggunakan modul `CSV` dan `OS` bawaan Python agar data tidak hilang ketika aplikasi ditutup.

---

## 📦 Pustaka (Library) yang Digunakan

Pastikan Anda telah memasang dependensi berikut sebelum menjalankan aplikasi:

```bash
pip install pygame mutagen
```
