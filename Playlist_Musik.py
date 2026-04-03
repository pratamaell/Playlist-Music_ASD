import pygame
import os
import json  # Import untuk handling JSON di save/load playlist
from data_handler import save_to_csv, load_from_csv  # Anggota 3: Import untuk file handling CSV
from history_stack import HistoryStack  # Anggota 3: Import untuk stack riwayat lagu
from search_sort import search_title, search_artist, sort_title_asc, sort_duration_asc  # Anggota 3: Import untuk searching dan sorting
import random



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

        if title.strip() == "" or artist.strip() == "":
            print("Judul dan artis tidak boleh kosong!")
            return

        current = self.head
        while current:
            if current.id == id_song:
                print("ID sudah digunakan!")
                return
            current = current.next

        new_song = SongNode(id_song, title, artist, duration, file_path)

        if self.head is None:
            self.head = new_song
            self.tail = new_song
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song

        print("Lagu berhasil ditambahkan!")


    # ========================
    # TAMPILKAN PLAYLIST
    # ========================
    def show_playlist(self):

        if self.head is None:
            print("\nPlaylist kosong.")
            return

        current = self.head
        print("\n=== PLAYLIST ===")
        while current:
            print(f"{current.id}. {current.title} - {current.artist} ({current.duration})")
            current = current.next

    # ========================
    # PLAY
    # ========================
    def play_song(self):

        if self.head is None:  # Jika playlist kosong
            print("Playlist kosong.")  # Cetak pesan error
            return  # Keluar dari fungsi

        if self.current is None:  # Jika belum ada lagu yang dipilih
            self.current = self.head  # Set current ke head (lagu pertama)

        try:
            pygame.mixer.music.load(self.current.file_path)  # Load file lagu ke mixer
            pygame.mixer.music.play()  # Mulai pemutaran lagu

            # Anggota 3: Tambahkan lagu ke riwayat saat diputar
            self.history.push(self.current)  # Push lagu saat ini ke stack riwayat

            print("\n🎵 Now Playing:")  # Cetak header
            print(f"Judul  : {self.current.title}")  # Cetak judul
            print(f"Artis  : {self.current.artist}")  # Cetak artis
            print(f"Durasi : {self.current.duration} menit")  # Cetak durasi

        except Exception as e:  # Jika ada error saat load/play
            print("Gagal memutar lagu:", e)  # Cetak error

    # ========================
    # NEXT
    # ========================
    def next_song(self):

        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        if self.shuffle:
            import random
            all_nodes = []
            curr = self.head
            while curr:
                all_nodes.append(curr)
                curr = curr.next
            if all_nodes:
                self.current = random.choice(all_nodes)
        elif self.current.next:
            self.current = self.current.next
        elif self.loop_mode == 'semua':
            self.current = self.head
        elif self.loop_mode == 'satu':
            pass  # stay
        else:
            print("Akhir playlist (loop off).")
            return

        self.play_song()

    # ========================
    # PREVIOUS
    # ========================
    def previous_song(self):

        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        if self.shuffle:
            import random
            all_nodes = []
            curr = self.head
            while curr:
                all_nodes.append(curr)
                curr = curr.next
            if all_nodes:
                self.current = random.choice(all_nodes)
        elif self.current.prev:
            self.current = self.current.prev
        elif self.loop_mode == 'semua':
            self.current = self.tail
        elif self.loop_mode == 'satu':
            pass
        else:
            print("Awal playlist (loop off).")
            return

        self.play_song()

    # ========================
    # DELETE
    # ========================
    def delete_song(self, id_song):

        current = self.head

        while current:

            if current.id == id_song:

                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None

                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None

                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev

                print("Lagu berhasil dihapus!")
                return

            current = current.next

        print("ID tidak ditemukan!")
        
    # ========================
    # PAUSE / RESUME
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
        music_path = os.path.abspath(self.music_dir)  # Dapatkan path absolut folder Music
        id_counter = 1  # Counter untuk ID lagu
        for file in os.listdir(music_path):  # Loop melalui file di folder
            if file.lower().endswith('.mp3'):  # Jika file adalah MP3
                full_path = os.path.join(music_path, file)  # Buat path lengkap
                title = os.path.splitext(file)[0]  # Ambil nama file tanpa ekstensi sebagai judul
                self.add_song(str(id_counter), title, 'Unknown', 'Unknown', full_path)  # Tambah lagu dengan ID auto
                id_counter += 1  # Tambah counter
        print("Lagu dari folder Music dimuat otomatis!")  

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
        print("4. Simpan ke CSV")
        print("5. Muat dari CSV")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            id_song = input("ID Lagu: ").strip()
            if id_song == "":
                print("ID tidak boleh kosong!")
                continue
            title = input("Judul: ").strip()
            artist = input("Artis: ").strip()
            duration = input("Durasi (contoh 03.30): ").strip()
            file_path = input("Path file lagu: ").strip()
            playlist.add_song(id_song, title, artist, duration, file_path)
        
        elif pilihan == "2":
            playlist.show_playlist()
        
        elif pilihan == "3":
            id_song = input("ID lagu yang dihapus: ").strip()
            if not id_song.isdigit():
                print("ID harus angka!")
                continue
            playlist.delete_song(int(id_song))
        
        elif pilihan == "4":
            save_to_csv(playlist)  # Anggota 3: Simpan data playlist ke file CSV untuk persistensi
        
        elif pilihan == "5":
            load_from_csv(playlist)  # Anggota 3: Muat data playlist dari file CSV saat startup
        
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
        print("7. Lihat Riwayat")
        print("8. Cari berdasarkan Judul")
        print("9. Cari berdasarkan Artis")
        print("10. Urutkan berdasarkan Judul A-Z")
        print("11. Urutkan berdasarkan Durasi Pendek-Panjang")
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
        
        elif pilihan == "7":
            playlist.history.show_history()  # Anggota 3: Tampilkan riwayat lagu yang telah diputar
        
        elif pilihan == "8":
            keyword = input("Kata kunci judul: ").strip()
            results = search_title(playlist, keyword)  # Anggota 3: Cari lagu berdasarkan judul
            if results:
                print(f"\nHasil pencarian untuk '{keyword}':")
                for song in results:
                    print(f"{song.id}. {song.title} - {song.artist}")
            else:
                print("Tidak ditemukan.")
        
        elif pilihan == "9":
            keyword = input("Kata kunci artis: ").strip()
            results = search_artist(playlist, keyword)  # Anggota 3: Cari lagu berdasarkan artis
            if results:
                print(f"\nHasil pencarian untuk '{keyword}':")
                for song in results:
                    print(f"{song.id}. {song.title} - {song.artist}")
            else:
                print("Tidak ditemukan.")
        
        elif pilihan == "10":
            sort_title_asc(playlist)  # Anggota 3: Urutkan playlist berdasarkan judul A-Z
        
        elif pilihan == "11":
            sort_duration_asc(playlist)  # Anggota 3: Urutkan playlist berdasarkan durasi pendek-panjang
        
        elif pilihan == "0":
            break
        
        else:
            print("Menu tidak valid!")

def menu_pengaturan():
    while True:
        print("\n--- MENU PENGATURAN ---")
        print("1. Set Volume")
        print("2. Toggle Shuffle")
        print("3. Set Loop Mode")
        print("4. Lihat Status")
        print("5. Reload Folder Music")
        print("0. Kembali ke Menu Utama")
        
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "1":
            try:
                vol = int(input("Volume (0-100): "))
                playlist.set_volume(vol)
            except ValueError:
                print("Volume harus angka!")
        
        elif pilihan == "2":
            playlist.toggle_shuffle()
        
        elif pilihan == "3":
            mode = input("Mode loop (semua/satu/off): ").strip().lower()
            playlist.set_loop_mode(mode)
        
        elif pilihan == "4":
            playlist.show_status()
        
        elif pilihan == "5":
            playlist.load_music_folder()
        
        elif pilihan == "0":
            break
        
        else:
            print("Menu tidak valid!")

while True:
    print("\n========== MENU UTAMA ==========")
    print("1. Menu Playlist (CRUD)")
    print("2. Menu Lagu")
    print("3. Menu Pengaturan")
    print("0. Keluar")
    
    pilihan = input("Pilih menu: ").strip()
    if pilihan == "1":
        menu_playlist()
    elif pilihan == "2":
        menu_lagu()
    elif pilihan == "3":
        menu_pengaturan()
    elif pilihan == "0":
        print("Program selesai.")
        break
    else:
        print("Menu tidak valid!")