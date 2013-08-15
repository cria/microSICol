function showStock() 
{
  if (window.frames['ifrm_stock'])
  {
    if (document.location.toString().indexOf("detail") > -1) type = "detail";
    else type = "other";
    window.frames['ifrm_stock'].location = "strains.stock.list.py?type=" + type + "&id=" + document.forms[0].id.value;
  }
}

function resizeIframe()
{
    new_size = document.getElementById("container").offsetHeight;
    fr = window.parent.document.getElementById("ifrm_stock");
    fr.style.height = new_size + "px";
}

function fillStockJson()
{
    hidden_field = window.parent.document.getElementById("stock_minimum_list");
    minimum_fields = $(".stock_minimum");
    
    var json = "{";
    
    for (i = 0; i < minimum_fields.length; i++) {
        var value = $("#"+minimum_fields[i].id).val();
        if (value && parseInt(value, 10) > 0) {
            json += minimum_fields[i].id.split("stock_minimum_")[1];
            json += ":";
            json += minimum_fields[i].value;
            json += ",";
        }
    }
    
    json += "}"
    
    hidden_field.value = json;
}

//Allow user to type numbers only
//To be used with onkeyup event
function numberOnly(obj)
{
  var numbers = "0123456789";
  var i = 0;
  var changed = false;
  for (i=0;i < obj.value.length; i++)
  {
    if (numbers.indexOf(obj.value.charAt(i)) == -1)
    {
      changed = true;
      break;
    }
  }
  if (changed)
  {
    //Remove all non-number characters
    obj.value = obj.value.replace(/\D+/,'');
  }
}