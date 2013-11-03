#!/usr/bin/python

import sys
from variable import Variable

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

	def function_logic(self, space):
		return self.function( * self.transform( self.arguments, space ) )

	def transform( self, arguments, space ):
		result = []
		for arg in arguments:
			result.append( Variable( arg ) )
		return result

#	logic for return: 
#	1) do regex test to see if return is called
#	2) compare return to all local variables
#	3) return logic if 'return' but 'not return local variable'

def translate( f, space, return_index = None, return_operation = None ):
	t = Translation( f );
	
	result =  'function ' + t.function_signature() + ' {\n'
	
	if t.has_local_variables():
		result += 'var ' + t.local_variables() + ';\n'
	
	if return_operation is not None:
		result += '  return '
	
	logic_result = t.function_logic( space )
	if logic_result is not None:
		result += str( logic_result ) + ';\n';
	
	if return_index is not None:
		result += '  return ' + f.func_code.co_varnames[return_index].strip( ',' ) + ';\n'

	return result + '}';

if __name__ == '__main__':
	Locals = {}
	exec( sys.argv[1], {}, Locals )
	result = translate( Locals[Locals.keys()[0]], [ 'x', 'y', 'z' ], None, None )
	sys.stdout.write( result )
