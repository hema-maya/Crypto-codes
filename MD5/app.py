from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Left rotate
def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

# Constants
s = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4
K = [int(abs(math.sin(i+1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]

def md5_with_steps(message):
    msg = bytearray(message.encode())
    orig_len = (8 * len(msg)) & 0xffffffffffffffff

    msg.append(0x80)
    while (len(msg) % 64) != 56:
        msg.append(0)

    msg += orig_len.to_bytes(8, byteorder='little')

    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476

    steps = []

    for i in range(0, len(msg), 64):
        chunk = msg[i:i+64]
        M = [int.from_bytes(chunk[j:j+4], 'little') for j in range(0, 64, 4)]

        a, b, c, d = A, B, C, D

        for j in range(64):

            if 0 <= j <= 15:
                f = (b & c) | (~b & d)
                g = j
            elif 16 <= j <= 31:
                f = (d & b) | (~d & c)
                g = (5*j + 1) % 16
            elif 32 <= j <= 47:
                f = b ^ c ^ d
                g = (3*j + 5) % 16
            else:
                f = c ^ (b | ~d)
                g = (7*j) % 16

            f = (f + a + K[j] + M[g]) & 0xFFFFFFFF
            a = d
            d = c
            c = b
            b = (b + left_rotate(f, s[j])) & 0xFFFFFFFF

            steps.append({
                "step": j+1,
                "A": hex(a),
                "B": hex(b),
                "C": hex(c),
                "D": hex(d)
            })

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    final_hash = ''.join(x.to_bytes(4, 'little').hex() for x in [A,B,C,D])
    return final_hash, steps

@app.route('/', methods=['GET','POST'])
def index():
    result = ""
    steps = []

    if request.method == 'POST':
        text = request.form['text']
        result, steps = md5_with_steps(text)

    return render_template('index.html', result=result, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)