from collections import Counter


cipher = """FRRUU OIIYE AMIRN QLQVR BOKGK NSNQQ IUTTY
IIYEA WIJTG LVILA ZWZKT ZCJQH IFNYI WQZXH
RWZQW OHUTI KWNNQ YDLKA EOTUV XELMT SOSIX
JSKPR BUXTI TBUXV BLNSX FJKNC HBLUK PDGUI
IYEAM OJCXW FMJVM MAXYT XFLOL RRLAA JZAXT
YYWFY NBIVH VYQIO SLPXH ZGYLH WGFSX LPSND
UKVTR XPKSS VKOWM QKVCR TUUPR WQMWY XTYLQ
XYYTR TJJGO OLMXV CPPSL KBSEI PMEGC RWZRI
YDBGE BTMFP ZXVMF MGPVO OKZXX IGGFE SIBRX
SEWTY OOOKS PKYFC ZIEYF DAXKG ARBIW KFWUA
SLGLF NMIVH VVPTY IJNSX FJKNC HBLUK PDGUI
IYEAM HVFDY CULJS EHHMX LRXBN OLVMR"""

cipher = cipher.replace("\n", "").replace(" ","")
print(f"Counter: {Counter(cipher)}")

# Check the probability of two alike letters getting picked after eachother
def index_coincidence(text):
    n = len(text)
    freqs = Counter(text) # Counts the frequency of text f.eks: a = 2, b = 4, c=2
    numerator = sum(f*(f-1) for f in freqs.values()) #Eks: Counter(A) * (Counter(A)-1) = 73 * 73-1
    denominator = n * (n-1) # len(cipher) * (len(cipher)-1) = 1000 * 1000-1
    return numerator / denominator  

def step1_ic_analysis(cipher, max_L = 6):
    print("IC-analysis:")
    for i in range(1, max_L + 1):
        columns = [cipher[j::i] for j in range(i)] # Slicing, jump i forward for index j
        average_ic = round(sum(index_coincidence(col) for col in columns) / i, 4)
        print('L =', i, average_ic)  # Average IC is close to the English value of 0,068


# Kasiski, check for patterns in the cipher text
def step2_kasiski(cipher, target="FJKNCHBLUKPDGUIIYEAM"):
    positions = [i for i in range(len(cipher)) if cipher[i:i+len(target)] == target] #Index of the target
    print(positions)
    distance = positions[1] - positions[0] # Delta distance of the index target
    print("Distance:", distance)
    for L in range(1, 7):
        if distance % L == 0:
            print(L, "Share distance") # Trying to find the Key Length



# English letter frequency 
english_freq = {
    'A': 0.0817, 'B': 0.0149, 'C': 0.0278,
    'D': 0.0425, 'E': 0.1270, 'F': 0.0223,
    'G': 0.0202, 'H': 0.0609, 'I': 0.0697,
    'J': 0.0015, 'K': 0.0077, 'L': 0.0403,
    'M': 0.0241, 'N': 0.0675, 'O': 0.0751,
    'P': 0.0193, 'Q': 0.0010, 'R': 0.0599,
    'S': 0.0633, 'T': 0.0906, 'U': 0.0276,
    'V': 0.0098, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.0197, 'Z': 0.0007
}

# Check amount expected given textlength. Low score = higher probarbility english text
def chi_squared(text, freq_table):
    counts = Counter(text)
    n = len(text)
    score = 0
    for letter in freq_table:
        observed = counts[letter]  
        expected = n * freq_table[letter]
        score += (observed - expected) ** 2 / expected
    return score

# Shift each letter backwards with mod 26
def decrypt_ceasar(text, shift):
    result = ""
    for c in text:
        number = ord(c) - ord('A') #ord('A') is int(65), Unicode for the letter A.
        number_shifted = (number-shift) % 26 # 26 possible letter positions
        new_char = chr(number_shifted + ord('A')) # chr is unicode string 
        result += new_char
    return result


def unroll_chain(c, r, m, guess): 
    # Calculate the clear text for a number of positions 
    # in autokey cipher based on guessing first letter in a chain. 
    idx = list(range(r, len(c), m))
    plain = []
    prev = guess
    for j, i in enumerate(idx):
        if j == 0:
            cur = guess
        else:
            cur = (ord(c[i]) - ord('A') - prev) % 26
        plain.append(cur)
        prev = cur
    return plain


def step3_autokey(cipher, m):
    plaintext = [None] * len(cipher) # Creates a list of n amount of Nones
    key = [None] * m

    for r in range(m): # Loops m=6 from 0-5
        best_score = float('inf')
        best_kjede = None
        beste_guess = None
        for guess in range(26):
            kjede = unroll_chain(cipher, r, m, guess)
            tekst = "".join(chr(x + 65) for x in kjede) # Makes every number to letters
            score = chi_squared(tekst, english_freq) # Gives a score on the letters to english
            if score < best_score:
                best_score = score
                best_kjede = kjede
                beste_guess = guess
        for j, i in enumerate(range(r, len(cipher), m)): # Place the best score in plaintext
            plaintext[i] = best_kjede[j]
        key[r] = (ord(cipher[r]) - 65 - beste_guess) % 26 # Place the keyword in key

    plaintext_str = "".join(chr(x + 65) for x in plaintext)
    key_str = "".join(chr(x + 65) for x in key)
    return plaintext_str, key_str




step1_ic_analysis(cipher)
step2_kasiski(cipher)
plaintext, key = step3_autokey(cipher, m=6)
print("Cleartext:", plaintext)
print("Keyword:", key)