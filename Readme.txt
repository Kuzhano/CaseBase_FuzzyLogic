SISTEM PENDUKUNG KEPUTUSAN PEMILIHAN RESTORAN - FUZZY LOGIC

Prasyarat:
- Python 3.x
- Library Pandas dan Openpyxl (untuk baca/tulis Excel)
  pip install pandas openpyxl

Cara Menjalankan:
1. Pastikan file 'restoran.xlsx' berada di folder yang sama dengan 'main.py'.
2. Buka terminal atau command prompt.
3. Jalankan perintah: python main.py
4. Program akan menampilkan 5 restoran terbaik di terminal.
5. Hasil peringkat lengkap akan tersimpan di file 'peringkat.xlsx'.

Catatan Teknis:
- Program ini menggunakan Logika Fuzzy dengan metode Sugeno.
- Fuzzifikasi menggunakan fungsi keanggotaan Trapesium.
- Proses Defuzzifikasi dilakukan secara manual tanpa library fuzzy khusus sesuai instruksi tugas.