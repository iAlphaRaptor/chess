import pygame, move
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

	def resetPiece(self):
		self.rect.x = self.coords[0] * SQUAREWIDTH
		self.rect.y = self.coords[1] * SQUAREWIDTH

	def getStraightMoves(self, board, limit=8):
		""" Gets all possible moves in the horizontal and vertical directions from a given piece.
		Returns a list of tuples, representing the co-ords which can be moved to."""
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		moves = []

		for d in directions:
			distance = 1
			nextMove = (self.coords[0] + distance*d[0], self.coords[1] + distance*d[1])
			while distance <= limit and board.isSquareEmpty(nextMove) and nextMove[0] in range(0, 8) and nextMove[1] in range(0, 8):
				moves.append(move.Move(nextMove))

				distance += 1
				nextMove = (self.coords[0] + distance*d[0], self.coords[1] + distance*d[1])
			if not board.isSquareEmpty(nextMove):
				moves.append(move.Move(nextMove))

		for m in moves:
			if m.coords[0] < 0 or m.coords[1] < 0:
				moves.remove(m)
		return moves

	def getDiagonalMoves(self, board, limit=False):
		""" Gets all possible moves in the diagonals from a given piece.
		Returns a list of tuples, representing the co-ords which can be moved to."""
		possibleDirections = [(1,1), (-1,1), (1,-1), (-1,-1)]
		moves = []
		if not limit:
			for i in range(1, min([7-self.coords[0], 7-self.coords[1]]) + 1):
				moves.append(move.Move((self.coords[0] + i, self.coords[1] + i)))
				if not board.isSquareEmpty((self.coords[0] + i, self.coords[1] + i)):
					break
			for i in range(1, min([7-self.coords[0], self.coords[1]]) + 1):
				moves.append(move.Move((self.coords[0] + i, self.coords[1] - i)))
				if not board.isSquareEmpty((self.coords[0] + i, self.coords[1] - i)):
					break
			for i in range(1, min([self.coords[0], self.coords[1]]) + 1):
				moves.append(move.Move((self.coords[0] - i, self.coords[1] - i)))
				if not board.isSquareEmpty((self.coords[0] - i, self.coords[1] - i)):
					break
			for i in range(1, min([self.coords[0], 7-self.coords[1]]) + 1):
				moves.append(move.Move((self.coords[0] - i, self.coords[1] + i)))
				if not board.isSquareEmpty((self.coords[0] - i, self.coords[1] + i)):
					break
		else:
			for i in range(4):
				for j in range(1, limit+1):
					possibleMove = (self.coords[0]+(possibleDirections[i][0]*j), (self.coords[1]+(possibleDirections[i][1]*j)))
					moves.append(move.Move(possibleMove))
					if not board.isSquareEmpty((possibleMove[0], possibleMove[1])):
						break

		return moves


class Pawn(Piece):
	def __init__(self, colour, coords):
		super().__init__("Pawn", colour, coords)

		self.direction = 1 if self.colour == "black" else -1

	def getMoves(self, board):
		moves = []
		oneSquare = (self.coords[0], self.coords[1] + self.direction)
		if board.isSquareEmpty((oneSquare[0], oneSquare[1])):
			moves.append(move.Move(oneSquare))
		if not board.isSquareEmpty((self.coords[0]-1, self.coords[1]+self.direction)): ## Check if can take diagonally
			moves.append(move.Move((self.coords[0]-1, self.coords[1]+self.direction)))
		if not board.isSquareEmpty((self.coords[0]+1, self.coords[1]+self.direction)): ## Check if can take diagonally
			moves.append(move.Move((self.coords[0]+1, self.coords[1]+self.direction)))

		if self.noMoves == 0: ## Check if its the first move, so can move two squares
			moves.append(move.Move((self.coords[0], self.coords[1] + 2*self.direction)))
		elif self.coords[1] in [3, 4]: ## Check for en passent
			right = board.getPiece((self.coords[0]+1, self.coords[1]))
			rightMove = (self.coords[0]+1, self.coords[1]+1 if self.colour == "black" else self.coords[1]-1)
			left = board.getPiece((self.coords[0]-1, self.coords[1]))
			leftMove = (self.coords[0]-1, self.coords[1]+1 if self.colour == "black" else self.coords[1]-1)
			if right != False and right.piece == "Pawn" and right.noMoves == 1:
				moves.append(move.Move(rightMove, specialMove="EP", thirdParty=(right)))
			if left != False and left.piece == "Pawn" and left.noMoves == 1:
				moves.append(move.Move(leftMove, specialMove="EP", thirdParty=(left)))

		return moves

class Knight(Piece):
	def __init__(self, colour, coords):
		super().__init__("Knight", colour, coords)

	def getMoves(self, board):
		possibleDirections = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2)]
		moves = []

		for d in possibleDirections:
			possible = (self.coords[0] + d[0], self.coords[1] + d[1])
			moves.append(move.Move(possible))

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

	def getMoves(self, board, ignoreCastles=False):
		moves = []

		## Check for castling
		if not ignoreCastles:
			if self.noMoves == 0 and not board.checkCheck(self.colour):
				kingSidePieces = [board.getPiece((i, self.coords[1])) for i in range(5, 8)]
				queenSidePieces = [board.getPiece((i, self.coords[1])) for i in range(0, 5)]
				if kingSidePieces[2] != False and kingSidePieces[2].noMoves == 0 and kingSidePieces[0] == False and kingSidePieces[1] == False:
					possible = True
					for x in range(6, 8):
						tempKing = King(self.colour, (x, self.coords[1]))
						board.piecesGroup.add(tempKing)
						if board.checkCheck(self.colour):
							possible = False
						board.piecesGroup.remove(tempKing)

					if possible:
						moves.append(move.Move((6, self.coords[1]), specialMove="Castle", thirdParty=(kingSidePieces[2], (5, self.coords[1]))))
				if queenSidePieces[0] != False and queenSidePieces[0].noMoves == 0 and queenSidePieces[1] == False and queenSidePieces[2] == False and queenSidePieces[3] == False:
					possible = True
					for x in range(1, 5):
						tempKing = King(self.colour, (x, self.coords[1]))
						board.piecesGroup.add(tempKing)
						if board.checkCheck(self.colour):
							possible = False
						board.piecesGroup.remove(tempKing)

					if possible:
						moves.append(move.Move((2, self.coords[1]), specialMove="Castle", thirdParty=(queenSidePieces[0], (3, self.coords[1]))))

		return moves + self.getStraightMoves(board, limit=1) + self.getDiagonalMoves(board, limit=1)