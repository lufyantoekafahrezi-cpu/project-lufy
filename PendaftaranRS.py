import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# === SETUP WINDOW ===
root = tk.Tk()
root.title("Pendaftaran Pasien")
root.geometry("800x550")

# === FORM ENTRY ===
fields = ['Nama', 'Umur', 'Jenis Kelamin', 'Alamat', 'Keluhan']
entries = {}

for i, field in enumerate(fields):
    lbl = tk.Label(root, text=field)
    lbl.grid(row=i, column=0, padx=10, pady=5, sticky='w')
    
    if field == 'Jenis Kelamin':
        cb = ttk.Combobox(root, values=['Laki-laki', 'Perempuan'], width=37)
        cb.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = cb
    else:
        ent = tk.Entry(root, width=40)
        ent.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = ent

# === TABEL PASIEN ===
tree = ttk.Treeview(root, columns=fields, show='headings')
for col in fields:
    tree.heading(col, text=col)
    tree.column(col, width=130)
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# === PENYIMPANAN DATA ===
data_pasien = []

# === FUNGSI ===
def tambah_data():
    data = [entries[f].get() for f in fields]
    if '' in data:
        messagebox.showwarning("Peringatan", "Semua data harus diisi!")
        return
    tree.insert('', 'end', values=data)
    data_pasien.append(data)
    for f in fields:
        entries[f].delete(0, tk.END)

def export_excel():
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])
    if not file_path:
        return
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(fields)
    for row in data_pasien:
        ws.append(row)
    wb.save(file_path)
    messagebox.showinfo("Sukses", f"Data berhasil disimpan ke Excel:\n{file_path}")

def export_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return
    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    style = getSampleStyleSheet()
    elements = [Paragraph("Data Pendaftaran Pasien", style['Title']), Paragraph(" ")]
    
    table_data = [fields] + data_pasien
    t = Table(table_data, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(t)
    pdf.build(elements)
    messagebox.showinfo("Sukses", f"Data berhasil disimpan ke PDF:\n{file_path}")

# === BUTTONS ===
btn_tambah = tk.Button(root, text="Tambah", command=tambah_data, width=20)
btn_tambah.grid(row=5, column=0, padx=10, pady=10)

btn_excel = tk.Button(root, text="Export ke Excel", command=export_excel, width=20)
btn_excel.grid(row=5, column=1, padx=10, pady=10)

btn_pdf = tk.Button(root, text="Export ke PDF", command=export_pdf, width=20)
btn_pdf.grid(row=5, column=2, padx=10, pady=10)

root.mainloop()

