import spacy
nlp = spacy.load('en')
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for token in doc:
    print(token.text, token.dep_)
