from constants import CARD_PAIRS_QUANTITY
import random
import uuid

def generate_card_pair(i):
    card = { "card_id": uuid.uuid4(), "card_pair": i, "turn_turned": False }
    return [card, card.copy()]

cards = [generate_card_pair(i + 1) for i in range(CARD_PAIRS_QUANTITY)]
cards = [card for card_pair in cards for card in card_pair] # Flat

for i in range(len(cards)):
    random_index = random.randint(0, len(cards) - 1)
    card_to_shuffle_with = cards[random_index]
    cards[random_index] = cards[i]
    cards[i] = card_to_shuffle_with

for j in range(8):
    for i in range(5):
        print(cards[j * 5 + i]['card_pair'], end=" ")
    print("")