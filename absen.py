import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# Nama file Excel untuk menyimpan data absensi
EXCEL_FILE = 'data_absensi.xlsx'

# List siswa/i yang akan diabsen
# Anda bisa mengubah atau menambahkan nama siswa di sini
daftar_siswa = [
    "Ani", "Budi", "Citra", "Doni", "Eka", "Fani"
]

def load_data():
    """
    Memuat data absensi dari file Excel.
    Jika file tidak ada, akan membuat DataFrame kosong.
    """
    if os.path.exists(EXCEL_FILE):
        try:
            df = pd.read_excel(EXCEL_FILE, index_col=0)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat file Excel: {e}")
            return pd.DataFrame(index=daftar_siswa)
    else:
        return pd.DataFrame(index=daftar_siswa)

def save_data(df):
    """
    Menyimpan DataFrame ke file Excel.
    """
    try:
        df.to_excel(EXCEL_FILE)
        messagebox.showinfo("Sukses", f"Data absensi berhasil disimpan ke {EXCEL_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan file Excel: {e}")

def update_persentase(df):
    """
    Menghitung dan memperbarui persentase kehadiran setiap siswa.
    """
    df_copy = df.copy()
    
    # Hapus kolom persentase lama jika ada untuk menghindari duplikasi
    if 'Persentase Kehadiran (%)' in df_copy.columns:
        df_copy = df_copy.drop(columns=['Persentase Kehadiran (%)'])
        
    kolom_absensi = [col for col in df_copy.columns if col not in ['Nama Siswa']]
    
    if not kolom_absensi:
        # Jika tidak ada data absensi, persentase semua siswa adalah 0
        df_copy['Persentase Kehadiran (%)'] = 0.0
    else:
        # Hitung jumlah "Hadir" dan total kehadiran
        total_hadir = df_copy[kolom_absensi].apply(lambda row: row.value_counts().get('Hadir', 0), axis=1)
        total_absen = len(kolom_absensi)
        df_copy['Persentase Kehadiran (%)'] = (total_hadir / total_absen * 100).round(2)
        
    return df_copy


class AbsensiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Absensi Siswa")
        self.geometry("800x600")
        
        # Load data absensi yang sudah ada
        self.df_absensi = load_data()
        
        self.setup_ui()

    def setup_ui(self):
        # Frame untuk tombol dan input tanggal
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Tanggal Absensi (DD-MM-YYYY):").pack(side=tk.LEFT, padx=5)
        self.tanggal_entry = ttk.Entry(control_frame)
        self.tanggal_entry.pack(side=tk.LEFT, padx=5)

        absen_button = ttk.Button(control_frame, text="Mulai Absen", command=self.mulai_absen)
        absen_button.pack(side=tk.LEFT, padx=10)
        
        # Tabel absensi dengan Treeview
        columns = ('Nama Siswa', 'Status Kehadiran')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('Nama Siswa', text='Nama Siswa')
        self.tree.heading('Status Kehadiran', text='Status Kehadiran')
        self.tree.column('Nama Siswa', anchor=tk.CENTER, width=200)
        self.tree.column('Status Kehadiran', anchor=tk.CENTER, width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tambahkan data siswa ke Treeview
        for siswa in daftar_siswa:
            self.tree.insert('', 'end', values=(siswa, 'Belum Hadir'))
            
        # Bind double click event
        self.tree.bind('<Double-1>', self.on_item_select)
        
        # Tombol simpan data
        save_button = ttk.Button(self, text="Simpan Data & Hitung Persentase", command=self.simpan_data)
        save_button.pack(pady=10)

    def mulai_absen(self):
        """
        Mulai proses absensi untuk tanggal yang ditentukan.
        """
        self.tanggal = self.tanggal_entry.get()
        if not self.tanggal:
            messagebox.showerror("Error", "Mohon masukkan tanggal absensi.")
            return

        if self.tanggal in self.df_absensi.columns:
            messagebox.showwarning("Peringatan", f"Absensi untuk tanggal {self.tanggal} sudah ada.")
            return

        # Kosongkan status yang ada di Treeview
        for item in self.tree.get_children():
            self.tree.item(item, values=(self.tree.item(item, 'values')[0], 'Belum Hadir'))
            
        # Tambahkan kolom baru untuk tanggal absensi
        self.df_absensi[self.tanggal] = 'Belum Hadir'
        messagebox.showinfo("Info", f"Silakan mulai absensi untuk tanggal {self.tanggal}.")

    def on_item_select(self, event):
        """
        Menampilkan pop-up untuk memilih status kehadiran saat baris diklik.
        """
        if not hasattr(self, 'tanggal') or not self.tanggal:
            messagebox.showerror("Error", "Mulai absensi terlebih dahulu dengan memasukkan tanggal.")
            return
            
        item_id = self.tree.selection()[0]
        siswa_terpilih = self.tree.item(item_id, 'values')[0]
        
        # Buat pop-up window untuk pilihan status
        self.popup_window = tk.Toplevel(self)
        self.popup_window.title(f"Absensi {siswa_terpilih}")
        
        status_frame = ttk.Frame(self.popup_window)
        status_frame.pack(pady=10)
        
        # Tombol-tombol pilihan status dengan warna
        self.status_buttons = {}
        status_options = {
            "Hadir": "green",
            "Sakit": "yellow",
            "Izin": "orange",
            "Alfa": "red",
            "Bolos": "purple"
        }
        
        for status, color in status_options.items():
            btn = ttk.Button(status_frame, text=status,
                             command=lambda s=status, i=item_id, p=self.popup_window: self.update_status(s, i, p))
            btn.pack(side=tk.LEFT, padx=5)
            btn.configure(style=f'{status}.TButton')
            
            # Buat style untuk setiap warna tombol
            style = ttk.Style()
            style.configure(f'{status}.TButton', background=color, foreground='black')

    def update_status(self, status, item_id, popup_window):
        """
        Memperbarui status kehadiran siswa di Treeview dan DataFrame.
        """
        nama_siswa = self.tree.item(item_id, 'values')[0]
        self.tree.item(item_id, values=(nama_siswa, status))
        
        # Update DataFrame pandas
        self.df_absensi.loc[nama_siswa, self.tanggal] = status
        
        # Tutup pop-up window
        popup_window.destroy()

    def simpan_data(self):
        """
        Menyimpan data absensi ke file Excel dan menampilkan persentase.
        """
        if self.df_absensi.empty or len(self.df_absensi.columns) <= 0:
            messagebox.showwarning("Peringatan", "Tidak ada data absensi untuk disimpan.")
            return

        # Hitung persentase kehadiran
        self.df_absensi = update_persentase(self.df_absensi)
        save_data(self.df_absensi)
        
        # Tampilkan DataFrame dengan persentase di konsol
        print("\n--- Data Absensi Lengkap dengan Persentase ---")
        print(self.df_absensi.to_string())
        print("---------------------------------------------")

if __name__ == "__main__":
    app = AbsensiApp()
    app.mainloop()