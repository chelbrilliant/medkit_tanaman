import csv
import os
import pyfiglet
from tabulate import tabulate

# Fungsi untuk signup
def signup():
    print('- Masukkan kode "000" pada inputan apapun untuk keluar dari menu Signup -')
    while True:
        role = input("Masukkan peran (admin/user): ").strip().lower()
        if role == "000":
            return
        if not role:
            print("Role tidak boleh kosong")
            continue
        if role == "admin":
            kode_admin = input("Masukkan kode admin: ").strip()
            if kode_admin == "000":
                return
            if kode_admin != "AdminXMedTan":
                print("Kode admin salah. Anda tidak dapat mendaftar sebagai admin.")
        if role not in ["admin", "user"]:
            print("Peran tidak valid. Masukkan 'admin' atau 'user'.")
            continue
        break

    while True:
        username = input("Masukkan username baru: ").strip()
        if username == "000":
            return
        if not username:
            print("Anda belum mengisi username.")
            continue

        password = input("Masukkan password baru: ").strip()
        if password == "000":
            return
        if not password:
            print("Anda belum mengisi password.")
            continue
        break

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
    print('- Masukkan kode "000" pada inputan apapun untuk keluar dari menu Signup -')
    while True:
        username = input("Masukkan username: ").strip()
        if username == "000":
            return
        if not username:
            print("Anda belum mengisi username")
            continue
        break
    
    while True:
        password = input("Masukkan password: ").strip()
        if password == "000":
            return
        if not password:
            print("Anda belum mengisi password")
            continue
        break

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
def lihat_produk(stok_terkini=None):
    try:
        with open("produk.csv", "r") as file:
            reader = csv.DictReader(file)
            produk = list(reader)

        if not produk:
            print("Belum ada produk yang tersedia.")
            return

        # Header tabel
        header = ["Kode", "Nama", "Harga (Rp)", "Stok Awal", "Sisa Stok", "Manfaat"]

        # Data untuk tabel
        data = []
        for row in produk:
            stok_awal = int(row["Stok"])
            stok_setelah = stok_awal
            if stok_terkini and row["Kode"] in stok_terkini:
                stok_setelah = stok_awal - stok_terkini[row["Kode"]]
            data.append([row["Kode"], row["Nama"], row["Harga"], stok_awal, stok_setelah, row["Manfaat"]])

        # Menampilkan tabel
        print("\n==> DAFTAR PRODUK")
        print(tabulate(data, headers=header, tablefmt="fancy_grid"))
    except FileNotFoundError:
        print("Belum ada produk yang tersedia.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

# Fungsi untuk menambah obat (admin)
def tambah_obat():
    print("\n==> TAMBAH PRODUK")
    print('- Masukkan kode "000" pada inputan apapun untuk keluar dari sub-menu Tambah Produk -')
    
    while True:
        pilihan_tambah = input("\nIngin tambah produk baru atau stok produk yang sudah ada? (baru/stok): ").lower()

        if pilihan_tambah == "000":
            print("Keluar dari menu Tambah Produk")
            return

        if pilihan_tambah != "baru" and pilihan_tambah != "stok" and pilihan_tambah != "000":
            print("Masukkan inputan yang sesuai. Silahkan lakukan input ulang.")
            continue
        break

    if pilihan_tambah == "stok":
        lihat_produk
        try:
            kode_tambah_stok = input("\nMasukkan kode produk: ").strip()
            if kode_tambah_stok == "000":
                print("Keluar dari sub-menu Tambah Stok.")
                return

            jumlah_tambah_stok = int(input("Masukkan jumlah penambahan stok: ").strip())
            if str(jumlah_tambah_stok) == "000":
                print("Keluar dari sub-menu Tambah Stok.")
                return
            if jumlah_tambah_stok == 0:
                print("Jumlah stok produk tidak bertambah.")
                return
            elif jumlah_tambah_stok < 0:
                print("Jumlah stok harus bernilai positif.")
                return
            
            produk_diperbarui = []
            stok_ditemukan = False

            with open("produk.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Kode"] == kode_tambah_stok:
                        stok_awal = int(row["Stok"])
                        stok_baru = stok_awal + jumlah_tambah_stok
                        row["Stok"] = stok_baru  # Perbarui stok
                        stok_ditemukan = True
                    produk_diperbarui.append(row)

            if not stok_ditemukan:
                print("Kode produk tidak ditemukan.")
                return

            # Menulis kembali data produk dengan stok yang diperbarui
            with open("produk.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                writer.writeheader()
                writer.writerows(produk_diperbarui)

                print(f"Stok untuk produk dengan kode '{kode_tambah_stok}' berhasil ditambahkan!")
        except FileNotFoundError:
            print("File produk.csv tidak ditemukan.")
        except ValueError:
            print("Jumlah stok harus berupa angka positif.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
        return

    if pilihan_tambah == "baru":
    # Validasi input kode
        while True:
            kode = input("\nMasukkan kode produk: ").strip()
            if kode == "000":
                print("Keluar dari sub-menu Tambah Produk.")
                return
            if not kode:
                print("Anda belum memasukkan kode produk yang baru")
                continue
            break

        # Cek apakah kode obat sudah ada
        try:
            with open("produk.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Kode"] == kode:
                        print("Kode produk sudah ada. Gunakan kode lain.")
                        return
        except FileNotFoundError:
            pass

        nama = input("Masukkan nama produk: ").strip()
        if nama == "000":
            print("Keluar dari sub-menu Tambah Produk.")
            return

        # Validasi input harga
        while True:
            try:
                print('*Cukup inputkan nominal harga "0" jika ingin menambah produk bernilai gratis*')
                harga = float(input("Masukkan harga produk: ").strip())
                if str(harga) == "000":
                    print("Keluar dari sub-menu Tambah Produk.")
                    return
                if harga < 0:
                    print("Nominal harga harus bernilai positif.")
                    continue
            except ValueError:
                print("Harga harus bernilai angka. Silahkan ulangi dan masukkan nilai yang sesuai.")
                continue
            break

        # Validasi input stok
        while True:
            try:
                print('*Cukup inputkan jumlah stok "0" jika stok produk baru belum tersedia*')
                stok = int(input("Masukkan stok produk: ").strip())
                if str(stok) == "000":
                    print("Keluar dari sub-menu Tambah Produk.")
                    return
                if stok < 0:
                    print("Stok tidak boleh kurang dari nol.")
                    continue
            except ValueError:
                print("Stok harus bernilai angka bulat. Silahkan ulangi dan masukkan nilai yang sesuai.")
                continue
            break

        manfaat = input("Masukkan manfaat produk: ").strip()

        if manfaat == "000":
            print("Keluar dari sub-menu Tambah Produk.")
            return

        try:
            # Menambahkan obat ke file produk.csv
            with open("produk.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                if file.tell() == 0:  # Menambahkan header jika file kosong
                    writer.writeheader()
                writer.writerow({
                    "Kode": kode,
                    "Nama": nama,
                    "Harga": harga,
                    "Stok": stok,
                    "Manfaat": manfaat
                })
                print("\nProduk berhasil ditambahkan!")
        except Exception as e:
            print(f"\nTerjadi kesalahan: {e}")

# Fungsi untuk menghapus obat (admin)
def hapus_obat():
    print("\n==> HAPUS PRODUK")
    print('- Masukkan kode "000" pada inputan apapun untuk keluar dari sub-menu Hapus Produk -')

    while True:
        pilihan_kurang = input("\nIngin hapus produk atau kurangi stok produk yang sudah ada? (hapus/stok): ").lower()

        if pilihan_kurang == "000":
            print("Kleuar dari menu Hapus Obat")
            return
        if pilihan_kurang != "hapus" and pilihan_kurang != "stok" and pilihan_kurang != "000":
            print("Masukkan inputan yang sesuai. Silahkan lakukan input ulang.")
            continue
        break

    if pilihan_kurang == "stok":
        lihat_produk
        try:
            kode_kurang_stok = input("\nMasukkan kode produk: ").strip()
            if kode_kurang_stok == "000":
                print("Keluar dari sub-menu Kurang Stok.")
                return
            jumlah_kurang_stok = int(input("Masukkan jumlah pengurangan stok: ").strip())
            if str(jumlah_kurang_stok) == "000":
                print("Keluar dari sub-menu Kurang Stok.")
                return
            if jumlah_kurang_stok == 0:
                print("Jumlah stok produk tidak bertambah.")
                return
            elif jumlah_kurang_stok < 0:
                print("Jumlah pengurangan stok akan otomatis bernilai negatif,\
                      masukkan dalam jumlah nilai positif dahulu.")
                return
            
            produk_diperbarui = []
            stok_ditemukan = False

            with open("produk.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Kode"] == kode_kurang_stok:
                        stok_awal = int(row["Stok"])
                        stok_baru = stok_awal - jumlah_kurang_stok
                        if stok_baru < 0:
                            stok_baru = 0
                        row["Stok"] = stok_baru  # Perbarui stok
                        stok_ditemukan = True
                    produk_diperbarui.append(row)

            if not stok_ditemukan:
                print("Kode produk tidak ditemukan.")
                return

            # Menulis kembali data produk dengan stok yang diperbarui
            with open("produk.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                writer.writeheader()
                writer.writerows(produk_diperbarui)

                print(f"Stok untuk produk dengan kode '{kode_kurang_stok}' berhasil dikurangi!")
        except FileNotFoundError:
            print("File produk.csv tidak ditemukan.")
        except ValueError:
            print("Jumlah stok harus berupa angka positif,\
                  karena pengurangan stok akan otomatis bernilai negatif.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
        return

    if pilihan_kurang == "hapus":
        try:
            with open("produk.csv", "r") as file:
                reader = csv.DictReader(file)
                produk = list(reader)

            kode = input("\nMasukkan kode produk yang ingin dihapus: ").strip()

            if kode == "000":
                print("Keluar dari menu Hapus Produk.")
                return

            produk_baru = [p for p in produk if p["Kode"] != kode]

            if len(produk_baru) < len(produk):
                with open("produk.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                    writer.writeheader()
                    writer.writerows(produk_baru)
                print(f"Produk dengan kode '{kode}' berhasil dihapus.")
            else:
                print(f"Produk dengan kode '{kode}' tidak ditemukan.")
        except FileNotFoundError:
            print("Database produk belum tersedia.")
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

# Fungsi untuk transaksi pembelian obat (user)
def transaksi(username):
    daftar_pembelian = []  # Untuk menampung item belanja sementara
    stok_terkini = {}  # Menyimpan stok yang diperbarui sementara
    lihat_produk(stok_terkini)

    while True:
        print("\n1. Tambah daftar pembelian")
        print("2. Cek daftar pembelian")
        print("3. Hapus item daftar pembelian")
        print("4. Konfirmasi pembayaran")
        print("5. Batalkan transaksi")
        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "1":
            print("\n==> TAMBAH DAFTAR PEMBELIAN")
            while True:
                lihat_produk(stok_terkini)
                print('- Masukkan kode "000" pada inputan apapun untuk keluar dari sub-menu Tambah Daftar Pembelian -')
                kode = input("\nMasukkan kode produk yang ingin dibeli: ").strip()
                if kode == "000":
                    print("Keluar dari sub-menu Tambah Daftar Pembelian.")
                    break  # Keluar dari submenu ini, tapi tetap di fungsi `transaksi`
                if not kode:
                    print("Kode tidak boleh kosong.")
                    continue

                jumlah = input("Masukkan jumlah yang dibeli: ").strip()
                if jumlah == "000":
                    print("Keluar dari sub-menu Tambah Daftar Pembelian.")
                    break  # Keluar dari submenu ini
                try:
                    jumlah = int(jumlah)
                    if jumlah <= 0:
                        print("Perlu memesan minimal 1 item produk untuk melanjutkan pembelian.")
                        continue
                except ValueError:
                    print("Jumlah harus berupa angka positif.")
                    continue

                try:
                    # Membaca file produk
                    with open("produk.csv", "r") as file:
                        reader = csv.DictReader(file)
                        produk = list(reader)

                    for item in produk:
                        if item["Kode"] == kode:
                            stok_awal = float(item["Stok"])
                            stok_terkini_kode = stok_terkini.get(kode, 0)
                            stok_sisa = stok_awal - stok_terkini_kode

                            if stok_sisa >= jumlah:
                                # Perbarui stok terkini
                                stok_terkini[kode] = stok_terkini_kode + jumlah
                                # Tambahkan ke daftar pembelian
                                daftar_pembelian.append({
                                    "Kode": kode,
                                    "Nama": item["Nama"],
                                    "Harga": float(item["Harga"]),
                                    "Jumlah": jumlah,
                                    "Subtotal": float(item["Harga"]) * jumlah,
                                    "Manfaat": item["Manfaat"]
                                })
                                print(f"{item['Nama']} sebanyak {jumlah} berhasil ditambahkan ke daftar pembelian.")
                            else:
                                print("Stok tidak mencukupi.")
                            break
                    else:
                        print("Kode obat tidak ditemukan.")
                except FileNotFoundError:
                    print("Database obat belum tersedia.")
                except Exception as e:
                    print(f"Terjadi kesalahan: {e}")

        elif pilihan == "2":
            # Lihat daftar pembelian
            print("\n==> CEK DAFTAR PEMBELIAN")
            if daftar_pembelian:
                # Header tabel
                header = ["No", "Nama", "Harga (Rp)", "Jumlah", "Subtotal (Rp)"]
                # Data tabel dengan nomor urut
                data = [
                    [i + 1, item["Nama"], item["Harga"], item["Jumlah"], item["Subtotal"]]
                    for i, item in enumerate(daftar_pembelian)
                ]
                # Menampilkan tabel daftar pembelian
                print(tabulate(data, headers=header, tablefmt="fancy_grid"))
            else:
                print("Daftar pembelian masih kosong.")

        elif pilihan == "3":
            # Hapus item dari daftar pembelian
            while True:
                print("\n==> HAPUS ITEM DAFTAR PEMBELIAN")
                if daftar_pembelian:
                    # Header tabel
                    header = ["No", "Nama", "Harga (Rp)", "Jumlah", "Subtotal (Rp)", "Manfaat"]
                    # Data tabel dengan nomor urut
                    data = [
                        [i + 1, item["Nama"], item["Harga"], item["Jumlah"], item["Subtotal"], item.get("Manfaat", "")]
                        for i, item in enumerate(daftar_pembelian)
                    ]
                    # Menampilkan tabel daftar pembelian
                    print(tabulate(data, headers=header, tablefmt="fancy_grid"))
                    print('- Masukkan kode "000" pada inputan apapun untuk keluar dari sub-menu Hapus Item Daftar Pembelian -\n')

                    input_hapus = input("Masukkan nomor item yang ingin dihapus: ").strip()

                    if input_hapus == "000":
                        print("Keluar dari menu Hapus Item Daftar Pembelian.")
                        break

                    try:
                        hapus_daftar_pembelian = int(input_hapus) - 1
                        if 0 <= hapus_daftar_pembelian < len(daftar_pembelian):
                            item_dihapus = daftar_pembelian.pop(hapus_daftar_pembelian)
                            stok_terkini[item_dihapus["Kode"]] -= item_dihapus["Jumlah"]
                            print(f"{item_dihapus['Nama']} berhasil dihapus dari daftar pembelian.")
                        else:
                            print("Nomor item tidak valid. Pilih nomor dari daftar.")
                    except ValueError:
                        print("Masukkan nomor yang valid.")
                else:
                    print("Daftar pembelian masih kosong.")
                    break

        elif pilihan == "4":
            # Lanjut ke pembayaran
            if not daftar_pembelian:
                print("Daftar pembelian masih kosong. Tambahkan produk terlebih dahulu.")
                continue

            print("\n==> KONFIRMASI PEMBAYARAN")
            total_belanja = sum(item["Subtotal"] for item in daftar_pembelian)
            print(f"Total yang harus dibayar: Rp{total_belanja}")

            while True:
                try:
                    uang_dibayar = int(input("Masukkan jumlah uang yang dibayarkan: Rp").strip())
                    if uang_dibayar < total_belanja:
                        print("Uang yang dibayarkan tidak cukup.")
                        continue
                    break
                except ValueError:
                    print("Masukkan jumlah uang dalam angka.")

            kembalian = uang_dibayar - total_belanja
            print(f"\nPembayaran berhasil. Kembalian: Rp{kembalian}")

            try:
                # Perbarui stok di file produk.csv
                with open("produk.csv", "r") as file:
                    reader = csv.DictReader(file)
                    produk = list(reader)

                with open("produk.csv", "w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["Kode", "Nama", "Harga", "Stok", "Manfaat"])
                    writer.writeheader()
                    for item in produk:
                        if item["Kode"] in stok_terkini:
                            item["Stok"] = int(item["Stok"]) - stok_terkini[item["Kode"]]
                        writer.writerow(item)

                print("Stok produk berhasil diperbarui.")

                # Catat transaksi ke transaksi.csv
                with open("transaksi.csv", "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=["Username", "Kode", "Nama", "Jumlah", "Total", "Pembayaran", "Kembalian"])
                    if file.tell() == 0:
                        writer.writeheader()
                    for item in daftar_pembelian:
                        writer.writerow({
                            "Username": username,
                            "Kode": item["Kode"],
                            "Nama": item["Nama"],
                            "Jumlah": item["Jumlah"],
                            "Total": item["Subtotal"],
                            "Pembayaran": uang_dibayar,
                            "Kembalian": kembalian
                        })

                print("Transaksi berhasil disimpan.")
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
            return

        elif pilihan == "5":
            print("Transaksi dibatalkan.")
            return
        else:
            print("Pilihan tidak valid. Coba lagi.")

# Fungsi untuk melihat history transaksi (admin)
def lihat_riwayat():
    try:
        with open("transaksi.csv", "r") as file:
            reader = csv.DictReader(file)
            print("\n==> RIWAYAT TRANSAKSI")
            for row in reader:
                print(f"Username: {row['Username']}, Obat: {row['Nama']}, Jumlah: {row['Jumlah']}, Total: Rp{row['Total']}")
    except FileNotFoundError:
        print("Belum ada transaksi yang tercatat.")

# Menu untuk admin
def menu_admin():
    while True:
        print("\n>>> MENU ADMIN")
        print("\n1. Lihat Produk")
        print("2. Tambah Produk")
        print("3. Hapus Produk")
        print("4. Lihat History Transaksi")
        print("5. Logout")
        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            tambah_obat()
        elif pilihan == "3":
            hapus_obat()
        elif pilihan == "4":
            lihat_riwayat()
        elif pilihan == "5":
            print("\nLogout berhasil!")
            break
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

# Menu untuk user
def menu_user(username):
    while True:
        print("\n>>> MENU USER")
        print("\n1. Lihat Produk")
        print("2. Transaksi")
        print("3. Logout")
        pilihan = input("\nPilih menu: ").strip()

        if pilihan == "1":
            lihat_produk()
        elif pilihan == "2":
            transaksi(username)
        elif pilihan == "3":
            print("\nLogout berhasil!")
            break
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

# Menu utama
def menu_utama():
    while True:
        # Membuat judul menggunakan pyfiglet
        judul = pyfiglet.figlet_format("   MEDKIT", font="blocky")
        judul2 = pyfiglet.figlet_format("TANAMAN", font="blocky")

        # Mencetak judul dan subjudul dengan center
        print("\n" + judul.center(70))
        print(judul2.center(70))
        print("=" * 70)
        print("-Solusi Kesehatan untuk Tanaman Anda-".center(70))
        print("=" * 70 + "\n")

        # Mencetak menu utama dengan teks terpusat
        print("+" * 29 + " MENU UTAMA " + "+" * 29 + "\n")
        print("1. Login".center(68))
        print("2. Signup".center(70))
        print("3. Keluar\n".center(70))

        # Meminta input pilihan menu dari pengguna
        pilihan = input("Pilih menu: ".center(70)).strip()
        print("")

        if pilihan == "1":
            login()
        elif pilihan == "2":
            signup()
        elif pilihan == "3":
            print("\nTerima kasih telah mengunjungi MEDKIT TANAMAN!")
            break
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

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
