import pygame, piece
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR

screen = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

playing = True
moves = []

piecesGroup = pygame.sprite.Group()
## Add Pawns
for i in range(0, 8):
	piecesGroup.add(piece.Pawn("white", [i, 6]),
					piece.Pawn("black", [i, 1]))

## Add black pieces
piecesGroup.add(piece.Rook("black", [0, 0]),
				piece.Knight("black", [1, 0]),
				piece.Bishop("black", [2, 0]),
				piece.Queen("black", [3, 0]), 
				piece.King("black", [4, 0]),
				piece.Bishop("black", [5, 0]),
				piece.Knight("black", [6, 0]),
				piece.Rook("black", [7, 0]))

## Add white pieces
piecesGroup.add(piece.Rook("white", [0, 7]),
				piece.Knight("white", [1, 7]),
				piece.Bishop("white", [2, 7]),
				piece.Queen("white", [3, 7]), 
				piece.King("white", [4, 7]),
				piece.Bishop("white", [5, 7]),
				piece.Knight("white", [6, 7]),
				piece.Rook("white", [7, 7]))

board = [[" " for x in range(9)] for y in range(9)]
for p in piecesGroup.sprites():
	board[p.coords[0]][p.coords[1]] = p.piece

currentPlayer = "white"
inCheck = False

def movePiece(movingPiece, move):
	movingPiece.coords[0] = move[0]
	movingPiece.coords[1] = move[1]
	movingPiece.rect.x = movingPiece.coords[0] * SQUAREWIDTH
	movingPiece.rect.y = movingPiece.coords[1] * SQUAREWIDTH

	board[movingPiece.coords[0]][movingPiece.coords[1]] = movingPiece.piece
	movingPiece.noMoves += 1

def takePiece(movingPiece, targetPiece, move):
	piecesGroup.remove(targetPiece)
	movePiece(movingPiece, move)

def resetPiece(movingPiece):
	movingPiece.rect.x = movingPiece.coords[0] * SQUAREWIDTH
	movingPiece.rect.y = movingPiece.coords[1] * SQUAREWIDTH

def checkCheck():
	for p in piecesGroup.sprites():
		if p.piece == "King":
			if p.colour == currentPlayer:
				return p.isInCheck(board, piecesGroup)


while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousex, mousey = pygame.mouse.get_pos()
			for poss in piecesGroup.sprites():
				poss.isClicked(mousex, mousey)
		elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
			mousex, mousey = pygame.mouse.get_pos()
			for poss in piecesGroup.sprites():
				if poss.active:
					poss.rect.x = mousex - SQUAREWIDTH / 2
					poss.rect.y = mousey - SQUAREWIDTH / 2
		elif event.type == pygame.MOUSEBUTTONUP:
			mousex, mousey = pygame.mouse.get_pos()
			for poss in piecesGroup.sprites():
				if poss.active:
					moveX = mousex // SQUAREWIDTH
					moveY = mousey // SQUAREWIDTH
					if (mousex // SQUAREWIDTH, mousey // SQUAREWIDTH) in poss.getMoves(board) and poss.colour == currentPlayer and not inCheck: ## Move a piece
						originalCoords = [poss.coords[0], poss.coords[1]]
						board[poss.coords[0]][poss.coords[1]] = " "

						if board[moveX][moveY] != " ":
							for target in piecesGroup.sprites():
								if target.coords[0] == moveX and target.coords[1] == moveY:
									if target.colour != poss.colour:
										takePiece(poss, target, (moveX, moveY))
									else:
										resetPiece(poss)
						else:
							movePiece(poss, (moveX, moveY))

						if checkCheck(): ## Check if the player has moved into check
							board[poss.coords[0]][poss.coords[1]] = " "
							movePiece(poss, originalCoords)
						else: ## i.e. the move is legal
							## Check for pawn promotion
							if poss.piece == "Pawn" and poss.coords[1] in [0,7]:
								piecesGroup.remove(poss)
								piecesGroup.add(piece.Queen(poss.colour, [poss.coords[0], poss.coords[1]]))

								board[poss.coords[0]][poss.coords[1]] = "queen"

							currentPlayer = "black" if currentPlayer == "white" else "white"

							inCheck = checkCheck()
					elif inCheck:
						currentCoords = (poss.coords[0], poss.coords[1])

						if board[moveX][moveY] != " ":
							for target in piecesGroup.sprites():
								if target.coords[0] == moveX and target.coords[1] == moveY:
									if target.colour != poss.colour:
										temp = target
										piecesGroup.remove(target)
										if not checkCheck():
											takePiece(poss, target, (moveX, moveY))
											currentPlayer = "black" if currentPlayer == "white" else "white"
										else:
											piecesGroup.add(temp)
									else:
										resetPiece(poss)
						else:
							board[poss.coords[0]][poss.coords[1]] = " "
							movePiece(poss, (moveX, moveY))
							if checkCheck():
								board[poss.coords[0]][poss.coords[1]] = " "
								movePiece(poss, currentCoords)
							else:
								currentPlayer = "black" if currentPlayer == "white" else "white"
								inCheck = checkCheck()
					else:
						resetPiece(poss)

	screen.fill((255, 255, 255))

	## Draw the chess board
	## Fill the background dark
	screen.fill(DARKCOLOUR)
	## Draw the light
	for i in range(0, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))
	for i in range(1, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH+SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))

	for p in piecesGroup.sprites():
		if p.active:
			moves = p.getMoves(board)
	piecesGroup.draw(screen)

	if inCheck:
		pygame.draw.rect(screen, (0, 0, 0) if currentPlayer == "black" else (255, 255, 255), (0, 0, 25, 25))
	#for m in moves:
	#	pygame.draw.rect(screen, (0, 0, 255), (m[0]*SQUAREWIDTH + SQUAREWIDTH/2, m[1]*SQUAREWIDTH + SQUAREWIDTH/2, 10, 10))
	pygame.display.flip()
	clock.tick(60)

pygame.quit()