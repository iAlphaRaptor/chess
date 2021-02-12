import pygame, piece, board, move
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR

screen = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

playing = True
moves = []

piecesGroup = pygame.sprite.Group()
## Add Pawns
for i in range(0, 1):
	piecesGroup.add(piece.Pawn("white", [i, 6]),
					piece.Pawn("black", [i, 1]))

## Add black pieces
piecesGroup.add(#piece.Rook("black", [0, 0]),
				#piece.Knight("black", [1, 0]),
				#piece.Bishop("black", [2, 0]),
				#piece.Queen("black", [3, 0]), 
				piece.King("black", [4, 0]),
				#piece.Bishop("black", [5, 0]),
				#piece.Knight("black", [6, 0]),
				piece.Rook("black", [7, 0]))

## Add white pieces
piecesGroup.add(#piece.Rook("white", [0, 7]),
				#piece.Knight("white", [1, 7]),
				#piece.Bishop("white", [2, 7]),
				#piece.Queen("white", [3, 7]), 
				piece.King("white", [4, 7]),
				#piece.Bishop("white", [5, 7]),
				#piece.Knight("white", [6, 7]),
				piece.Rook("white", [7, 7]))

gameboard = board.Board(piecesGroup)

currentPlayer = "white"
inCheck = False
isMate = False

while playing:
	moved = False

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
			for poss in gameboard.piecesGroup.sprites():
				if poss.active:
					moveX = mousex // SQUAREWIDTH
					moveY = mousey // SQUAREWIDTH

					possibleMoves = poss.getMoves(gameboard)
					for m in possibleMoves:
							if list(m.coords) == [moveX, moveY]:
								nextMove = m

					if (mousex // SQUAREWIDTH, mousey // SQUAREWIDTH) in [x.coords for x in possibleMoves] and poss.colour == currentPlayer and not inCheck: ## Move a piece
						originalCoords = [poss.coords[0], poss.coords[1]]
						print(nextMove.coords)
						temp = ""
						if not gameboard.isSquareEmpty((moveX, moveY)):
							target = gameboard.getPiece((moveX, moveY))
							if target.colour != poss.colour:
								take = True
								temp = target
								gameboard.takePiece(poss, target, nextMove)
							else:
								poss.resetPiece()
						else:
							take = False
							gameboard.movePiece(poss, nextMove)

						if gameboard.checkCheck(currentPlayer): ## Check if the move is legal
							if take:
								gameboard.piecesGroup.add(temp)
								gameboard.movePiece(poss, nextMove)
							else:
								gameboard.movePiece(poss, move.Move(originalCoords))
						else:
							## Check for pawn promotion
							if poss.piece == "Pawn" and poss.coords[1] in [0,7]:
								gameboard.piecesGroup.remove(poss)
								gameboard.piecesGroup.add(piece.Queen(poss.colour, [poss.coords[0], poss.coords[1]]))

							moved = True
					elif inCheck and poss.colour == currentPlayer and (mousex // SQUAREWIDTH, mousey // SQUAREWIDTH) in [x.coords for x in possibleMoves]:
						currentCoords = (poss.coords[0], poss.coords[1])

						if not gameboard.isSquareEmpty((moveX, moveY)):
							for target in gameboard.piecesGroup.sprites():
								if target.coords[0] == moveX and target.coords[1] == moveY:
									if target.colour != poss.colour:
										temp = target
										piecesGroup.remove(target)
										gameboard.movePiece(poss, nextMove)
										if not gameboard.checkCheck(currentPlayer):
											gameboard.takePiece(poss, target, nextMove)
											moved = True
										else:
											gameboard.movePiece(poss, nextMove)
											gameboard.piecesGroup.add(temp)
									else:
										poss.resetPiece()
						else:
							gameboard.movePiece(poss, nextMove)
							if gameboard.checkCheck(currentPlayer):
								gameboard.movePiece(poss, move.Move(currentCoords))
							else:
								moved = True
					else:
						poss.resetPiece()

	if moved:
		currentPlayer = "black" if currentPlayer == "white" else "white"
		inCheck = gameboard.checkCheck(currentPlayer)
		isMate = gameboard.mateCheck(currentPlayer)

	screen.fill((255, 255, 255))

	## Draw the chess gameboard
	## Fill the background dark
	screen.fill(DARKCOLOUR)
	## Draw the light squares
	for i in range(0, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))
	for i in range(1, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH+SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))

	gameboard.piecesGroup.draw(screen)

	if isMate:
		#gameboard.piecesGroup.empty()

		mateFont = pygame.font.Font("Assets/Blacksword.otf", int(SCREENWIDTH*(3/20)))
		mateText = mateFont.render("Checkmate", True, (0, 0, 0))
		winnerFont = pygame.font.Font("Assets/Blacksword.otf", int(SCREENWIDTH*(3/40)))
		winnerText = "Black" if currentPlayer == "white" else "White" + " wins"
		winner = winnerFont.render(winnerText, True, (0, 0, 0))

		mateWidth, mateHeight = mateFont.size("Checkmate")
		winnerWidth, winnerHeight = winnerFont.size(winnerText)
		screen.blit(mateText, (int(SCREENWIDTH/2-mateWidth/2), int(SCREENWIDTH/2-mateHeight), 1000, 1000))
		screen.blit(winner, (int(SCREENWIDTH/2-winnerWidth/2), int(SCREENWIDTH/2), 1000, 1000))

	pygame.display.flip()
	clock.tick(60)

pygame.quit()