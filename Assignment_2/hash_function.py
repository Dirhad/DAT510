
MASK = 2 ** 256 - 1 # keep everything at 256 bits

PRIME = 2 ** 168 + 2 ** 8 + 0x63 # Large prime multiplier

START = 0x6a09e667bb67ae853c6ef372a54ff53a510e527f9b05688c1f83d9ab5be0cd19



def rot1(x, n): # Rotate a 256-bit number n bits to the left
    return ((x << n) | (x >> (256 - n))) & MASK

def mix(h): # #cramble a 256-bit number 8 rounds
    for r in range(8):
        h = (h * PRIME) & MASK # Spread bits upwards
        h ^= h >> 128          # Fold top half into bottom half
        h = rot1(h, 97)        # Move mixed bits around
        h = (h + r) & MASK     # Round constant
    return h



def my_hash(text): 
    data = text.encode('utf-8')
    h = START
    for i in range(0, len(data), 32):                # 32-byte blocks
        block = int.from_bytes(data[i:i + 32], 'big')
        h = mix(h ^ block) ^ h
    return mix(h ^ len(data))  # Mix in the length




    
if __name__ == '__main__':
    print(hex(my_hash('hello')))
    print(hex(my_hash('hellp')))
    