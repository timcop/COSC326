import sys
words_array = []
vowels = ['a','e','i','o','u']
for line in sys.stdin:
    line = line.strip()
    words_array.append(line)
for line in words_array:
    syllable_count = 0
    vowel_count = 0
    syllables = []
    cur_syllable = ""
    for letter in line:
        cur_syllable += letter
        if letter in vowels:
            vowel_count+= 1
        else:
            if vowel_count > 0:
                syllables.append(cur_syllable)
                cur_syllable = ""
                vowel_count = 0
    print(line, len(syllables))
