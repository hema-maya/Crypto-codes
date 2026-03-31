import string
def caesar_encrypt(text, key=3):
    result = ""
    print("\n--- Caesar Encryption Steps ---")
    for ch in text:
        if ch.isalpha():
            val = ord(ch.lower()) - 97
            new = (val + key) % 26
            print(f"{ch} -> {val}+{key} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
        else:
            result += ch
    return result
def caesar_decrypt(text, key=3):
    result = ""
    print("\n--- Caesar Decryption Steps ---")
    for ch in text:
        if ch.isalpha():
            val = ord(ch.lower()) - 97
            new = (val - key) % 26
            print(f"{ch} -> {val}-{key} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
        else:
            result += ch
    return result
def shift_encrypt(text, key):
    result = ""
    print("\n--- Shift Encryption Steps ---")
    for ch in text:
        if ch.isalpha():
            val = ord(ch.lower()) - 97
            new = (val + key) % 26
            print(f"{ch} -> {val}+{key} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
        else:
            result += ch
    return result
def shift_decrypt(text, key):
    result = ""
    print("\n--- Shift Decryption Steps ---")
    for ch in text:
        if ch.isalpha():
            val = ord(ch.lower()) - 97
            new = (val - key) % 26
            print(f"{ch} -> {val}-{key} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
        else:
            result += ch
    return result
def generate_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()
    for ch in key:
        if ch not in used and ch.isalpha():
            used.add(ch)
            matrix.append(ch)
    for ch in string.ascii_uppercase:
        if ch not in used and ch != 'J':
            matrix.append(ch)
    matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    print("\nPlayfair Matrix:")
    for row in matrix:
        print(row)
    return matrix
def find_pos(matrix, ch):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j
def playfair_encrypt(text, key):
    matrix = generate_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    print("\nPairs:", pairs)
    result = ""
    for a, b in pairs:
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        print(f"\nProcessing {a}{b}")
        if r1 == r2:
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2:
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result
def playfair_decrypt(text, key):
    matrix = generate_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    print("\n--- Playfair Decryption Steps ---")
    pairs = []
    for i in range(0, len(text), 2):
        pairs.append((text[i], text[i+1]))
    print("Pairs:", pairs)
    result = ""
    for a, b in pairs:
        r1, c1 = find_pos(matrix, a)
        r2, c2 = find_pos(matrix, b)
        print(f"\nProcessing {a}{b}")
        # SAME ROW → move LEFT
        if r1 == r2:
            print("Same Row")
            result += matrix[r1][(c1-1) % 5] + matrix[r2][(c2-1) % 5]
        # SAME COLUMN → move UP
        elif c1 == c2:
            print("Same Column")
            result += matrix[(r1-1) % 5][c1] + matrix[(r2-1) % 5][c2]
        # RECTANGLE RULE
        else:
            print("Rectangle Rule")
            result += matrix[r1][c2] + matrix[r2][c1]
    return result
def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    k = 0
    print("\n--- Vigenere Encryption Steps ---")
    for ch in text:
        if ch.isalpha():
            p = ord(ch.lower()) - 97
            k_val = ord(key[k % len(key)]) - 97
            new = (p + k_val) % 26
            print(f"{ch} -> {p}+{k_val} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
            k += 1
        else:
            result += ch
    return result
def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    k = 0
    print("\n--- Vigenere Decryption Steps ---")
    for ch in text:
        if ch.isalpha():
            p = ord(ch.lower()) - 97
            k_val = ord(key[k % len(key)]) - 97
            new = (p - k_val) % 26
            print(f"{ch} -> {p}-{k_val} -> {new} -> {chr(new+97)}")
            result += chr(new + 97)
            k += 1
        else:
            result += ch
    return result
def mod_inverse(a, m):
    for i in range(1, m):
        if (a*i) % m == 1:
            return i
    return None
def inverse_matrix(key):
    a,b = key[0]
    c,d = key[1]
    det = (a*d - b*c) % 26
    inv_det = mod_inverse(det,26)
    if inv_det is None:
        print("Not invertible")
        return None
    inv = [
        [(d*inv_det)%26, (-b*inv_det)%26],
        [(-c*inv_det)%26, (a*inv_det)%26]
    ]
    print("\nInverse Matrix:")
    for row in inv:
        print(row)
    return inv
def hill_encrypt(text, key):
    text = text.upper().replace(" ","")
    if len(text)%2!=0:
        text+='X'
    print("\n--- Hill Encryption Steps ---")
    res=""
    for i in range(0,len(text),2):
        p1=ord(text[i])-65
        p2=ord(text[i+1])-65
        print(f"\nPair {text[i]}{text[i+1]} -> [{p1},{p2}]")
        c1=(key[0][0]*p1 + key[0][1]*p2)%26
        c2=(key[1][0]*p1 + key[1][1]*p2)%26
        print(f"{c1},{c2}")
        res+=chr(c1+65)+chr(c2+65)
    return res
def hill_decrypt(text, key):
    inv = inverse_matrix(key)
    if inv is None:
        return ""
    print("\n--- Hill Decryption Steps ---")
    res=""
    for i in range(0,len(text),2):
        c1=ord(text[i])-65
        c2=ord(text[i+1])-65
        print(f"\nPair {text[i]}{text[i+1]} -> [{c1},{c2}]")
        p1=(inv[0][0]*c1 + inv[0][1]*c2)%26
        p2=(inv[1][0]*c1 + inv[1][1]*c2)%26
        print(f"{p1},{p2}")
        res+=chr(p1+65)+chr(p2+65)
    return res
while True:
    print("\n===== CRYPTO MENU =====")
    print("1.Caesar 2.Shift 3.Playfair 4.Vigenere 5.Hill 6.Exit")
    ch = int(input("Enter choice: "))
    if ch == 1:
        text = input("Enter text: ")
        enc = caesar_encrypt(text)
        print("Encrypted:", enc)
        print("Decrypted:", caesar_decrypt(enc))
    elif ch == 2:
        key = int(input("Enter key: "))
        text = input("Enter text: ")
        enc = shift_encrypt(text, key)
        print("Encrypted:", enc)
        print("Decrypted:", shift_decrypt(enc, key))
    elif ch == 3:
        text = input("Enter text: ")
        key = input("Enter key: ")
        enc = playfair_encrypt(text, key)
        print("Encrypted:", enc)
        dec = playfair_decrypt(enc, key)
        print("Decrypted:", dec)
    elif ch == 4:
        text = input("Enter text: ")
        key = input("Enter key: ")
        enc = vigenere_encrypt(text, key)
        print("Encrypted:", enc)
        print("Decrypted:", vigenere_decrypt(enc, key))
    elif ch == 5:
        print("Enter 2x2 key:")
        key = [[int(input()), int(input())],
               [int(input()), int(input())]]
        text = input("Enter text: ")
        enc = hill_encrypt(text, key)
        print("Encrypted:", enc)
        print("Decrypted:", hill_decrypt(enc, key))
    elif ch == 6:
        break