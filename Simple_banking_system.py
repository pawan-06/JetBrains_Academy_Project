=======================================================================================================================================
#jetbrainsacademy.simplebankingsystem with database.project3
=======================================================================================================================================


import random
import sqlite3
cards = sqlite3.connect('card.s3db')
cur = cards.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card
            (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)'''), cards.commit()


def start():
    c = int(input('1. Create an account\n2. Log into account\n0. Exit\n'))
    if c == 1:
        return create()
    if c == 2:
        return login()
    if c == 0:
        print('\nBye!')


def create():
    new_card, pin = str(random.randrange(400000000000000, 400000009999999)), str(random.randint(0000, 9999)).zfill(4)
    luhn = 0
    for i in range(len(str(new_card))):
        if i % 2 == 0:
            luhn += int(new_card[i]) * 2 if int(new_card[i]) * 2 < 10 else int(new_card[i]) * 2 - 9
        if i % 2 != 0:
            luhn += int(new_card[i])
    checksum = 0
    while luhn % 10:
        checksum += 1
        luhn += 1
    new_card += str(checksum)
    cur.execute(f'''INSERT INTO card (number, pin) VALUES({new_card}, {pin})'''), cards.commit()
    print(f'\nYour card has been created\nYour card number:\n{new_card}\nYour card PIN:\n{pin}\n')
    return start()


def login():
    card_number = input('Enter your card number:\n')
    pin = input('Enter your PIN:\n')
    c = cur.execute('''SELECT number, pin FROM card WHERE number = {} AND pin = {}'''.format(card_number, pin))
    if c.fetchone():
        print('\nYou have successfully logged in!\n')
        return account(card_number)
    else:
        print('\nWrong card number or PIN!\n')
        return start()


def account(self):
    ch = input('''1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n''')
    if ch == '1':
        print(f'''\nBalance: {cur.execute(f'SELECT balance FROM card WHERE number = {self}').fetchone()[0]}\n''')
        return account(self)
    elif ch == '2':
        i = input('\nEnter income:\n')
        cur.execute(f'''UPDATE card SET balance = balance + {int(i)} WHERE number = {self}'''), cards.commit()
        print('Income was added!\n')
        return account(self)
    elif ch == '3':
        t = input('\nTransfer\nEnter card number:\n')
        luhn = 0
        for i in range(len(str(t))):
            if i % 2 == 0:
                luhn += int(t[i]) * 2 if int(t[i]) * 2 < 10 else int(t[i]) * 2 - 9
            if i % 2 != 0:
                luhn += int(t[i])
        if luhn % 10:
            print('Probably you made a mistake in the card number. Please try again!\n')
            return account(self)
        elif not cur.execute(f'SELECT number FROM card WHERE number = {t}').fetchone():
            print('Such a card does not exist\n')
            return account(self)
        elif t == self:
            print("You can't transfer money to the same account!\n")
            return account(self)
        else:
            print(cur.execute(f'SELECT balance FROM card WHERE number = {self}').fetchone())
            a = input('Enter how much money you want to transfer:\n')
            if int(a) > int(cur.execute(f'SELECT balance FROM card WHERE number = {self}').fetchone()[0]):
                print('Not enough money!\n')
                return account(self)
            else:
                cur.execute(f'UPDATE card SET balance = balance - {int(a)} WHERE number = {self}')
                cur.execute(f'UPDATE card SET balance = balance + {int(a)} WHERE number = {t}')
                cards.commit()
                print('Success!')
                return account(self)
    elif ch == '4':
        cur.execute(f'DELETE FROM card WHERE number = {self}'), cards.commit()
        print('The account has been closed!')
        return start()
    elif ch == '5':
        print('You have successfully logged out!\n')
        return start()
    elif ch == '0':
        print('\nBye!')
        return None
    else:
        print('Invalid Input')
        return account(self)

start()
