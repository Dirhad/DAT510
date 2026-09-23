import random
from math import gcd
from task1_part_2 import encrypt, decrypt

# Symmetric Cipher
# Pseudo-random generators
# Public-key cryptography (PKC)-based key exchange protocol

# Step 1. Public key (Diffie Helman)
p = 1187
g = 2 # p-1 = 2 * 593 (prime 593)

a = 23
b = 192

x = g**a % p # Same as doing pow(g, a, p)
y = g**b % p # Same as doing pow(g, b, p)

Ka = y**a % p
Kb = x**b % p


# Step 2. Convert K_ab -> key K with PKC-based key exchange protocol. Blum Blum Shub (BBS)
# Find prime numbers where P = Q = 3 mod(4)
def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    d = 3
    while d*d <= x:
        if x % d == 0:
            return False
        d += 2
    return True

def is_blum_prime(x):
    return is_prime(x) and x % 4 == 3

def random_blum_prime(low, high):
    while True:
        x = random.randint(low, high)
        if is_blum_prime(x):
            return x

P = random_blum_prime(400, 1000)
Q = random_blum_prime(400, 1000)
n = P * Q

def bbs_bits(seed, n_bits):
    x_i = seed % n
    while gcd(x_i, n) != 1 or x_i in (0,1):
        x_i = (x_i + 1) % n
    bits = []
    for _ in range(n_bits):
        x_i = (x_i**2) % n
        bits.append(str(x_i & 1))
    return "".join(bits)

Kab = Ka # Shared secret key from DH
K = bbs_bits(Kab, 10) # 10 bits for SDES

# Step 3. Helpers
def text_to_bits(text):
    return "".join(format(ord(c), "08b") for c in text)

def bits_to_text(bits):
    return "".join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))

def sdes_encrypt(bits, key):
    return "".join(encrypt(bits[i:i+8], key) for i in range(0, len(bits), 8))

def sdes_decrypt(bits, key):
    return "".join(decrypt(bits[i:i+8], key) for i in range(0, len(bits), 8))

# Step 3. Alice encrypts file with K and send it (Use SDES)
message = input("Alice, enter message to encrypt: ")
pt_bits = text_to_bits(message)
cipher_bits = sdes_encrypt(pt_bits, K)
print(f"Alice sends ciphertext: {cipher_bits}")


# Step 4. Bob decrypts file with K
recovered_text = bits_to_text(sdes_decrypt(cipher_bits, K))
print(f"Bob decrypts ciphertext to: {recovered_text}")


#Step 5.
print(f"Public parameters: p = {p}, g = {g}")
print(f"Alice's public key (PUa): {x}")
print(f"Bob's public key (PUb): {y}")
print(f"Shared key Kab: {Ka}")
print(f"Derived symmetric key K: {K}")