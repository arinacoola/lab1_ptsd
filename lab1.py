def euler_phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def generalized_euler_phi(n, m):
    primes = []
    for num in range(2, m + 1):
        if is_prime(num):
            primes.append(num)

    result = n
    for p in primes:
        if p > n:
            break
        result -= result // p
    return result + 1

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

if __name__ == "main":
    n = int(input("Enter n: "))
    m = int(input("Enter m: "))
    print(f"φ({n}) = {euler_phi(n)}")
    print(f"φ({n}, {m}) = {generalized_euler_phi(n, m)}")
