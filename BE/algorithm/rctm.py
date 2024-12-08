def robust_tent_map(x0, mu, N):
    # Implementasi Robust Chaotic Tent Map (RCTM)
    # Args:
    #     x0 (float): Kondisi awal (0 < x0 < 1)
    #     mu (float): Parameter kontrol (2 < mu < 100)
    #     N (int): Panjang bitstream yang dihasilkan
    # Returns:
    #     list: Urutan bilangan acak dalam bentuk floating-point
    if not (0 < x0 < 1):
        raise ValueError("x0 harus berada dalam interval (0, 1).")
    if not (2 < mu < 100) or int(mu) == mu:
        raise ValueError("mu harus berada dalam interval (2, 100) dan bukan bilangan bulat.")
    
    x = [x0]
    n1 = 0.5 - (mu / 2) % 1 / mu
    n2 = 0.5 + (mu / 2) % 1 / mu
    
    for _ in range(N - 1):
        if n1 <= x[-1] <= n2:
            if x[-1] < 0.5:
                x_next = (mu * x[-1]) % 1 / ((mu / 2) % 1)
            else:
                x_next = (mu * (1 - x[-1])) % 1 / ((mu / 2) % 1)
        else:
            if x[-1] < 0.5:
                x_next = (mu * x[-1]) % 1
            else:
                x_next = (mu * (1 - x[-1])) % 1
        x.append(x_next)
    
    return x

def generate_bitstream(x_values):
    # Menghasilkan bitstream dari urutan floating-point menggunakan threshold 0.5
    # Args:
    #     x_values (list): Urutan bilangan floating-point
    # Returns:
    #     list: Bitstream (0 atau 1)
    return [1 if x >= 0.5 else 0 for x in x_values]

if __name__ == "__main__":
    # Parameter
    x0 = 0.23  # Kondisi awal
    mu = 61.81  # Parameter kontrol
    N = 1000  # Panjang bitstream

    # Jalankan algoritma
    chaotic_sequence = robust_tent_map(x0, mu, N)
    bitstream = generate_bitstream(chaotic_sequence)

    # Output
    print("Bitstream:", bitstream)