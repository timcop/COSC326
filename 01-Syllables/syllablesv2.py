import sys

# Params
words_array = []
vowels = ['a','e','i','o','u', 'y']

# Read from standard input and store words in words_array
for word in sys.stdin:
    word = word.strip()
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
        if vowel_count == 0:
            cur_syllable += letter
            if letter in vowels:
                vowel_count+=1
        elif vowel_count == 1:
            if (letter in vowels):
                if cur_syllable[-1] in vowels:
                    cur_syllable += letter
                else:
                    syllables.append(cur_syllable)
                    cur_syllable = letter
                    vowel_count = 1
            else:
                cur_syllable += letter
 
    letter = word[-1]
    if (letter == 'y' and not(cur_syllable[-1] in vowels) and not(word[len(word) - 3] in vowels)):
        syllables.append(cur_syllable)
        syllables.append('y')
    else:
        cur_syllable+=letter
        if cur_syllable == 'ed':
            syllables[-1] += cur_syllable
        elif (cur_syllable == 'es' and not(syllables[-1][-1] in ['c', 's'])):
            syllables[-1] += cur_syllable
        
        else:
            syllables.append(cur_syllable)
    
    print(syllables)


