function popWinOpen(zURL,zWidth,zHeight,zType) 
{
    boxy = new Boxy( '<div id="framediv" > <iframe FRAMEBORDER="0" onload="reSizeIFrame(' + zWidth + ');" id="TextLinkIframe" style="border:0; margin:0; padding:0" src ="' + zURL + '" width="' + zWidth + '" height="' + zHeight + '" > <p>Your browser does not support iframes.</p></iframe></div>',
        { title: zType, modal: true, closeText: "<img src='../img/close.png' ALT='" + _('Close') + "' />", show: true, unloadOnHide: true }); 
    boxy.center();
    boxy.show();
} 

function reSizeIFrame(zWidth)
{
    var _y = document.getElementById('framediv');
    var _z = document.getElementById('TextLinkIframe');
    
    for (i = 0; i < window.frames.length ;i++)
    {
        if (window.frames[i].document.body.id == 'popup')
        {
            var _x = window.frames[i].document.body.innerHTML;
            if (_x != '')
            {
                //_y.innerHTML = _x;
                _z.height = window.frames[i].document.body.clientHeight + 10;
                if (_z.height > document.documentElement.clientHeight-50)
                    _z.height = document.documentElement.clientHeight-50;
                _y.style.width = zWidth + 'px';
                _y.style.margin = 0;
                _y.style.padding = 0;
            }
        }
    }
    
    var _w = document.getElementById('boxyTable');
    var height = (document.documentElement.clientHeight - _w.clientHeight)/2;
    if (height > 100)
        height = 100;
    _w.style.top = height + 'px';
}
