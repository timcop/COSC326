# COSC326

## 01 - Syllable Attributes
The number of syllables in a word is closesly related to the number of vowels the word contains, however there are many exceptions. 
For example, "Cat" has 1 vowel and 1 syllable, "Computer" has 3 vowels and 3 syllables but "Team" has 2 vowels and 1 syllable. 
There are examples of words where #vowels > #syllables, however I don't think the reverse is true.
Looking at [Link](https://factsumo.com/blog/syllable-rules-overview/), we can see that *All syllables have at least one vowel.*.
**This gives us a maximum number of syllables in a word, num_syllables <= num_vowels.**
This is a good starting point, once we compute the maximum number of syllables a given word has, we can then look at running the word through a 
number of checks to reduce this syllable count to something closer to the true value. Having a maximum count is also useful as a sanity check.

- Words ending in s doesn't change syllable count
- Set of consequtive vowels, i.e "ea" or "ou", generally are the same syllable.
- Think of weird cases like "Rhythm", "Lion", "Naive", "Strengths", "Cooperation" 
- Is "i" the only vowel which can end 1 vowel and start another, i.e "Naive"?
- If a word ends in a constanent and then a y then the y is a new syllable
- If a word ends in an e will it always be the same syllable?



- [ ] Find the maximum number of syllables a word can have