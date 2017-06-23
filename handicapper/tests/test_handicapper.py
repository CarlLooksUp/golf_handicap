import pytest
from handicapper.handicapper import Handicapper
from handicapper.errors import *

@pytest.fixture
def h():
    return Handicapper()

def test_differential(h):
    score, rating, slope = (61, 60, 113)
    differential = h.differential(score, rating, slope)
    assert differential == 1

def test_round_limiter(h):
    results = { 4: 0,
                5: 1,
                6: 1,
                7: 2,
                8: 2,
                9: 3,
                10: 3,
                11: 4,
                12: 4,
                13: 5,
                14: 5,
                15: 6,
                16: 6,
                17: 7,
                18: 8,
                19: 9,
                20: 10,
                21: 10,
                22: 10,
                23: 10,
                24: 10 }
    for size, result in results.items():
        h.rounds = [[]] * size
        if size < 5:
            with pytest.raises(NotEnoughRoundsError):
                h.trimmed_rounds(h.rounds)
        else:
            assert len(h.trimmed_rounds(h.rounds)) == result

def test_round_date_sort(h):
    date_1 = {'DATE': '5/8/13', 'SCORE': 61, 'RATING': 60, 'SLOPE': 113}
    date_2 = {'DATE': '1/8/14', 'SCORE': 61, 'RATING': 60, 'SLOPE': 113}
    date_3 = {'DATE': '3/28/16', 'SCORE': 61, 'RATING': 60, 'SLOPE': 113}
    date_4 = {'DATE': '4/18/17', 'SCORE': 61, 'RATING': 60, 'SLOPE': 113}
    scrambled_dates = [date_3, date_2, date_4, date_1]

    h.rounds = scrambled_dates
    h.sort_rounds()

    assert h.rounds == [date_1, date_2, date_3, date_4]

def test_handicap():
    h = Handicapper(filename = 'data/rounds.csv')
    assert h.handicap() == 19.97
