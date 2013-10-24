#!/usr/bin/python

import sys

def cleanstr( list ):
	result = str( list )
	result = result.replace( '\'', '' ).strip( '(),' );
	return result

class Translation(object):

	def __init__(self, function):
		self.function = function
		self.arguments = function.func_code.co_varnames[0:function.func_code.co_argcount]
	
	def has_local_variables(self):
		fc = self.function.func_code
		return fc.co_argcount != len(fc.co_varnames)

	def local_variables(self):
		fc = self.function.func_code
		return cleanstr( fc.co_varnames[fc.co_argcount:] )

	def function_signature(self):
		result =  self.function.func_name + '('
		result += cleanstr( self.arguments ) + ')'
		return result

	#def function_logic(self, space):
	#	future = self.function( * self.transform( self.arguments, space ) )
	#	return future.project( space )
		
	#	for dim in space:							
	#		result += '  ' + self[dim] + ';\n'
	#	return result


	#def transform( self, arguments, space ):
		#result = []
	#	for arg in arguments:
	#		result.append( Future( arg, space ) )
	#	return result

if __name__ == '__main__':
	locs = {}
	exec( sys.argv[1], {}, locs )
	t = Translation( locs[locs.keys()[0]] );
	sys.stdout.write( t.function_signature() );
