import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# ==============================
# Konfigurasi
# ==============================
N = 500  # Rentang data: 1 sampai N
OUTPUT_FILENAME = f"theoretical_complexity_N{N}.png"

# Warna dalam (R, G, B)
COLORS = {
    "Bubble Sort": (60, 60, 255),
    "Quick Sort": (60, 255, 60),
    "Merge Sort": (255, 60, 60)
}

# Konversi ke format matplotlib (0–1)
def to_float(rgb):
    return tuple(c / 255.0 for c in rgb)

# ==============================
# Buat data teoretis
# ==============================
n_values = np.arange(1, N + 1)

# Normalisasi agar skala sebanding (opsional, tapi lebih rapi)
# Kita bagi dengan konstanta agar tidak terlalu besar
bubble_theoretical = n_values ** 2
quick_theoretical = n_values * np.log2(np.maximum(n_values, 2))  # log(1)=0 → pakai max(2)
merge_theoretical = n_values * np.log2(np.maximum(n_values, 2))

# Opsional: normalisasi ke [0,1] atau skala relatif
# Tapi kita tampilkan nilai absolut (relatif saja)

# ==============================
# Plot
# ==============================
plt.figure(figsize=(10, 6))

plt.plot(n_values, bubble_theoretical, 
         label="Bubble Sort — O(n²)", 
         color=to_float(COLORS["Bubble Sort"]), 
         linewidth=2.5)

plt.plot(n_values, quick_theoretical, 
         label="Quick Sort — O(n log n)", 
         color=to_float(COLORS["Quick Sort"]), 
         linewidth=2.5, linestyle='--')

plt.plot(n_values, merge_theoretical, 
         label="Merge Sort — O(n log n)", 
         color=to_float(COLORS["Merge Sort"]), 
         linewidth=2.5, linestyle=':')

# Label dan gaya
plt.title(f"Kompleksitas Teoretis Algoritma Sorting (n = 1 sampai {N})", fontsize=14, weight='bold')
plt.xlabel("Jumlah Data (n)", fontsize=12)
plt.ylabel("Kompleksitas Relatif", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Simpan
plt.savefig(OUTPUT_FILENAME, dpi=200, bbox_inches='tight')
plt.close()

print(f"✅ Grafik teoretis disimpan sebagai:")
print(f"   {os.path.abspath(OUTPUT_FILENAME)}")