import pygame
from constants import SCREENWIDTH, SQUAREWIDTH
pygame.init()

blackPieces = {"Pawn" : pygame.image.load("Assets/dPawn.png"),
			   "Knight" : pygame.image.load("Assets/dKnight.png"),
			   "Bishop" : pygame.image.load("Assets/dBishop.png"),
			   "Rook" : pygame.image.load("Assets/dRook.png"),
			   "Queen" : pygame.image.load("Assets/dQueen.png"),
			   "King" : pygame.image.load("Assets/dKing.png")}

whitePieces = {"Pawn" : pygame.image.load("Assets/lPawn.png"),
			   "Knight" : pygame.image.load("Assets/lKnight.png"),
			   "Bishop" : pygame.image.load("Assets/lBishop.png"),
			   "Rook" : pygame.image.load("Assets/lRook.png"),
			   "Queen" : pygame.image.load("Assets/lQueen.png"),
			   "King" : pygame.image.load("Assets/lKing.png")}

for piece, pieceImg in blackPieces.items():
	resizeImage = pygame.transform.scale(pieceImg, (SQUAREWIDTH, SQUAREWIDTH))
	blackPieces[piece] = resizeImage

for piece, pieceImg in whitePieces.items():
	resizeImage = pygame.transform.scale(pieceImg, (SQUAREWIDTH, SQUAREWIDTH))
	whitePieces[piece] = resizeImage

class Piece(pygame.sprite.Sprite):
	def __init__(self, piece, colour, coords):
		super().__init__()

		self.image = pygame.Surface([SQUAREWIDTH, SQUAREWIDTH])
		self.image.set_colorkey((2, 2, 2))
		self.image.fill((2, 2, 2))

		self.rect = self.image.get_rect()
		self.rect.x = coords[0] * SQUAREWIDTH
		self.rect.y = coords[1] * SQUAREWIDTH

		self.image.blit(blackPieces[piece] if colour == "black" else whitePieces[piece], (0,0))

class Pawn(Piece):
	def __init__(self, colour, coords):
		super().__init__("Pawn", colour, coords)

class Knight(Piece):
	def __init__(self, colour, coords):
		super().__init__("Knight", colour, coords)

class Bishop(Piece):
	def __init__(self, colour, coords):
		super().__init__("Bishop", colour, coords)

class Rook(Piece):
	def __init__(self, colour, coords):
		super().__init__("Rook", colour, coords)

class Queen(Piece):
	def __init__(self, colour, coords):
		super().__init__("Queen", colour, coords)

class King(Piece):
	def __init__(self, colour, coords):
		super().__init__("King", colour, coords)