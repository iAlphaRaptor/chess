import pygame
from constants import SCREENWIDTH, SQUAREWIDTH, LIGHTCOLOUR, DARKCOLOUR
pygame.init()

class Board:
	def __init__(self, piecesGroup):
		self.piecesGroup = piecesGroup

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