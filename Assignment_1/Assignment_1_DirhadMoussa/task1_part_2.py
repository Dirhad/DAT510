
# Task 1
# S-DES, simpler version of DES
# Symmetric Block Cipher, same key is used for Encryption and Decryption
# 10 Bit Raw, 8 Bit Plaintext, 8 Bit Ciphertext
# Max key length 56 Bits, Data goes through 16 Rounds


p10_permutation_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p8_permutation_table = [6, 3, 7, 4, 8, 5, 10, 9]
ip = [2, 6, 3, 1, 4, 8, 5, 7]
ep = [4, 1, 2, 3, 2, 3, 4, 1]
p4_permutation_table = [2, 4, 3, 1]
ip_inverse = [4, 1, 3, 5, 7, 2, 8, 6]

# Row = outer bits, Col = inner bits
# 1010 -> Outer = 10 & Inner = 01.
# Row 2, S[2][1] = 2 
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

def reorder(bits, table):
    return "".join(bits[i-1] for i in table) # Reorder bits according to a 1-indexed table

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b): # Compare two bits, and returns 1 if they are different, and 0 if they are the same
    return "".join("0" if x == y else "1" for x, y in zip(a, b))

def generate_keys(key10):
    key = reorder(key10, p10_permutation_table)
    left, right = key[:5], key[5:] # Split into to halves

    # Left shift 1 on both left and right -> K1
    left, right = left_shift(left, 1), left_shift(right, 1)

    k1 = reorder(left + right, p8_permutation_table)

    # Left shift 2 on both left and right -> K2
    left, right = left_shift(left, 2), left_shift(right, 2)

    k2 = reorder(left + right, p8_permutation_table)

    return k1, k2


# FK
def sbox_lookup(bits4, box):
    row = int(bits4[0] + bits4[3], 2) # Outer bits
    col = int(bits4[1] + bits4[2], 2) # Inner bits

    return format(box[row][col], "02b")

def fk(bits8, subkey): # split into 4 bits to left and right
    left, right = bits8[:4], bits8[4:]
    t = xor(reorder(right, ep), subkey)

    s = sbox_lookup(t[:4], S0) + sbox_lookup(t[4:], S1)
    s = reorder(s, p4_permutation_table)

    return xor(left, s) + right

def swap(bits8):
    return bits8[4:] + bits8[:4]


# Encrypt & Decrypt
def encrypt(plain8, key10):
    k1, k2 = generate_keys(key10)
    x = reorder(plain8, ip)      # Initial Permutation
    x = fk(x, k1)                # round 1 with K1
    x = swap(x)                  # Swap
    x = fk(x, k2)                # round 2 with K2
    return reorder(x, ip_inverse)    # IP^-1
 
def decrypt(cipher8, key10):
    # same structure, subkeys reversed
    k1, k2 = generate_keys(key10)
    x = reorder(cipher8, ip)
    x = fk(x, k2)                # K2 first
    x = swap(x)
    x = fk(x, k1)                # then K1
    return reorder(x, ip_inverse)



if __name__ == "__main__":

    # Find Ciphertext
    encryption_rows = [("0000000000", "00000000"),
            ("1111111111", "11111111"),
            ("0000011111", "00000000"),
            ("0000011111", "11111111")]

    # Find plaintext
    decryption_rows = [("1000101110", "00011100"),
            ("1000101110", "11000010"),
            ("0010011111", "10011101"),
            ("0010011111", "10010000")]

    print("Encryption")
    for key, pt in encryption_rows:
        ct = encrypt(pt, key)
        print(f"{key:<12}{pt:<12}{ct:<12}")

    print("\n")

    print("Decryption:")
    for key, pt in decryption_rows:
        ct = decrypt(pt, key)
        print(f"{key:<12}{pt:<12}{ct:<12}") 







# Task 2
class TripleSDES: # S-DES applied three times in a row
    def __init__(self, key1_10, key2_10):
        self.k1 = key1_10
        self.k2 = key2_10

    def encrypt(self, plain8):
        x = encrypt(plain8, self.k1) # Encrypt with k1
        x = decrypt(x, self.k2) # Decrypt with k2
        x = encrypt(x, self.k1) # Encrypt with k1
        return x

    def decrypt(self, cipher8):
        x = decrypt(cipher8, self.k1)  # Decrypt with k1
        x = encrypt(x, self.k2)  # Encrypt with k2
        x = decrypt(x, self.k1)  # Decrypt with k1
        return x



triple_encryption_rows = [
        ("0000000000", "0000000000", "00000000"),
        ("1000101110", "0110101110", "11010111"),
        ("1000101110", "0110101110", "10101010"),
        ("1111111111", "1111111111", "10101010")
    ]

triple_decryption_rows = [
        ("1000101110", "0110101110", "11100110"),
        ("1011101111", "0110101110", "01010000"),
        ("0000000000", "0000000000", "10000000")
    ]
if __name__ == "__main__":
    print("\n\nTriple SDES")
    print("Encryption:")
    for k1, k2, pt in triple_encryption_rows:
        ct = TripleSDES(k1, k2).encrypt(pt)
        print(f"{k1:<12}{k2:<12}{pt:<12}{ct:<12}")

    print("\nDecryption:")
    for k1, k2, ct in triple_decryption_rows:
        pt = TripleSDES(k1, k2).decrypt(ct)
        print(f"{k1:<12}{k2:<12}{pt:<12}{ct:<12}")



# Task 3 - Cracking SDES and TripleSDES
ctx1 = "".join("""010001110000000101000000110011011100101100000001011101000000000101101110010101110101
011101101110010001110000000101000111101110100100111110001000010001110110111001001100
101011111001011101101110011011101011101001001111101011110000100101001010100010000100
111111001101100101110100111100110010000000010101011101101110100100000100111110101111
010001111010111101110100011101000000000101001100000000010110111010111010100010000100
011101101110010011001010111110010111000000011000100010010000""".split())

blocks = [ctx1[i:i+8] for i in range(0, len(ctx1), 8)] # 60 blocks of 8 bits

def readable(text): # Count ASCII charachters such ass letters, digits, spaces..
    good = sum(1 for c in text if 32 <= ord(c) <= 126 or c in "\n\r\t")
    return good / len(text) > 0.95 # If more than 95% do, it is wrong.
#                           Random bytes fall in the printable range only about 37 %


if __name__ == "__main__":
    for i in range(1024):
        key = format(i, "010b") # Turns the number into 10 character binary string
        dec_bits = "".join(decrypt(b, key) for b in blocks)

        # Make every 8 bit block to ASCII 
        text = "".join(chr(int(dec_bits[j:j+8], 2)) for j in range(0, len(dec_bits), 8))
        if readable(text):
            print("\n")
            print("Key :", key)
            print("Message:", text)




ctx2 = "".join("""000000011010011100110010110001100110010010100111110101111010011110011100011101000111
010010011100000000011010011100000001100110011010000111011010000000011001110011101111
011111100010010010011100100111001001100110100001011111101010000010110011110110101010
000111000110001001001010000100100011101001110111010010011100010000011010000101111110
000000010111111011010111110101111010011111101111101001111001110010011001110110100000
000110011100111011110111111000100100101001111101101001000001""".split())

# Store each block as a number from 0-255, 60 blocks
cbytes = [int(ctx2[i:i+8], 2) for i in range(0, len(ctx2), 8)]
keys = [format(i, "010b") for i in range(1024)]

def readable(byts):
    good = sum(1 for c in byts if 32 <= c <= 126 or c in (10, 13, 9))
    return good / len(byts) > 0.95

if __name__ == "__main__":
    print("\n\nBuilding...")
    # Decrypt/Encrypt byte v with key number k. 1024 keys * 256 byte values.
    DEC = [[0]*256 for _ in range(1024)]
    ENC = [[0]*256 for _ in range(1024)]
    for ki, k in enumerate(keys):
        for v in range(256):
            b = format(v, "08b")
            DEC[ki][v] = int(decrypt(b, k), 2)
            ENC[ki][v] = int(encrypt(b, k), 2)
    print("Searching...")

    for k1 in range(1024):
        d1 = DEC[k1]
        step1 = [d1[c] for c in cbytes]  
        for k2 in range(1024): # encrypt with k2, decrypt with k1 
            e2 = ENC[k2]
            step3 = [d1[e2[b]] for b in step1]  # encrypt with e2 and decrypt with d1
            if readable(step3):
                text = "".join(chr(c) for c in step3)
                print("Key 1 :", format(k1, "010b"))
                print("Key 2 :", format(k2, "010b"))
                print("Message:", text)