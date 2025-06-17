from tabulate import tabulate
from datetime import datetime

# Data awal
data_karyawan = [
    {
        "id": "1",
        "nama": "Kesuma",
        "posisi": "General Manager",
        "gaji": 10000000,
        "kehadiran": None,
        "proyek": [],
        "riwayat_kehadiran": [],
        "nilai_kinerja": None
    },
    {
        "id": "2",
        "nama": "Tengil",
        "posisi": "Assistent Manager",
        "gaji": 5000000,
        "kehadiran": None,
        "proyek": [],
        "riwayat_kehadiran": [],
        "nilai_kinerja": None
    },
    {
        "id": "3",
        "nama": "Abdul",
        "posisi": "Project Manager",
        "gaji": 5000000,
        "kehadiran": None,
        "proyek": [],
        "riwayat_kehadiran": [],
        "nilai_kinerja": None
    }
]

# Konversi nilai ke presentase kenaikan/penurunan gaji
def nilai_ke_gaji(nilai):
    if nilai == 'A': 
        return 0.10
    elif nilai == 'B':
        return 0.05
    elif nilai == 'C':
        return 0
    elif nilai == 'D':
        return -0.05
    elif nilai == 'E':
        return -0.10
    return None

# Tambah karyawan baru
def create_karyawan():
    while True:
        id_ = input("\nMasukkan ID : ")
        if any(k['id'] == id_ for k in data_karyawan):
            print("ID Sudah Ada, Masukkan Dengan ID Yang Lain.")
            continue
        break
    nama = input("Nama: ").title().strip()
    posisi = input("Posisi: ").title().strip()
    while True:
        try:
            gaji = int(input("Gaji: "))
            break
        except:
            print("Gaji Harus Berupa Format Angka!")
    karyawan = {
        "id": id_,
        "nama": nama,
        "posisi": posisi,
        "gaji": gaji,
        "kehadiran": None,
        "proyek": [],
        "riwayat_kehadiran": [],
        "nilai_kinerja": None
    }
    data_karyawan.append(karyawan)
    print("\n✅ Karyawan berhasil ditambahkan.")

# Tampilkan karyawan + proyek + kehadiran
def tampilkan_detail_karyawan(k):
    print("\n" + "="*50)
    print(f" DATA KARYAWAN: {k['nama'].upper()} (ID: {k['id']})")
    print(tabulate([[
        k['id'], k['nama'], k['posisi'], f"Rp{k['gaji']:,}", k['kehadiran'] or '-', k['nilai_kinerja'] or '-'
    ]], headers=["ID", "Nama", "Posisi", "Gaji", "Kehadiran", "Nilai Kinerja"], tablefmt="grid"))

    # Riwayat Kehadiran
    print("\n📅 Riwayat Kehadiran Terakhir:")
    if k['riwayat_kehadiran']:
        print(tabulate(
            [[r['tanggal'], r['status']] for r in k['riwayat_kehadiran'][-3:]],# mengambil 3 terbaru riwayat kehadiran
            headers=["Tanggal", "Status"], tablefmt="fancy_grid"
        ))
    else:
        print("Belum ada data kehadiran.")

    # Proyek
    print("\n📌 Proyek yang Diikuti:")
    if k['proyek']:
        print(tabulate(
            [[p['nama'], p['peran']] for p in k['proyek']],
            headers=["Nama Proyek", "Peran"], tablefmt="fancy_grid"
        ))
    else:
        print("Belum ada proyek.")

# Submenu edit karyawan
def submenu_karyawan(k):
    while True:
        print("\n--- SUBMENU KARYAWAN ---")
        print("1. Update Data")
        print("2. Hapus Data")
        print("3. Tambah Proyek")
        print("4. Tambah Penilaian Kinerja (+/- Gaji)")
        print("5. Kembali")
        pilih = input("Pilih: 1-5 ")
        if pilih == '1':
            konfirmasi = input("Anda Yakin Ingin Merubah Data Ini?: (y/n)").upper()
            if konfirmasi == "Y":
                k['nama'] = input(f"Nama Baru ({k['nama']}): ") or k['nama']
                k['posisi'] = input(f"Posisi Baru ({k['posisi']}): ") or k['posisi']
                gaji_input = input(f"Gaji Baru ({k['gaji']}): ")
                if gaji_input:
                    try:
                        k['gaji'] = int(gaji_input)
                    except ValueError:
                        print("❌ Gaji Tidak Valid.")
                        continue
                print("✅ Data Berhasil Diperbarui.")
            else:
                print("Update Data Di Cancel.")
        elif pilih == '2':
            konfirmasi = input(f"Anda Yakin Ingin Menghapus Data Ini (y/n)?").upper()
            if konfirmasi == "Y":
                data_karyawan.remove(k)
                print("✅ Data Karyawan Dihapus.")
            else:
                print("Delete Data Di Cancel")  
            return
        elif pilih == '3':
            nama_proyek = input("Nama Proyek: ")
            peran = input("Peran: ")
            k['proyek'].append({"nama": nama_proyek, "peran": peran})
            print("✅ Data Proyek Berhasil Ditambahkan.")
        elif pilih == '4':
            while True:
                nilai = input("Masukkan nilai kinerja (A-E): ").upper()
                if nilai in ['A','B','C','D','E']:
                    perubahan = nilai_ke_gaji(nilai)
                    break
                else:
                    print("Nilai Tidak Valid! Hanya Dengan Huruf A → E")
            if perubahan is not None:
                gaji_lama = k['gaji']
                k['gaji'] = int(gaji_lama * (1 + perubahan))
                k['nilai_kinerja'] = nilai
                print(f"✅ Gaji diubah dari Rp{gaji_lama:,} → Rp{k['gaji']:,}")
        elif pilih == '5':
            return
        else:
            print("Pilihan tidak valid.")

# Kelola data karyawan
def kelola_karyawan():
    if not data_karyawan:
        print("Belum ada data.")
        return
    print("\n[1] Tampilkan Seluruh Data")
    print("[2] Kelola Data Berdasarkan ID")
    opsi = input("Pilih opsi: ")
    if opsi == '1':
        for k in data_karyawan:
            tampilkan_detail_karyawan(k)
    elif opsi == '2':
        id_ = input("Masukkan ID karyawan: ")
        for k in data_karyawan:
            if str(k['id']) == str(id_):
                tampilkan_detail_karyawan(k)
                submenu_karyawan(k)
                return
        print("❌ Karyawan tidak ditemukan.")
    else:
        print("❌ Pilihan tidak valid.")

# Tambah absensi
def tambah_kehadiran():
    print("\n[Tambah Kehadiran Hari Ini]")
    id_ = input("Masukkan ID Karyawan: ")
    for k in data_karyawan:
        if str(k['id']) == str(id_):
            while True:
                kehadiran = input("Kehadiran Karyawan (Hadir/Tidak): ").title().strip()
                if kehadiran in ["Hadir", "Tidak"]:
                    k['kehadiran'] = kehadiran
                    k['riwayat_kehadiran'].append({
                        "tanggal": datetime.today().strftime("%Y-%m-%d"),
                        "status": kehadiran
                    })
                    print("✅ Kehadiran ditambahkan.")
                    return
                else:
                    print("❌ Validasi hanya dengan kata 'Hadir' atau 'Tidak'.")
    print("❌ Karyawan tidak ditemukan.")

# Cari data
# Menu untuk menampilkan data yang dicari dengan ID atau nama.
def cari_data():
    keyword = input("Masukkan Nama atau ID Yang Ingin Dicari: ").strip().lower()
    hasil = [] # buat variable kosong untuk diisi dengan data yang dicari
    for k in data_karyawan:
        if keyword in str(k['id']).lower() or keyword in k['nama'].lower():
            hasil.append(k)# mencari keyword didalam 'id' dan 'nama' dengan 'in',misal huruf depan doang
    if hasil:
        print(f"\nDitemukan {len(hasil)} data:")
        for k in hasil:#kalau karakter ada kecenderungan dengan nama atau id, maka data utuh ditampilkan
            tampilkan_detail_karyawan(k)
    else:
        print("❌ Data tidak ditemukan.")

# Menu utama
def menu():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Tambah Karyawan")
        print("2. Lihat & Kelola Data Karyawan")
        print("3. Absensi")
        print("4. Cari Data Karyawan")
        print("5. Keluar")
        pilih = input("Pilih (1-5): ")
        if pilih == '1':
            create_karyawan()
        elif pilih == '2':
            kelola_karyawan()
        elif pilih == '3':
            tambah_kehadiran()
        elif pilih == '4':
            cari_data()
        elif pilih == '5':
            print("👋 Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")

# Jalankan menu
menu()

