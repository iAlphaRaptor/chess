import pygame, move
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

	def movePiece(self, piece, moveObj):
		piece.coords[0] = moveObj.coords[0]
		piece.coords[1] = moveObj.coords[1]
		piece.rect.x = piece.coords[0] * SQUAREWIDTH
		piece.rect.y = piece.coords[1] * SQUAREWIDTH

		if moveObj.specialMove == "Castle":
			self.movePiece(moveObj.thirdParty[0], move.Move(moveObj.thirdParty[1]))
		elif moveObj.specialMove == "EP":
			self.takePiece(piece, moveObj.thirdParty, moveObj, EP=True)

		piece.noMoves += 1

	def takePiece(self, movingPiece, targetPiece, moveObj, EP=False):
		self.piecesGroup.remove(targetPiece)
		if not EP:
			self.movePiece(movingPiece, moveObj)

	def checkCheck(self, currentPlayer):
		king = self.getCurrentKing(currentPlayer)

		for piece in self.piecesGroup.sprites():
			if piece.piece == "King":
				pieceMoves = piece.getMoves(self, ignoreCastles=True)
			else:
				pieceMoves = piece.getMoves(self)

			for possibleMove in pieceMoves:
				if list(possibleMove.coords) == list(king.coords) and piece.colour != currentPlayer:
					return True
		return False

	def mateCheck(self, currentPlayer):
		if self.checkCheck(currentPlayer):
			for piece in self.piecesGroup.sprites():
				if piece.colour == currentPlayer:
					pieceCoords = piece.coords[:]

					for possibleMove in piece.getMoves(self):
						nextMove = possibleMove.coords
						if nextMove[0] > 0 and nextMove[1] > 0:
							if self.isSquareEmpty(nextMove):
								self.movePiece(piece, move.Move(nextMove))
								if not self.checkCheck(currentPlayer):
									print("No Take", piece.piece, piece.colour, nextMove)
									self.movePiece(piece, move.Move(pieceCoords))
									return False
								self.movePiece(piece, move.Move(pieceCoords))
							else:
								targetPiece = self.getPiece(nextMove)
								if targetPiece.colour != piece.colour:
									temp = targetPiece

									self.takePiece(piece, targetPiece, move.Move(nextMove))
									if not self.checkCheck(currentPlayer):
										print("Take", piece.piece, piece.colour, nextMove)
										self.piecesGroup.add(temp)
										self.movePiece(piece, move.Move(pieceCoords))
										return False
									self.piecesGroup.add(temp)
								self.movePiece(piece, move.Move(pieceCoords))
					self.movePiece(piece, move.Move(pieceCoords))
			return True
		return False