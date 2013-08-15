var incGlobal = 0;
var errorsReports = false;
//var incDropDown = 1;
//Cria Primeira div (sem conector e não pode ser removida)

function AddClick(obj)
{
    if ($('#filterDiv_0_Childs')[0].childNodes.length == 0)
    {
        AddDiv('filterDiv_0', false);
    }
    else
    {
        AddDiv('filterDiv_0', true);
    }
    return false;
}

function AddDiv(idParent, showConnector)
{
    var tempDiv = newDiv(idParent, showConnector);
    if(navigator.appName == "Microsoft Internet Explorer")
    {
        $('#' + idParent)[0].innerHTML+="";
    }
    
    $('#' + idParent).find('#' + idParent + '_Childs')[0].appendChild(tempDiv);
    if(navigator.appName == "Microsoft Internet Explorer")
    {
        $('#' + idParent).find('#' + idParent + '_Childs')[0].innerHTML+="";
    }
    if ($(document).find('[idParent = ' + idParent + "]").length > 0)
    {
        $('#' + idParent).find('#' + idParent + '_Childs').attr("class","divWithChild");
    }
    else
    {
        $('#' + idParent).find('#' + idParent + '_Childs').attr("class","");
    }
}

function RemoveDiv(idDiv)
{
    idParentChilds = $('#' + idDiv).attr("idParent") + "_Childs";
     
    $('#' + idDiv).remove();
    
    if ($('#filterDiv_0_Childs')[0].childNodes.length > 0 &&
        $('#filterDiv_0_Childs')[0].childNodes[0].childNodes[0].id.indexOf('connector') != -1)
    {
        id_span   = $('#filterDiv_0_Childs')[0].childNodes[0].childNodes[0].id;
        id_select = $('#filterDiv_0_Childs')[0].childNodes[0].childNodes[6].id;
        $('#' + id_span).remove();
        $('#' + id_select).remove();
    }
    
    if ($('#' + idParentChilds)[0].childNodes.length > 0)
    {        
        $('#' + idParentChilds).attr("class","divWithChild");
    }
    else
    {
        $('#' + idParentChilds).attr("class","");
    }    
}

function newDiv(idParent, showConnector)
{
    incGlobal++;
 
    var tempDiv = document.createElement("div");
    tempDiv.id = 'filterDiv_' + incGlobal.toString();
        
    var tempDivChilds = document.createElement("div");
    tempDivChilds.id = 'filterDiv_' + incGlobal + '_Childs'.toString();
    
    var table = document.createElement("table");
    var line = document.createElement("tr");
    var line2 = document.createElement("tr");
    

    if (showConnector != false)
    {
        td = document.createElement("td");        
        td.appendChild(newSpan(_('connector'), 'connector','0'));
        line.appendChild(td);
        td = document.createElement("td");        
        td.appendChild(newSpan(_('field'),'field','0'));
        line.appendChild(td);
        td = document.createElement("td");        
        td.appendChild(newSpan(_('condition'),'condition','0'));
        line.appendChild(td);
        td = document.createElement("td");        
        td.appendChild(newSpan(_('type'),'type','0'));
        line.appendChild(td);
        td = document.createElement("td");        
        td.appendChild(newSpan(_('value'),'value','0'));        
        line.appendChild(td);
        td = document.createElement("td");        
        td.appendChild(newDropDown(arrayConnectors, arrayConnectors, 'connector', true));
        line2.appendChild(td);
    }
    else
    {
        td = document.createElement("td");
        line.appendChild(td);
        td = document.createElement("td");
        td.appendChild(newSpan(_('field'),'field','0'));
        line.appendChild(td);
        td = document.createElement("td");
        td.appendChild(newSpan(_('condition'),'condition','0'));
        line.appendChild(td);
        td = document.createElement("td");
        td.appendChild(newSpan(_('type'),'type','0'));
        line.appendChild(td);
        td = document.createElement("td");
        td.appendChild(newSpan(_('value'),'value','0'));
        line.appendChild(td);
        td = document.createElement("td");                
        td.appendChild(newDropDown([], [], 'connector', false));
        line2.appendChild(td);
    }
    
    td = document.createElement("td");
    line.appendChild(td);
    td = document.createElement("td");
    line.appendChild(td);
    
    td = document.createElement("td");
    td.appendChild(newDropDown(arrayFields, arrayFieldsValues, 'field', true));
    line2.appendChild(td);
    td = document.createElement("td");
    td.appendChild(newDropDown(arrayConditions, arrayConditionsValues,'condition', true));
    line2.appendChild(td);
    td = document.createElement("td");
    td.appendChild(newDropDown(arrayTypes, arrayTypesValues, 'type', true));
    line2.appendChild(td);
    td = document.createElement("td");
    td.appendChild(newTextBox());    
    td.appendChild(newDropDown(arrayFields, arrayFieldsValues, 'anotherfield', false));    
    td.appendChild(newDropDown([], [], 'enum', false));
    line2.appendChild(td);
    tempDiv.setAttribute("idParent", idParent);
    
    td = document.createElement("td");
    td.appendChild(newAddButton(tempDiv.id));
    line2.appendChild(td);
    td = document.createElement("td");
    td.appendChild(newDelButton(tempDiv.id));
    line2.appendChild(td);
  
    table.appendChild(line);
    table.appendChild(line2);
  
    tempDiv.appendChild(table);
    tempDiv.appendChild(tempDivChilds);    
    
    return tempDiv;
}

function newSpan(txt, id, size)
{    
    var tmp = document.createElement('label');
    tmp.style.marginLeft = size + 'px';
    tmp.setAttribute('for', id + '_' + incGlobal);
    tmp.innerHTML = txt;
    tmp.id = "span_" + id + "_" + incGlobal;
    
    return tmp;
}

function newTextBox()
{
    var tempText = document.createElement("input");
    tempText.type = "text";
    tempText.setAttribute('class','borderItem');
    tempText.setAttribute("onblur","if(!isEmpty(this,document.getElementById('span_value_"+ incGlobal + "'))) Feedback(0);");
    tempText.size='20';
    tempText.name= "value_" + incGlobal;
    tempText.id="value_" + incGlobal;
    
    return tempText;
}

function newAddButton(idDiv)
{
    var tempButton = document.createElement("img");
    tempButton.src = "../img/record_add.png";
    tempButton.style.cursor = 'pointer';
    tempButton.setAttribute("onclick","AddDiv('" + idDiv + "', true, true);return false;");    
    tempButton.value = ' + ';	
    
    return tempButton;
}

function newDelButton(idDiv)
{
    var tempButton = document.createElement("img");    
    tempButton.src = "../img/record_delete.png";    
    tempButton.style.cursor = 'pointer';
    tempButton.setAttribute("onclick","RemoveDiv('" + idDiv + "');return false;");        
    tempButton.value = ' x ';
    tempButton.setAttribute("class","button");
    tempButton.setAttribute("borderNone","0");
    
    return tempButton;
}

function showField(index)
{
    var data_type = arrayFieldsDef[$('#field_' + index).val()];
    var ddl_type = $('#type_' + index)[0];
   
    $('#enum_' + index).hide();
    $('#anotherfield_' + index).hide();
    $('#value_' + index).hide();
    $('#value_' + index).removeAttr('disabled');
    
    if (ddl_type.value == "Fixed" || ddl_type.value == "")
    {
        $('#value_' + index).show();            
        $('#span_value_' + index).text(_('value'));
    }
    else if (ddl_type.value == "Variable")
    {
        $('#value_' + index).show();
        $('#value_' + index).attr('disabled', 'disabled');
        $('#value_' + index).attr("value","");
        $('#span_value_' + index).text(_('value'));
    }
    else if (ddl_type.value == "Field")
    {
        $('#value_' + index).hide();
        $('#anotherfield_' + index)[0].style.display = 'inline';
        $('#span_value_' + index).text(_('field'));
    }
    
    if (data_type == 'enum')
    {
        $('#value_' + index).hide();
        if ($('#type_' + index).val() == 'Fixed' || $('#type_' + index).val() == '')
        {
            $('#enum_' + index)[0].style.display = 'inline';
        }
        else if ($('#type_' + index).val() == 'Field')
        {
            $('#anotherfield_' + index)[0].style.display = 'inline';
        }
        else
        {
            $('#value_' + index).show();
            $('#value_' + index).attr('disabled', 'disabled');
            $('#span_value_' + index).text(_('value'));
        }
        
        safeVal = $('#enum_' + index).val();
        dropDownItems('enum_' + index, index, $('#field_' + index).val());
         $('#enum_' + index).val(safeVal);
    }
    checkAnotherField(index);
    checkConditions(index);
}

function newDropDown(arrayItems, arrayValues, name, visible)
{
    var tempDD = document.createElement("select");			
    tempDD.name = name + '_' + incGlobal;
    tempDD.id = name + '_' + incGlobal;    
    tempDD.options[0] = new Option();
    
    
    
    if(navigator.appName == "Microsoft Internet Explorer"){        
        tempDD.className = "borderItem";
    }
    else{
        tempDD.setAttribute("class", "borderItem");
    }
    if (visible == false)
    {
        $(tempDD).hide();
    }
    
    for (i=0; i<arrayItems.length; i++)
    {	
        tempDD.options[i+1] = new Option(decodeString(arrayItems[i]), arrayValues[i]);
    }

    if (name == 'field')
    {
        tempDD.className = "borderItem select_field";
        tempDD.setAttribute("onChange", "$('#value_" + incGlobal + "').val('');" + "validateField(" + incGlobal + ",event); $('#value_" + incGlobal + "').change(); checkAnotherField(" + incGlobal + "); checkConditions(" + incGlobal + ");");        
    }
    
    if (name == 'condition')
    {       
        tempDD.className = "borderItem select_condition";
        tempDD.setAttribute("onChange", "$('#value_" + incGlobal + "').val('');" + "validateField(" + incGlobal + ",event);");        
    }
    
    if (name == 'type')
    {
        tempDD.className = "borderItem select_type";
        tempDD.setAttribute("onChange", "showField(" + incGlobal + ");");        
    }
    
    if (name == 'enum')
    {
        name = 'value';   
    }
    //IE
    if(navigator.appName == "Microsoft Internet Explorer"){
        tempDD.onblur = Function("if(!isEmpty(this, document.getElementById('span_" + name + "_" + incGlobal + "'))) Feedback(0);");
    }
    else{
        tempDD.setAttribute("onblur", "if(!isEmpty(this, document.getElementById('span_" + name + "_" + incGlobal + "'))) Feedback(0);");
    }
    
    return tempDD;
}

var filterFinal = '';

function validateForm()
{
    ok = true;      
    
    if (!validateReports(3))
    {
        ok = false;
    }

    return ok;
}

function saveData()
{
    $('#pageContents').val(escape($('#filterDiv_0')[0].innerHTML));
    filterFinal='[';
    getAllFilters('filterDiv_0');
    filterFinal += ']';
    
    $('#allFilters').val(filterFinal);    
}

function getAllFilters(Parent)
{    
    var filterDiv = $('#' + Parent);
    var divList = filterDiv.find("[idParent='" + Parent + "']");    
    for (var i = 0; i < divList.length; i++)
    {        
        var divAtual = $('#' + divList[i].id);        
        ddlField = divAtual.find('select[id^="field"]');
        ddlConnector = divAtual.find('select[id^="connector"]');
        ddlConditions = divAtual.find('select[id^="condition"]');    
        ddlType = divAtual.find('select[id^="type"]');
        txtValue = divAtual.find('input[id^="value"]');
        ddlValue = divAtual.find('select[id^="anotherfield"]');
        ddlEnum = divAtual.find('select[id^="enum"]');
        
        if (ddlField != null && ddlField.val() != undefined)
        {
            filterFinal += "{'field':'" + ddlField.val() + "', 'condition':'" + ddlConditions.val() + "'";
                      
            if (ddlConnector.val() != undefined)
            {
                filterFinal += ", 'connector':'" + ddlConnector.val() + "'";
            }
            
            if (ddlType.val() == "Fixed")
            {
                filterFinal += ", 'user_defined':'false'";

                if (ddlEnum.css("display").toLowerCase() != 'none')
                {
                    filterFinal += ", 'value':'" + ddlEnum.val() + "'";
                }
                if (txtValue.css("display").toLowerCase() != 'none')
                {
                    filterFinal += ", 'value':'" + txtValue.val().replace(/'/gi, "\\" + "'").replace(/"/gi,"&#34;").replace(/</gi,"&#60;").replace(/>/gi,"&#62;") + "'";
                }
                
            }
            else if (ddlType.val() == "Variable")
            {
                filterFinal += ", 'user_defined':'True'";
            }
            else if (ddlType.val() == "Field")
            {            
                filterFinal += ", 'field_lookup':'" + ddlValue.val() + "'";
            }
            //filterFinal += ">";
            filterFinal += ", 'childs':[";
        }

        if (filterDiv.find("[idParent='" + Parent + "']").length > 0)
        {
            getAllFilters(divAtual.attr("id"));
        }
        //filterFinal += "}";
        filterFinal += "]},";
    }    
}

function decodeString(utftext)
{
    var string = "";
    var i = 0;
    var c = c1 = c2 = 0;

    while ( i < utftext.length ) {

            c = utftext.charCodeAt(i);

            if (c < 128) {
                    string += String.fromCharCode(c);
                    i++;
            }
            else if((c > 191) && (c < 224)) {
                    c2 = utftext.charCodeAt(i+1);
                    string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
                    i += 2;
            }
            else {
                    c2 = utftext.charCodeAt(i+1);
                    c3 = utftext.charCodeAt(i+2);
                    string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
                    i += 3;
            }
    }

    return string;
}

function validateField(index, e, field_name, List)
{    
    var data_type;
    var field;
    
    var isList = false;
    if(List == undefined)
    {    
        if($('#condition_' + index).val() == 'in' || $('#condition_' + index).val() == 'not_in')
        {
            isList = true;
        }
    }
    else
    {
        isList = List;
    }
    
    if (field_name == undefined)
    {
        data_type = arrayFieldsDef[$('#field_' + index).val()];
        field = $('#field_' + index).val();
    }
    else
    {
        data_type = arrayFieldsDef[field_name];
        field = field_name;
    }
    $('#value_' + index).attr("data_type", data_type);
    
    $('#value_' + index)[0].maxLength = '500';
    
    $('#value_' + index).unbind("keypress");
    $('#value_' + index).unbind("keyup");
    $('#value_' + index).unbind("change");
        
    //$('#value_' + index).val("");
    //$('#enum' + index).val("");
    
    if (data_type == 'integer' || data_type == 'tinyint')
    {
        $('#value_' + index).keyup(function()
        {
            if(isList){
                numberOnlyGPS(this, ';');    
            }
            else
            {
                numberOnly(this);
            }
        });
    
        $('#value_' + index).change( function() 
        {
            if(isList)
            {
                var txt = this.value.split(';');
                for(var i = 0; i < txt.length; i++)
                {
                    if (!isInteger(txt[i]))
                    {
                        showError(this,null,_("Only numbers are allowed for this field."));
                        Feedback(-16);
                        break;
                    }      
                }                
            }
            else
            {
                if (!isInteger(this.value))
                {
                    showError(this,null,_("Only numbers are allowed for this field."));
                    Feedback(-16);
                }
            }
        })
    }
    else if (data_type == 'date')
    {
        $('#value_' + index)[0].setAttribute("onblur", "");
        var length = 10;
        if(isList)
        {
            length = 255;
        }
        $('#value_' + index)[0].maxLength = length;
        $('#value_' + index).keypress( function(e)
        {
            if(isList)
            {
                    return checkDateSlash($('#value_' + index)[0], e, true);
            }
            else
            {
                return checkDateSlash($('#value_' + index)[0], e);
            }
        });
        
        $('#value_' + index).keyup(function(e)
        {
            if(isList)
            {
                checkCharModifier(this, e, true);
            }
            else
            {
                checkCharModifier(this, e);
            }
        });        
        
        $('#value_' + index).change( function(e) 
        {
            if (lang_code == 'en')
            {
                date_format = '%m/%d/%Y';
            }
            else
            {
                date_format = '%d/%m/%Y';
            }
            if(!isEmpty(this, document.getElementById('span_value_' + index))){                            
                checkValidDate(this, document.getElementById('span_value_' + index), date_format, false);
            }            
        })
    }
    else if (data_type == 'decimal_gps')
    {        
        separator = '.';
        if(isList)
        {
            $('#value_' + index)[0].maxLength = '255';
        }
        else
        {
            $('#value_' + index)[0].maxLength = '11';
        }
        
        $('#value_' + index).change( function() 
        {
            if(isList)
            {
                if (!checkListGPS($('#field_' + index).val(), this))
                {
                    showError(this,null,_("Only decimal gps format: (+/-)DD.DDDDDDDD are allowed for this field."));
                    Feedback(-16);
                }
                else
                {
                    Feedback(0);
                }
            }
            else
            {
                if (!checkGPS($('#field_' + index).val(), this))
                {
                    showError(this,null,_("Only decimal gps format: (+/-)DD.DDDDDDDD are allowed for this field."));
                    Feedback(-16);
                }
                else
                {
                    Feedback(0);
                }
            }
        })
    }
    else if (data_type == 'decimal')
    {        
        //Não existem campos desse tipo, por isso não foi colocada máscara.
        //Futuramente, caso precise, deve ser adicionada aqui.
        $('#value_' + index).change( function() 
        {
            if (!checkFloat(this, null, 9, 9, true, isList))
            {
                showError(this,null,_("Only decimal numbers are allowed for this field."));
                Feedback(-16);
            }
            else
            {
                Feedback(0);
            }            
        })
    }    
    else if (data_type == 'enum')
    {
        if (field_name == undefined)
        {
            name_field = 'enum_' + index;
        }
        else
        {   
            name_field = 'value_' + index;
        }
        
        safeVal = $('#enum_' + index).val();
        dropDownItems(name_field, index, field);
        $('#enum_' + index).val(safeVal);
    }

    if (field_name == undefined)
    {
        showField(index);
    }
}

function dropDownItems(id, index, field)
{
    var arrayItems = [];
    var arrayValues = [];
    
    for (var key in enum_label_values[field])
    {            
        arrayItems[arrayItems.length] = enum_values[enum_label_values[field][key]];
        arrayValues[arrayValues.length] = key;
    }
    
    $('#' + id + ' option').each(function()
    {
        $(this).remove();
    });    

    for (i=0; i<arrayItems.length; i++)
    {	
        $('#' + id)[0].options[i] = new Option(decodeString(arrayItems[i]), arrayValues[i]);        
    }
}

function checkAnotherField(index)
{
    if ($('#type_' + index).val() == 'Field')
    {
        var data_type = arrayFieldsDef[$('#field_' + index).val()];
        var valueField = $('#anotherfield_' + index).val();
        $('#anotherfield_' + index + ' option').each(function()
        {
            $(this).remove();
        });
        
        var option = document.createElement("option");        
        $('#anotherfield_' + index)[0].options[0] = new Option();

        var j = 1;
        for (i=0; i<arrayFields.length; i++)
        {				
            data_type_another = arrayFieldsDef[arrayFieldsValues[i]];            
            if (data_type == data_type_another)
            {                
                $('#anotherfield_' + index)[0].options[j] = new Option(decodeString(arrayFields[i]), arrayFieldsValues[i]);
                j++;
            }
        }
        
        $('#anotherfield_' + index).val(valueField);
    }
}

function checkConditions(index)
{
    //index conditions
    //0 - Equal
    //1 - Contains
    //2 - in
    //3 - not_in
    //4 - greater
    //5 - greater_or_equal
    //6 - less
    //7 - less_or_equal
        
    arrayToString = ['equal', 'differs', 'contains', 'in', 'not_in'];
    arrayToOthers = ['equal', 'differs', 'contains', 'in', 'not_in', 'greater', 'greater_or_equal', 'less', 'less_or_equal'];
    arrayToEnum = ['equal', 'differs'];
    
    var data_type = arrayFieldsDef[$('#field_' + index).val()];
    var valueSafe = $('#condition_' + index).val();
    $('#condition_' + index + ' option').each(function()
    {
        $(this).remove();
    });        
    
    $('#condition_' + index)[0].options[0] = new Option();

    if(typeof data_type == 'undefined')
    {
        var arrayAll = arrayToOthers;
    }
    else{
        if (data_type.toLowerCase() == "text" || data_type.toLowerCase() == "varchar")
        {
            var arrayAll = arrayToString;
        }
        else if (data_type.toLowerCase() == "enum")
        {
            var arrayAll = arrayToEnum;
        }
        else
        {
            var arrayAll = arrayToOthers;
        }
    }

    for (i=0; i<arrayAll.length; i++)
    {	
        $('#condition_' + index)[0].options[i + 1] = new Option(decodeString(arrayConditions[i]), arrayAll[i]);
    }
    
    $('#condition_' + index).val(valueSafe);
    
    $('#span_type_' + index).css('left',$('#type_' + index).css('left'))
}

function populateEnumValues(index, field)
{
    var data_type = arrayFieldsDef[field];
    $('#value_' + index + ' option').each(function()
    {
        $(this).remove();
    });
    
    var option = document.createElement("option");   
    $('#value_' + index)[0].appendChild(option);

    for (i=0; i<arrayFields.length; i++)
    {				
        data_type_another = arrayFieldsDef[arrayFieldsValues[i]];            
        if (data_type == data_type_another)
        {
            var option = document.createElement("option");
            option.value = arrayFieldsValues[i];
            option.text = decodeString(arrayFields[i]);
            $('#value_' + index)[0].appendChild(option);
        }
    }
}

function validateGenerateFields(finalIndex)
{ 
    retValue = true;
    for (p=1; p<=finalIndex; p++)
    {
        obj = $('#value_' + p);
        if (obj.val() == "")
        {
            showError(obj[0], null, _("Field must not be empty."));
            Feedback(-1);
            retValue = false;
        }        
        else 
        {
            var type = obj.attr('data_type');
            if(type == 'date')
            {
                if (lang_code == 'en')
                {
                    date_format = '%m/%d/%Y';
                }
                else
                {
                    date_format = '%d/%m/%Y';
                }
                if(!checkValidDate(document.getElementById('value_' + p), null, date_format, false))
                {
                    Feedback(-16);
                    retValue = false;
                }
            }
        }
        if(retValue == true)
        {
            resetField(obj[0], null);
        }
    }
    return retValue;
}