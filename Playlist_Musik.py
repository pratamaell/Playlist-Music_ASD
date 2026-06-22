import pygame
import os
import json  # Import untuk handling JSON di save/load playlist
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from data_handler import save_to_csv  # Anggota 3: Import untuk file handling CSV
from history_stack import HistoryStack  # Anggota 3: Import untuk stack riwayat lagu
from search_sort import search_title, search_artist, sort_title_asc, sort_duration_asc  # Anggota 3: Import untuk searching dan sorting
import random
from tkinter import filedialog
import tkinter as tk



pygame.mixer.init()


class SongNode:
    def __init__(self, id_song, title, artist, duration, file_path):
        self.id = id_song
        self.title = title
        self.artist = artist
        self.duration = duration
        self.file_path = file_path
        self.next = None
        self.prev = None


class Playlist:
    def __init__(self):
        self.head = None  # Pointer ke node pertama (head) doubly linked list playlist
        self.tail = None  # Pointer ke node terakhir (tail) doubly linked list playlist
        self.current = None  # Pointer ke lagu yang sedang diputar saat ini
        self.history = HistoryStack()  # Anggota 3: Inisialisasi stack untuk menyimpan riwayat lagu yang diputar
        self.loop_mode = 'semua'  # Mode loop: 'semua' (ulang semua), 'satu' (ulang satu lagu), 'off' (tidak ulang)
        self.volume = 50
        self.shuffle = False
        self.music_dir = 'Music'


# ========================
    # TAMBAH LAGU
    # ========================
    def add_song(self, id_song, title, artist, duration, file_path):
        # Validasi 1: Memastikan input string untuk judul dan artis tidak kosong/hanya spasi
        if title.strip() == "" or artist.strip() == "":
            print("Judul dan artis tidak boleh kosong!")
            return # Membatalkan proses penambahan

        # Validasi 2: Cek keunikan ID (traversal dari head untuk memastikan ID belum terpakai)
        current = self.head
        while current:
            if current.id == id_song:
                print("ID sudah digunakan!")
                return # Membatalkan proses jika ditemukan ID duplikat
            current = current.next

        # Membuat instance objek node baru dari class SongNode
        new_song = SongNode(id_song, title, artist, duration, file_path)

        # Kondisi A: Jika playlist masih kosong, node baru otomatis menjadi head sekaligus tail
        if self.head is None:
            self.head = new_song
            self.tail = new_song
        # Kondisi B: Jika playlist sudah ada isinya, pasang node baru di ujung belakang (tail)
        else:
            self.tail.next = new_song  # Hubungkan next dari tail lama ke node baru
            new_song.prev = self.tail  # Hubungkan prev dari node baru ke tail lama
            self.tail = new_song       # Geser pointer tail utama ke node baru yang sekarang berada di ujung

        print("Lagu berhasil ditambahkan!")


    # ========================
    # TAMPILKAN PLAYLIST
    # ========================
    def show_playlist(self):
        # Validasi: Jika head kosong, berarti tidak ada lagu untuk ditampilkan
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        # Proses Traversal: Menelusuri linked list dari head sampai ujung (None)
        current = self.head
        print("\n=== PLAYLIST ===")
        while current:
            # Mencetak informasi detail dari setiap node lagu yang dilewati
            print(f"{current.id}. {current.title} - {current.artist} ({current.duration})")
            current = current.next # Pindah ke node berikutnya


    # ========================
    # DELETE
    # ========================
    def delete_song(self, id_song):
            current = self.head
            # Konversi input ke string agar cocok dengan tipe data saat penyimpanan (antisipasi input int/str)
            id_target = str(id_song)

            # Pencarian node yang akan dihapus berdasarkan ID
            while current:
                # Bandingkan id dalam bentuk string
                if str(current.id) == id_target:
                    
                    # KASUS 1: Node yang dihapus adalah HEAD (Lagu pertama)
                    if current == self.head:
                        self.head = current.next # Geser head ke node kedua
                        if self.head:
                            self.head.prev = None # Putus hubungan prev node baru ke node lama
                        else:
                            self.tail = None # Jika setelah digeser head jadi None, berarti list sekarang kosong (tail juga None)
                            
                    # KASUS 2: Node yang dihapus adalah TAIL (Lagu terakhir)
                    elif current == self.tail:
                        self.tail = current.prev # Mundurkan tail ke node sebelum terakhir
                        if self.tail:
                            self.tail.next = None # Putus hubungan next dari tail baru
                            
                    # KASUS 3: Node yang dihapus berada di TENGAH playlist
                    else:
                        current.prev.next = current.next # Hubungkan next milik node SEBELUMNYA langsung ke node SESUDAHNYA
                        current.next.prev = current.prev # Hubungkan prev milik node SESUDAHNYA langsung ke node SEBELUMNYA

                    # Fitur Safety: Jika lagu yang sedang diputar (current) adalah lagu yang dihapus
                    if self.current == current:
                        self.current = None # Reset pointer lagu aktif menjadi None
                        pygame.mixer.music.stop() # Hentikan audio yang sedang berjalan agar tidak error

                    print(f"Lagu dengan ID {id_song} berhasil dihapus!")
                    return # Keluar dari fungsi setelah berhasil menghapus

                current = current.next # Geser ke node berikutnya jika ID belum cocok

            # Pesan ini hanya tercapai jika perulangan 'while' selesai tanpa memicu 'return'
            print(f"ID {id_song} tidak ditemukan!")
            
            
    # ========================
    # EDIT LAGU
    # ========================
    def edit_song(self, id_song, new_title=None, new_artist=None, new_duration=None, new_file_path=None):
        current = self.head
    
        # Pencarian node lagu yang akan diedit berdasarkan ID
        while current:
            if current.id == id_song:
                # Blok pengecekan parameter optional: Data hanya diperbarui jika argumen diisi dan bukan spasi kosong
                if new_title and new_title.strip() != "":
                    current.title = new_title.strip()
                    
                if new_artist and new_artist.strip() != "":
                    current.artist = new_artist.strip()
                    
                if new_duration and new_duration.strip() !="":
                    current.duration = new_duration.strip()
                    
                if new_file_path and new_file_path.strip() != "":
                    current.file_path = new_file_path.strip()
                    
                print("Lagu berhasil diedit!")
                return # Keluar fungsi setelah berhasil memperbarui data
                
            current = current.next # Lanjut cari ke node berikutnya
    
        
# ========================
    # PLAY
    # ========================
    def play_song(self):
        # Validasi 1: Periksa apakah playlist dalam keadaan kosong
        if self.head is None:  
            print("Playlist kosong.")  
            return  # Menghentikan fungsi agar tidak lanjut ke proses play

        # Validasi 2: Jika pemutar musik baru dibuka atau belum ada lagu aktif yang dipilih
        if self.current is None:  
            self.current = self.head  # Set pointer lagu saat ini ke lagu pertama (head)

        # Blok penanganan error untuk mengantisipasi masalah pada file audio (misal: file corrupt atau path salah)
        try:
            pygame.mixer.music.load(self.current.file_path)  # Memuat file audio dari path yang tersimpan di node
            pygame.mixer.music.play()  # Memulai pemutaran audio menggunakan Pygame

            # Anggota 3: Tambahkan lagu ke riwayat saat diputar
            self.history.push(self.current)  # Menyimpan object node lagu saat ini ke dalam Stack riwayat

            # Menampilkan informasi metadata lagu yang sedang aktif di konsol
            print("\n🎵 Now Playing:")  
            print(f"Judul  : {self.current.title}")  
            print(f"Artis  : {self.current.artist}")  
            print(f"Durasi : {self.current.duration} menit")  

        # Menangkap segala jenis exception/error yang terjadi di dalam blok try
        except Exception as e:  
            print("Gagal memutar lagu:", e)  # Menampilkan pesan error spesifik tanpa menghentikan paksa program

    # ========================
    # NEXT
    # ========================
    def next_song(self):
        # Validasi: Tidak bisa pindah lagu jika belum ada lagu yang sedang aktif
        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        # KONDISI 1: Jika fitur acak (Shuffle) aktif
        if self.shuffle:
            all_nodes = []
            curr = self.head
            # Lakukan traversal untuk mengumpulkan semua node lagu ke dalam list
            while curr:
                all_nodes.append(curr)
                curr = curr.next
            # Memilih satu node lagu secara acak dari list menggunakan library random
            if all_nodes:
                self.current = random.choice(all_nodes)
                
        # KONDISI 2: Jika shuffle mati, dan masih ada node lagu berikutnya (Doubly Linked List)
        elif self.current.next:
            self.current = self.current.next
            
        # KONDISI 3: Jika sudah di ujung playlist, tetapi mode loop diatur ke 'semua'
        elif self.loop_mode == 'semua':
            self.current = self.head  # Kembali ke lagu paling pertama
            
        # KONDISI 4: Jika mode loop diatur ke 'satu' (mengulang lagu yang sama)
        elif self.loop_mode == 'satu':
            pass  # Pointer current tetap diam di node yang sama (stay)
            
        # KONDISI 5: Jika sudah di ujung playlist dan mode loop mati (off)
        else:
            print("Akhir playlist (loop off).")
            return # Keluar dari fungsi dan tidak memanggil play_song()

        # Panggil fungsi play_song() untuk memutar lagu baru yang sudah ditentukan pointernya di atas
        self.play_song()

    # ========================
    # PREVIOUS
    # ========================
    def previous_song(self):
        # Validasi: Tidak bisa kembali ke lagu sebelumya jika belum ada lagu yang aktif
        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        # KONDISI 1: Jika fitur acak (Shuffle) aktif, lagu sebelumnya juga diacak
        if self.shuffle:
            all_nodes = []
            curr = self.head
            # Kumpulkan semua node ke dalam list untuk diacak kembali
            while curr:
                all_nodes.append(curr)
                curr = curr.next
            if all_nodes:
                self.current = random.choice(all_nodes)
                
        # KONDISI 2: Jika shuffle mati, dan masih ada node lagu sebelumnya (Double Linked list .prev)
        elif self.current.prev:
            self.current = self.current.prev
            
        # KONDISI 3: Jika berada di awal playlist, tetapi mode loop diatur ke 'semua'
        elif self.loop_mode == 'semua':
            self.current = self.tail  # Lompat langsung ke lagu paling terakhir (tail)
            
        # KONDISI 4: Jika mode loop diatur ke 'satu' (mengulang lagu yang sama)
        elif self.loop_mode == 'satu':
            pass  # Pointer current tidak bergeser
            
        # KONDISI 5: Jika berada di awal playlist dan mode loop mati (off)
        else:
            print("Awal playlist (loop off).")
            return # Keluar dari fungsi dan tidak memanggil play_song()

        # Panggil fungsi play_song() untuk memutar lagu berdasarkan pointer yang baru
        self.play_song()
        
        # Catatan: Baris print di bawah ini berada di luar kendali alur (unreachable/dead code jika kondisi else terpenuhi), 
        # kemungkinan sisa debugging atau salah penempatan indentasi.
        print("ID tidak ditemukan!")
        
    # ========================
    # PAUSE / RESUME / STOP
    # ========================
    def pause_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            print("⏸ Lagu di-pause")
        else:
            print("Tidak ada lagu yang sedang diputar.")


    def resume_song(self):
        pygame.mixer.music.unpause()
        print("▶️ Lagu dilanjutkan")

    """
    ANGOTA 3: Pengaturan - Atur volume, toggle shuffle, set loop mode, dan tampilkan status saat ini
    """
    def set_volume(self, vol):
        vol = max(0, min(100, vol))  # Batasi volume antara 0-100
        pygame.mixer.music.set_volume(vol / 100.0)  # Set volume mixer pygame (0.0-1.0)
        self.volume = vol  # Simpan volume ke atribut
        print(f"🔊 Volume: {vol}%")  # Cetak status volume

    def stop_song(self):
        pygame.mixer.music.stop()  # Hentikan pemutaran musik
        print("⏹ Lagu dihentikan")  # Cetak pesan stop

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle  # Toggle nilai shuffle (True/False)
        print(f"🎲 Shuffle: {'ON' if self.shuffle else 'OFF'}")  # Cetak status shuffle

    def set_loop_mode(self, mode):
        if mode in ['semua', 'satu', 'off']:  # Periksa mode valid
            self.loop_mode = mode  # Set mode loop
            print(f"🔁 Loop: {mode}")  # Cetak status loop
        else:
            print("Mode tidak valid!")  # Cetak error jika invalid

    def show_status(self):
        if self.current:  # Jika ada lagu aktif
            print(f"🎵 Current: {self.current.title} - {self.current.artist}")  # Cetak lagu saat ini
            print(f"🔊 Vol: {self.volume}% | 🎲 Shuffle: {'ON' if self.shuffle else 'OFF'} | 🔁 Loop: {self.loop_mode}")  # Cetak status
        else:
            print("Tidak ada lagu aktif.")  # Cetak jika tidak ada lagu

    def save_playlist(self, filename='playlist.json'):
        data = []  # Inisialisasi list untuk data playlist
        curr = self.head  # Mulai dari head
        while curr:  # Loop melalui semua node
            data.append({  # Tambahkan dict lagu ke list
                'id': curr.id,
                'title': curr.title,
                'artist': curr.artist,
                'duration': curr.duration,
                'file_path': curr.file_path
            })
            curr = curr.next  # Pindah ke node berikutnya
        with open(filename, 'w') as f:  # Buka file untuk menulis
            json.dump(data, f, indent=2)  # Dump data ke JSON dengan indent
        print("Playlist disimpan!")  # Cetak pesan sukses

    def load_playlist(self, filename='playlist.json'):
        if os.path.exists(filename):  # Periksa file ada
            with open(filename, 'r') as f:  # Buka file untuk membaca
                data = json.load(f)  # Load data dari JSON
            self.head = None  # Reset head
            self.tail = None  # Reset tail
            self.current = None  # Reset current
            for song_data in data:  # Loop melalui data
                self.add_song(song_data['id'], song_data['title'], song_data['artist'], song_data['duration'], song_data['file_path'])  # Tambah lagu
            print("Playlist dimuat!") 
        else:
            print("File tidak ditemukan.") 
    def load_music_folder(self):

        music_path = os.path.abspath(self.music_dir)
        id_counter = 1

        for file in os.listdir(music_path):

            if file.lower().endswith('.mp3'):

                full_path = os.path.join(music_path, file)

                # default
                title = os.path.splitext(file)[0]
                artist = "Unknown"
                duration = "Unknown"

                try:
                    audio = MP3(full_path, ID3=EasyID3)

                    # ambil title
                    if 'title' in audio:
                        title = audio['title'][0]

                    # ambil artist
                    if 'artist' in audio:
                        artist = audio['artist'][0]

                    # ambil durasi
                    audio_info = MP3(full_path)
                    total_seconds = int(audio_info.info.length)

                    minutes = total_seconds // 60
                    seconds = total_seconds % 60

                    duration = f"{minutes}:{seconds:02d}"

                except:
                    pass

                # =========================
                # FALLBACK DARI NAMA FILE
                # =========================
                if artist == "Unknown":

                    filename = os.path.splitext(file)[0]

                    if " - " in filename:
                        artist, title = filename.split(" - ", 1)

                self.add_song(
                    str(id_counter),
                    title,
                    artist,
                    duration,
                    full_path
                )

                id_counter += 1

        print("Lagu dari folder Music dimuat!")

# ========================
# HELPER FUNCTION - FILE PICKER
# ========================
def pick_music_file():
    """
    Buka file picker dialog untuk memilih file MP3 dari mana saja di sistem.
    Return: file path jika user memilih, atau None jika cancel.
    """
    root = tk.Tk()
    root.withdraw()  # Sembunyikan window tkinter
    root.attributes('-topmost', True)  # Buat window selalu di atas
    
    file_path = filedialog.askopenfilename(
        title="Pilih file MP3",
        filetypes=[("MP3 Files", "*.mp3"), ("Semua File", "*.*")],
        initialdir=os.path.expanduser("~")  # Buka dari home directory
    )
    
    root.destroy()  # Tutup window tkinter
    return file_path if file_path else None

# ========================
# PROGRAM UTAMA
# ========================
playlist = Playlist()
playlist.load_music_folder()

print("🚀 Playlist Musik siap! Gunakan menu untuk navigasi.")

def menu_playlist():
    while True:
        print("\n--- MENU PLAYLIST (CRUD) ---")
        print("1. Tambah Lagu")
        print("2. Lihat Playlist")
        print("3. Hapus Lagu")
        print("4. Edit Lagu")            
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        
        if pilihan == "1":
            print("\nMembuka file picker...")  
            file_path = pick_music_file()

            if file_path is None:
                print("Pembatalan pemilihan file.")
                continue
            
            if not os.path.exists(file_path):
                print("File tidak ditemukan!")
                continue

            file_name = os.path.basename(file_path)
            filename = os.path.splitext(file_name)[0]

            title = filename
            artist = "Unknown"
            duration = "Unknown"

            try:
                audio = MP3(file_path, ID3=EasyID3)

                # title
                if 'title' in audio:
                    title = audio['title'][0]

                # artist
                if 'artist' in audio:
                    artist = audio['artist'][0]

                # duration
                audio_info = MP3(file_path)

                total_seconds = int(audio_info.info.length)

                minutes = total_seconds // 60
                seconds = total_seconds % 60

                duration = f"{minutes}:{seconds:02d}"

            except:
                pass

            # fallback nama file
            if artist == "Unknown":
                if " - " in filename:
                    artist, title = filename.split(" - ", 1)

            # auto ID random
            id_song = str(random.randint(1000, 9999))

            playlist.add_song(
                id_song,
                title,
                artist,
                duration,
                file_path
            )
        
        elif pilihan == "2":
            playlist.show_playlist()
        
        elif pilihan == "3":
            id_song = input("ID lagu yang dihapus: ").strip()
            if not id_song.isdigit():
                print("ID harus angka!")
                continue
            playlist.delete_song(id_song)
            
        # ========================
        # BLOK EDIT LAGU DITAMBAHKAN
        # ========================
        elif pilihan == "4":
            id_song = input("Masukkan ID lagu yang ingin diedit: ").strip()
            
            print("Tips: Kosongkan isian dan langsung tekan Enter jika tidak ingin mengubah data tersebut.")
            new_title = input("Judul baru: ").strip()
            new_artist = input("Artis baru: ").strip()
            new_duration = input("Durasi baru (contoh 03:45): ").strip()
            new_file_path = input("Path file MP3 baru: ").strip()
            
            playlist.edit_song(id_song, new_title, new_artist, new_duration, new_file_path)
        
        elif pilihan == "5":
            save_to_csv(playlist)  # Anggota 3: Simpan data playlist ke file CSV untuk persistensi
        
        elif pilihan == "0":
            break
        
        else:
            print("Menu tidak valid!")

def menu_lagu():
    while True:
        print("\n--- MENU LAGU ---")
        print("1. Play Lagu")
        print("2. Next Lagu")
        print("3. Previous Lagu")
        print("4. Pause Lagu")
        print("5. Resume Lagu")
        print("6. Stop Lagu")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            playlist.play_song()
        
        elif pilihan == "2":
            playlist.next_song()
        
        elif pilihan == "3":
            playlist.previous_song()
        
        elif pilihan == "4":
            playlist.pause_song()
        
        elif pilihan == "5":
            playlist.resume_song()
        
        elif pilihan == "6":
            playlist.stop_song()
        
        elif pilihan == "0":
            break
        
        else:
            print("Menu tidak valid!")


def menu_utility():
    while True:
        print("\n--- MENU UTILITY ---")
        print("1. Lihat Riwayat")
        print("2. Cari berdasarkan Judul")
        print("3. Cari berdasarkan Artis")
        print("4. Urutkan berdasarkan Alfabet")
        print("5. Urutkan berdasarkan Durasi Pendek-Panjang")
        print("6. Simpan ke CSV")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            playlist.history.show_history()
        
        elif pilihan == "2":
            keyword = input("Kata kunci judul: ").strip()
            results = search_title(playlist, keyword)
            if results:
                print(f"\nHasil pencarian untuk '{keyword}':")
                for song in results:
                    print(f"{song.id}. {song.title} - {song.artist}")
            else:
                print("Tidak ditemukan.")
        
        elif pilihan == "3":
            keyword = input("Kata kunci artis: ").strip()
            results = search_artist(playlist, keyword)
            if results:
                print(f"\nHasil pencarian untuk '{keyword}':")
                for song in results:
                    print(f"{song.id}. {song.title} - {song.artist}")
            else:
                print("Tidak ditemukan.")
        
        elif pilihan == "4":
            sort_title_asc(playlist)
        
        elif pilihan == "5":
            sort_duration_asc(playlist)
        
        elif pilihan == "6":
            save_to_csv(playlist)
        
        elif pilihan == "0":
            break
        
        else:
            print("Menu tidak valid!")

while True:
    print("\n========== MENU UTAMA ==========")
    print("1. Menu Playlist (CRUD)")
    print("2. Menu Lagu")
    print("3. Menu Utility")
    print("0. Keluar")
    
    pilihan = input("Pilih menu: ").strip()
    if pilihan == "1":
        menu_playlist()
    elif pilihan == "2":
        menu_lagu()
    elif pilihan == "3":
        menu_utility()
    elif pilihan == "0":
        print("Program selesai.")
        break
    else:
        print("Menu tidak valid!")