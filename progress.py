def load_progress():
    global hero, LEVEL
    with open('saves.txt', encoding='utf8') as f:
        text = f.readlines()

    text = [i.strip() for i in text]
    for i in range(len(text)):
        if i == 0:
            hp = text[i].split(' = ')[1]
            hero.hp = hp
        if i == 1:
            dmg = text[i].split(' = ')[1]
            hero.dmg = dmg
        if i == 2:
            LEVEL = text[i].split(' = ')[1]
        if i == 3:
            coins = text[i].split(' = ')[1]
            hero.coins = coins


def save_progress():
    with open('saves.txt', 'wt', encoding='utf8') as f:
        f.write(f'hp = {hero.hp}\ndmg = {hero.dmg}\nlevel = {LEVEL}\ncoins = {hero.coins}')

