from Crypto.Util.number import getPrime
import random
import algorithm.rctm as rctm
# import robust_tent_map, generate_bitstream

def rctm_seed(x0, mu, N=1024):
    """
    Menggunakan RCTM untuk menghasilkan seed untuk random generator.
    """
    chaotic_sequence = rctm.robust_tent_map(x0, mu, N)
    bitstream = rctm.generate_bitstream(chaotic_sequence)
    seed = int(''.join(map(str, bitstream[:N])), 2)  # Ambil seed dari N bit pertama
    # print("seed:", seed)
    return seed, bitstream

def rctm_random_bits(length, x0, mu):
    """
    Menggunakan RCTM sebagai seed generator untuk mempercepat random number generation.
    """
    # Hasilkan seed dari RCTM
    seed, bitstream = rctm_seed(x0, mu)
    random.seed(seed)  # Seed generator bawaan Python
    # print("RCTM random bit")
    return random.getrandbits(length), bitstream

def elgamal_key_generation(bit_length=512):
    """
    Generate ElGamal keys dengan RCTM
    """
    p = getPrime(bit_length, randfunc=lambda n: random.getrandbits(n).to_bytes((n + 7) // 8, byteorder='big'))
    g = 2
    x = random.getrandbits(bit_length - 1)  # Private key
    y = pow(g, x, p)  # Public key: y = g^x mod p
    return (p, g, y), x  # Public key: (p, g, y), Private key: x
    

def elgamal_encrypt(message, public_key, x0=0.23, mu=61.81):
    """
    Enkripsi pesan menggunakan kunci publik ElGamal
    """
    p, g, y = public_key
    random_bits, bitstream = rctm_random_bits(len(bin(p)) - 2, x0, mu)
    k = random_bits  % (p - 1)  # Ephemeral key
    c1 = pow(g, k, p)
    c2 = (message * pow(y, k, p)) % p
    return (c1, c2), bitstream

def elgamal_decrypt(ciphertext, private_key, public_key):
    """
    Dekripsi pesan menggunakan kunci privat ElGamal
    """
    p, _, _ = public_key
    c1, c2 = ciphertext
    x = private_key
    s = pow(c1, x, p)  # s = c1^x mod p
    s_inv = pow(s, -1, p)  # s^(-1) mod p
    return (c2 * s_inv) % p

def string_to_integer(input_string):
    if not input_string:
        raise ValueError("Input string cannot be empty.")
    
    integer_representation = int("".join(f"{ord(char):03d}" for char in input_string))
    return integer_representation

def integer_to_string(input_integer):
    if not isinstance(input_integer, int):
        raise ValueError("Input must be an integer.")
    
    # Convert the integer to a string, pad to groups of 3 digits
    integer_string = str(input_integer)
    if len(integer_string) % 3 == 2:
        integer_string = "0" + integer_string
    elif len(integer_string) % 3 == 1:
        integer_string = "00" + integer_string
    if len(integer_string) % 3 != 0:
        raise ValueError("Invalid integer representation. Length must be a multiple of 3.")
    
    decoded_string = "".join(chr(int(integer_string[i:i+3])) for i in range(0, len(integer_string), 3))
    return decoded_string


if __name__ == "__main__":
    # Generate keys
    public_key, private_key = elgamal_key_generation()
    print("Public Key (p, g, y):", public_key)
    print("Private Key (x):", private_key)

    # Encrypt and Decrypt a message
    message = "kucing"
    int_message = string_to_integer(str(message))
    ciphertext, bitstream = elgamal_encrypt(int_message, public_key)
    print("Ciphertext:", ciphertext)

    decrypted_message = elgamal_decrypt(ciphertext, private_key, public_key)
    str_message = integer_to_string(int(decrypted_message))
    print("Decrypted Message:", str_message)
