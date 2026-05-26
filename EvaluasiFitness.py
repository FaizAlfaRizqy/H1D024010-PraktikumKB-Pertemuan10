def hitung_fitness(kromosom, barang, kapasitas_tas):
    total_harga = 0
    total_bobot = 0
    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_harga += barang[i][1]
            total_bobot += barang[i][2]
    
    if total_bobot > kapasitas_tas:
        return 0 # Penalti jika melebihi kapasitas
    else:
        return total_harga
