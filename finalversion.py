import random
import sys
Width = 8  # Игровое поле содержит 8 клеток по ширине.
Height = 8 # Игровое поле содержит 8 клеток по высоте.
def drawBoard(board):
    # Вывести игровое поле, переданное этой функции. Ничего не возвращать.
    print('  12345678')
    print(' +--------+')
    for y in range(Height):
        print('%s|' % (y+1), end='')
        for x in range(Width):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    # Создать структуру данных нового чистого игрового поля.
    board = []
    for i in range(Width):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, tile, xstart, ystart):
    # Вернуть False, если ход игрока в клетку с координатами
    # xstart, ystart – недопустимый.
    # Если это допустимый ход, вернуть список клеток,
    # которые "присвоил" бы игрок, если бы сделал туда ход.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    if tile == 'Х':
        otherTile = 'О'
    else:
        otherTile = 'Х'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # первый шаг в направлении x
        y += ydirection # первый шаг в направлении y
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # продолжать двигаться в этом направлении x и y.
            x += xdirection
            y += ydirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # Есть фишки, которые можно перевернуть.
                # Двигаться в обратном направлении до достижения исходной клетки, отмечая все фишки на этом пути.

                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    if len(tilesToFlip) == 0: # Если ни одна из фишек не перевернулась, это недопустимый ход.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Вернуть True, если координаты есть на игровом поле.
    return x >= 0 and x <= Width - 1 and y >= 0 and y <= Height - 1

def getBoardWithValidMoves(board, tile):
    # Вернуть новое поле с точками, обозначающими допустимые ходы, которые может сделать игрок.
    boardCopy = getBoardCopy(board)

    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def getValidMoves(board, tile):
    # Вернуть список списков с координатами x и y допустимых ходов для данного игрока на данном игровом поле.
    validMoves = []
    for x in range(Width):
        for y in range(Height):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Определить количество очков, подсчитав фишки. Вернуть словарь с ключами 'Х' и 'О'.
    xscore = 0
    oscore = 0
    for x in range(Width):
        for y in range(Height):
            if board[x][y] == 'Х':
                xscore += 1
            if board[x][y] == 'О':
                oscore += 1
    return {'Х':xscore, 'О':oscore}

def enterPlayerTile():
    # Возможность выбрать игроку за какую фишку ему играть
    tile = ''
    while not (tile == 'Х' or tile == 'О'):
        print('Вы играете за Х или О (кириллица)?')
        tile = input().upper()

    # первое значение это фишка игрока, второе значение это фишка компьютера
    if tile == 'Х':
        return ['Х', 'О']
    else:
        return ['О', 'Х']

def whoGoesFirst():
    # Случайно выбрать, кто ходит первым.
    if random.randint(0, 1) == 0:
        return 'Компьютер'
    else:
        return 'Человек'

def makeMove(board, tile, xstart, ystart):
    # Поместить фишку на игровое поле в позицию xstart, ystart и перевернуть какую-либо фишку противника.
    # Вернуть False, если это недопустимый ход; вернуть True, если допустимый.

    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Сделать копию списка board и вернуть её.
    boardCopy = getNewBoard()

    for x in range(Width):
        for y in range(Height):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    # Вернуть True, если указанная позиция находится в одном из 4 углов.
    return (x == 0 or x == Width - 1) and (y == 0 or y == Height - 1)

def getPlayerMove(board, playerTile):
    # Позволить игроку ввести свой ход.
    # Вернуть ход в виде [x, y] или вернуть строки 'подсказка' или 'выход'.
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Укажите ход(столбец строка), текст "выход" для завершения игры или "подсказка" для вывода подсказки.')
        move = input().lower()
        if move == 'выход' or move == 'подсказка':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер столбца 1-8 и номер ряда 1-8.')
            print('К примеру, значение 81 перемещает в верхний правый угол.')

    return [x, y]

def getComputerMove(board, computerTile):
    # Учитывая данное игровое поле и данную фишку компьютера, определить,
    # куда сделать ход, и вернуть этот ход в виде списка [x, y].
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # Порядок ходов случайный

    # Всегда делать ход в угол, если это возможно.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Найти ход с наибольшим возможным количеством очков.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('Ваш счет: %s. Счет компьютера: %s.' % (scores[playerTile], scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print(turn + ' ходит первым.')

    # Очистить игровое поле и выставить стартовые фишки.
    board = getNewBoard()
    board[3][3] = 'Х'
    board[3][4] = 'О'
    board[4][3] = 'О'
    board[4][4] = 'Х'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)

        if playerValidMoves == [] and computerValidMoves == []:
            return board  # Конец игры, так как ходов нет ни у кого
        # Ход человека
        elif turn == 'Человек':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'выход':
                    print('Благодарим за игру!')
                    sys.exit()  # завершение работы программы.
                elif move == 'подсказка':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'Компьютер'
        # Ход компьютера
        elif turn == 'Компьютер':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile)

                #input('Нажмите клавишу Enter для просмотра хода компьютера.')
                move = getComputerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'Человек'


print('Приветствуем вас в игре "Реверси"!')
print('Ввод данных производится по типу столбец строка')

playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)

    # Отображение итогового счеа.
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X набрал %s очков. O набрал %s очков.' % (scores['Х'], scores['О']))
    if scores[playerTile] > scores[computerTile]:
        print('Вы победили компьютер, обогнав его на %s очков! Поздравления!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('Вы проиграли. Компьютер победил вас, обогнав на %s очков.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('Ничья!')

    print('Хотите сыграть еще раз? (да или нет)')
    if not input().lower().startswith('д'):
        exit(0)
    else:
        playerTile, computerTile = enterPlayerTile()