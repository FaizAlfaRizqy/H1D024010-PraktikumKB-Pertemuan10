import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt

# Import modul algoritma genetika kita
from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import roulette_wheel_selection, tournament_selection
from crossover import one_point_crossover, two_point_crossover, uniform_crossover
from mutation import swap_mutation, inversion_mutation, uniform_mutation

# Data Barang
# Format: (Nama, Keuntungan, Ukuran)
DATA_BARANG = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7),
]

def aturan_berdasarkan_nim(nim):
    """
    Fungsi untuk memecah NIM dan memilih metode sesuai PDF Pertemuan 10
    """
    if len(nim) < 2:
        raise ValueError("NIM terlalu pendek.")
    
    digit_terakhir = nim[-2:]
    if not digit_terakhir.isdigit():
        raise ValueError("2 karakter terakhir NIM harus berupa angka.")
        
    d1 = int(digit_terakhir[0])
    d2 = int(digit_terakhir[1])
    
    # Aturan Seleksi: Check digit pertama (dari 2 terakhir)
    # Genap = RWS, Ganjil = TS
    if d1 % 2 == 0:
        seleksi = "RWS"
    else:
        seleksi = "TS"
        
    # Aturan Crossover: Digit kedua mod 3
    # 0 = One Point, 1 = Two Point, 2 = Uniform
    cross_map = ["One Point", "Two Point", "Uniform"]
    crossover = cross_map[d2 % 3]
    
    # Aturan Mutasi: Penjumlahan 2 digit -> Ambil digit terakhir -> mod 3
    # 0 = Swap, 1 = Inversion, 2 = Uniform
    jumlah_digit = d1 + d2
    digit_akhir_jumlah = jumlah_digit % 10
    mut_map = ["Swap", "Inversion", "Uniform"]
    mutasi = mut_map[digit_akhir_jumlah % 3]
    
    return seleksi, crossover, mutasi


def run_ga(seleksi_method, crossover_method, mutasi_method, kapasitas_tas):
    jumlah_generasi = 50
    jumlah_populasi = 20
    prob_crossover = 0.8
    prob_mutasi = 0.1
    
    jumlah_gen = len(DATA_BARANG)
    
    # 1. Inisialisasi Populasi
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)
    
    best_fitness_list = []
    
    # 2. Proses Evolusi
    for generasi in range(jumlah_generasi):
        # Hitung Fitness
        fitness_populasi = [hitung_fitness(ind, DATA_BARANG, kapasitas_tas) for ind in populasi]
        
        # Simpan nilai terbaik generasi ini
        best_fitness = max(fitness_populasi)
        best_fitness_list.append(best_fitness)
        
        new_populasi = []
        used_indices = []
        
        # Membentuk Populasi Baru
        while len(new_populasi) < jumlah_populasi:
            
            # --- SELEKSI ---
            if seleksi_method == "RWS":
                parent1, idx1 = roulette_wheel_selection(populasi, fitness_populasi)
            else:
                parent1, idx1 = tournament_selection(populasi, fitness_populasi)
            used_indices.append(idx1)
            
            # Memastikan parent2 berbeda
            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]
                
            temp_pop = [populasi[i] for i in available_indices]
            temp_fit = [fitness_populasi[i] for i in available_indices]
            
            if seleksi_method == "RWS":
                parent2, _ = roulette_wheel_selection(temp_pop, temp_fit)
            else:
                parent2, _ = tournament_selection(temp_pop, temp_fit)
            used_indices.append(available_indices[_])
            
            # --- CROSSOVER ---
            if random.random() < prob_crossover:
                if crossover_method == "One Point":
                    anak1, anak2 = one_point_crossover(parent1, parent2)
                elif crossover_method == "Two Point":
                    anak1, anak2 = two_point_crossover(parent1, parent2)
                else:  # Uniform
                    anak1, anak2 = uniform_crossover(parent1, parent2)
            else:
                anak1, anak2 = parent1[:], parent2[:]
                
            # --- MUTASI ---
            if random.random() < prob_mutasi:
                if mutasi_method == "Swap": anak1 = swap_mutation(anak1)
                elif mutasi_method == "Inversion": anak1 = inversion_mutation(anak1)
                else: anak1 = uniform_mutation(anak1)
                
            if random.random() < prob_mutasi:
                if mutasi_method == "Swap": anak2 = swap_mutation(anak2)
                elif mutasi_method == "Inversion": anak2 = inversion_mutation(anak2)
                else: anak2 = uniform_mutation(anak2)
                
            # Tambahkan ke populasi baru
            new_populasi.extend([anak1, anak2])
            
        # Potong agar pas dengan jumlah populasi
        populasi = new_populasi[:jumlah_populasi]

    # Evaluasi hasil akhir
    fitness_populasi = [hitung_fitness(ind, DATA_BARANG, kapasitas_tas) for ind in populasi]
    best_fitness = max(fitness_populasi)
    best_idx = fitness_populasi.index(best_fitness)
    best_individu = populasi[best_idx]
    
    # PLOTTING HASIL
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, jumlah_generasi+1), best_fitness_list, color='blue', label='Fitness Tertinggi')
    plt.title(f'Progress GA\nSeleksi: {seleksi_method} | Crossover: {crossover_method} | Mutasi: {mutasi_method}')
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness (Keuntungan)')
    plt.legend()
    plt.grid(True)
    plt.show()

    return best_individu, best_fitness


def jalankan_aplikasi():
    nim = entry_nim.get().strip()
    kapasitas_str = entry_kapasitas.get().strip()
    
    if not nim or not kapasitas_str:
        messagebox.showwarning("Peringatan", "Mohon isi NIM dan Kapasitas Tas.")
        return
        
    try:
        kapasitas = int(kapasitas_str)
        # Menentukan metode berdasar perhitungan NIM
        sel, cross, mut = aturan_berdasarkan_nim(nim)
        
        lbl_status.config(text=f"Metode: {sel}, {cross}, {mut}\nSedang memproses Evolusi...")
        root.update()
        
        # Eksekusi Evaluasi GA
        best_ind, best_fit = run_ga(sel, cross, mut, kapasitas)
        
        # Rekap hasil akhir
        barang_pilihan = []
        total_berat = 0
        for i, bit in enumerate(best_ind):
            if bit == 1:
                barang_pilihan.append(DATA_BARANG[i][0])
                total_berat += DATA_BARANG[i][2]
                
        hasil = (
            f"--- METODE DIGUNAKAN ---\n"
            f"Seleksi   : {sel}\n"
            f"Crossover : {cross}\n"
            f"Mutasi    : {mut}\n\n"
            f"--- HASIL TERBAIK ---\n"
            f"Keuntungan (Fitness): {best_fit}\n"
            f"Total Ukuran Pakai  : {total_berat} / {kapasitas}\n"
            f"Barang Terpilih     : \n" + ", ".join(barang_pilihan)
        )
        
        lbl_status.config(text=hasil)
        
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# ================================
# TAMPILAN GUI TKINTER
# ================================
root = tk.Tk()
root.title("GA Praktikum Pertemuan 10 - Knapsack")
root.geometry("450x450")
root.configure(padx=20, pady=20)

tk.Label(root, text="STUDI KASUS KNAPSACK PROBLEM (GA)", font=("Helvetica", 12, "bold")).pack(pady=10)

# Input NIM
tk.Label(root, text="Masukkan NIM Anda:").pack(anchor="w")
entry_nim = tk.Entry(root, width=50)
entry_nim.pack(pady=5)
entry_nim.insert(0, "H1D023110") # Sesuai contoh pada PDF

# Input Kapasitas Tas (Ukuran Maksimal)
tk.Label(root, text="Kapasitas / Ukuran Maksimal Gudang:").pack(anchor="w")
entry_kapasitas = tk.Entry(root, width=50)
entry_kapasitas.pack(pady=5)
entry_kapasitas.insert(0, "15")

# Tombol Proses
tk.Button(root, text="PROSES ALGORITMA GENETIKA", command=jalankan_aplikasi, bg="#007bff", fg="white", font=("Helvetica", 10, "bold")).pack(pady=15)

# Label Hasil
lbl_status = tk.Label(root, text="Hasil evaluasi akan muncul di sini.", justify="left", fg="black")
lbl_status.pack(anchor="w", pady=10)

root.mainloop()
