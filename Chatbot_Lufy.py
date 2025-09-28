# chatbot_gui.py
import tkinter as tk
from tkinter import scrolledtext
import json

# Load data latihan
with open("latihan_botlufy.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def chatbot_response(user_input):
    user_input = user_input.lower()
    for item in data:
        if item["tanya"] in user_input:
            return item["jawab"]
    return "Maaf, saya belum mengerti. Bisa ulangi lagi?"

def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "Kamu: " + user_input + "\n")
    response = chatbot_response(user_input)
    chat_window.insert(tk.END, "Chatbot: " + response + "\n\n")
    chat_window.config(state=tk.DISABLED)

    entry.delete(0, tk.END)

# === GUI SETUP ===
root = tk.Tk()
root.title("Chatbot Sederhana")
root.geometry("400x500")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)

send_button = tk.Button(root, text="Kirim", command=send_message)
send_button.pack(pady=5)

root.mainloop()