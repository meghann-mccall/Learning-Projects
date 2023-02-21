from classes.deck import Deck
import random

bicycle = Deck()

class PlayerHand:
    def __init__(self):
        self.card1 = deal()
        self.card2 = deal()
        self.card3 = deal()
        self.card4 = deal()
        self.card5 = deal()

def deal():
    #pluck a random card from the bicycle deck and return it, then remove that card from the deck
    c = random.randrange(len(bicycle.cards))
    card = bicycle.cards[c]
    # print(f"{card.string_val} of {card.suit}")
    del bicycle.cards[c]
    return card

def converthand(hand):
    #check the player's hand for any duplicate cards by creating a dictionary that counts the number of each type of card owned
    new_hand = [hand.card1, hand.card2, hand.card3, hand.card4, hand.card5]
    cardtable = {}
    for card in new_hand:
        keys = cardtable.keys()
        cardvalue = card.point_val
        if cardvalue not in keys:
            cardtable.update({cardvalue: 1})
            #if there is not already a card with this number in the dictionary, add one
        else:
            for key, count in cardtable.items():
                if (key == cardvalue):
                    count += 1
                    cardtable.update({key: count})
                    #if a duplicate is found, increase its count in the dictionary
    return cardtable

playerlist = {}
scoreboard = {}
def build_player_list(name, playerhand):
    playerlist.update({name: playerhand})
    scoreboard.update({name: 0})



def initializePlayer(playername):
    name = playername
    playername = PlayerHand()
    playername = converthand(playername)
    build_player_list(name, playername)
    return playername


def takeTurn(playerhand, playername):
    match = False
    delcard = 0

    if not bicycle.cards:
        gameovermsg = "The game has ended, no cards left in the pool"
        print(gameovermsg)
        winnerscore = 0
        winnername = ""
        for name, score in scoreboard.items():
            if (score > winnerscore):
                winnerscore = score
                winnername = name
            elif (score == winnerscore):
                winnername = winnername + " and " + name
                winnername = "a tie betweeen " + winnername
        winnerscore = str(winnerscore)
        winnermsg = "Winner is " + winnername + " with a score of " + winnerscore
        print(winnermsg)
        gameover = "Game Over"
        return gameover

    #first, check if there are any quads of a card. if so, discard them
    print(f"{playername}'s Turn!")
    for card, count in playerhand.items():
        if (count > 3):
            print(f"{playername} got a match of {card}")
            match = True
            delcard = card
    if match:
        del playerhand[delcard]
        for name, score in scoreboard.items():
            if (name == playername):
                score +=1
                scoreboard.update({playername: score})

    #if the player has no cards left, they won. 
    if not playerhand:
        gameovermsg = playername + " has no cards left! " + playername + " is the winner!"
        print(gameovermsg)
        gameover = "Game Over"
        return gameover
    else:
    #if player still has cards left, choose a cardnum and other player to ask for cards
    #choose the first cardnum that player already has the most cards of. If no duplicates, choose the first card in the player's hand
        highcardcount = 0
        mostcards = 0
        for card, count in playerhand.items():
            if (count > highcardcount):
                highcardcount = count
                mostcards = card
        # print(mostcards)

    #choose the other player at random, but cannot choose self
        newplayerlist = {}
        for key, value in playerlist.items():
            if (key != playername):
                newplayerlist.update({key: value})
        #print(newplayerlist)
        otherplayername, otherplayerhand = random.choice(list(newplayerlist.items()))
        #print(otherplayername, otherplayerhand, mostcards)

        passedcards = checkotherplayershand(otherplayername, otherplayerhand, mostcards)
        if not passedcards:
            print("Go Fish!")
            playerhand = gofish(playerhand)
            playerlist.update({playername: playerhand})
        else:
            highcardcount += passedcards[1]
            playerhand.update({mostcards: highcardcount})
            playerlist.update({playername: playerhand})
            print(f"{playername} got {passedcards[1]} cards with number {mostcards} from {otherplayername} ")
    return playerhand

def checkotherplayershand(playername, playerhand, mostcards):
    passedcards = []
    found = False
    for card, count in playerhand.items():
        if (card == mostcards):
            passedcards.append(card)
            passedcards.append(count)
            found = True
    if found:
        del playerlist[playername][mostcards]
    # print(playerlist)
    # print(passedcards)
    return passedcards

def gofish(playerhand):
    newcard = deal()
    found = False
    checknum = newcard.point_val
    # print(checknum)
    #if cardnum already exists in playerhand, increase count
    for key, value in playerhand.items():
        if (checknum == key):
            value +=1
            found = True
            playerhand.update({key: value})
    if not found:
        playerhand.update({checknum: 1})
    return playerhand

def Play(indicator):
    if (indicator == "Game Over"):
        print(scoreboard)
        return "Game Over"
    else: 
        for player, hand in playerlist.items():
            turnresults = takeTurn(hand, player)
            if (turnresults == "Game Over"):
                results = "Game Over"
                break
            else:
                print(f"{player}: {turnresults}")
                results = "b"
        Play(results)




Meghann = initializePlayer("Meghann")
Kaitlin = initializePlayer("Kaitlin")
# Searc = initializePlayer("Searc")
# Mom = initializePlayer("Mom")
print(playerlist)
Play("a")