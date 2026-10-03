# DAT510 – Assignment 1

## Requirements

- Python 3.8 og newer
- No external packages. Only standard library is used ('colelctions', 'math', 'random'). No cryptographic libraries are used, per the assignment rules.

## How to run

Open a terminal in the project folder

### Task 1, Part 1 - Autokey cryptoanalysis

```bash
python3 task1_part_1.py
```

The script prints, in order:

1. The letter frequency count of the ciphertext.
2. The average index of coincidence for key lengths L = 1 to 6. The key length with an IC closest to English (0,066) is the most likely.
3. The kasiski result: positions of the repeated sequence, the distance between them, and which key lengths divide that distance.
4. The recovered plaintext and keyword, found by testing all 26 starting values for each column and choosing the one with lowest chi-squared score.

### Task 1, Part 2 - S-DES, Triple S-DES and cracking

```bash
python3 task1_part_2.py
````

The scrip prints in order:
1. S-DES encryption/decryption tables - key, input and output for each row given in the assignment.
2. Triple S-DES encryption/decryption tables - key1, key2, plaintext and ciphertext.
3. Cracking S-DES - brute force over all 2^10 = 1024 keys, Prints the key and message that decrypt to readable ASCII text.
4. Cracking Triple S-DES - builds lookup tables for all keys, then searches all 1024 * 1024 key pairs. Prints key 1, key 2 and the recovered message.

**Note:** The Triple S-DES search tests over a million key pairs and can take a few minutes during `Building...` and `Searching...` so you can see it is stil working.


### Task 2 - Secure communication system

```bash
python3 task2.py
````

This script will ask:

```
Alice, enter message to encrypt:
```

Type any message and press enter. The script then prints: 

1. Compute the Diffie-Hellman public keys and shared secret with p = 1187, g = 2 and private keys a = 23, b = 192.
2. Generate two random Blum primes (P = Q = 3 mod 4) and uses BBS, seeded with the shared key, to derive a 10-bit S-DES key K.
3. Encrypts the message with S-DES (Alice) and prints the ciphertext bits.
4. Decrypts the ciphertext with same key (Bob) and prints the decrypted message.
5. Prints the public paramters, both public keys, the shared key K_ab, and the derived key K.

**Note:** P and Q are chosen randomly on each run, so the derived key K and the ciphertext will be different every time. The Diffie-Hellman values stay the same and the decrypted message should always match the input.