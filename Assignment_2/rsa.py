import secrets
from hash_function import my_hash


def is_prime(n, rounds=50): # True if n is prime
    if n < 2:
        return False
    
    for p in [2, 3, 5, 7, 11, 13]:
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s +=1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:    
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits): # Random prime with extactly n times bits
    while True:
        n = secrets.randbits(bits) | (3 << (bits - 2)) | 1
        if is_prime(n):
            return n

def generate_keys(bits=2048): # Returns (e, d, n). PK = (e, n), P
    e = 65537

    while True:
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)

        phi = (p-1) * (q-1)
        if p != q and phi % e != 0:
            break

    n = p*q
    d = pow(e, -1, phi) # Find d by solving for d: (e * d) (mod phi) = 1
    return e, d, n

def sign(text, d, n):
    return pow(my_hash(text), d, n)

def verify(text, signature, e, n):
    return pow(signature, e, n) == my_hash(text)


if __name__ == '__main__':
    e, d, n = generate_keys()
    s = sign('hello', d, n)
    print('n bits:', n.bit_length())
    print('valid:  ', verify('hello', s, e, n))
    print('changed:', verify('hellp', s, e, n))