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
    for i, letter in enumerate(line):
        cur_syllable += letter
        if letter in vowels:
            vowel_count+= 1
            #check if end of line
            if i == len(line)-1 and letter != 'e':
                syllables.append(cur_syllable)
                cur_syllable = ""
                vowel_count = 0
            elif #l e case
        else:
            if vowel_count > 0:
                #ed case
                if cur_syllable[-1:] == 'e':
                    if letter == 'd' or letter == 's':
                        #do something
                else:
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0
    print(line, len(syllables))
