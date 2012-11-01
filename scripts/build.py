import sqlite3, re

dir = "[DIR]"

annotations = {
    ':': "The word is an otherwise unmarked abbreviation. This suffix may appear in combination with another suffix.",
    '&': "The word is primarily a non-American usage.",
    '#': "The word is generally held to be a variant or less preferred form of another word.",
    '<': "This form of a word is held to be the primary form by fewer dictionaries than some other form of the word.",
    '^': "This form of the word was selected arbitrarily from a set of variants, none of which was clearly preferred.",
    '=': "Roughly, this indicates a \"second class\" word, as described below.",
    '+': "The word is a signature word."
}

conn = sqlite3.connect(dir + 'words.sqlite')
#conn.row_factory = dict_factory
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "commons" (id INTEGER PRIMARY KEY AUTOINCREMENT, "word" VARCHAR(50) UNIQUE, "frequency" INTEGER DEFAULT 0)')

#c.execute('DELETE FROM "commons"')
#conn.commit()

def add_words(path):
    count = 0
    for line in open(path):
        word = re.match("[A-Za-z0-9\s\-\.\']+", line).group(0)
        if word[0] != word[0].upper():
            c.execute("INSERT OR IGNORE into commons ('word') VALUES (\"%s\")" % word)
            count += 1
            if count % 100 == 0:
                conn.commit()
    print "done with", path
    
add_words(dir + "dictionaries/6of12a-m.txt")
add_words(dir + "dictionaries/6of12n-z.txt")

conn.commit()
conn.close()