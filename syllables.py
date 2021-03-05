import sys
words_array = []
vowels = ['a','e','i','o','u', 'y']
for word in sys.stdin:
    word = word.strip()
    words_array.append(word)
for word in words_array:
    syllable_count = 0
    vowel_count = 0
    syllables = []
    cur_syllable = ""
    for i, letter in enumerate(word):
        cur_syllable += letter
        if letter in vowels:
            vowel_count+= 1
            #check if end of word
            if (i == len(word)-1 and letter != 'e') or (i == len(word)-1 and letter == 'e' and cur_syllable[-2:-1] == 'l'):
                syllables.append(cur_syllable)
                cur_syllable = ""
                vowel_count = 0
        else:
            if vowel_count > 0:
                #ed case
                if i != len(word)-1:
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0
                elif letter not in ['d', 's']:
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0
                elif cur_syllable[-2:-1] != 'e' or (cur_syllable[-2:-1] == 'e' and vowel_count > 1):
                    syllables.append(cur_syllable)
                    cur_syllable = ""
                    vowel_count = 0


    print(word, len(syllables))
