from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------------
# GCD FUNCTION
# -----------------------------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    error = None
    steps = ""

    if request.method == "POST":

        p = request.form.get("p")
        q = request.form.get("q")
        e = request.form.get("e")
        message = request.form.get("message")

        if p and q and e and message:
            try:
                p = int(p)
                q = int(q)
                e = int(e)

                steps += "========== RSA KEY GENERATION ==========\n\n"

                # Step 1
                steps += f"Step 1: Choose two prime numbers\n"
                steps += f"p = {p}, q = {q}\n\n"

                # Step 2
                n = p * q
                steps += f"Step 2: Compute n = p × q\n"
                steps += f"n = {p} × {q} = {n}\n\n"

                # Step 3
                phi = (p - 1) * (q - 1)
                steps += "Step 3: Compute Euler Function\n"
                steps += f"φ(n) = (p-1)(q-1)\n"
                steps += f"φ(n) = ({p}-1)({q}-1)\n"
                steps += f"φ(n) = {phi}\n\n"

                # Step 4
                steps += "Step 4: Choose public exponent e\n"
                steps += f"e = {e}\n"

                if gcd(e, phi) != 1:
                    error = "e is not prime"
                else:

                    steps += f"gcd({e}, {phi}) = 1 valid\n\n"

                    # Step 5
                    steps += "Step 5: Compute private key d\n"

                    d = pow(e, -1, phi)

                    steps += f"d = {d}\n\n"

                    steps += "Public Key = (e, n)\n"
                    steps += f"Public Key = ({e}, {n})\n\n"

                    steps += "Private Key = (d, n)\n"
                    steps += f"Private Key = ({d}, {n})\n\n"


                    # --------------------------------
                    # INTEGER MESSAGE
                    # --------------------------------
                    if message.isdigit():

                        m = int(message)

                        steps += "========== ENCRYPTION ==========\n\n"
                        steps += "Ciphertext Formula:\n"

                        steps += f"M = {m}\n"
                        steps += f"e = {e}\n"
                        steps += f"n = {n}\n\n"

                        encrypted = pow(m, e, n)

                        steps += f"C = {m}^{e} mod {n}\n"
                        steps += f"C = {encrypted}\n\n"

                        steps += "========== DECRYPTION ==========\n\n"
                        steps += "Plaintext Formula:\n"

                        decrypted = pow(encrypted, d, n)

                        steps += f"M = {encrypted}^{d} mod {n}\n"
                        steps += f"M = {decrypted}\n"


                    # --------------------------------
                    # STRING MESSAGE
                    # --------------------------------
                    else:

                        steps += "========== STRING ENCRYPTION ==========\n\n"

                        encrypted = []
                        decrypted = ""

                        for ch in message:

                            m = ord(ch)

                            steps += f"Character = {ch}\n"
                            steps += f"ASCII = {m}\n"

                            c = pow(m, e, n)

                            steps += f"C = {m}^{e} mod {n} = {c}\n\n"

                            encrypted.append(c)

                        steps += "\n========== STRING DECRYPTION ==========\n\n"

                        for c in encrypted:

                            m = pow(c, d, n)

                            steps += f"M = {c}^{d} mod {n} = {m}\n"
                            steps += f"Character = {chr(m)}\n\n"

                            decrypted += chr(m)

                    result = {
                        "n": n,
                        "phi": phi,
                        "public_key": (e, n),
                        "private_key": (d, n),
                        "encrypted": encrypted,
                        "decrypted": decrypted,
                        "steps": steps
                    }

            except:
                error = "Please enter valid values!"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)