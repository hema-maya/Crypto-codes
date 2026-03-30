from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    steps = ""
    error = None

    if request.method == "POST":

        try:
            p = int(request.form.get("p"))
            g = int(request.form.get("g"))
            a = int(request.form.get("a"))
            b = int(request.form.get("b"))

            steps += " DIFFIE-HELLMAN KEY EXCHANGE \n"

            steps += "Step 1: Public Values\n"
            steps += f"Prime number (p) = {p}\n"
            steps += f"Primitive root (g) = {g}\n\n"

            steps += "Step 2: Alice chooses private key\n"
            steps += f"a = {a}\n"

            A = pow(g, a, p)

            steps += "Compute public value:\n"
            steps += f"A = g^a mod p\n"
            steps += f"A = {g}^{a} mod {p}\n"
            steps += f"A = {A}\n\n"

            # Step 3
            steps += "Step 3: Bob chooses private key\n"
            steps += f"b = {b}\n"

            B = pow(g, b, p)

            steps += "Compute public value:\n"
            steps += f"B = g^b mod p\n"
            steps += f"B = {g}^{b} mod {p}\n"
            steps += f"B = {B}\n\n"

            # Step 4
            steps += "Step 4: Exchange Public Keys\n"
            steps += f"Alice sends A = {A} to Bob\n"
            steps += f"Bob sends B = {B} to Alice\n\n"

            # Step 5
            steps += "Step 5: Alice computes shared key\n"
            steps += "Key = B^a mod p\n"

            key_alice = pow(B, a, p)

            steps += f"Key = {B}^{a} mod {p}\n"
            steps += f"Key = {key_alice}\n\n"

            # Step 6
            steps += "Step 6: Bob computes shared key\n"
            steps += "Key = A^b mod p\n"

            key_bob = pow(A, b, p)

            steps += f"Key = {A}^{b} mod {p}\n"
            steps += f"Key = {key_bob}\n\n"

            steps += "Both keys are equal.So this a shared key.\n"

            result = {
                "A": A,
                "B": B,
                "key_alice": key_alice,
                "key_bob": key_bob,
                "steps": steps
            }

        except:
            error = "Please enter valid numbers"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)