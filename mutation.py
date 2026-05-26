import random

# Swap Mutation
def swap_mutation(kromosom):
    kromosom = list(kromosom)
    posisi1, posisi2 = random.sample(range(len(kromosom)), 2)
    kromosom[posisi1], kromosom[posisi2] = kromosom[posisi2], kromosom[posisi1]
    return kromosom

# Inversion Mutation
def inversion_mutation(kromosom):
    kromosom = list(kromosom)
    posisi1 = random.randint(0, len(kromosom) - 2)
    posisi2 = random.randint(posisi1 + 1, len(kromosom) - 1)
    kromosom[posisi1:posisi2] = list(reversed(kromosom[posisi1:posisi2]))
    return kromosom

# Uniform Mutation
def uniform_mutation(kromosom, mutation_rate=0.1):
    kromosom = list(kromosom)
    for i in range(len(kromosom)):
        if random.random() < mutation_rate:
            kromosom[i] = 1 - kromosom[i]
    return kromosom
