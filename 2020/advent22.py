from copy import deepcopy


def parse(input):
    return [list(map(int, split.split("\n")[1:])) for split in input.split("\n\n")]


def f1(input):
    deck1, deck2 = deepcopy(input)

    while len(deck1) and len(deck2):
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)
    winner = deck1 or deck2
    return sum((i + 1) * v for i, v in enumerate(reversed(winner)))


def f2(input):
    game_count = 0

    def hash(deck):
        return " ".join([str(i) for i in deck])

    def play_game(deck1, deck2):
        nonlocal game_count
        game = (game_count := game_count + 1)
        seen = set()
        round = 0
        print(f"\n=== Game {game} ===\n")

        while len(deck1) > 0 and len(deck2) > 0:
            keys = "p1:" + hash(deck1), "p2:" + hash(deck2)
            if keys[0] in seen or keys[1] in seen:
                return 1  # player 1 wins game
            round += 1
            seen.update(keys)
            print(f"-- Round {round} (Game {game}) --")
            print(f"Player 1's deck {keys[0]}")
            print(f"Player 2's deck {keys[1]}")
            card1, card2 = deck1.pop(0), deck2.pop(0)
            print(f"Player 1 plays {card1}")
            print(f"Player 2 plays {card2}")

            if len(deck1) >= card1 and len(deck2) >= card2:
                print("Playing a sub-game to determine the winner...")
                winner = play_game(deck1[:card1], deck2[:card2])
                print(f"...anyway, back to game {game}.")
            else:
                winner = 1 if card1 > card2 else 2

            print(f"Player {winner} wins round {round} of game {game}\n")
            if winner == 1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)

        winner = 1 if len(deck1) else 2
        print(f"The winner of of game {game} is {winner}\n")
        return winner

    winner = play_game(*input)
    deck = input[winner - 1]
    return sum((i + 1) * v for i, v in enumerate(reversed(deck)))
