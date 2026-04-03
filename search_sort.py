# Anggota 3: Searching - Cari lagu berdasarkan judul atau artis untuk memudahkan pencarian dalam playlist besar
# Anggota 3: Sorting - Urutkan playlist berdasarkan judul A-Z atau durasi pendek-panjang untuk organisasi yang lebih baik

def search_title(playlist, keyword):
    """
    Cari lagu berdasarkan kata kunci di judul (case-insensitive).
    """
    results = []  # Inisialisasi list kosong untuk menyimpan hasil pencarian
    curr = playlist.head  # Mulai dari head playlist
    while curr:  # Loop melalui semua node
        if keyword.lower() in curr.title.lower():  # Periksa apakah keyword ada di judul 
            results.append(curr)  # Tambahkan node ke hasil jika cocok
        curr = curr.next  # Pindah ke node berikutnya
    return results  # Kembalikan list hasil

def search_artist(playlist, keyword):
    """
    Cari lagu berdasarkan kata kunci di nama artis (case-insensitive).
    """
    results = []  # Inisialisasi list kosong untuk hasil
    curr = playlist.head  # Mulai dari head
    while curr:  # Loop melalui node
        if keyword.lower() in curr.artist.lower():  # Periksa keyword di artis (case-insensitive)
            results.append(curr)  # Tambahkan jika cocok
        curr = curr.next  # Pindah ke berikutnya
    return results  # Kembalikan hasil

def sort_title_asc(playlist):
    """
    Urutkan playlist berdasarkan judul lagu secara ascending (A-Z) menggunakan bubble sort.
    """
    # Bubble sort DLL by title
    if not playlist.head:  # Jika playlist kosong, keluar
        return
    swapped = True  # Flag untuk menandai apakah ada pertukaran
    while swapped:  # Loop sampai tidak ada pertukaran lagi
        swapped = False  # Reset flag
        curr = playlist.head  # Mulai dari head
        while curr.next:  # Loop sampai sebelum tail
            if curr.title > curr.next.title:  # Jika judul saat ini > berikutnya, tukar
                # Swap nodes - proses pertukaran node di doubly linked list
                prev = curr.prev  # Simpan prev dari curr
                next_node = curr.next  # Simpan next dari curr
                if prev:  # Jika ada prev, set next-nya ke next_node
                    prev.next = next_node
                else:  # Jika curr adalah head, set head ke next_node
                    playlist.head = next_node
                curr.next = next_node.next  # Set next curr ke next dari next_node
                next_node.prev = prev  # Set prev next_node ke prev
                next_node.next = curr  # Set next next_node ke curr
                curr.prev = next_node  # Set prev curr ke next_node
                if curr.next:  # Jika curr punya next, set prev-nya ke curr
                    curr.next.prev = curr
                else:  # Jika curr adalah tail, set tail ke curr
                    playlist.tail = curr
                swapped = True  # Tandai ada pertukaran
    print("✅ Diurutkan judul A-Z") 

def sort_duration_asc(playlist):
    """
    Urutkan playlist berdasarkan durasi lagu secara ascending (pendek ke panjang) menggunakan bubble sort.
    """
    # Bubble sort by duration (assume MM:SS -> seconds)
    def duration_to_sec(dur):  # Fungsi helper untuk konversi durasi ke detik
        m, s = map(int, dur.split('.'))  # Split MM.SS dan konversi ke int
        return m*60 + s  # Hitung total detik
    
    if not playlist.head:  # Jika kosong, keluar
        return
    swapped = True  # Flag pertukaran
    while swapped:  # Loop bubble sort
        swapped = False
        curr = playlist.head
        while curr.next:
            d1 = duration_to_sec(curr.duration)  # Durasi curr dalam detik
            d2 = duration_to_sec(curr.next.duration)  # Durasi next dalam detik
            if d1 > d2:  # Jika d1 > d2, tukar
                # Swap (same as above) - sama seperti di sort_title
                prev = curr.prev
                next_node = curr.next
                if prev:
                    prev.next = next_node
                else:
                    playlist.head = next_node
                curr.next = next_node.next
                next_node.prev = prev
                next_node.next = curr
                curr.prev = next_node
                if curr.next:
                    curr.next.prev = curr
                else:
                    playlist.tail = curr
                swapped = True  # Tandai pertukaran
    print("✅ Diurutkan durasi pendek- panjang")  

