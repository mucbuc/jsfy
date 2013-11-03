#!/usr/bin/env node

var assert = require( 'assert' )
  , Processor = require( 'mucbuc-jsthree' ).Processor
  , events = require( 'events' ); 

assert( Processor );

testBasic();

function testBasic() {
	var e = new events.EventEmitter()
	  , p = new Processor( { cmd: "python", args: [ "translate.py", "def hello():pass\n" ], cwd: "../logic/" }, e )
	  , result = ''; 

	e.on( 'read', function( data ) {
		result += data.toString();
	} );

	e.on( 'close', function() {
		assert( result == 'function hello() {\n}' );
		console.log( 'basic test passed' );
	} );

	e.on( 'child_error', function(data) {
		console.log( data.toString() );
	} );

	e.emit( 'execute' );
}