import pygame, piece
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR

screen = pygame.display.set_mode((SCREENWIDTH, SCREENWIDTH))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

playing = True

piecesGroup = pygame.sprite.Group()
piecesGroup.add(piece.Pawn("black", (0, 0)),
				piece.Rook("white", (2, 5)),
				piece.King("black", (0, 7)),
				piece.Queen("white", (4, 2)))

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

	piecesGroup.draw(screen)
	pygame.display.flip()
	clock.tick(60)

pygame.quit()