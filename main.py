import pygame, piece
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR

screen = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

playing = True
moves = []

piecesGroup = pygame.sprite.Group()
piecesGroup.add(piece.Pawn("white", [0, 3]),
				piece.Bishop("white", [2, 5]),
				piece.Knight("black", [3, 5]),
				piece.Queen("white", [4, 4]), 
				piece.King("black", [2, 2]),
				piece.Rook("white", [6, 4]))

board = [[" " for x in range(9)] for y in range(9)]
for piece in piecesGroup.sprites():
	board[piece.coords[0]][piece.coords[1]] = piece.piece

while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousex, mousey = pygame.mouse.get_pos()
			for piece in piecesGroup.sprites():
				piece.isClicked(mousex, mousey)
		elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
			mousex, mousey = pygame.mouse.get_pos()
			for piece in piecesGroup.sprites():
				if piece.active:
					piece.rect.x = mousex - SQUAREWIDTH / 2
					piece.rect.y = mousey - SQUAREWIDTH / 2
		elif event.type == pygame.MOUSEBUTTONUP:
			mousex, mousey = pygame.mouse.get_pos()
			for piece in piecesGroup.sprites():
				if piece.active:
					if (mousex // SQUAREWIDTH, mousey // SQUAREWIDTH) in piece.getMoves(board):
						board[piece.coords[0]][piece.coords[1]] = " "

						piece.coords[0] = mousex // SQUAREWIDTH
						piece.coords[1] = mousey // SQUAREWIDTH
						piece.rect.x = piece.coords[0] * SQUAREWIDTH
						piece.rect.y = piece.coords[1] * SQUAREWIDTH

						board[piece.coords[0]][piece.coords[1]] = piece.piece
					else:
						piece.rect.x = piece.coords[0] * SQUAREWIDTH
						piece.rect.y = piece.coords[1] * SQUAREWIDTH

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

	for m in moves:
		pygame.draw.rect(screen, (0, 0, 255), (m[0]*SQUAREWIDTH + SQUAREWIDTH/2, m[1]*SQUAREWIDTH + SQUAREWIDTH/2, 10, 10))
	pygame.display.flip()
	clock.tick(60)

pygame.quit()