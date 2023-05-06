import numpy as np

# Galois Field Math
def GF_add(a, b, F):
    return (a + b) % F

def GF_sub(a, b, F):
    return (a - b) % F

def GF_mul(a, b, F):
    return (a * b) % F

def GF_div(a, b, F):
    return (a * b ** (F - 2)) % F

def GF_pow(a, b, F):
    return (a ** b) % F

def GF_eval(p, x, F):
    y = 0
    for i in range(len(p)):
        y = GF_add(y, GF_mul(p[i], GF_pow(x, i, F), F), F)
    return y

# Code Parameters
F = 11 # Galois Field F11
n = 11 # Size of codeword (the encoded message)
k = 7 # Size of message (the original message)
t = 2 # Error correction capability

eval_points = np.arange(0, F) # Evaluation points
print("Evaluation points: ", eval_points)

# parity check matrix
H = []
for point in eval_points:   
    H.append(np.array([GF_pow(point, i, F) for i in range(n-k)]))
H = np.array(H)
H = H.T
print("H: ", H)

# calculate the syndromes
def find_syndromes(received_vector):
    syndromes = np.dot(received_vector, H.T) % F
    return syndromes

# Berlekamp-Massey algorithm to find error locator polynomial
def find_error_locator(syndromes, eval_points):
    l = 0
    r = 0
    L = np.array([1])
    R = [1]

    while r < 2*t:
        r += 1
        desc = 0
        for i in range(l + 1):
            if len(L) < l+1:
                L = np.append(L, np.zeros(l+1 - len(L)))
            desc = GF_add(desc, GF_mul(L[i], syndromes[r-i-1], F), F)

        if desc == 0:
            continue
        else:
            if isinstance(R, np.ndarray):
                R = R.tolist()
            L_new = [0] + R
            L_new = desc * np.array(L_new)

            if len(L_new) > len(L):
                L = np.append(L, np.zeros(len(L_new) - len(L)))
            else:
                L_new = np.append(L_new, np.zeros(len(L) - len(L_new)))

            L_old = L
            L = GF_sub(L, L_new, F).astype(int)

            if 2*l <= r-1:
                l = r - l
                R = GF_div(L_old, desc, F).astype(int)
            else:
                R = [0] + R

    return L

# Chien search to find error positions
def find_error_positions(error_locator, eval_points):
    error_positions = []
    for i in range(len(eval_points)):
        if GF_eval(error_locator, eval_points[i], F) == 0:
            error_positions.append(i)
    error_positions = np.array(error_positions)
    return error_positions

# error evaluator polynomial
def find_error_evaluator(error_locator, syndromes):
    L = error_locator

    error_evaluator = np.zeros(len(L) + len(syndromes) - 1)
    for i in range(len(L)):
        for j in range(len(syndromes)):
            error_evaluator[i+j] = GF_add(error_evaluator[i+j], GF_mul(L[i], syndromes[j], F), F)

    error_evaluator = error_evaluator[:2*t].astype(int)
    return error_evaluator

# Forney algorithm to find error values
def find_error_values(error_locator, error_evaluator, error_positions):
    numerator = GF_eval(error_evaluator, error_positions, F).astype(int)
    L_dash = error_locator[1:] # derivative of error locator polynomial
    denominator = GF_eval(L_dash, error_positions, F).astype(int)

    error_values = GF_add(F - GF_div(GF_div(numerator, denominator, F), error_positions, F), 0, F)

    return error_values


# Decoding of the data present in data.txt:

# read the file data.txt line by line and store the values in an np array
# the file junk values at the beginning, take only the values between the line that says "start" and the line that says "stop"

cnt = 0
data = []
with open("data.txt", "r") as f:
    for line in f:
        if line.strip() == "start":
            break
    for line in f:
        if line.strip() == "stop":
            break
        if cnt == 0:
            data.append(int(line.strip()))
        cnt += 1
        if cnt == 4:
            cnt = 0

# data = []
# with open("data.txt", "r") as f:
#     for line in f:
#         data.append(int(line.strip()))
received_vector = np.array(data)
print("Received vector: ", received_vector)

syndromes = find_syndromes(received_vector)
print("Syndromes: ", syndromes)

error_locator = find_error_locator(syndromes, eval_points)
print("Error locator: ", error_locator)

error_positions = find_error_positions(error_locator, eval_points)
print("Error positions: ", error_positions)

error_evaluator = find_error_evaluator(error_locator, syndromes)
print("Error evaluator: ", error_evaluator)

error_values = find_error_values(error_locator, error_evaluator, error_positions)
print("Error values: ", error_values)

# correct the errors
corrected_vector = received_vector.copy()
corrected_vector[error_positions] = GF_sub(corrected_vector[error_positions], error_values, F)
print("Corrected vector: ", corrected_vector)