from flask import Flask, render_template, request

app = Flask(__name__)

BLOCK_SIZE = 16

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad(msg):
    padding_steps = []
    original_len = len(msg)

    if len(msg) % BLOCK_SIZE == 0:
        padding_steps.append("No padding needed")
        return msg, padding_steps

    padding = BLOCK_SIZE - len(msg) % BLOCK_SIZE
    padded = msg + bytes([padding] * padding)

    padding_steps.append(f"Original Length: {original_len}")
    padding_steps.append(f"Padding Added: {padding} bytes")
    padding_steps.append(f"Padded Message: {padded}")

    return padded, padding_steps

# Simple "encryption" (educational only)
def fake_encrypt(block, key):
    result = []
    for i in range(len(block)):
        val = (block[i] + key[i % len(key)]) % 256
        result.append(val)
    return bytes(result)

def cmac_with_steps(message, key):
    msg = message.encode()
    key = key.encode()

    msg, padding_steps = pad(msg)

    steps = []
    prev = bytes([0] * BLOCK_SIZE)

    for i in range(0, len(msg), BLOCK_SIZE):
        block = msg[i:i+BLOCK_SIZE]

        xored = xor_bytes(block, prev)
        encrypted = fake_encrypt(xored, key)

        steps.append({
            "block_num": i//BLOCK_SIZE + 1,
            "block": block.hex(),
            "prev": prev.hex(),
            "xor": xored.hex(),
            "encrypted": encrypted.hex()
        })

        prev = encrypted

    final_tag = prev.hex()

    return final_tag, steps, padding_steps

@app.route('/', methods=['GET','POST'])
def index():
    result = ""
    steps = []
    padding_steps = []

    if request.method == 'POST':
        text = request.form['text']
        key = request.form['key']

        result, steps, padding_steps = cmac_with_steps(text, key)

    return render_template('index.html',
                           result=result,
                           steps=steps,
                           padding_steps=padding_steps)

if __name__ == '__main__':
    app.run(debug=True)