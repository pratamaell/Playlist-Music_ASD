class SongNode:
    def __init__(self, id_song, title, artist, duration):
        self.id = id_song
        self.title = title
        self.artist = artist
        self.duration = duration
        self.next = None
        self.prev = None


class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None


    # ========================
    # CREATE
    # ========================
    def add_song(self, id_song, title, artist, duration):

        if title.strip() == "" or artist.strip() == "":
            print("Judul dan artis tidak boleh kosong!")
            return

        current = self.head
        while current:
            if current.id == id_song:
                print("ID sudah digunakan!")
                return
            current = current.next

        new_song = SongNode(id_song, title, artist, duration)

        if self.head is None:
            self.head = new_song
            self.tail = new_song
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song

        print("Lagu berhasil ditambahkan!")


    # ========================
    # READ (TABEL DINAMIS)
    # ========================
    def show_playlist(self):

        if self.head is None:
            print("\nPlaylist kosong.")
            return

        current = self.head
        songs = []

        while current:
            songs.append(current)
            current = current.next

        title_width = max(len(song.title) for song in songs)
        artist_width = max(len(song.artist) for song in songs)

        title_width = max(title_width, len("Judul"))
        artist_width = max(artist_width, len("Artis"))

        header = f"{'ID':<5} {'Judul':<{title_width}} {'Artis':<{artist_width}} {'Durasi':<15}"
        table_width = len(header)

        print("\n" + "=" * table_width)
        print("PLAYLIST".center(table_width))
        print("=" * table_width)

        print(header)
        print("-" * table_width)

        for song in songs:
            print(f"{song.id:<5} {song.title:<{title_width}} {song.artist:<{artist_width}} {song.duration} menit")


    # ========================
    # UPDATE
    # ========================
    def edit_song(self, id_song):

        if self.head is None:
            print("Playlist kosong.")
            return

        current = self.head

        while current:

            if current.id == id_song:

                print("\nKosongkan jika tidak ingin mengubah")

                title = input("Judul baru: ")
                artist = input("Artis baru: ")

                while True:
                    duration_input = input("Durasi baru (contoh: 03.30 menit): ")

                    if duration_input == "":
                        break

                    if "." in duration_input:
                        try:
                            menit, detik = duration_input.split(".")
                            int(menit)
                            int(detik)
                            break
                        except:
                            print("Format durasi salah!")
                    else:
                        print("Gunakan format menit.detik (contoh 03.30)")

                if title != "":
                    current.title = title

                if artist != "":
                    current.artist = artist

                if duration_input != "":
                    current.duration = duration_input

                print("Data lagu berhasil diperbarui!")
                return

            current = current.next

        print("ID lagu tidak ditemukan.")


    # ========================
    # DELETE
    # ========================
    def delete_song(self, id_song):

        if self.head is None:
            print("Playlist kosong.")
            return

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

        print("ID lagu tidak ditemukan.")


# ========================
# PROGRAM UTAMA
# ========================

playlist = Playlist()

while True:

    print("\n========== MENU PLAYLIST ==========")
    print("1. Tambah Lagu")
    print("2. Lihat Playlist")
    print("3. Edit Lagu")
    print("4. Hapus Lagu")
    print("0. Keluar")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":

        while True:
            try:
                id_song = int(input("ID Lagu: "))
                break
            except ValueError:
                print("ID harus berupa angka!")

        title = input("Judul: ")
        artist = input("Artis: ")

        while True:
            duration = input("Durasi (contoh: 03.30 menit): ")

            if "." in duration:
                try:
                    menit, detik = duration.split(".")
                    int(menit)
                    int(detik)
                    break
                except:
                    print("Format salah! Gunakan contoh 03.30")
            else:
                print("Gunakan format menit.detik (03.30)")

        playlist.add_song(id_song, title, artist, duration)

    elif pilihan == "2":
        playlist.show_playlist()

    elif pilihan == "3":

        while True:
            try:
                id_song = int(input("Masukkan ID lagu yang ingin diedit: "))
                break
            except ValueError:
                print("ID harus angka!")

        playlist.edit_song(id_song)

    elif pilihan == "4":

        while True:
            try:
                id_song = int(input("Masukkan ID lagu yang ingin dihapus: "))
                break
            except ValueError:
                print("ID harus angka!")

        playlist.delete_song(id_song)

    elif pilihan == "0":
        print("Program selesai.")
        break

    else:
        print("Menu tidak valid!")