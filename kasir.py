# #PELATIHAN PYTHON ELGIZER DAY 2 13-09-2025
# import datetime

# # List untuk menyimpan item belanja
# items = []

# # Fungsi untuk menambahkan item
# def tambah_item():
#     nama = input("Nama barang: ")
#     harga = float(input("Harga satuan (Rp): "))
#     jumlah = int(input("Jumlah: "))
#     total = harga * jumlah
#     items.append({"nama": nama, "harga": harga, "jumlah": jumlah, "total": total})

# # Fungsi untuk menampilkan struk
# def tampilkan_struk():
#     print("\n=== STRUK PEMBELIAN ===")
#     print("Tanggal:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     print("----------------------------")
#     total_bayar = 0
#     for item in items:
#         print(f"{item['nama']} x{item['jumlah']} = Rp{item['total']:.2f}")
#         total_bayar += item['total']
#     print("----------------------------")
#     print(f"Total Bayar: Rp{total_bayar:.2f}")
#     print("============================\n")

# # Main program
# while True:
#     print("=== MENU KASIR ===")
#     print("1. Tambah Barang")
#     print("2. Tampilkan Struk & Keluar")
#     pilihan = input("Pilih menu (1/2): ")

#     if pilihan == "1":
#         tambah_item()
#     elif pilihan == "2":
#         tampilkan_struk()
#         break
#     else:
#         print("Pilihan tidak valid. Coba lagi.")

# KASIR DENGAN GUI (GRAPHICAL USER INTERFACE)

# import tkinter as tk
# from tkinter import messagebox

# items = []

# def tambah_item():
#     nama = entry_nama.get()
#     try:
#         harga = float(entry_harga.get())
#         jumlah = int(entry_jumlah.get())
#     except ValueError:
#         messagebox.showerror("Input Error", "Harga dan jumlah harus angka.")
#         return

#     total = harga * jumlah
#     items.append((nama, harga, jumlah, total))
    
#     listbox.insert(tk.END, f"{nama} x{jumlah} = Rp{total:,.2f}")
#     entry_nama.delete(0, tk.END)
#     entry_harga.delete(0, tk.END)
#     entry_jumlah.delete(0, tk.END)

# def tampilkan_struk():
#     total_bayar = sum([item[3] for item in items])
#     struk_text.delete("1.0", tk.END)
#     struk_text.insert(tk.END, "======= STRUK PEMBELIAN =======\n")
#     for item in items:
#         struk_text.insert(tk.END, f"{item[0]} x{item[2]} = Rp{item[3]:,.2f}\n")
#     struk_text.insert(tk.END, "------------------------------\n")
#     struk_text.insert(tk.END, f"Total Bayar: Rp{total_bayar:,.2f}\n")
#     struk_text.insert(tk.END, "==============================\n")

# def clear_semua():
#     items.clear()
#     listbox.delete(0, tk.END)
#     struk_text.delete("1.0", tk.END)
#     entry_nama.delete(0, tk.END)
#     entry_harga.delete(0, tk.END)
#     entry_jumlah.delete(0, tk.END)
#     messagebox.showinfo("Reset", "Semua data berhasil dihapus.")

# # Setup GUI
# root = tk.Tk()
# root.title("Program Kasir Sederhana")

# # Input Form
# tk.Label(root, text="Nama Barang").grid(row=0, column=0)
# tk.Label(root, text="Harga").grid(row=1, column=0)
# tk.Label(root, text="Jumlah").grid(row=2, column=0)

# entry_nama = tk.Entry(root)
# entry_nama.grid(row=0, column=1)

# entry_harga = tk.Entry(root)
# entry_harga.grid(row=1, column=1)

# entry_jumlah = tk.Entry(root)
# entry_jumlah.grid(row=2, column=1)

# tk.Button(root, text="Tambah", command=tambah_item).grid(row=3, column=0, columnspan=2, pady=5)

# # Listbox dan tombol struk
# listbox = tk.Listbox(root, width=40)
# listbox.grid(row=4, column=0, columnspan=2)

# tk.Button(root, text="Tampilkan Struk", command=tampilkan_struk).grid(row=5, column=0, pady=5)
# tk.Button(root, text="Clear", command=clear_semua).grid(row=5, column=1, pady=5)

# # Area Struk
# struk_text = tk.Text(root, height=10, width=40)
# struk_text.grid(row=6, column=0, columnspan=2, pady=5)

# root.mainloop()
