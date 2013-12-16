#!/usr/bin/env node

var assert = require( 'assert' )
  , Processor = require( 'mucbuc-jsthree' ).Processor
  , events = require( 'events' ); 

assert( Processor );

testNOP();
testLocals();

function testLocals() {

	translate( 'def dot(a, b, c):return a+b+c\n', function( result ) {
		
		console.log( 'result', result );

		assert( result == 'function hello(a) {\nvar loc;\n}' );
		console.log( 'testLocals passed' );
	} );
}

function testNOP() {

	translate( 'def hello():pass\n', done );

	function done( result ) {
		assert( result == 'function hello() {\n}' );
		console.log( 'testNOP passed' );
	}
}

function translate( code, done ) {
	var e = new events.EventEmitter()
	  , p = new Processor( { cmd: "python", args: [ "translate.py", code ], cwd: "../logic/" }, e )
	  , result = ''; 

	e.on( 'read', function( data ) {
		result += data.toString();
	} );

	e.on( 'close', function() {
		done( result );
	} );

	e.on( 'child_error', function(data) {
		console.log( data.toString() );
	} );

	e.emit( 'execute' );
}