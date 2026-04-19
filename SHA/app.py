from flask import Flask, render_template, request

app = Flask(__name__)

def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

def ch(x, y, z): return (x & y) ^ (~x & z)
def maj(x, y, z): return (x & y) ^ (x & z) ^ (y & z)
def sigma0(x): return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)
def sigma1(x): return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)
def gamma0(x): return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
def gamma1(x): return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

K = [  # 64 constants
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,
    0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
    0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,
    0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,
    0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
    0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,
    0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,
    0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
    0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
]

def sha256_with_steps(msg):
    msg = bytearray(msg.encode())
    length = len(msg) * 8

    msg.append(0x80)
    while (len(msg) * 8) % 512 != 448:
        msg.append(0)

    msg += length.to_bytes(8, 'big')

    H = [
        0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
        0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19
    ]

    all_rounds = []

    for i in range(0, len(msg), 64):
        chunk = msg[i:i+64]
        w = [0]*64

        for j in range(16):
            w[j] = int.from_bytes(chunk[j*4:(j+1)*4], 'big')

        for j in range(16, 64):
            w[j] = (gamma1(w[j-2]) + w[j-7] + gamma0(w[j-15]) + w[j-16]) & 0xFFFFFFFF

        a,b,c,d,e,f,g,h = H

        for j in range(64):
            t1 = (h + sigma1(e) + ch(e,f,g) + K[j] + w[j]) & 0xFFFFFFFF
            t2 = (sigma0(a) + maj(a,b,c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

            # Save each round
            all_rounds.append({
                "round": j+1,
                "a": hex(a),
                "b": hex(b),
                "c": hex(c),
                "d": hex(d),
                "e": hex(e),
                "f": hex(f),
                "g": hex(g),
                "h": hex(h)
            })

        H = [(x+y) & 0xFFFFFFFF for x,y in zip(H,[a,b,c,d,e,f,g,h])]

    final_hash = ''.join(f'{x:08x}' for x in H)
    return final_hash, all_rounds

@app.route('/', methods=['GET','POST'])
def index():
    result = ""
    rounds = []
    if request.method == 'POST':
        text = request.form['text']
        result, rounds = sha256_with_steps(text)
    return render_template('index.html', result=result, rounds=rounds)

if __name__ == '__main__':
    app.run(debug=True)