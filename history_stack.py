# Anggota 3: Stack - Riwayat lagu yang telah diputar, menggunakan struktur data stack (LIFO)

class HistoryStack:
    """
    Stack untuk menyimpan riwayat lagu yang diputar. Push saat play, pop untuk undo, show untuk tampilkan.
    """
    def __init__(self, max_size=100):
        self.top = None  # Inisialisasi pointer top stack sebagai None, menandakan stack kosong
        self.size = 0  # Inisialisasi counter ukuran stack sebagai 0
        self.max_size = max_size  # Maksimal ukuran stack untuk mencegah memory leak
    
    def push(self, song):
        """
        Tambahkan lagu ke riwayat (push ke stack).
        """
        # Jika sudah mencapai max_size, buang node terakhir dari stack
        if self.size >= self.max_size:
            # Traverse ke node kedua dari akhir dan hapus node terakhir
            if self.top and self.top.next:
                curr = self.top
                while curr.next and curr.next.next:
                    curr = curr.next
                curr.next = None  # Hapus link ke node terakhir
            self.size -= 1  # Kurangi size
        
        try:
            new_node = type('Node', (), {'song': song, 'next': self.top})()  # Buat node baru dengan song dan next menunjuk ke top saat ini
            self.top = new_node  # Set top baru sebagai node yang baru dibuat
            self.size += 1  # Tambah ukuran stack
            print(f"Riwayat: {song.title} ditambahkan")  # Cetak pesan konfirmasi penambahan ke riwayat
        except Exception as e:
            print(f"Error menambah riwayat: {e}")
    
    def pop(self):
        """
        Hapus lagu terakhir dari riwayat (pop dari stack).
        """
        if not self.top:  # Jika stack kosong (top adalah None)
            print("Riwayat kosong")  # Cetak pesan bahwa riwayat kosong
            return None  # Kembalikan None
        
        try:
            song = self.top.song  # Simpan song dari top sebelum dihapus
            self.top = self.top.next  # Pindah top ke node berikutnya
            self.size -= 1  # Kurangi ukuran stack
            print(f"Pop: {song.title}")  # Cetak pesan pop dengan judul lagu
            return song  # Kembalikan song yang di-pop
        except Exception as e:
            print(f"Error saat pop: {e}")
            return None
    
    def show_history(self):
        """
        Tampilkan semua lagu di riwayat pemutaran.
        """
        if not self.top:  # Jika stack kosong
            print("Riwayat kosong")  # Cetak pesan riwayat kosong
            return  # Keluar dari fungsi
        
        try:
            print("\nRIWAYAT LAGU DIPUTAR:")  # Cetak header riwayat
            curr = self.top  # Mulai dari top stack
            i = 1  # Counter untuk nomor urut
            while curr:  # Loop selama ada node
                print(f"{i}. {curr.song.title} - {curr.song.artist}")  # Cetak nomor, judul, dan artis lagu
                curr = curr.next  # Pindah ke node berikutnya
                i += 1  # Tambah counter
        except Exception as e:
            print(f"Error menampilkan riwayat: {e}")

