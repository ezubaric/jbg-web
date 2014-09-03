

if __name__ == "__main__":
    import nltk
    from nltk import FreqDist
    from nltk.corpus import gutenberg, brown, treebank
    import re

    # Find all examples of "thou *th"
    thou_regexp = re.compile(r"[Tt]hou\s[\w]*t\s")
    thou_count = FreqDist()
    for ii in thou_regexp.findall(gutenberg.raw('bible-kjv.txt')):
        thou_count.inc(ii)
    print("\n".join("%s:%i" % (x, thou_count[x]) for x in thou_count.keys()[:10]))

    # Find everything that looks like a street
    street_regexp = re.compile(r"[A-Z]\w*\s[S]treet")
    for fileid in gutenberg.fileids():
        print(fileid, street_regexp.findall(gutenberg.raw(fileid)))

    print("-----------------------------------------")
        
    # Find repeated words
    repeat_regexp = re.compile(r'\b(\w+)\s(\1\b)+')
    for fileid in gutenberg.fileids():
        matches = list(repeat_regexp.finditer(gutenberg.raw(fileid)))        
        print(fileid, [x.group(0) for x in matches])        
    

    print("-----------------------------------------")
        
    # Find repeated words separated by some other word
    repeat_regexp = re.compile(r"\b(\w+)\s\w+\s(\1\b)+")
    for fileid in gutenberg.fileids():
        matches = list(repeat_regexp.finditer(gutenberg.raw(fileid)))
        print(fileid, [x.group(0) for x in matches])
        
