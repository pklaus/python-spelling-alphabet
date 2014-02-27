#!/usr/bin/env python

import argparse
import json

def spell(word, alphabet, mark_uppercase=False):
    for letter in word:
        if letter in alphabet["letters"]:
            if mark_uppercase and letter.isupper():
                print("{} - Upper Case {}".format(letter, alphabet["letters"][letter]))
            else:
                print("{} - {}".format(letter, alphabet["letters"][letter]))
        else:
            print("{} - {}".format(letter, letter))

def load_alphabet(fp):
    alphabet = json.load(fp)
    assert(alphabet["name"])
    assert(alphabet["letters"])
    assert(type(alphabet["letters"]) == dict)
    # Now we insert the lower case letters to our dictionary.
    # They are left out in the JSON file to make it more readable.
    letters_lower = dict()
    for letter in alphabet["letters"]:
        letters_lower[letter.lower()] = alphabet["letters"][letter]
    alphabet["letters"].update(letters_lower)
    return alphabet

def main():
    parser = argparse.ArgumentParser(description='Spelling words for you.')
    parser.add_argument('words', metavar='WORD', nargs='+',
                       help='an integer for the accumulator')
    parser.add_argument('-a', '--alphabet', default="NATO",
                       help='The spelling alphabet to use (NATO).')
    parser.add_argument('-u', '--upper', action='store_true',
                       help='Include notes for uppercase characters')
    
    args = parser.parse_args()

    try:
	with open('alphabets/{}.json'.format(args.alphabet)) as f:
            alphabet = load_alphabet(f)
    except:
        raise
        parser.error("Sorry, I don't trust the alphabet file.")

    for word in args.words:
        print("Spelling  {}  with the {} alphabet:".format(word, args.alphabet))
        spell(word, alphabet, mark_uppercase=args.upper)

if __name__ == "__main__":
    main()
