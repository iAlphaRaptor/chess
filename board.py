import pygame
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR
pygame.init()

class Board:
	def __init__(self, piecesGroup):
		self.piecesGroup = piecesGroup

	def getCurrentKing(self, colour):
		for piece in self.piecesGroup.sprites():
			if piece.piece == "King" and piece.colour == colour:
				return piece

	def getPiece(self, coords):
		for piece in self.piecesGroup.sprites():
			if list(coords) == list(piece.coords):
				return piece
		return False

	def isSquareEmpty(self, coords):
		for piece in self.piecesGroup:
			if piece.coords[0] == coords[0] and piece.coords[1] == coords[1]:
				return False
		return True

	def movePiece(self, piece, dest):
		piece.coords[0] = dest[0]
		piece.coords[1] = dest[1]
		piece.rect.x = piece.coords[0] * SQUAREWIDTH
		piece.rect.y = piece.coords[1] * SQUAREWIDTH

		piece.noMoves += 1

	def takePiece(self, movingPiece, targetPiece, move):
		self.piecesGroup.remove(targetPiece)
		self.movePiece(movingPiece, move)

	def checkCheck(self, currentPlayer):
		king = self.getCurrentKing(currentPlayer)

		for piece in self.piecesGroup.sprites():
			pieceMoves = piece.getMoves(self)
			for move in pieceMoves:
				if list(move) == list(king.coords) and piece.colour != currentPlayer:
					return True
		return False

	def mateCheck(self, currentPlayer):
		if self.checkCheck(currentPlayer):
			for piece in self.piecesGroup.sprites():
				pieceCoords = piece.coords[:]

				for move in piece.getMoves(self):
					nextMove = (piece.coords[0]+move[0], piece.coords[1]+move[1])
					if self.isSquareEmpty(nextMove):
						self.movePiece(piece, nextMove)
						if not self.checkCheck(currentPlayer):
							self.movePiece(piece, pieceCoords)
							return False
						self.movePiece(piece, pieceCoords)
					else:
						targetPiece = self.getPiece(nextMove)
						temp = targetPiece

						self.takePiece(piece, targetPiece, nextMove)
						if not self.checkCheck(currentPlayer):
							self.piecesGroup.add(temp)
							self.movePiece(piece, pieceCoords)
							return False
						self.piecesGroup.add(temp)
						self.movePiece(piece, pieceCoords)
				self.movePiece(piece, pieceCoords)
			return True
		return False