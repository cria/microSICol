//data div manipulation
function show(div)
{
    if (div == 'undefined') div = 'general';

    var prefix = 'tab_';
    var divs;
    if (document.getElementById('tab_deposit')) //case - Strains
    {
     divs = new Array('general','coll_event','isolation','identification','deposit','culture','characs','properties','quality','stock','security');
  }
    else if (document.getElementById('tab_groups')) //case - Configuration - admin mode
    {
     divs = new Array('general','groups','colls','subcolls','combos','dbs','configxml','divisions', 'templates');
  }
    else if (document.getElementById('tab_security')) //case - Tabs (species,documents,references...)
    {
     divs = new Array('general','security');
  }
    else if (document.getElementById('tab_account')) //case - Preferences
    {
     divs = new Array('general','account');
  }
    else //none of the others...
    {
     divs = new Array('general');
  }
    //Hide all divs
    for (var x = 0; x <divs.length; x++)
    {
        $('#' + divs[x]).css('display', 'none');
        $('#' + prefix + divs[x]).attr('class', '');        
    }
    //Show only chosen div
    $('#' + div).css('display', 'block');
    $('#' + prefix + div).attr('class', 'on_menu');        
    
  if (document.getElementById('tab_groups')) //case - Configuration
  {
     change_submenu(div);
  }
    //Add anchor to chosen tab in location.href
    strURL = window.location.href;
    if (strURL.indexOf('#') == -1 )
    {
        //Add new anchor
        strURL += '#'+div+'';
        window.location.href = strURL; //last # needed in order to avoid scrolling down the screen
    }
    else
    {
        //Remove old anchor
        strURL = strURL.substring(0,strURL.indexOf('#'));
        //Add new anchor
        strURL += '#'+div+'';
        window.location.href = strURL; //last # needed in order to avoid scrolling down the screen
    }
    //unFocus menu button
    if($('#' + div)[0])
    {
        $('#' + div)[0].focus();
        $('#' + div)[0].blur();
    }
    //Fix weird IE-tinyMCE bug
  showOnlyDefaultFieldTabs_Fix();
}

function show_anchored_tab()
{
  if (location.href.indexOf("&print=1") == -1)
  {
      //Get which tab must be activated
      div_tab = getActiveTab();
      show(div_tab);
      //Exception for quality and stock
      if (div_tab == 'quality') showQuality();
      if (div_tab == 'stock') showStock();
  }
  else //print this page
  {
    //Dynamically add "print.css"
    head = document.getElementsByTagName("head")[0];
    css = document.createElement('link');
    css.rel  = 'stylesheet';
    css.href = '../css/print.css';
    css.media = 'all';
    css.type  = 'text/css';
    head.appendChild(css);
    window.print();
  }
}

//Fix IE weird tinyMCE bug
function showOnlyDefaultFieldTabs_Fix(){
    langs = document.getElementById('data_langs');
    if (langs == null) return;
    langs = langs.value.split(',');

    for(field in default_multi_language_fields){
        for(lang in langs){
            field_current = document.getElementById(default_multi_language_fields[field]+"_field_"+langs[lang]);
            if (field_current == undefined || field_current == null) continue;

            field_current.style.display = 'block';
            field_current.style.display = 'none';
            field_current.style.display = 'block';
            if (lang == 0) {
                field_current.style.display = 'block';
            } else {
                field_current.style.display = 'none';
            }
        }
    }
}

//Add event for window.onload
addEvent(window, 'load', show_anchored_tab);
