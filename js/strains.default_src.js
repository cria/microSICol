function hideIfLotDontExist() 
{    
    if(typeof lot_exist != 'undefined')
    {
        if (lot_exist == 0)
        {
            document.getElementById('tab_quality').style.display = 'none';
            document.getElementById('quality').style.display = 'none';
            if (location.href.indexOf('#quality') > -1)
            {
                show('general');
            }
        }
    }
}

addEvent(window, 'load', hideIfLotDontExist);