def probability_rulers_sum(n, s):
    if n == 1:
        return 1/10 if s in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512] else 0

    total_ways = 0
    for i in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]:
        if s >= i:
            total_ways += probability_rulers_sum(n - 1, s - i)

    return total_ways / 10

def total_probability_rulers_sum():
    total_probability = 0
    for s in range(1000, 10000 + 1):
        if s <= 10 * 512:
            total_probability += probability_rulers_sum(10, s)

    return total_probability

# Calculate the probability of having a consecutive block of rulers whose lengths add up to 1000 meters
probability = total_probability_rulers_sum()
print(f"The probability of achieving a sum of 1000 meters is: {probability:.10f}")
