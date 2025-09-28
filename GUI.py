"""
simple_store_gui.py
Sistem penjualan online sederhana (GUI dengan Tkinter)
Fitur:
- Menampilkan produk
- Menambahkan produk ke keranjang
- Menghapus produk dari keranjang
- Melihat ringkasan keranjang
- Checkout: menyimpan order ke file JSON
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json, uuid
from datetime import datetime

# Data produk
PRODUCTS = [
    {"id": "P001", "name": "CHROME BOOK i3 gen 10", "price": 4500000, "stock": 90},
    {"id": "P002", "name": "CHROME BOOK i5 gen 8", "price": 5000000, "stock": 43},
    {"id": "P003", "name": "CHROME BOOK i7 gen 10", "price": 7000000, "stock": 65},
    {"id": "P004", "name": "CHROME BOOK i9 gen 8", "price": 7500000, "stock": 33},
]

ORDERS_FILE = "orders.json"
cart = {}  # pid -> qty


def load_orders():
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)


def find_product(pid):
    for p in PRODUCTS:
        if p['id'] == pid:
            return p
    return None


def refresh_products():
    for row in tree_products.get_children():
        tree_products.delete(row)
    for p in PRODUCTS:
        tree_products.insert("", tk.END, values=(p['id'], p['name'], f"Rp{p['price']:,}", p['stock']))


def refresh_cart():
    for row in tree_cart.get_children():
        tree_cart.delete(row)
    total = 0
    for pid, qty in cart.items():
        p = find_product(pid)
        subtotal = p['price'] * qty
        total += subtotal
        tree_cart.insert("", tk.END, values=(pid, p['name'], qty, f"Rp{subtotal:,}"))
    lbl_total.config(text=f"Total: Rp{total:,}")


def add_to_cart():
    try:
        selected = tree_products.selection()[0]
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih produk dulu!")
        return

    pid = tree_products.item(selected, "values")[0]
    p = find_product(pid)
    if not p:
        return

    try:
        qty = int(entry_qty.get())
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka > 0")
        return

    in_cart = cart.get(pid, 0)
    if qty + in_cart > p['stock']:
        messagebox.showerror("Error", f"Stok tidak cukup. Sisa stok: {p['stock'] - in_cart}")
        return

    cart[pid] = in_cart + qty
    refresh_cart()
    messagebox.showinfo("Sukses", f"Berhasil menambahkan {qty} x {p['name']} ke keranjang.")


def remove_from_cart():
    try:
        selected = tree_cart.selection()[0]
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih item di keranjang!")
        return
    pid = tree_cart.item(selected, "values")[0]
    if pid in cart:
        del cart[pid]
        refresh_cart()
        messagebox.showinfo("Info", "Item dihapus dari keranjang.")


def checkout():
    if not cart:
        messagebox.showwarning("Peringatan", "Keranjang masih kosong.")
        return

    name = entry_name.get().strip()
    address = entry_address.get().strip()
    phone = entry_phone.get().strip()
    if not (name and address and phone):
        messagebox.showerror("Error", "Lengkapi data pembeli!")
        return

    items = []
    total = 0
    for pid, qty in cart.items():
        p = find_product(pid)
        subtotal = p['price'] * qty
        items.append({
            "id": pid, "name": p['name'], "price": p['price'],
            "qty": qty, "subtotal": subtotal
        })
        total += subtotal
        # kurangi stok
        p['stock'] -= qty

    order = {
        "order_id": str(uuid.uuid4()),
        "date": datetime.now().isoformat(),
        "buyer": {"name": name, "address": address, "phone": phone},
        "items": items,
        "total": total
    }

    save_order(order)
    cart.clear()
    refresh_cart()
    refresh_products()
    messagebox.showinfo("Sukses", f"Checkout berhasil!\nOrder ID: {order['order_id']}\nTotal: Rp{total:,}")


# === GUI ===
root = tk.Tk()
root.title("SimpleStore GUI")

# Frame Produk
frame_products = ttk.LabelFrame(root, text="Daftar Produk")
frame_products.pack(fill="both", padx=10, pady=5)

cols = ("ID", "Nama", "Harga", "Stok")
tree_products = ttk.Treeview(frame_products, columns=cols, show="headings", height=5)
for c in cols:
    tree_products.heading(c, text=c)
tree_products.pack(side="left", fill="both", expand=True)
scroll_products = ttk.Scrollbar(frame_products, orient="vertical", command=tree_products.yview)
tree_products.configure(yscroll=scroll_products.set)
scroll_products.pack(side="right", fill="y")

refresh_products()

# Input qty + tombol tambah
frame_action = tk.Frame(root)
frame_action.pack(pady=5)
tk.Label(frame_action, text="Jumlah:").pack(side="left")
entry_qty = tk.Entry(frame_action, width=5)
entry_qty.pack(side="left", padx=5)
btn_add = tk.Button(frame_action, text="Tambah ke Keranjang", command=add_to_cart)
btn_add.pack(side="left")

# Frame Keranjang
frame_cart = ttk.LabelFrame(root, text="Keranjang Belanja")
frame_cart.pack(fill="both", padx=10, pady=5)

cols_cart = ("ID", "Nama", "Qty", "Subtotal")
tree_cart = ttk.Treeview(frame_cart, columns=cols_cart, show="headings", height=5)
for c in cols_cart:
    tree_cart.heading(c, text=c)
tree_cart.pack(side="left", fill="both", expand=True)
scroll_cart = ttk.Scrollbar(frame_cart, orient="vertical", command=tree_cart.yview)
tree_cart.configure(yscroll=scroll_cart.set)
scroll_cart.pack(side="right", fill="y")

btn_remove = tk.Button(root, text="Hapus dari Keranjang", command=remove_from_cart)
btn_remove.pack(pady=5)

lbl_total = tk.Label(root, text="Total: Rp0", font=("Arial", 12, "bold"))
lbl_total.pack()

# Frame Checkout
frame_checkout = ttk.LabelFrame(root, text="Data Pembeli")
frame_checkout.pack(fill="x", padx=10, pady=5)
tk.Label(frame_checkout, text="Nama:").grid(row=0, column=0, sticky="e")
tk.Label(frame_checkout, text="Alamat:").grid(row=1, column=0, sticky="e")
tk.Label(frame_checkout, text="No. HP:").grid(row=2, column=0, sticky="e")

entry_name = tk.Entry(frame_checkout, width=40)
entry_address = tk.Entry(frame_checkout, width=40)
entry_phone = tk.Entry(frame_checkout, width=40)
entry_name.grid(row=0, column=1, pady=2)
entry_address.grid(row=1, column=1, pady=2)
entry_phone.grid(row=2, column=1, pady=2)

btn_checkout = tk.Button(root, text="Checkout", command=checkout, bg="green", fg="white")
btn_checkout.pack(pady=10)

root.mainloop()
