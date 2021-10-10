from bui_src.algorithm import MonteCarlo
from bui_src.game import GameLogic, GameState
from bui_src.server import ServerHandler

import random

from bui_src.definition.enumeration import CharacterStatus

DEPTH = 2
NUMBER_SIMULATED_GAMES = 70

if __name__ == '__main__':
    with ServerHandler() as server:
        game_logic = GameLogic()
        character = None

        while True:
            question = server.receive()
            if question:
                if question['question type'] == "select character":
                    character = None
                monte_carlo = MonteCarlo(game_logic, GameState(question['game state'], character, question['question type']), DEPTH, NUMBER_SIMULATED_GAMES)

                monte_carlo.built()
                timeline = monte_carlo.get_best_choice()

                choice = timeline[0]
                if question['question type'] == "select character":
                    character = choice
                elif choice == CharacterStatus.ACTIVATED:
                    choice = 1
                elif choice == CharacterStatus.NOT_ACTIVATED:
                    choice = 0
                count = 0
                for possibility in question['data']:
                    if question['question type'] == "select character":
                        if possibility['color'] == choice:
                            response = count
                            break
                    else:
                        if possibility == choice:
                            response = count
                            break
                    count += 1

                if count >= len(question['data']):
                    response = random.randint(0, len(question['data'])-1)

                server.send(response)
            else:
                break
