# -*- coding: utf-8 -*-
class FamilyNode:
	def __init__(self, identify = None, parentId = None, 
		children = None, nodeInfo = None):
		self.identify = identify
		self.parentId = parentId
		self.children = children
		self.nodeInfo = nodeInfo