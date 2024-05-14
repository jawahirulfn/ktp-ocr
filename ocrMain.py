import cv2
import pytesseract
import json

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

class ImageProcessor:
    def __init__(self, imagePath):
        self.image = cv2.imread(imagePath)

    def preprocess(self):
        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Apply Adaptive Thresholding
        adaptive_thresh = cv2.adaptiveThreshold(thresh, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 11, 2)
        return adaptive_thresh

class OCRProcessor:
    def __init__(self):
        self.text = ""

    def performOCR(self, image):
        my_config = '--psm 3 --oem 3'
        self.text = pytesseract.image_to_string(image, lang='ind', config=my_config)
        return self.text

class DataExtractor:
    def __init__(self):
        self.rawData = ""
        self.fields = {
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

    def extractData(self, text):
        self.rawData = text
        lines = text.split('\n')
        for line in lines:
            for field in self.fields:
                if field in line.lower():
                    self.fields[field] = line.split(":")[-1].strip()
        return self.fields

class JSONFormatter:
    @staticmethod
    def toJSON(data):
        result = {"KTP_Info": data}
        return json.dumps(result, ensure_ascii=False, indent=4)


imageProcessor = ImageProcessor('ktp_contoh/ktp2.jpg')
processedImage = imageProcessor.preprocess()

ocrProcessor = OCRProcessor()
text = ocrProcessor.performOCR(processedImage)

dataExtractor = DataExtractor()
extractedData = dataExtractor.extractData(text)


jsonFormatter = JSONFormatter()
json_output = jsonFormatter.toJSON(extractedData)
print(json_output)

# Tampilkan gambar hasil OCR
cv2.imshow('OCR Result', processedImage)
cv2.waitKey(0)
cv2.destroyAllWindows()
