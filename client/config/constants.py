from enum import Enum

CARD_COLUMNS = 5
CARD_PAIRS_QUANTITY = 20

Results = Enum('Results', ['YOU_WON', 'OTHER_WON', 'DRAW', 'KEEP_PLAYING'])
results_text = { Results.YOU_WON: "Você ganhou", Results.OTHER_WON: "Adversário ganhou", Results.DRAW: "Empate" }
