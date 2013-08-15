function showDivs(){
    var value = document.getElementById('format').value;
    
    if(value == 1){
        document.getElementById('default_html_options').style.display = 'block';
        document.getElementById('csv_options').style.display = 'none';
        document.getElementById('chart_options').style.display = 'none';
        document.getElementById('custom_html_options').style.display = 'none';
    }
    else if(value == 2){
        document.getElementById('default_html_options').style.display = 'none';
        document.getElementById('csv_options').style.display = 'block';
        document.getElementById('chart_options').style.display = 'none';
        document.getElementById('custom_html_options').style.display = 'none';
    }
    else if(value == 3){
        document.getElementById('default_html_options').style.display = 'none';
        document.getElementById('csv_options').style.display = 'none';
        document.getElementById('chart_options').style.display = 'block';
        document.getElementById('custom_html_options').style.display = 'none';
    }
    else if(value == 4){
        document.getElementById('default_html_options').style.display = 'none';
        document.getElementById('csv_options').style.display = 'none';
        document.getElementById('chart_options').style.display = 'none';
        document.getElementById('custom_html_options').style.display = 'inline-block';
    }
    else if(value == 5){
        document.getElementById('default_html_options').style.display = 'none';
        document.getElementById('csv_options').style.display = 'none';
        document.getElementById('chart_options').style.display = 'none';
        document.getElementById('custom_html_options').style.display = 'none';
    }

}


function openFieldLinkPopUp(id, field, label){    
    var url = 'fieldlink.py?id=' + id + '&label=' + label + '&field=' + field;    
    return window.open(url,'mywindow','location=0,status=0,toolbar=0,scrollbars=0,menubar=0,resizable=0,width=350,height=200, left=20, top=20');
}