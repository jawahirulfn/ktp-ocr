import cv2
import pytesseract
import json

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

image_path = cv2.imread('contoh/ktp3.jpg')

# Preprocessing image before OCR

# Convert to grayscale
gray = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)

# Apply thresholding
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Apply Adaptive Thresholding
adaptive_thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 11, 2)

# OCR
text = pytesseract.image_to_string(thresh, lang='ind', config='--psm 3 --oem 3')

# Split the text into separate fields
fields = {
    "provinsi": "",
    "kabupaten": "",
    "nik": "",
    "nama": "",
    "tempat_lahir": "",
    "tanggal_lahir": "",
    "jenis_kelamin": "",
    "golongan_darah": "",
    "alamat": "",
    "rt_rw": "",
    "kelurahan_desa": "",
    "kecamatan": "",
    "agama": "",
    "status_perkawinan": "",
    "pekerjaan": "",
    "kewarganegaraan": "",
    "berlaku_hingga": ""
}

lines = text.split('\n')
for line in lines:
    for field in fields:
        if field in line.lower():
            fields[field] = line.split(":")[-1].strip()

# Create a JSON object
result = {
    "KTP_Info": fields
}

# Convert to JSON format
json_output = json.dumps(result, ensure_ascii=False, indent=4)

# Print JSON
print(json_output)

# Tampilkan gambar hasil OCR
cv2.imshow('Hasil OCR', adaptive_thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()