# Anggota 3: File Handling - Load dan Save data playlist ke CSV untuk persistensi data

import csv  
import os  

CSV_FILE = 'playlist.csv'  # Konstanta nama file CSV untuk menyimpan data playlist

def save_to_csv(playlist):
    """
    Simpan playlist ke file CSV agar data tidak hilang saat restart aplikasi.
    """
    data = []  # Inisialisasi list kosong untuk menyimpan data lagu
    curr = playlist.head  # Mulai dari head playlist (node pertama)
    while curr:  # Loop melalui semua node di playlist
        data.append([curr.id, curr.title, curr.artist, curr.duration, curr.file_path])  # Tambahkan data lagu ke list
        curr = curr.next  # Pindah ke node berikutnya
    
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:  # Buka file CSV untuk menulis (mode write)
        writer = csv.writer(f)  # Buat writer untuk menulis ke CSV
        writer.writerow(['ID', 'Title', 'Artist', 'Duration', 'FilePath'])  # Tulis header kolom
        writer.writerows(data)  # Tulis semua data lagu
    print("✅ Data disimpan ke playlist.csv")  # Cetak pesan konfirmasi penyimpanan

def load_from_csv(playlist):
    """
    Muat playlist dari file CSV saat startup aplikasi.
    """
    if not os.path.exists(CSV_FILE):  # Periksa apakah file CSV ada
        print("📄 playlist.csv tidak ditemukan.")  # Cetak pesan jika file tidak ada
        return  # Keluar dari fungsi
    
    playlist.head = None  # Reset head playlist
    playlist.tail = None  # Reset tail playlist
    playlist.current = None  # Reset current playlist
    
    with open(CSV_FILE, 'r', encoding='utf-8') as f:  # Buka file CSV untuk membaca
        reader = csv.DictReader(f)  # Buat reader untuk membaca CSV sebagai dictionary
        for row in reader:  # Loop melalui setiap baris di CSV
            playlist.add_song(row['ID'], row['Title'], row['Artist'], row['Duration'], row['FilePath'])  # Tambahkan lagu ke playlist
    print("✅ Data dimuat dari playlist.csv")  # Cetak pesan konfirmasi pemuatan

