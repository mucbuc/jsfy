#!/usr/bin/python

import sys
import copy

class Context(object):
  	dimensions = [ 'x', 'y', 'z' ]
		
class Scalar(object):
	def __init__(self, name ):
		self.name = name
	def __str__(self):
		return self.name
	def __len__(self):
		return 1
	def __radd__(self, other):
		return self
	def __add__(self, other):
		return Scalar( str(self) + '+' + str(other) )
	def __mul__(self, other):
		return Scalar( str(self) + '*' + str(other) )

class Future(object):
	def __add__(self, other):
		return Node( self, '+', other )
	def __mul__(self, other):
		return Node( self, '*', other )

class Variable(Future):
	def __init__(self, name):
		self.name = name
	def __len__(self):
		return len( Context.dimensions )
	def __iter__(self):
		return Iterator( self ) 
	def __getitem__(self, i):
		return Scalar( self.name + '.' + str( i ) )

class Node(Future):
	def __init__(self, lhs, op, rhs): 
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	def __len__(self):
		return len( self.lhs )
	def __iter__(self):
		return Iterator( self ) 
	def __getitem__( self, i ):
		return Scalar( str( self.lhs[i] ) + self.op + str( self.rhs[i] ) )
	def __str__( self ):
		if len(self.lhs) > 1:
			result = ''
			for i in Context.dimensions:	
				result += str( self[i] ) + '\n'
			return result
		return str( self.lhs ) + self.op + str( self.rhs )

class Iterator(object): 
	def __init__( self, container ):
		self.container = container
		self.iter = iter( Context.dimensions )
	def next( self ):
		return self.container[ self.iter.next() ]

def main_loop():
	
	print 'function dot( a, b ) {'
	print '  return ' + str( sum( Variable( 'a' ) * Variable( 'b' ) ) ) + ';'
	print '}'
	
if __name__ == '__main__':
	main_loop()