import random
import json

def getRandomPokemonID(area):
	return {
		1 : random.randrange(1,50,1),
		2 : random.randrange(51,100,1),
		3 : random.randrange(101,150,1),
        -1 : random.randrange(1,151,1)
	} [area]

def getRandomPokemon(area):
    with open('gen1.json') as pokelist:
        plist = json.load(pokelist)
    
    ID = getRandomPokemonID(area)
    return (plist["name"][ID])