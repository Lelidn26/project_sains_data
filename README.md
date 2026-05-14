# 🚗 Prediksi Harga Mobil

---

## 📌 Deskripsi Project

Project ini merupakan aplikasi prediksi harga mobil menggunakan metode Machine Learning Linear Regression berdasarkan dataset `Car_sales.xls`.

Sistem dibuat untuk membantu memprediksi harga mobil berdasarkan spesifikasi kendaraan yang diinputkan oleh pengguna melalui aplikasi berbasis web menggunakan Streamlit.

---

## 📁 Struktur Folder

```plaintext
project_sains_data/
│
├── app.py
├── model.pkl
├── Car_sales.xls
├── requirements.txt
└── README.md
```

Keterangan:

* `app.py` → aplikasi web Streamlit
* `model.pkl` → model hasil training dari Google Colab
* `Car_sales.xls` → dataset penjualan mobil
* `requirements.txt` → daftar dependency/library
* `README.md` → dokumentasi project

Catatan:
File `model.pkl` dihasilkan dari proses training dan pemodelan machine learning pada Google Colab menggunakan dataset `Car_sales.xls`.

---

## ⚙️ Teknologi yang Digunakan

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Pickle
* Matplotlib
* Seaborn

---

## 🖥️ Fitur Aplikasi

* Input spesifikasi mobil
* Prediksi harga mobil secara realtime
* Tampilan interaktif berbasis web
* Menggunakan model Linear Regression
* Menampilkan hasil prediksi harga berdasarkan spesifikasi kendaraan

---

## 📊 Dataset

Dataset yang digunakan pada project ini adalah:

```plaintext
Car_sales.xls
```

Dataset berisi informasi penjualan mobil beserta spesifikasi kendaraan yang digunakan untuk proses analisis data dan pembuatan model machine learning.

---

## ▶️ Cara Menjalankan Aplikasi

### 1. Install dependency

Buka terminal pada folder project, lalu jalankan:

```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi Streamlit

```bash
py -m streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser melalui localhost.

---