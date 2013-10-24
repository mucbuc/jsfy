
var assert = require( 'assert' )
  , Processor = require( 'mucbuc-jsthree' ).Processor
  , events = require( 'events' ); 

assert( Processor );

function translate(req, res) {
	var e = new events.EventEmitter()
	  , p = new Processor( { cmd: "python", args: [ "translate.py", req.body.code ], cwd: "logic/" }, e )
	  , result = ''; 

	e.on( 'read', function( data ) {
		result += data.toString();
	} );

	e.on( 'exit', function() {
		res.end( result );
	} );

	e.on( 'child_error', function(data) {
		var msg = '\n*** error:';
		msg += typeof data !== 'undefined' ? data.toString() : data; 
		msg += '\n';
		result += msg;

		console.log( msg );
	} );

	e.emit( 'execute' );

	console.log( 'translate', req.body ); 
}

exports.translate = translate;