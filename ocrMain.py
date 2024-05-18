import cv2
import pytesseract
import json
import psycopg2

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

class PostgresDB:
    def __init__(self, dbname, user, password, host, port):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS ktp_data (
            id SERIAL PRIMARY KEY,
            provinsi TEXT,
            kabupaten TEXT,
            nik TEXT,
            nama TEXT,
            tempat_lahir TEXT,
            tanggal_lahir TEXT,
            jenis_kelamin TEXT,
            golongan_darah TEXT,
            alamat TEXT,
            rt_rw TEXT,
            kelurahan_desa TEXT,
            kecamatan TEXT,
            agama TEXT,
            status_perkawinan TEXT,
            pekerjaan TEXT,
            kewarganegaraan TEXT,
            berlaku_hingga TEXT
        );
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO ktp_data (provinsi, kabupaten, nik, nama, tempat_lahir, tanggal_lahir, 
                              jenis_kelamin, golongan_darah, alamat, rt_rw, kelurahan_desa, 
                              kecamatan, agama, status_perkawinan, pekerjaan, kewarganegaraan, 
                              berlaku_hingga) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        self.cursor.execute(insert_query, (
            data.get("provinsi"), data.get("kabupaten"), data.get("nik"), data.get("nama"),
            data.get("tempat_lahir"), data.get("tanggal_lahir"), data.get("jenis_kelamin"), data.get("golongan_darah"),
            data.get("alamat"), data.get("rt_rw"), data.get("kelurahan_desa"), data.get("kecamatan"),
            data.get("agama"), data.get("status_perkawinan"), data.get("pekerjaan"), data.get("kewarganegaraan"),
            data.get("berlaku_hingga")
        ))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


# imageProcessor = ImageProcessor('ktp_contoh/ktp2.jpg')
# processedImage = imageProcessor.preprocess()

# ocrProcessor = OCRProcessor()
# text = ocrProcessor.performOCR(processedImage)

# dataExtractor = DataExtractor()
# extractedData = dataExtractor.extractData(text)


# jsonFormatter = JSONFormatter()
# json_output = jsonFormatter.toJSON(extractedData)
# print(json_output)

# # Tampilkan gambar hasil OCR
# cv2.imshow('OCR Result', processedImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
