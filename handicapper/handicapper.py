import csv
import sys
from datetime import datetime
from errors import *

class Handicapper:

    def __init__(self, filename = ""):
        if filename != "":
            self.read_rows_file(filename)

    def read_rows_file(self, filename):
        rounds = []
        with open(filename, 'rU') as roundsfile:
            reader = csv.DictReader(roundsfile)
            for row in reader:
                rounds.append(row)
        self.rounds = rounds
        self.sort_rounds()
        if len(self.rounds) > 20:
            self.rounds = self.rounds[-20:]

    def sort_rounds(self):
        self.rounds.sort(key = lambda x: datetime.strptime(x['DATE'], '%m/%d/%y'))

    def differential(self, score, rating, slope):
        return ((float(score) - float(rating)) * 113 / float(slope))

    def trimmed_rounds(self, rounds):
        if type(rounds) is not list or len(rounds) < 5:
            raise NotEnoughRoundsError
        elif len(rounds) < 16:
            size = (len(rounds) + 1) / 2 - 2
        elif len(rounds) < 21:
            size = (len(rounds) - 10)
        else:
            size = 10
        return rounds[:size]

    def handicap(self):
        #clone list before sorting destructively
        round_set = self.rounds[:]
        for _round in round_set:
            _round['DIFFERENTIAL'] = self.differential(_round['SCORE'], _round['RATING'], _round['SLOPE'])

        round_set.sort(key = lambda x: x['DIFFERENTIAL'])
        round_set = self.trimmed_rounds(round_set)
        handicap = reduce(lambda holdover, _round:_round['DIFFERENTIAL'] + holdover, round_set, 0) / float(len(round_set)) * 0.96

        return round(handicap, 2)

if __name__ == "__main__":
    h = Handicapper(filename = sys.argv[1])
    print h.handicap()
