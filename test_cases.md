# Test cases
1. Identical text in both boxes: expect 100% similarity.
2. Completely different words: expect 0% similarity.
3. Partly shared text: expect a score between 0 and 100 and verified common three-word phrases.
4. `HELLO, world! this is text.` vs `hello world this is text`: expect 100% after normalization.
5. Leave one box empty: expect validation message.
6. Punctuation-only input: should not crash or divide by zero.
