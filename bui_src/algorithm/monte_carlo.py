import copy
from ..definition import AbstractGameLogic, AbstractGameState
from multiprocessing import Process, RawValue, Lock
from threading import Thread
from random import choice

from ..definition.enumeration import InternalQuestion


class MonteCarlo:

    def __init__(self, game_logic: AbstractGameLogic, game_state: AbstractGameState, depth: int, number_simulated_games: int) -> None:
        self._depth = depth
        self._game_logic = game_logic
        self._game_state = game_state
        self._number_simulated_games = number_simulated_games
        self._best_timeline = {}
        self._lock = Lock()
        self._win = 0
        self._serialized = []

    def _simulate(self, game_state: AbstractGameState):
        res = None
        while res != InternalQuestion.END_GAME:
            res, moves = self._game_logic.get_next_possibilities(game_state)
            if len(moves) > 0 and moves[0] == 'inspector':
                with self._lock:
                    self._win += 1
                return
            if len(moves) > 0:
                self._game_logic.apply_possibility(res, choice(moves), game_state)
            else:
                self._game_logic.apply_possibility(res, moves, game_state)

    def _built(self, game_state: AbstractGameState, path: tuple, depth: int) -> None:
        if depth == 0:
            self._win = 0
            threads = []
            for i in range(80):
                new_game_state = copy.deepcopy(game_state)
                t = Thread(target=self._simulate, args=(new_game_state,))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            self._best_timeline[self._win/80] = path
            gs_serialized = game_state.serialize()
            gs_serialized.append(self._win/80)
            self._serialized.append(gs_serialized)
            return

        question, moves = self._game_logic.get_next_possibilities(game_state)
        if question == InternalQuestion.END_GAME:
            if moves[0] == 'inspector':
                self._best_timeline[1] = path
            else:
                self._best_timeline[0] = path
            return

        if not moves:
            game_state_copied = copy.deepcopy(game_state)
            self._built(game_state_copied, path + (None,), depth - 1)

        for move in moves:
            game_state_copied = copy.deepcopy(game_state)

            self._game_logic.apply_possibility(question, move, game_state_copied)
            self._built(game_state_copied, path + (move,), depth - 1)


    def built(self):
        self._built(self._game_state, tuple(), self._depth)
        self._game_state.write_csv(self._serialized)

    def get_best_choice(self):
        max = 0
        best_moves = None
        best_key = 0
        for key in self._best_timeline:
            if max <= key:
                max = key
                best_moves = self._best_timeline[key]
        #print(_moves)
        #print('\nThe best time line is ' + str(best_moves) + ' with ' + str(best_key) + '% winrate')
        #print('\nChoices are :\n')
        #print(self._best_timeline)
        return best_moves

