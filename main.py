import random
import time

monsters = dict()
with open('monsters.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        data = line[:len(line) - 1].split(',')
        monsters[data[1]] = [data[0], *data[2:]]

stats = ['HP', 'Physical', 'Magic', 'Armor', 'Magic Res', 'Movement', 'Regen']


def delay():
    time.sleep(0.5)


def damage_calc(atk, df):
    noise = random.uniform(0, 10)
    return atk * 1 / (1 + df / 100) + noise


def assign_monsters(n):
    p1 = set()
    p2 = set()
    while len(p1) < n:
        p1.add(random.choice(list(monsters.keys())))
    while len(p2) < n:
        p2.add(random.choice(list(monsters.keys())))
    return list(p1), list(p2)


def monster_desc(mons_stats):
    print(f"Origin: {mons_stats[1]}")
    print(f"Description: {mons_stats[2]}")
    print(*[stats[i] + ': ' + str(mons_stats[i+3]) for i in range(7)])


def game_loop(p1, p2):
    g = str(input("Do you want a tutorial? y/n"))
    if g == 'y':
        guide()
    d = str(input("Do you want descriptions on? y/n"))

    running = True
    print("What monster do you want to play?")
    p1_mons = str(input(p1))
    p2_mons = random.choice(list(p2))

    print('')

    print(f"Player 1 picks {p1_mons}!")
    p1_mons_stats = monsters[p1_mons]
    p1_mons_stats[3:] = [int(s) + 1 for s in p1_mons_stats[3:]]
    p1_hp = 50 + 2 * p1_mons_stats[3]

    if d == 'y':
        monster_desc(p1_mons_stats)
    delay()

    print('')
    print('')

    print(f"Player 2 picks {p2_mons}!")
    p2_mons_stats = monsters[p2_mons]
    p2_mons_stats[3:] = [int(s)+1 for s in p2_mons_stats[3:]]
    p2_hp = 50 + 2 * p2_mons_stats[3]

    if d == 'y':
        monster_desc(p2_mons_stats)
    delay()

    while running:

        print('')
        print('')
        print('')
        print('')

        print("Choose your attack:")
        atk_type = int(input("1: Physical, 2: Magic"))

        print(f"{p1_mons} attacks {p2_mons}!")

        if atk_type == 1:
            dodge = random.uniform(0, 1.0) < 0.01 * p2_mons_stats[8]
            dmg = 1.1 * damage_calc(p1_mons_stats[4], p2_mons_stats[6])
        else:
            dodge = False
            dmg = damage_calc(p1_mons_stats[5], p2_mons_stats[7])

        if dodge:
            print(f"{p2_mons} has dodged the attack!")
        else:
            p2_hp -= dmg
            p2_hp = 0 if p2_hp < 0 else p2_hp
            print(f"{p2_mons} has taken {round(dmg, 2)} damage! {p2_mons} has {round(p2_hp, 2)} hp left.")

        print('')
        delay()
        delay()
        delay()

        if p2_hp == 0:
            print(f"{p2_mons} has retreated!")
            p2.remove(p2_mons)

            if len(p2) <= 0:
                running = False
                print("Player 1 has won!")
                break

            p2_mons = random.choice(p2)
            p2_mons_stats[3:] = [int(s) for s in p2_mons_stats[3:]]
            p2_hp = 50 + 2 * p2_mons_stats[3]
            print(f"Player 2 picks {p2_mons}!")

            if d == 'y':
                monster_desc(p2_mons_stats)
            delay()

        else:
            atk_type = random.randint(1, 2)
            print(f"{p2_mons} attacks {p1_mons}!")

            if atk_type == 1:
                dodge = random.uniform(0, 1.0) < 0.01 * p1_mons_stats[8]
                dmg = 1.1 * damage_calc(p2_mons_stats[4], p1_mons_stats[6])
            else:
                dodge = False
                dmg = damage_calc(p2_mons_stats[5], p1_mons_stats[7])

            if dodge:
                print(f"{p1_mons} has dodged the attack!")
            else:
                p1_hp -= dmg
                p1_hp = 0 if p1_hp < 0 else p1_hp
                print(f"{p1_mons} has taken {round(dmg, 2)} damage! {p1_mons} has {round(p1_hp, 2)} hp left.")

        if p1_hp == 0:
            delay()
            print(f"{p1_mons} has retreated!")
            p1.remove(p1_mons)

            if len(p1) <= 0:
                running = False
                print("Player 2 has won!")
                break

            print("What monster do you want to play?")
            p1_mons = str(input(p1))
            p1_mons_stats[3:] = [int(s) for s in p1_mons_stats[3:]]
            p1_hp = 50 + 2 * p1_mons_stats[3]
            print(f"Player 1 picks {p1_mons}!")

            if d == 'y':
                monster_desc(p1_mons_stats)
            delay()

        p1_hp = min(p1_hp + 0.1 * p1_mons_stats[9], 50 + 2 * p1_mons_stats[3])
        p2_hp = min(p2_hp + 0.1 * p2_mons_stats[9], 50 + 2 * p2_mons_stats[3])
        delay()


def guide():
    print("This game is a turn based text game")
    print("Your objective is to defeat your all monsters on the enemies team")
    delay(), delay(), delay()
    print("Each monster has various stats, each ranging from 0-30")
    print("HP is the health each monster has, and regen is how much the monster heals each round")
    delay(), delay(), delay()
    print("There are 2 types of attacks: Physical and Magic")
    print("Each monster has does different Physical and Magical damage, and has varying resistance to each attack")
    print("Physical does more damage, but can be dodged by the enemy, dependent on the Movement stat")


p1, p2 = assign_monsters(3)

game_loop(p1, p2)


