import random
import sqlite3
import time

def initialize_db():
    with sqlite3.connect('game_scores.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                name TEXT,
                guesses INTEGER,
                time REAL,
                score REAL
            )
        ''')

def insert_score(name, guesses, total_time):
    score = guesses + total_time / 10
    with sqlite3.connect('game_scores.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO scores (name, guesses, time, score) VALUES (?, ?, ?, ?)
        ''', (name, guesses, total_time, score))
        conn.commit()

def get_best_score():
    with sqlite3.connect('game_scores.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, guesses, time, score
            FROM scores
            ORDER BY score ASC
            LIMIT 1
        ''')
        return cursor.fetchone()

def generate_number():
    digits = random.sample(range(10), 4)
    return ''.join(map(str, digits))

def check_guess(secret, guess):
    plus = sum(1 for s, g in zip(secret, guess) if s == g)
    minus = sum(1 for g in guess if g in secret) - plus
    return '+' * plus + '-' * minus

def play_game():
    name = input('Enter your name: ')
    secret_number = generate_number()
    guesses, start_time = 0, time.time()

    while True:
        guess = input('Enter your guess: ')
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            print('Invalid input. Enter a 4-digit number with unique digits.')
            continue

        guesses += 1
        result = check_guess(secret_number, guess)
        print(result)

        if result == '++++':
            total_time = time.time() - start_time
            print(f'Congratulations, {name}! You guessed the number in {guesses} guesses and {total_time:.2f} seconds.')
            insert_score(name, guesses, total_time)
            break

    best_score = get_best_score()
    if best_score:
        print(f'Best score: {best_score[0]} with {best_score[1]} guesses and {best_score[2]:.2f} seconds (score: {best_score[3]:.2f})')

if __name__ == '__main__':
    initialize_db()
    while True:
        play_game()
        if input('Do you want to play again? (y/n): ').lower() != 'y':
            break
