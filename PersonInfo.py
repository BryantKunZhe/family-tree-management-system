# -*- coding: utf-8 -*-
class PersonInfo:
	def __init__(self, name = None, birthday = None, address = None,
	 marry = None, alive = None, deathday = None):
		self.name = name
		self.birthday = birthday
		self.address = address
		self.marry = marry
		self.alive = alive
		self.deathday = deathday

	def SetName(self, name):
		self.name = name

	def SetBirthday(self, birthday):
		self.birthday = birthday

	def SetAddress(self, address):
		self.address = address

	def SetMarry(self, marry):
		self.marry = marry

	def SetAlive(self, alive):
		self.alive = alive

	def SetDeathday(self, deathday):
		self.deathday = deathday