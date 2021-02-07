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

		self.piece = piece
		self.colour = colour
		self.coords = coords
		self.noMoves = 0
		self.active = False

		self.image = pygame.Surface([SQUAREWIDTH, SQUAREWIDTH])
		self.image.set_colorkey((2, 2, 2))
		self.image.fill((2, 2, 2))

		self.rect = self.image.get_rect()
		self.rect.x = self.coords[0] * SQUAREWIDTH
		self.rect.y = self.coords[1] * SQUAREWIDTH

		self.image.blit(blackPieces[piece] if colour == "black" else whitePieces[piece], (0,0))

	def isClicked(self, mousex, mousey):
		if self.rect.collidepoint(mousex, mousey):
			self.active = True
			return True
		self.active = False
		return False

	def getStraightMoves(self, board, limit=7):
		""" Gets all possible moves in the horizontal and vertical directions from a given piece.
		Returns a list of tuples, representing the co-ords which can be moved to."""
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		moves = []

		for d in directions:
			distance = 1
			nextMove = (self.coords[0] + distance*d[0], self.coords[1] + distance*d[1])
			nextSquare = board[nextMove[0]][nextMove[1]]
			while distance < limit + 1 and nextSquare == " " and self.coords[0] + distance*d[0] in range(-1, 9) and self.coords[1] + distance*d[1] in range (-1, 9):
				moves.append(nextMove)

				nextMove = (self.coords[0] + distance*d[0], self.coords[1] + distance*d[1])
				nextSquare = board[nextMove[0]][nextMove[1]]
				distance += 1
			if nextSquare != " ":
				moves.append(nextMove)

		return moves

	def getDiagonalMoves(self, board, limit=False):
		""" Gets all possible moves in the diagonals from a given piece.
		Returns a list of tuples, representing the co-ords which can be moved to."""
		possibleDirections = [(1,1), (-1,1), (1,-1), (-1,-1)]
		moves = []
		if not limit:
			for i in range(1, min([7-self.coords[0], 7-self.coords[1]]) + 1):
				moves.append((self.coords[0] + i, self.coords[1] + i))
				if board[self.coords[0] + i][self.coords[1] + i] != " ":
					break
			for i in range(1, min([7-self.coords[0], self.coords[1]]) + 1):
				moves.append((self.coords[0] + i, self.coords[1] - i))
				if board[self.coords[0] + i][self.coords[1] - i] != " ":
					break
			for i in range(1, min([self.coords[0], self.coords[1]]) + 1):
				moves.append((self.coords[0] - i, self.coords[1] - i))
				if board[self.coords[0]- i][self.coords[1] - i] != " ":
					break
			for i in range(1, min([self.coords[0], 7-self.coords[1]]) + 1):
				moves.append((self.coords[0] - i, self.coords[1] + i))
				if board[self.coords[0] - i][self.coords[1] + i] != " ":
					break
		else:
			for i in range(4):
				for j in range(1, limit+1):
					move = (self.coords[0]+(possibleDirections[i][0]*j), (self.coords[1]+(possibleDirections[i][1]*j)))
					moves.append(move)
					if board[move[0]][move[1]] != " ":
						break

		return moves


class Pawn(Piece):
	def __init__(self, colour, coords):
		super().__init__("Pawn", colour, coords)

		self.direction = 1 if self.colour == "black" else -1

	def getMoves(self, board):
		moves = []
		oneSquare = (self.coords[0], self.coords[1] + self.direction)
		if board[oneSquare[0]][oneSquare[1]] == " ":
			moves.append(oneSquare)
		if board[self.coords[0]-1][self.coords[1]+self.direction] != " ": ## Check if can take diagonally
			moves.append((self.coords[0]-1, self.coords[1]+self.direction))
		if board[self.coords[0]+1][self.coords[1]+self.direction] != " ": ## Check if can take diagonally
			moves.append((self.coords[0]+1, self.coords[1]+self.direction))

		if self.noMoves == 0: ## Check if its the first move, so can move two squares
			moves.append((self.coords[0], self.coords[1] + 2*self.direction))

		return moves

class Knight(Piece):
	def __init__(self, colour, coords):
		super().__init__("Knight", colour, coords)

	def getMoves(self, board):
		possibleDirections = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
		moves = []

		for d in possibleDirections:
			possible = (self.coords[0] + d[0], self.coords[1] + d[1])
			moves.append(possible)

		return moves

class Bishop(Piece):
	def __init__(self, colour, coords):
		super().__init__("Bishop", colour, coords)

	def getMoves(self, board):
		return self.getDiagonalMoves(board)

class Rook(Piece):
	def __init__(self, colour, coords):
		super().__init__("Rook", colour, coords)

	def getMoves(self, board):
		return self.getStraightMoves(board)

class Queen(Piece):
	def __init__(self, colour, coords):
		super().__init__("Queen", colour, coords)

	def getMoves(self, board):
		return self.getStraightMoves(board) + self.getDiagonalMoves(board)

class King(Piece):
	def __init__(self, colour, coords):
		super().__init__("King", colour, coords)

	def getMoves(self, board):
		return self.getStraightMoves(board, limit=1) + self.getDiagonalMoves(board, limit=1)

	def isInCheck(self, board, pieces):
		for p in pieces.sprites():
			for move in p.getMoves(board):
				#print(p.coords, move)
				if p.colour != self.colour and self.coords[0] == move[0] and self.coords[1] == move[1]:
					return True
		return False