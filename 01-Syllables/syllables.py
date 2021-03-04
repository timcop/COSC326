import sys
words_array = []
vowels = ['a','e','i','o','u', 'y']
for line in sys.stdin:
    line = line.strip()
    words_array.append(line)
for line in words_array:
    syllable_count = 0
    vowel_count = 0
    syllables = []
    cur_syllable = ""
    # length = line.length
    for letter in line:
        if letter in vowels:
            cur_syllable += letter
            vowel_count+= 1
            if letter == line[len(line)-1] and letter != 'e':
                syllables.append(cur_syllable)
                cur_syllable = ""
        else:
            if cur_syllable[-1:] in vowels:
                cur_syllable += letter
                syllables.append(cur_syllable)
                cur_syllable = ""


    print(syllables)
