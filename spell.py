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


class Alphabet(object):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.letters = dict()
        self.additional_letters = dict()

    def from_JSON(self, fp):
        a = json.load(fp)
        assert(type(a) == dict)
        assert("name" in a)
        assert("letters" in a)
        assert(type(a["letters"]) == dict)

        if("description" in a):
            self.description = a["description"]
        self.name = a["name"]

        # The letters are inserted into the dictionary as lower case letters:
        for letter in a["letters"]:
            self.letters[letter.lower()] = a["letters"][letter]

        if( ("additional_letters" in a) and (type(a["additional_letters"]) == dict)):
            self.additional_letters = a["additional_letters"]

    def has(self, letter):
        letter = letter.lower()
        return letter in self.letters or letter in self.additional_letters

    def get(self, letter):
        letter = letter.lower()
        if letter in self.letters:
            return self.letters[letter]
        if letter in self.additional_letters:
            return self.additional_letters[letter]

def spell(word, alphabet, mark_uppercase=False):
    for letter in word:
        if alphabet.has(letter):
            if mark_uppercase and letter.isupper():
                print("{} - Upper Case {}".format(letter, alphabet.get(letter)))
            else:
                print("{} - {}".format(letter, alphabet.get(letter)))
        else:
            print("{} - {}".format(letter, letter))

def main():
    parser = argparse.ArgumentParser(description='Spelling words for you.')
    parser.add_argument('words', metavar='WORD', nargs='+',
                       help='The word or words you want to be spelled.')
    parser.add_argument('-a', '--alphabet', default="NATO",
                       help='The spelling alphabet to use (NATO).')
    parser.add_argument('-u', '--upper', action='store_true',
                       help='Include notes for uppercase characters')
    
    args = parser.parse_args()

    alphabet = Alphabet()
    alphabet_filename = 'alphabets/{}.json'.format(args.alphabet)
    try:
        with open(alphabet_filename, encoding="utf-8") as f:
            alphabet.from_JSON(f)
    except:
        parser.error("Sorry, couldn't load the alphabet file {}.".format(alphabet_filename))

    for word in args.words:
        print('Spelling  "{}"  with the {} alphabet:'.format(word, args.alphabet))
        spell(word, alphabet, mark_uppercase=args.upper)

if __name__ == "__main__":
    main()

