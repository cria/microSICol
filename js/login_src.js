//Login Test 
var count = 0;

function login_test(code,is_admin)
{
	var target = document.getElementById('result');
    var frame_msg = document.getElementsByName('request').item(0);
	var msg = _("Login Success");
	var color = '#009900';

	switch (code)
	{
		case (2): //success - many subcollections
			document.location = './subcollections.py';
			break;
		case (1): //success- one subcollection
			document.forms['start'].submit();
			break;
		case (0): //generic error
			msg = _("Unknown error on Login");
			color = "#FF0000";
			break;
		case (-1): //empty fields error
			msg = _("Empty field(s).");
			color = "#0033CC";
			break;
		case (-2): //login error
			msg = _("Incorrect user or password.");
			color = "#FF0000";
			break;
		case (-3): //probably SQLite login-pass does not match MySQL login-pass
			msg = _("Access denied on main database.");
			color = "#FF0000";
			break;
		case (-4): //database is not activated
			msg = _("Unable to connect to database.");
			color = "#FF0000";
			break;
		case (-5): //Invalid label_lang entry in config.xml.
			msg = _("Invalid label_lang entry in config.xml.");
			color = "#FF0000";
			break;
		case (-6):
			msg = _("Login Failed: User does not have access to this database.");
			color = "#FF0000";
			break;
    default: //generic error
			msg = _("Unknown error on Login");
			color = "#FF0000";
      break;
   }
	
	target.style.color = color;
	target.innerHTML = msg+"<br />";
	//if (code < 1) target.innerHTML += _("Attempts:") + "  " + (++count) + " " + _("times.");
    if ((code < -2) || !code) frame_msg.className = 'frame';
    else frame_msg.className = '';
}
