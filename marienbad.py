import copy
import pickle  #lib to save data struct in file

class node:
    def __init__(self, board):
        self.board = board
        self.moves = []

    def add_move(self, move_obj):
        self.moves.append(move_obj)

    def best_move(self):
        result = None
        for i in self.moves:
            if result == None or result.points < i.points:
                result = i
        return result

    def to_print(self):
        result = str(self.plateau) + "->"
        for i in self.moves:
            result += "\n\t" + i.to_print()
        return result

class move:
    def __init__(self, move):
        self.move = move
        self.points = 0.

    def to_print(self):
        return "move:" + str(self.move) + "-points:" + str(self.points)

class Game:
    def __init__(self, player1, player2, first):
        self.board = [7,5,3,1]
        self.who = first
        self.player = [player1, player2]

    def show(self):
        j = 0
        print("### BOARD ###")
        for i in self.board:
            print(str(j) + " - " + "I" * i)
            j = j + 1
        print("#############")

    def possible_moves(self):
        moves = []
        for i in range(len(self.board)):
            for j in range(1, self.board[i] + 1):
                move = (i,j)
                moves.append(move)
        return moves

    def play(self, move):
        line = move[0]
        number = move[1]
        if self.board[line] >= number:
            self.board[line] -= number
            self.who += 1
            self.who %= 2

    def win(self, player):
        return self.player[self.who] == player

    def over(self):
        return sum(self.board) == 1

    def turn(self):
        return self.player[self.who]

def create_player(number):
    print("Joueur " + str(number) + "? (0-Human; 1-Bot) :")
    j = int(input())
    if j != 0 and j != 1:
        print("Err")
    else:
        if (j == 0):
            print("Name?")
            name = input()
            player = Player(name)
        else:
            name = "Bot" + str(number)
            player = Bot(name)
    return player

def who_play_first(player1, player2):
    print("Qui commence? (0-" + player1.name + "; 1-" + player2.name + ") :")
    j = int(input())
    if j != 0 and j != 1:
        print("Err")
    else:
        return (j)

class Player:
    def __init__(self, name):
        self.name = name

    def play(self, game):
        print(self.name + " :")
        print("ligne? (0-3) : ")
        l = int(input())
        print("nombre? : ")
        n = int(input())
        game.play((l,n))

class Bot(Player):
    def __init__(self, name):
        Player.__init__(self, name)
        self.historic = []
        self.file = name + "_memory"
        try:
            f = open(self.file, "rb")
            self.IA = pickle.load(f)
            f.close()
        except:
            print("New memory")
            self.IA = []
            

    def play(self, game):
        position = None
        for i in self.IA: #search in my database
            if i.board == game.board:
                #print("FIND")
                #print(jeu.plateau)
                #print(i.plateau)
                position = i

        if position == None: #if not found
            #print("add new position")
            #print("-->" + str(jeu.plateau))
            position = node(copy.copy(game.board))
            #print("2->" + str(position.plateau))
            #print(position.to_print())
            for i in game.possible_moves():
                bot_move = move(i)
                position.add_move(bot_move)
            self.IA.append(position)
    
        best_move = position.best_move()
        game.play(best_move.move)

        self.historic.append(best_move)


    def improve(self, game):
        for i in range(len(self.historic)):
            if game.turn() == self:
                self.historic[i].points -= float(i + 1)/float(len(self.historic))
            else:
                self.historic[i].points += float(i + 1)/float(len(self.historic))

    def save(self):
        f = open(self.file, "wb")
        pickle.dump(self.IA, f)
        f.close()

def classic_game():
    p1 = create_player(0)
    p2 = create_player(1)
    w = who_play_first(p1, p2)

    g = Game(p1, p2, w)

    while not g.over():
        g.show()
        g.turn().play(g)
        if g.over():
            print(g.turn().name + " Looser !!")

    try:
        p1.improve(g)
        p2.improve(g)
        p1.save()
        p2.save()
    except:
        pass

def bot_training(it):
    while it != 0:
        b1 = Bot("Bot0")
        b2 = Bot("Bot1")
        w = it % 2

        g = Game(b1, b2, w)

        print(g.turn().name + " playing first!")

        while not g.over():
            g.turn().play(g)
            if g.over():
                print(g.turn().name + " Looser !!")

        try:
            b1.improve(g)
            b2.improve(g)
            b1.save()
            b2.save()
        except:
            print("Err improving or saving")
        it -= 1

print("0-Classic game / 1-Bot training :")
j = int(input())
if j != 0 and j != 1:
    print("Err")
else:
    if j == 0:
        classic_game()
    else:
        print("number of iterations ?")
        it = int(input())
        bot_training(it)
