import csv
import os

# Fungsi untuk signup
def signup():
    username = input("Masukkan username baru: ").strip()
    password = input("Masukkan password baru: ").strip()
    role = input("Masukkan peran (admin/user): ").strip().lower()

    if role not in ["admin", "user"]:
        print("Peran tidak valid. Masukkan 'admin' atau 'user'.")
        return

    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username:
                    print("Username sudah ada. Coba lagi.")
                    return
    except FileNotFoundError:
        pass

    with open("users.csv", "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Username", "Password", "Role"])
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({"Username": username, "Password": password, "Role": role})
        print("Signup berhasil! Silakan login.")

# Fungsi untuk login
def login():
    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()

    try:
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    print(f"Login berhasil sebagai {row['Role']}!")
                    if row["Role"] == "admin":
                        menu_admin()
                    elif row["Role"] == "user":
                        menu_user(username)
                    return
        print("Username atau password salah.")
    except FileNotFoundError:
        print("Belum ada pengguna terdaftar. Silakan signup terlebih dahulu.")

# Fungsi untuk melihat produk
def lihat_produk():
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            print("\n=== Daftar Produk ===")
            for row in reader:
                print(f"{row['Kode']} - {row['Nama']} - Rp{row['Harga']} - Stok: {row['Stok']} - Manfaat: {row['Manfaat']}")
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")

# Fungsi untuk menambah obat (admin)
def tambah_obat():
    kode = input("Masukkan kode obat: ").strip()

    # Cek apakah kode obat sudah ada
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Kode"] == kode:
                    print("Kode obat sudah ada. Gunakan kode lain.")
                    return
    except FileNotFoundError:
        pass

    nama = input("Masukkan nama obat: ").strip()
    harga = input("Masukkan harga obat: ").strip()
    stok = input("Masukkan stok obat: ").strip()
    manfaat = input("Masukkan manfaat obat: ").strip()

    try:
        with open("produk.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({"Kode": kode, "Nama": nama, "Harga": harga, "Stok": stok, "Manfaat": manfaat})
            print("Obat berhasil ditambahkan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


# Fungsi untuk menghapus obat (admin)
def hapus_obat():
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            produk = list(reader)

        kode = input("Masukkan kode obat yang ingin dihapus: ").strip()
        produk_baru = [p for p in produk if p["Kode"] != kode]

        if len(produk_baru) < len(produk):
            with open("produk.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                writer.writeheader()
                writer.writerows(produk_baru)
            print(f"Obat dengan kode '{kode}' berhasil dihapus.")
        else:
            print(f"Obat dengan kode '{kode}' tidak ditemukan.")
    except FileNotFoundError:
        print("Database obat belum tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Fungsi untuk transaksi pembelian obat (user)
def transaksi(username):
    lihat_produk()
    kode = input("Masukkan kode obat yang dibeli: ").strip()
    jumlah = int(input("Masukkan jumlah yang dibeli: ").strip())

    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            produk = list(reader) 

        for item in produk:
            if item["Kode"] == kode:
                if int(item["Stok"]) >= jumlah:
                    total_harga = int(item["Harga"]) * jumlah
                    item["Stok"] = str(int(item["Stok"]) - jumlah)
                    print(f"Total harga: Rp{total_harga}")

                    # Meminta pengguna untuk memasukkan jumlah uang yang dibayarkan
                    uang_dibayar = int(input("Masukkan jumlah uang yang dibayarkan: Rp").strip())

                    if uang_dibayar < total_harga:
                        print("Uang yang dibayarkan tidak cukup.")
                        return
                    else:
                        kembalian = uang_dibayar - total_harga
                        print(f"Kembalian: Rp{kembalian}")

                    # Update stok
                    with open("produk.csv", "w", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                        writer.writeheader()
                        writer.writerows(produk)

                    # Catat transaksi
                    with open("transaksi.csv", "a", newline="") as file:
                        writer = csv.DictWriter(file, fieldnames=["Username", "Kode", "Nama", "Jumlah", "Total", "Pembayaran", "Kembalian"])
                        if file.tell() == 0:
                            writer.writeheader()
                        writer.writerow({
                            "Username": username,
                            "Kode": kode,
                            "Nama": item["Nama"],
                            "Jumlah": jumlah,
                            "Total": total_harga,
                            "Pembayaran": uang_dibayar,
                            "Kembalian": kembalian
                        })
                    print("Transaksi berhasil!")
                    return
                else:
                    print("Stok tidak mencukupi.")
                    return
        print("Obat tidak ditemukan.")
    except FileNotFoundError:
        print("Database obat belum tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


# Fungsi untuk melihat history transaksi (admin)
def lihat_history():
    try:
        with open("transaksi.csv", "r") as file:
            reader = csv.DictReader(file)
            print("\n=== History Transaksi ===")
            for row in reader:
                print(f"Username: {row['Username']}, Obat: {row['Nama']}, Jumlah: {row['Jumlah']}, Total: Rp{row['Total']}")
    except FileNotFoundError:
        print("Belum ada transaksi yang tercatat.")

# Menu untuk admin
def menu_admin():
    while True:
        print("\n=== Menu Admin ===")
        print("1. Lihat Produk")
        print("2. Tambah Obat")
        print("3. Hapus Obat")
        print("4. Lihat History Transaksi")
        print("5. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            tambah_obat()
        elif pilihan == "3":
            hapus_obat()
        elif pilihan == "4":
            lihat_history()
        elif pilihan == "5":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menu untuk user
def menu_user(username):
    while True:
        print("\n=== Menu User ===")
        print("1. Lihat Produk")
        print("2. Transaksi")
        print("3. Logout")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            transaksi(username)
        elif pilihan == "3":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Menu utama
def menu_utama():
    while True:
        print("\n===================================")
        print("        MEDKIT TANAMAN")
        print("Solusi Kesehatan untuk Tanaman Anda")
        print("===================================\n")
        print("=== Menu Utama ===")
        print("1. Login")
        print("2. Signup")
        print("3. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            login()
        elif pilihan == "2":
            signup()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan MEDKIT TANAMAN!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")


# Membuat file CSV jika belum ada
def buat_file_csv():
    # Cek dan buat file users.csv
    if not os.path.exists("users.csv"):
        with open("users.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Username", "Password", "Role"])
            writer.writeheader()
        print("File users.csv berhasil dibuat.")

    # Cek dan buat file produk.csv
    if not os.path.exists("produk.csv"):
        with open("produk.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
            writer.writeheader()
        print("File produk.csv berhasil dibuat.")

    # Cek dan buat file transaksi.csv
    if not os.path.exists("transaksi.csv"):
        with open("transaksi.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Username", "Kode", "Nama", "Jumlah", "Total"])
            writer.writeheader()
        print("File transaksi.csv berhasil dibuat.")


# Menjalankan aplikasi
buat_file_csv() # Memastikan file CSV tersedia
menu_utama()