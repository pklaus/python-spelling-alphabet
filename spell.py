#!/usr/bin/env python3

# spell.py - spelling alphabet for Python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    if "additional_letters" in alphabet:
        alphabet["letters"].update(alphabet["additional_letters"])
    return alphabet

def main():
    parser = argparse.ArgumentParser(description='Spelling words for you.')
    parser.add_argument('words', metavar='WORD', nargs='+',
                       help='The word or words you want to be spelled.')
    parser.add_argument('-a', '--alphabet', default="NATO",
                       help='The spelling alphabet to use (NATO).')
    parser.add_argument('-u', '--upper', action='store_true',
                       help='Include notes for uppercase characters')
    
    args = parser.parse_args()

    try:
        with open('alphabets/{}.json'.format(args.alphabet), encoding="utf-8") as f:
           alphabet = load_alphabet(f)
    except:
        raise
        parser.error("Sorry, I don't trust the alphabet file.")

    for word in args.words:
        print('Spelling  "{}"  with the {} alphabet:'.format(word, args.alphabet))
        spell(word, alphabet, mark_uppercase=args.upper)

if __name__ == "__main__":
    main()
