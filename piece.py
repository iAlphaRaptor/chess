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

		self.colour = colour
		self.coords = coords

		self.image = pygame.Surface([SQUAREWIDTH, SQUAREWIDTH])
		self.image.set_colorkey((2, 2, 2))
		self.image.fill((2, 2, 2))

		self.rect = self.image.get_rect()
		self.rect.x = self.coords[0] * SQUAREWIDTH
		self.rect.y = self.coords[1] * SQUAREWIDTH

		self.image.blit(blackPieces[piece] if colour == "black" else whitePieces[piece], (0,0))

	def getStraightMoves(self, limit=False):
		moves = []
		if not limit:
			for x in range(0, 8):
				if x != self.coords[0]:
					moves.append((x, self.coords[1]))
			for y in range(0, 8):
				if y != self.coords[1]:
					moves.append((self.coords[0], y))
		else:
			for x in range(self.coords[0]-limit, self.coords[0]+limit+1):
				if x != self.coords[0]:
					moves.append((x, self.coords[1]))
			for y in range(self.coords[1]-limit, self.coords[1]+limit+1):
				if y != self.coords[1]:
					moves.append((self.coords[0], y))

		return moves

	def getDiagonalMoves(self, limit=False):
		moves = []
		if not limit:
			for i in range(1, min([7-self.coords[0], 7-self.coords[1]]) + 1):
				moves.append((self.coords[0] + i, self.coords[1] + i))
			for i in range(1, min([7-self.coords[0], self.coords[1]]) + 1):
				moves.append((self.coords[0] + i, self.coords[1] - i))
			for i in range(1, min([self.coords[0], self.coords[1]]) + 1):
				moves.append((self.coords[0] - i, self.coords[1] - i))
			for i in range(1, min([self.coords[0], 7-self.coords[1]]) + 1):
				moves.append((self.coords[0] - i, self.coords[1] + i))
		else:
			dir = [(1,1), (-1,1), (1,-1), (-1,-1)]
			for i in range(4):
				for j in range(1, limit+1):
					moves.append((self.coords[0]+(dir[i][0]*j), (self.coords[1]+(dir[i][1]*j))))

		return moves


class Pawn(Piece):
	def __init__(self, colour, coords):
		super().__init__("Pawn", colour, coords)

		self.possibleMoves = [(self.coords[0], self.coords[1] + 1 if self.colour == "black" else self.coords[1] - 1)]

class Knight(Piece):
	def __init__(self, colour, coords):
		super().__init__("Knight", colour, coords)
		possibleDirections = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
		self.possibleMoves = []

		for d in possibleDirections:
			self.possibleMoves.append((self.coords[0] + d[0], self.coords[1] + d[1]))

class Bishop(Piece):
	def __init__(self, colour, coords):
		super().__init__("Bishop", colour, coords)

		self.possibleMoves = self.getDiagonalMoves()

class Rook(Piece):
	def __init__(self, colour, coords):
		super().__init__("Rook", colour, coords)

		self.possibleMoves = self.getStraightMoves()

class Queen(Piece):
	def __init__(self, colour, coords):
		super().__init__("Queen", colour, coords)

		self.possibleMoves = self.getStraightMoves() + self.getDiagonalMoves()

class King(Piece):
	def __init__(self, colour, coords):
		super().__init__("King", colour, coords)

		self.possibleMoves = self.getStraightMoves(limit=1) + self.getDiagonalMoves(limit=1)