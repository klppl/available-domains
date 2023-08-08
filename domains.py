import requests
import itertools
import string
import concurrent.futures
import threading

def generate_pronounceable_combinations(length):
    vowels = 'aeiou'
    consonants = ''.join(set(string.ascii_lowercase) - set(vowels))
    
    if length % 2 == 0:
        patterns = [vowels, consonants] * (length // 2)
    else:
        patterns = [vowels, consonants] * (length // 2) + [vowels]
    
    combinations = itertools.product(*patterns)
    return combinations

def check_domain(combination):
    word = ''.join(combination)
    for tld in tlds:
        url = f'http://free.iis.se/free?q={word}{tld}'
        response = requests.get(url)
        if 'free' in response.text:
            result = f"free {word}{tld}"
            with lock:
                print(result)
                file.write(f"{result}\n")

# Ask the user for input
num_letters = int(input("Enter how many letters for the domain name: "))
tlds_to_check = input("Which tld (.se or .nu) do you want to check? (se, nu or both): ").strip().lower()
pronounceable = input("Do you want to generate pronounceable words? (yes/no): ").strip().lower() == 'yes'

# Validate TLD input
if tlds_to_check not in ['se', 'nu', 'both']:
    print("Invalid input for TLDs. Enter 'se', 'nu' or 'both'.")
    exit()

tlds = ['.se', '.nu'] if tlds_to_check == 'both' else [f'.{tlds_to_check}']

# Generate combinations based on user preference
if pronounceable:
    combinations = generate_pronounceable_combinations(num_letters)
else:
    combinations = itertools.product(string.ascii_lowercase, repeat=num_letters)

# Create a thread lock
lock = threading.Lock()

# Check each combination
with open('domains.txt', 'w') as file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_domain, combinations)
