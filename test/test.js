#!/usr/bin/env node

var assert = require( 'assert' )
  , Processor = require( 'mucbuc-jsthree' ).Processor
  , events = require( 'events' ); 

assert( Processor );

testBasic();

function testBasic() {
	var e = new events.EventEmitter()
	  , p = new Processor( { cmd: "python", args: [ "translate.py" ], cwd: "../src/" }, e )
	  , result = ''; 


	e.on( 'read', function( data ) {
		result += data.toString();
	} );

	e.on( 'exit', function() {
		assert( 'result\ncleanstr(list)\n' );
	} );

	e.emit( 'execute' );
}