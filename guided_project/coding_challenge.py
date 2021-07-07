"""
Print out all of the strings in the following array in alphabetical order, each on a separate line.
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
The expected output is:
'Cha Cha'
'Foxtrot'
'Jive'
'Paso Doble'
'Rumba'
'Samba'
'Tango'
'Viennese Waltz'
'Waltz'
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.
"""

words = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot',
         'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

for i in range(len(words)):
    current_word = words[0]
    for j in range(len(words)):
        if current_word[0] > words[j][0]:
            current_word = words[j]
    print(current_word)
    words.pop(words.index(current_word))
