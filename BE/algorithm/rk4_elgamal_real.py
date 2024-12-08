import torch
import algorithm.rk4 as RK4
import algorithm.nist_test as NIST
import random

def generate_model():
    seed = [0.1, 0.1, 0.1]
    rk4_model = RK4.model
    return rk4_model, seed

def fractional_to_binary(fractional_part, length=10):
    """
    Convert fractional part of a number into binary representation of fixed length.
    """
    binary_array = []
    while len(binary_array) < length:
        fractional_part *= 2
        if fractional_part >= 1:
            binary_array.append(1)
            fractional_part -= 1
        else:
            binary_array.append(0)
    return binary_array

def concatenate_binary(data):
    """
    Convert array [[x1, y1, z1], [x2, y2, z2], ..., [xn, yn, zn]] into a binary array.
    """
    binary_array = []
    
    for row in data:
        row_binary = []
        curr_col = 1
        for value in row:
            fractional_part = value - int(value)
            
            binary = fractional_to_binary(abs(fractional_part), 10+(7%curr_col))
            curr_col += 1
            row_binary.extend(binary)  # Combine the binary representation
        binary_array.extend(row_binary)  # Combine the row binary representation
    
    return binary_array

def generate_seed(seed,model,N=1024):
    x_values = []

    state = torch.tensor(seed, dtype=torch.float32).unsqueeze(0)
    for _ in range(32):
        state = model(state)
        x_values.append([state[0, 0].item(), state[0, 1].item(), state[0, 2].item()])
    
    bitstream = concatenate_binary(x_values)
    seed = int(''.join(map(str, bitstream[:N])), 2)
    return seed, bitstream

def rk4_random_bits(length, model, rk4_seed):
    """
    Menggunakan ANN sebagai seed generator.
    """
    # Hasilkan seed dari ANN
    seed, bitstream = generate_seed(model=model,seed=rk4_seed)
    random.seed(seed)
    return random.getrandbits(length), bitstream

def elgamal_encrypt(message, public_key, model, seed):
    """
    Enkripsi pesan menggunakan kunci publik ElGamal
    """
    p, g, y = public_key
    random_bits, bitstream = rk4_random_bits(len(bin(p)) - 2, model, seed)
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
    if len(integer_string) % 3 != 0:
        raise ValueError("Invalid integer representation. Length must be a multiple of 3.")
    
    decoded_string = "".join(chr(int(integer_string[i:i+3])) for i in range(0, len(integer_string), 3))
    return decoded_string

if __name__ == "__main__":
    model, seed = generate_model()

    gen_seed, bitstream = generate_seed(seed, model, 32)
    result = NIST.do_nist_test(bitstream)
    NIST.print_nist_result(result)