def options():
    file = open('saves.txt', 'w')
    file.write('''hp = 5
    dmg = 1
    level = 0
    coins = 0
    regeneration = 1''')
    file.close()
