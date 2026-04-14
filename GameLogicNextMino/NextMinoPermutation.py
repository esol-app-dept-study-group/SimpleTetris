import itertools
import random

from SimpleTetris.TetriminoDef import TetriminoType

# 5040通り
all_patterns = list(itertools.permutations(TetriminoType))


def get_patterns(index: int) -> tuple:
    #指定されたインデックス(0～5039)に対応する順列を返す
    return all_patterns[index]


def get_random_permutation() -> tuple:
    index = random.randint(0, len(all_patterns) - 1)
    return get_patterns(index)
