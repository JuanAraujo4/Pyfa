from time import sleep
from base.base import return_player

introducao = """----- Jogo Muito Massa -----"""

print("-" * len(introducao))

for letra in introducao:
    print(letra, end="")
    if letra != " ":
        sleep(0.22)

print()
print("-" * len(introducao))

print(return_player("haaland"))

