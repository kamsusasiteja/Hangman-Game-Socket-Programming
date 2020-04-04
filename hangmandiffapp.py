"""
Hangman program
"""

import random


def is_word_guessed(secretword, r_word, letters_guess):

    """
    In this function we are checking the letters guessed with the secret word. if the
    letter is present in the secret word, then the index and the corresponding values are appending
    to the empty list which were declare initially.if its Good guess then it will return true
    otherwise it will return false.
    """

    # print(secretword)
    index = []
    und = []

    if letters_guess in secretword:
        for i_iterable in enumerate(secretword):
            if secretword[i_iterable[0]] == letters_guess:
                index.append(i_iterable[0])
                und.append(letters_guess)
        for j_iterable in enumerate(index):
            r_word[index[j_iterable[0]]] = und[j_iterable[0]]
        print("Good guess:", " ".join(r_word))
        print("_ " * 9)
        return True
    return False


def letters_available(r_word, v_list, let, z_initial, y_initial):

    """
    this function helps to display the available letters for the suser to pick guess
    letter and will remove that guess from the existing set of alphabets
    """

    if let in v_list:
        if "_" in r_word:
            print("you have ", (z_initial) - (y_initial), "guesses left")
            v_list.remove(let)
    else:
        print("Oops you have already guessed that letter: ", " ".join(r_word))
        print("you have ", (z_initial) - (y_initial), "guesses left")


def letters_guessed(h_random, r_word):

    """
    this function is to take inputs from the user of guessed letters which will
    call another functions for checking the elements already present or not in the
    secret word. Also replaces the r_word (_) with new elements that are present in
    the secret word
    """

    y_initial = 1
    v_list = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    z_initial = 9

    while y_initial < 9:
        let = input("please guess a letter : ")
        let = let.lower()
        if let.isalpha() and len(let) == 1:
            if is_word_guessed(h_random, r_word, let):
                letters_available(r_word, v_list, let, z_initial, y_initial)
                if "_" not in r_word:
                    break
                else:
                    print("available letters :", "".join(v_list))
                    continue

            else:
                if let in v_list:
                    print("Oops! That letter is not in my word: ", " ".join(r_word))
                    print("_ " * 9)
                    if (z_initial)-(y_initial)-1>0:
                        print("you have ", (z_initial) - (y_initial) - 1, "guesses left")
                        v_list.remove(let)
                        print("available letters :", "".join(v_list))
                    y_initial = y_initial + 1
                    continue
                else:
                    print(
                        "Oops you have already guessed that letter: ", " ".join(r_word)
                    )
                    print("you have ", (z_initial) - (y_initial), "guesses left")
                    continue

        else:
            print("please enter again: ")
            print("_ " * 9)
    if "_" in r_word:
        print("_ " * 9)
        print("sorry, you ran out of guesses. The word was", h_random)
    else:
        print("congratulations, you won!")


def process():

    """
    we are opening the required file , reading that file and spliting it. After splitting the
    words in first element of the list we are importing random module for the usage of the random
    in-built functions like random.choice. we are displaying the required pattern by using print
    function. finally we are calling letters_guessed function for checking guessed letters with '
    secret word.
    """

    file = open("words.txt", "r")
    lines = file.readlines()
    g_split = lines[0].split()
    h_random = random.choice(g_split)
    print("welcome to the game, Hangman!")
    print("I am thinking of a word that is", len(h_random), "letters long.")
    print("_ " * 9)
    print("You have 8 guesses left")
    print("available letters : abcdefghijklmnopqrstuvwxyz")
    r_word = "_" * (len(h_random))
    r_word = list(r_word)
    letters_guessed(h_random, r_word)


process()