import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Data jumlah siswa
tahun = [2020, 2021, 2022, 2023, 2024, 2025]
jumlah_siswa = [130, 150, 200, 180, 220, 250]

# Fungsi untuk menampilkan grafik
def tampilkan_grafik(jenis):
    fig, ax = plt.subplots(figsize=(6,4))

    if jenis == "Line":
        ax.plot(tahun, jumlah_siswa, marker='o', color='blue')
        ax.set_title("Line Chart Perkembangan Siswa SMK Hijau Muda")
    elif jenis == "Bar":
        ax.bar(tahun, jumlah_siswa, color='green')
        ax.set_title("Bar Chart Perkembangan Siswa SMK Hijau Muda")
    elif jenis == "Scatter":
        ax.scatter(tahun, jumlah_siswa, color='red', s=100)
        ax.set_title("Scatter Plot Perkembangan Siswa SMK Hijau Muda")
    elif jenis == "Pie":
        ax.pie(jumlah_siswa, labels=tahun, autopct='%1.1f%%',
               startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title("Pie Chart Distribusi Siswa 2020-2025")

    # Hapus grafik lama sebelum mengganti
    for widget in frame_chart.winfo_children():
        widget.destroy()

    # Tampilkan ke Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().pack()

# GUI Tkinter
root = tk.Tk()
root.title("Visualisasi Perkembangan Pelajar")

# Frame untuk tombol
frame_btn = tk.Frame(root)
frame_btn.pack(side=tk.TOP, pady=10)

# Frame untuk chart
frame_chart = tk.Frame(root)
frame_chart.pack(side=tk.BOTTOM)

# Tombol-tombol
tk.Button(frame_btn, text="Line Chart", command=lambda: tampilkan_grafik("Line")).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Bar Chart", command=lambda: tampilkan_grafik("Bar")).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Scatter Plot", command=lambda: tampilkan_grafik("Scatter")).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Pie Chart", command=lambda: tampilkan_grafik("Pie")).pack(side=tk.LEFT, padx=5)

# Default tampil line chart dulu
tampilkan_grafik("Line")

root.mainloop()
