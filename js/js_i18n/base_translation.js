//Get translation from python-generated array
function _(translate_string)
{
    if (__tr[translate_string] == null) return translate_string;
    else return __tr[translate_string];
}

var __tr = new Array();
