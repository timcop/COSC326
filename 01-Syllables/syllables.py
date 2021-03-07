#surely, something
import sys

# Params
words_array = []
vowels = ['a','e','i','o','u', 'y']

# Read from standard input and store words in words_array
for word in sys.stdin:
    word = word.strip()
    words_array.append(word)

# Algorithm to determine syllable count
for word in words_array:
    syllable_count = 0
    vowel_count = 0
    syllables = []
    cur_syllable = ""
    for i, letter in enumerate(word):
        cur_syllable += letter
        if letter in vowels:
            vowel_count+= 1
            #check if el end of word
            if (i == len(word)-1 and letter != 'e') or (i == len(word)-1 and letter == 'e' and cur_syllable[-2:-1] == 'l'):
                syllables.append(cur_syllable)
                cur_syllable = ""
                vowel_count = 0
        else:
            if vowel_count > 0:
                #ed case
                if i != len(word)-1 or ((i == len(word)-1) and cur_syllable[-2:-1] != 'e') or ((i == len(word)-1) and cur_syllable[-2:-1] == 'e' and vowel_count > 1) or ((i == len(word)-1) and cur_syllable[-2:-1] == 'e' and vowel_count == 1 and letter not in ['d', 's']):
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0
                #ces and ses case being a syllable.
                elif (i == len(word)-1) and cur_syllable[-2:-1] == 'e' and vowel_count == 1 and letter in ['d', 's'] and cur_syllable[-3:-2] in ['c', 's']:
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0

    print(word, len(syllables))
