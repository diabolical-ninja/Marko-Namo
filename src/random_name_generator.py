"""Main class to generate random names"""

from typing import List, Tuple
import random

import src.utils as ut


class RandomBusinessName:
    def __init__(
        self,
        name_length: int,
        number_of_names: int,
        domain_extensions: List[str],
        training_words: List[str],
        n_grams: List[int] = [1, 2, 3],
        godaddy=None,
    ) -> None:
        self.name_length = name_length
        self.number_of_names = number_of_names
        self.n_grams = n_grams
        self.domain_extensions = domain_extensions
        self.training_words = training_words
        self.godaddy = godaddy

    def create_random_name(self) -> Tuple[list, list]:
        """Main method to generate random names.

        Returns:
            Tuple[list, list]:
                - Created Names
                - If goDaddy credentials provided, price & availability info for each available name
        """
        random_words = [
            self.create_random_word(self.training_words, self.name_length)
            for x in range(0, self.number_of_names)
        ]

        created_names = []
        available_domain_names = []

        # If no goDaddy info is provided simply return the randomly created words
        if self.godaddy is None:
            created_names = random_words
        else:
            available_domains = [
                x
                for x in self.godaddy.check_domain_availability(
                    random_words, self.domain_extensions
                )["domains"]
            ]

            # Check if all domains are available
            for rw in random_words:
                all_available_extensions = [
                    x
                    for x in available_domains
                    if x["domain"].split(".")[0] == rw and x["available"]
                ]
                if len(all_available_extensions) == len(self.domain_extensions):
                    for x in all_available_extensions:
                        x.update({"price": x["price"] / 1000000})
                    available_domain_names.extend(all_available_extensions)
                    created_names.append(rw)

        print("Generated Business Names:")
        [print(x) for x in created_names]
        if len(available_domain_names) == 0:
            print("Did not check for domain name availability")
        else:
            [print(x) for x in available_domain_names]

        return (
            created_names,
            available_domain_names if len(available_domain_names) > 0 else None,
        )

    def word_letter_frequency(self, word: str) -> dict:
        """For a given word, build a frequency table for the proceeding characters using a
         lightweight markov approach.

        It will examine n-grams both as the reference point and the characters following.
        Eg, with a sample word of "abcd"
            - n-gram of 1:
                {
                    "a": ["b"],
                    "b": ["c"],
                    "c": ["d"],
                    "d": [None],
                }
            - n-gram of 2:
                {
                    "ab": ["cd"],
                    "bc": ["d"],
                    "cd": [None]
                }
            - etc

        Args:
            word (str): The word to build a frequency table for

        Returns:
            dict:
                - Keys correspond to the n-gram/s charaters
                - Values are lists of the proceeding n-gram/s characters
        """
        frequency_table = {}
        for i in range(0, len(word)):
            for j in self.n_grams:
                if len(word) >= i + j:
                    if word[i : i + j] not in frequency_table:
                        frequency_table[word[i : i + j]] = []

                    for gram_size in self.n_grams:
                        next_letters = (
                            None
                            if i + j + gram_size > len(word)
                            else word[i + j : i + j + gram_size]
                        )
                        frequency_table[word[i : i + j]].append(next_letters)

        return frequency_table

    def create_random_word(
        self, reference_words: list, maximum_word_length: int = 100
    ) -> str:
        """Builds a random word of length N based on the learnt frequency table

        Args:
            reference_words (list): Words to learn from
            maximum_word_length (int, optional): How long the word is allowed to be. Note:
                - Word can be longer than max if the next random addition is an n-gram exceeding
                  the delta between the current word length and the max value
                - Defaults to 100.

        Returns:
            str: Randomly generated word
        """
        term_frequencies = {}
        for word in reference_words:
            tmp = self.word_letter_frequency(word)
            term_frequencies = ut.merge_dictionaries(term_frequencies, tmp)

        letter = random.choice(list(term_frequencies))
        word = letter

        while letter is not None and len(word) < maximum_word_length:
            letter = random.choice(term_frequencies[letter])
            word = f"{word}{letter if letter else ''}"

        return word.strip()
