import pygame
import os

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
        self.head = None
        self.tail = None
        self.current = None

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

        if self.head is None:
            print("Playlist kosong.")
            return

        if self.current is None:
            self.current = self.head

        try:
            pygame.mixer.music.load(self.current.file_path)
            pygame.mixer.music.play()

            print("\n🎵 Now Playing:")
            print(f"Judul  : {self.current.title}")
            print(f"Artis  : {self.current.artist}")
            print(f"Durasi : {self.current.duration} menit")

        except Exception as e:
            print("Gagal memutar lagu:", e)

    # ========================
    # NEXT
    # ========================
    def next_song(self):

        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        if self.current.next:
            self.current = self.current.next
        else:
            self.current = self.head  # looping ke awal

        self.play_song()

    # ========================
    # PREVIOUS
    # ========================
    def previous_song(self):

        if self.current is None:
            print("Belum ada lagu diputar.")
            return

        if self.current.prev:
            self.current = self.current.prev
        else:
            self.current = self.tail  # looping ke akhir

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


# ========================
# PROGRAM UTAMA
# ========================
playlist = Playlist()

while True:

    print("\n========== MENU PLAYLIST ==========")
    print("1. Tambah Lagu")
    print("2. Lihat Playlist")
    print("3. Hapus Lagu")
    print("4. Play Lagu")
    print("5. Next Lagu")
    print("6. Previous Lagu")
    print("7. Pause Lagu")
    print("8. Resume Lagu")
    print("0. Keluar")

    pilihan = input("Pilih menu: ")
    if pilihan == "1":

        id_song = input("ID Lagu: ").strip()

        if id_song == "":
            print("ID tidak boleh kosong!")
            continue

        title = input("Judul: ")
        artist = input("Artis: ")
        duration = input("Durasi (contoh 03.30): ")
        file_path = input("Path file lagu: ")

        playlist.add_song(id_song, title, artist, duration, file_path)

    elif pilihan == "2":
        playlist.show_playlist()

    elif pilihan == "3":
        try:
            id_song = int(input("ID lagu yang dihapus: "))
            playlist.delete_song(id_song)
        except:
            print("ID harus angka!")

    elif pilihan == "4":
        playlist.play_song()

    elif pilihan == "5":
        playlist.next_song()

    elif pilihan == "6":
        playlist.previous_song()
        
    elif pilihan == "7":
        playlist.pause_song()

    elif pilihan == "8":
        playlist.resume_song()

    elif pilihan == "0":
        print("Program selesai.")
        break

    else:
        print("Menu tidak valid!")