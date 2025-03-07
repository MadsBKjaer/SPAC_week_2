from string import ascii_lowercase as alphabet
import enchant
from random_word import RandomWords
from collections import defaultdict


class Wordle:
    word_dictionary: enchant.Dict
    word_generator: RandomWords
    correctly_placed_letters: defaultdict[str]
    incorrectly_placed_letters: defaultdict[list[str]]
    unused_letters: list[str]
    wrong_letters: list[str]
    correct_letters: list[str]
    target_word: str
    word_length: int
    keep_playing: bool
    attempts: int

    def __init__(self, language: str = "en_US") -> None:
        self.word_generator = RandomWords()

        if enchant.dict_exists(language):
            self.word_dictionary = enchant.Dict(language)
        else:
            print(
                f"Unsupported language: {language}. Please use one from {enchant.list_languages()}"
            )
            return

        self.init_game()

    def init_game(self) -> None:
        self.correctly_placed_letters = defaultdict(lambda: "[]")
        self.incorrectly_placed_letters = defaultdict(lambda: [])
        self.wrong_letters = []
        self.correct_letters = []
        self.unused_letters = list(alphabet.upper())
        self.target_word = self.word_generator.get_random_word().upper()

        while not self.word_dictionary.check(self.target_word):
            self.target_word = self.word_generator.get_random_word().upper()

        self.word_length = len(self.target_word)
        self.attempts = 0

        while self.try_word():
            pass
        self.request_new_game()

    def print_game_state(self) -> None:
        print(
            f"\nUnused: {self.unused_letters}\n"
            f"Wrong: {self.wrong_letters}\n"
            f"Correct: {self.correct_letters}\n"
            f"Incorrectly placed: {[self.incorrectly_placed_letters[i] for i in range(self.word_length)]}\n"
            f"Correctly placed: {[self.correctly_placed_letters[i] for i in range(self.word_length)]}\n"
        )

    def check_letter_placement(
        self, letter: str, placement: int, letter_count: int
    ) -> None:

        for _ in range(
            min(
                self.target_word.count(letter) - self.correct_letters.count(letter),
                letter_count - self.correct_letters.count(letter),
            )
        ):
            self.correct_letters.append(letter)
        self.correct_letters.sort()

        if self.target_word[placement] == letter:
            self.correctly_placed_letters[placement] = letter
            return

        if letter not in self.incorrectly_placed_letters[placement]:
            self.incorrectly_placed_letters[placement].append(letter)

    def request_new_game(self) -> None:
        if input("New game? (y/n) ") == "y":
            self.init_game()

    def try_word(self) -> bool:
        word = input(f"Type word of length {self.word_length} or 'q' to quit. ").upper()
        if word == "Q":
            print(
                f"You gave up after {self.attempts} attempts. The correct word was {self.target_word}."
            )
            return False

        if word == "I AM A FILTHY CHEATER":
            print(f"Correct word: {self.target_word}")
            return True

        if len(word) != self.word_length:
            print(
                f"{word} is the wrong length. Expected word of length {self.word_length}."
            )
            self.print_game_state()
            return True

        if not self.word_dictionary.check(word):
            print(f"{word} is not in the dictionary.")
            self.print_game_state()
            return True

        if word == self.target_word:
            print(
                f"Congratulations the correct word was {self.target_word}! You took {self.attempts} attempts."
            )
            return False

        self.attempts += 1
        for placement, letter in enumerate(word):
            if letter in self.unused_letters:
                self.unused_letters.remove(letter)

            if letter in self.target_word:
                letter_count: int = word.count(letter)
                self.check_letter_placement(letter, placement, letter_count)
                continue

            if letter not in self.wrong_letters:
                self.wrong_letters.append(letter)
                self.wrong_letters.sort()

        self.print_game_state()
        return True


if __name__ == "__main__":
    wordle = Wordle()
