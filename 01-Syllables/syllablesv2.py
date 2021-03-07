import sys

# Params
words_array = []
vowels = ['a','e','i','o','u', 'y']

# Read from standard input and store words in words_array
for word in sys.stdin:
    word = word.strip().lower()
    words_array.append(word)

# Loop over all the words
for word in words_array:
    syllable_count = 0
    vowel_count = 0
    syllables = []
    cur_syllable = ""
    # Iterate over word to 2nd last letter
    for i in range(0, len(word) - 1):
        letter = word[i]

        if vowel_count == 0: # If no vowels are in the current syllable, add the letter to current syllable
            cur_syllable += letter
            if letter in vowels:
                vowel_count+=1
        else:
            if (letter in vowels):
                if cur_syllable[-1] in vowels: # Generally if we have 2 vowels in a row they are in the same syllable
                    cur_syllable += letter
                else: # Add current syllable to the syllables array then start a new syllable with current letter
                    syllables.append(cur_syllable)
                    cur_syllable = letter
                    vowel_count = 1
            else: # Add the letter to the current syllable if it isn't a vowel
                cur_syllable += letter


    # Here we handle a few cases for the end of the word
    letter = word[-1]
    # Generally, a word ending in "Const, Const, 'y'" should be seperated into two syllables "Const, Const" & "'y"
    if (letter == 'y' and not(cur_syllable[-1] in vowels) and not(word[len(word) - 3] in vowels)):
        syllables.append(cur_syllable)
        syllables.append('y')
    else:
        cur_syllable+=letter
        if cur_syllable == 'ed': # Generally words ending in 'ed' will not be a new syllable
            syllables[-1] += cur_syllable
        elif (cur_syllable == 'es' and not(syllables[-1][-1] in ['c', 's'])): # Words ending in 'es' but not 'ces' and 'ses' will not be a new syllable
            syllables[-1] += cur_syllable

        else:
            syllables.append(cur_syllable)

    print(word, len(syllables))
