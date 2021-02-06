import pygame, piece
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR

screen = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

playing = True

piecesGroup = pygame.sprite.Group()
piecesGroup.add(piece.Pawn("white", (0, 3)),
				piece.Rook("white", (2, 5)),
				piece.King("black", (3, 3)),
				piece.Queen("white", (4, 2)),
				piece.Knight("black", (3, 5)))

while playing:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False

	screen.fill((255, 255, 255))

	## Draw the chess board
	## Fill the background dark
	screen.fill(DARKCOLOUR)
	## Draw the light
	for i in range(0, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))
	for i in range(1, 33, 2):
		pygame.draw.rect(screen, LIGHTCOLOUR, ((i%8)*SQUAREWIDTH, (i//8)*2*SQUAREWIDTH+SQUAREWIDTH, SQUAREWIDTH, SQUAREWIDTH))

	for m in piecesGroup.sprites()[4].possibleMoves:
		pygame.draw.rect(screen, (0, 0, 255), (m[0]*SQUAREWIDTH, m[1]*SQUAREWIDTH, 10, 10))
	piecesGroup.draw(screen)
	pygame.display.flip()
	clock.tick(60)

pygame.quit()