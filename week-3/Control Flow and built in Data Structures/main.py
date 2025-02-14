#code to filter all sub-strings which has even number of vowel
def q1(sentance):
    vowels = "aeiou"
    out = []
    word_bank = sentance.split()
    ##remember
    # word_list = sum(1 for char in word if char in vowels)
    for word in word_bank:
        vowel_count = 0
        for char in word.lower():
            if char in vowels:
                vowel_count+=1
        if vowel_count%2 == 1:
            out.append(word)
    return out



def q2(astring):
    word_bank = astring.split()
    word_map = {}
    for word in word_bank:
        word_map[word] = word_map.get(word, 0) + 1

    for item in sorted(word_map.items(), key = lambda item: item[1], reverse=True):
        print(item)



def q3(astring):
    word_set = set()
    out = []
    for word in astring.split():
        if word in word_set:
            out.append(word)
        else:
            word_set.add(word)
    print(out)



astring = """Python Multiline String Using Triple-Quotes

Using the triple quotes style is one of the easiest and most common ways to split a large string into a 
multiline Python string. Triple quotes (''' or \""") can be used to create a multiline string. It allows 
you to format text over many lines and include line breaks. Put two triple quotes around the multiline 
Python string, one at the start and one at the end, to define it."""

word_bank = astring.split()

word_counts = {}

for word in word_bank:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

result = []
for word, count in word_counts.items():
    if count > 1:
        result.append((word, count))


result.sort()


print("Word\t Length\tOccurence")
for word, count in result:
    print(f"{word}\t {len(word)}\t{count}")