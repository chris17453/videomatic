# 
# ░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░░▒▓███████▓▒░▒▓███████▓▒░ 
# ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░        
# ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░     ░▒▓█▓▒░        
# ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓███████▓▒░       ░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░  ░▒▓██████▓▒░░▒▓██████▓▒░  
# ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░     ░▒▓█▓▒░ 
# ░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░     ░▒▓█▓▒░ 
# ░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░▒▓███████▓▒░▒▓███████▓▒░  
# 
# Author: Chris Watkins
# Created: 2024-08-14
                                                                                                                            

from itertools import permutations

guesses = [
    {"guess": [6, 8, 2], "correct": 1, "wrong_position": 0},
    {"guess": [6, 1, 4], "correct": 0, "wrong_position": 1},
    {"guess": [2, 0, 6], "correct": 0, "wrong_position": 2},
    {"guess": [7, 3, 8], "correct": 0, "wrong_position": 0, "none_of_these": True},
    {"guess": [7, 8, 0], "correct": 0, "wrong_position": 1},
]

not_this = []
maybe = []

for g in guesses:
    if 'none_of_these' in g and g['none_of_these']:
        not_this.extend(g['guess'])
        continue
    maybe.extend(g['guess'])

not_this = sorted(set(not_this))
maybe = sorted(set(maybe))
maybe = [num for num in maybe if num not in not_this]

# Generate all permutations of maybe digits for 3 positions
possible_combinations = list(permutations(maybe, 3))

# Function to validate a combination against a rule
def validate_combination(combination, guess, correct, wrong_position):
    correct_count = sum([1 for i in range(3) if combination[i] == guess[i]])
    wrong_position_count = sum([1 for i in range(3) if combination[i] in guess and combination[i] != guess[i]])
    return correct_count == correct and wrong_position_count == wrong_position

# Filter valid combinations based on the rules
valid_combinations = []

for combination in possible_combinations:
    valid = True
    for g in guesses:
        if not validate_combination(combination, g['guess'], g['correct'], g['wrong_position']):
            valid = False
            break
    if valid:
        valid_combinations.append(combination)

# Output the valid combinations
print("Valid combinations:", valid_combinations)


from itertools import permutations

guesses = [
    {"guess": [6, 8, 2], "correct": 1, "wrong_position": 0},
    {"guess": [6, 1, 4], "correct": 0, "wrong_position": 1},
    {"guess": [2, 0, 6], "correct": 0, "wrong_position": 2},
    {"guess": [7, 3, 8], "correct": 0, "wrong_position": 0, "none_of_these": True},
    {"guess": [7, 8, 0], "correct": 0, "wrong_position": 1},
]

not_this = []
maybe = []

for g in guesses:
    if 'none_of_these' in g and g['none_of_these']:
        not_this.extend(g['guess'])
        continue
    maybe.extend(g['guess'])

not_this = sorted(set(not_this))
maybe = sorted(set(maybe))
maybe = [num for num in maybe if num not in not_this]

# Generate all permutations of maybe digits for 3 positions
possible_combinations = list(permutations(maybe, 3))

# Function to validate a combination against a rule
def validate_combination(combination, guess, correct, wrong_position):
    correct_count = sum([1 for i in range(3) if combination[i] == guess[i]])
    wrong_position_count = sum([1 for i in range(3) if combination[i] in guess and combination[i] != guess[i]])
    return correct_count == correct and wrong_position_count == wrong_position

# Filter valid combinations based on the rules
valid_combinations = []

for combination in possible_combinations:
    valid = True
    for g in guesses:
        if not validate_combination(combination, g['guess'], g['correct'], g['wrong_position']):
            valid = False
            break
    if valid:
        valid_combinations.append(combination)

# Output the valid combinations
print("Valid combinations:", valid_combinations)


