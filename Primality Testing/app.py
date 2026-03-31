def is_prime(n):
    print("\n--- Primality Test Steps ---")
    if n <= 1:
        print(f"{n} <= 1 → Not Prime")
        return False
    for i in range(2, int(n**0.5) + 1):
        print(f"Checking: {n} % {i} = {n % i}")
        if n % i == 0:
            print(f"Divisible by {i} → Not Prime")
            return False
    print("No divisors found -> Prime Number")
    return True
def gcd(a, b):
    print("\n--- Euclidean Algorithm Steps ---")
    step = 1
    while b != 0:
        print(f"Step {step}: GCD({a}, {b})")
        print(f"→ {a} % {b} = {a % b}")
        a, b = b, a % b
        step += 1
    print(f"\nFinal GCD = {a}")
    return a
def primitive_root(p):
    print("\n--- Primitive Root Steps ---")
    if not is_prime(p):
        print("Primitive root exists only for prime numbers")
        return None
    phi = p - 1
    print(f"\nphi({p}) = {phi}")
    for g in range(2, p):
        print(f"\nChecking g = {g}")
        values = set()
        for i in range(1, phi + 1):
            val = pow(g, i, p)
            print(f"{g}^{i} mod {p} = {val}")
            values.add(val)
        print(f"Generated set: {values}")
        if len(values) == phi:
            print(f"\nPrimitive Root Found: {g}")
            return g
    print("No primitive root found")
    return None
while True:
    print("\n===== MENU =====")
    print("1. Primality Test")
    print("2. Euclidean Algorithm (GCD)")
    print("3. Primitive Root")
    print("4. Exit")
    choice = int(input("Enter choice: "))
    if choice == 1:
        n = int(input("Enter number: "))
        result = is_prime(n)
        print("Result:", "Prime" if result else "Not Prime")
    elif choice == 2:
        a = int(input("Enter a: "))
        b = int(input("Enter b: "))
        print("GCD:", gcd(a, b))
    elif choice == 3:
        p = int(input("Enter prime number: "))
        root = primitive_root(p)
        print("Primitive Root:", root)
    elif choice == 4:
        print("Exiting program...")
        break
    else:
        print("Invalid choice!")