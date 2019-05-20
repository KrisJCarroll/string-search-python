##############################################################################
# Author: Kristopher Carroll
# CSCE A351
# Assignment 4
# Purpose: Implements naive, Rabin-Karp and Knuth-Morris-Pratt string searching algorithms
#          and tests them in worst case scenarios and average scenarios
##############################################################################

class StringSearchEngine:
    # O(n) in best case (first character of pattern does not appear at all in text)
    # O(m (n-m+1)) in worst case (all characters are the same or only the last character is different)
    def naive_string_search(self, pattern, text):
        matches = 0
        m = len(pattern)
        n = len(text)
        indices = [] # blank list to store Boolean values for indices searched
        for i in range(n - m + 1): # check entire possible range for matches
            for j in range(m):
                if text[i + j] != pattern[j]: # check to see if entire pattern is found
                    indices.append(False)
                    break
                if j == m - 1: # found a match
                    matches += 1
                    indices.append(True)

        # add remaining Booleans (all False since pattern can't fit in remaining portion of text
        for i in range(m - 1):
            indices.append(False)
        return (matches, indices)
    # O(n+m) average and best case - preprocessing makes these the same
    # O(nm) worst case when all the values of the window match the hash value of the pattern causing each index in text
    # to be checked letter by letter.
    # radix is usually 256 for ASCII
    def rabin_karp_search(self, pattern, text, radix, prime):
        matches = 0
        m = len(pattern)
        n = len(text)
        p = 0 # hash value of pattern
        t = 0 # hash value for text
        h = pow(radix, m-1) % prime # our updating value for t
        indices = [] # blank list to store Boolean values for indices searched

        # Calculate hash value of pattern and matching number of characters in text
        for i in range(m):
            p = (radix * p + ord(pattern[i])) % prime
            t = (radix * t + ord(text[i])) % prime

        # slide across text, updating t as we go
        for i in range(n - m + 1):
            if p == t: # possible match found, check individual characters
                for j in range(m):
                    if text[i+j] != pattern[j]: # spurious hit
                        indices.append(False)
                        break
                    if j == m - 1: # match found
                        matches += 1
                        indices.append(True)

            else:
                indices.append(False)

            # update hash value for next window of text
            if i < n - m: # there's room left for another window
                t = (radix * (t - ord(text[i]) * h) + ord(text[i+m])) % prime # remove leading digit and add trailing digit
        # add remaining Booleans (all False since pattern can't fit in remaining portion of text
        for i in range(m - 1):
            indices.append(False)
        return (matches, indices)

    # compute an array that demonstrates the longest prefix that is also a suffix for pattern
    def compute_prefix_function(self, pattern):
        m = len(pattern)
        pi_func = [0 for _ in range(m)] # initialize to 0
        k = 0
        for q in range(1, m):
            while k > 0 and pattern[k] != pattern[q]:
                k = pi_func[k - 1]
            if pattern[k] == pattern[q]:
                k += 1
                pi_func[q] = k
        return pi_func

    # Computing prefix function takes O(m) in all cases
    # Searching takes O(n) in all cases
    # Total complexity is O(n+m) in all cases
    def kmp_search(self, pattern, text):
        m = len(pattern)
        n = len(text)
        matches = 0
        indices = []
        pi_func = StringSearchEngine.compute_prefix_function(self, pattern)
        q = 0
        for i in range(n):
            while q > 0 and pattern[q] != text[i]:
                q = pi_func[q - 1]
            if pattern[q] == text[i]:
                q += 1
            if q == m:
                matches += 1
                q = pi_func[q - 1]
                indices.append(True)
            else:
                indices.append(False)

        # add remaining Booleans (all False since pattern can't fit in remaining portion of text
        for i in range(m - 1):
            indices.append(False)

        return (matches, indices)




import timeit as time

string_searcher = StringSearchEngine()


text = 'A' * 5000000 + 'B'
pattern = "AAB"
print("Testing algorithms with 5 million A's followed by a single B, searching for 'AAB':\n")

# testing naive algorithm
start_search_time = time.default_timer()
print("\tNaive search starting at:", start_search_time)
result = string_searcher.naive_string_search(pattern, text)
stop_search_time = time.default_timer()
print("\tNaive search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")

# testing Rabin-Karp
start_search_time = time.default_timer()
print("\tRabin-Karp search starting at:", start_search_time)
result = string_searcher.rabin_karp_search(pattern, text, 256, 101)
stop_search_time = time.default_timer()
print("\tRabin-Karp search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")

# testing KMP
start_search_time = time.default_timer()
print("\tKMP search starting at:", start_search_time)
result = string_searcher.kmp_search(pattern, text)
stop_search_time = time.default_timer()
print("\tKMP search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")

f = open("alice.txt", "r")
text = f.read()
pattern = "Alice"
print("Testing algorithms with Alice and Wonderland as text, searching for 'Alice':\n")

# testing naive algorithm
start_search_time = time.default_timer()
print("\tNaive search starting at:", start_search_time)
result = string_searcher.naive_string_search(pattern, text)
stop_search_time = time.default_timer()
print("\tNaive search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")

# testing Rabin-Karp
start_search_time = time.default_timer()
print("\tRabin-Karp search starting at:", start_search_time)
result = string_searcher.rabin_karp_search(pattern, text, 256, 101)
stop_search_time = time.default_timer()
print("\tRabin-Karp search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")

# testing KMP
start_search_time = time.default_timer()
print("\tKMP search starting at:", start_search_time)
result = string_searcher.kmp_search(pattern, text)
stop_search_time = time.default_timer()
print("\tKMP search finished at:", stop_search_time)
print("\tTotal runtime:", stop_search_time - start_search_time, "seconds.")
print("\tTotal matches:", result[0], "\n")