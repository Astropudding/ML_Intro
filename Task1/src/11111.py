import pymorphy2

morph = pymorphy2.MorphAnalyzer()

lex = morph.parse('думать')[0]

print(lex.inflect({'PRTF'}).word)