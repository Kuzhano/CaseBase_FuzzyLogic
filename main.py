import pandas as pd

# 1. FUNGSI KEANGGOTAAN (MEMBERSHIP FUNCTIONS)
def trapesium(x, a, b, c, d):
    # Menghitung derajat keanggotaan menggunakan kurva trapesium/segitiga.
    if x <= a or x >= d:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a) if b != a else 1
    elif b < x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c) if d != c else 1
    return 0

# 2. PROSES FUZZIFICATION
def get_servis_membership(val):
    return {
        'Buruk': trapesium(val, 0, 0, 30, 50),
        'Biasa': trapesium(val, 40, 60, 70, 80),
        'Bagus': trapesium(val, 70, 90, 100, 100)
    }

def get_harga_membership(val):
    return {
        'Murah': trapesium(val, 25000, 25000, 30000, 35000),
        'Normal': trapesium(val, 30000, 40000, 45000, 50000),
        'Mahal': trapesium(val, 45000, 50000, 55000, 55000)
    }

# 3. MESIN INFERENSI & DEFUZZIFICATION (SUGENO)
def fuzzy_inference_sugeno(servis_val, harga_val):
    servis = get_servis_membership(servis_val)
    harga = get_harga_membership(harga_val)
    
    # Nilai Output Tetap (Singleton Sugeno)
    out_val = {'Rendah': 40, 'Menengah': 70, 'Tinggi': 100}
    
    numerator = 0
    denominator = 0
    
    # Rules Matrix
    rules = [
        (servis['Buruk'], harga['Murah'], 'Rendah'),
        (servis['Buruk'], harga['Normal'], 'Rendah'),
        (servis['Buruk'], harga['Mahal'], 'Rendah'),
        (servis['Biasa'], harga['Murah'], 'Tinggi'),
        (servis['Biasa'], harga['Normal'], 'Menengah'),
        (servis['Biasa'], harga['Mahal'], 'Rendah'),
        (servis['Bagus'], harga['Murah'], 'Tinggi'),
        (servis['Bagus'], harga['Normal'], 'Tinggi'),
        (servis['Bagus'], harga['Mahal'], 'Menengah'),
    ]
    
    for s_score, h_score, category in rules:
        # Operator AND (Mencari nilai minimal)
        w = min(s_score, h_score)
        # Weighted Average
        numerator += w * out_val[category]
        denominator += w
        
    if denominator == 0:
        return 0
    return numerator / denominator

# 4. ALUR UTAMA (MAIN PROGRAM)
def main():
    try:
        # Membaca data dari excel
        df = pd.read_excel('restoran.xlsx')
        
        # Validasi sederhana untuk memastikan kolom yang dibutuhkan ada
        required_columns = ['id Pelanggan', 'Pelayanan', 'harga']
        if not all(col in df.columns for col in required_columns):
            print(f"[ERROR] Kolom tidak sesuai. Pastikan ada kolom: {required_columns}")
            return

        results = []
        
        for index, row in df.iterrows():
            # Mengambil data berdasarkan nama kolom yang Anda tentukan
            id_restoran = row['id Pelanggan']
            servis = row['Pelayanan']
            harga = row['harga']
            
            # Proses Hitung Skor Fuzzy (menggunakan fungsi yang sudah dibuat sebelumnya)
            skor = fuzzy_inference_sugeno(servis, harga)
            
            results.append({
                'id Pelanggan': id_restoran,
                'Pelayanan': servis,
                'harga': harga,
                'Skor': skor # Nama kolom output hasil defuzzifikasi
            })
            
        # Konversi hasil ke DataFrame
        res_df = pd.DataFrame(results)
        
        # Mengambil 5 terbaik berdasarkan Skor Kelayakan
        top_5 = res_df.sort_values(by='Skor', ascending=False).head(5)
        
        # Output Terminal sesuai spesifikasi tugas
        print("\n" + "="*50)
        print("HASIL 5 RESTORAN TERBAIK - SISTEM FUZZY")
        print("="*50)
        print(top_5.to_string(index=False))
        print("="*50)
        
        # Simpan ke file peringkat.xlsx
        top_5.to_excel('peringkat.xlsx', index=False)
        print("\n[INFO] File 'peringkat.xlsx' telah berhasil dibuat.")

    except FileNotFoundError:
        print("[ERROR] File 'restoran.xlsx' tidak ditemukan.")
    except Exception as e:
        print(f"[ERROR] Terjadi kegagalan sistem: {e}")

if __name__ == "__main__":
    main()