import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import cv2
import pytesseract
import json

# Import classes from ocrMain.py
from ocrMain import ImageProcessor, OCRProcessor, DataExtractor, JSONFormatter, PostgresDB

# Konfigurasi database PostgreSQL
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""
DB_HOST = ""
DB_PORT = ""

# Global variable to store extracted data
extracted_data = None

# Fungsi untuk memilih file gambar
def select_image():
    global panelA, panelB, extracted_data

    # buka dialog file untuk memilih gambar
    path = filedialog.askopenfilename()

    if len(path) > 0:
        # muat gambar dari path
        image = Image.open(path)
        image = image.resize((400, 250), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        # jika panel gambar belum ada, buat
        if panelA is None or panelB is None:
            panelA = tk.Label(image=image)
            panelA.image = image
            panelA.pack(side="left", padx=10, pady=10)

            panelB = tk.Text(root, height=15, width=60)
            panelB.pack(side="right", padx=10, pady=10)
        else:
            # update panel gambar
            panelA.configure(image=image)
            panelA.image = image

        # Proses OCR
        img_processor = ImageProcessor(path)
        processed_img = img_processor.preprocess()
        ocr_processor = OCRProcessor()
        extracted_text = ocr_processor.performOCR(processed_img)
        
        # Ekstrak data dari teks
        data_extractor = DataExtractor()
        extracted_data = data_extractor.extractData(extracted_text)
        
        # Format data menjadi JSON
        formatted_data = JSONFormatter.toJSON(extracted_data)
        
        # Tampilkan hasil OCR dan data yang diekstraksi di panelB
        panelB.delete("1.0", tk.END)
        panelB.insert(tk.END, formatted_data)

# Fungsi untuk menyimpan data ke database
def save_to_database():
    global extracted_data
    if extracted_data:
        db = PostgresDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
        db.create_table()
        db.insert_data(extracted_data)
        db.close()
        tk.messagebox.showinfo("Sukses", "Data berhasil disimpan ke database!")
    else:
        tk.messagebox.showwarning("Peringatan", "Tidak ada data yang diekstraksi untuk disimpan.")

# inisialisasi GUI Tkinter
root = tk.Tk()
root.title("OCR KTP apps")

# # Buat canvas untuk menempatkan gambar
# canvas = tk.Canvas(root, width=200, height=200)
# canvas.pack()

# # Muat gambar
# image_path = "assets/kominfo.png"
# original_image = Image.open(image_path)

# # Resize gambar
# resized_image = original_image.resize((100, 100))

# # Konversi gambar ke format Tkinter
# photo = ImageTk.PhotoImage(resized_image)

# # Atur gambar di tengah canvas
# canvas.create_image(100, 100, anchor=tk.CENTER, image=photo)

title = tk.Label(root, text="OCR KTP", font=("Helvetica", 16))
title.pack(side="top", pady=10)

panelA = None
panelB = None

# Frame untuk tombol
button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

# tombol untuk memilih gambar
btn_select_image = tk.Button(button_frame, text="Pilih Gambar KTP", command=select_image, bg="#399496", fg="white")
btn_select_image.grid(row=0, column=0, padx=10, pady=10)

# tombol untuk menyimpan data ke database
btn_save_db = tk.Button(button_frame, text="Simpan ke Database", command=save_to_database, bg="#399496", fg="white")
btn_save_db.grid(row=0, column=1, padx=10, pady=10)

# mulai loop utama Tkinter
root.mainloop()
