# COSC326

## Syllable Attributes
The number of syllables in a word is closesly related to the number of vowels the word contains, however there are many exceptions. 
For example, "Cat" has 1 vowel and 1 syllable, "Computer" has 3 vowels and 3 syllables but "Team" has 2 vowels and 1 syllable. 
There are examples of words where #vowels > #syllables, however I don't think the reverse is true.
Looking at [Link](https://factsumo.com/blog/syllable-rules-overview/), we can see that *All syllables have at least one vowel.*.
**This gives us a maximum number of syllables in a word, 'num_syllables >= num_vowels.'**
This is a good starting point, once we compute the maximum number of syllables a given word has, we can then look at running the word through a 
number of checks to reduce this syllable count to something closer to the true value. 