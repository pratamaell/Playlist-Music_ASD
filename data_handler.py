# Anggota 3: File Handling - Load dan Save data playlist ke CSV untuk persistensi data

import csv  
import os  

CSV_FILE = 'playlist.csv'  # Konstanta nama file CSV untuk menyimpan data playlist

def save_to_csv(playlist):
    """
    Simpan playlist ke file CSV agar data tidak hilang saat restart aplikasi.
    """
    try:
        data = []  # Inisialisasi list kosong untuk menyimpan data lagu
        curr = playlist.head  # Mulai dari head playlist (node pertama)
        while curr:  # Loop melalui semua node di playlist
            data.append([curr.id, curr.title, curr.artist, curr.duration, curr.file_path])  # Tambahkan data lagu ke list
            curr = curr.next  # Pindah ke node berikutnya
        
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:  # Buka file CSV untuk menulis (mode write)
            writer = csv.writer(f)  # Buat writer untuk menulis ke CSV
            writer.writerow(['ID', 'Title', 'Artist', 'Duration', 'FilePath'])  # Tulis header kolom
            writer.writerows(data)  # Tulis semua data lagu
        print(f"Data disimpan ke {CSV_FILE}")  # Cetak pesan konfirmasi penyimpanan
    except Exception as e:
        print(f"Error menyimpan CSV: {e}")

