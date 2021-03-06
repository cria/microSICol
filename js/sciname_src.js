// maps the case formatters 
var caseFormatters = { 
    'ucfirst': 
        function(name) {
            return name.substr(0,1).toUpperCase()+name.substr(1,name.length-1).toLowerCase();
        },

    'upper': 
        function(name) {
            return name.toUpperCase();
        },

    'lower': 
        function(name) {
            return name.toLowerCase();
        }
};

// maps the format formatters
var formatFormatters = {
    'italic':
        function(name) {
            if (name.search(/sp\\./) == -1) { 
                return '<i>'+name+'</i>';
            }
            return name;
        },

    'bold':
        function(name) {
            return '<b>'+name+'</b>';
        }
};

var formatters = {
    // case formatters
    'string_case': caseFormatters,
    // format (bold, italic) formatters
    'string_format': formatFormatters
};

function formatSciName(taxon_group, seq, use_author) {
    var defDict = sciname_dict[taxon_group][seq];
    var prefix = defDict['type_prefix']; 
    var sciName = '';
    
    if (use_author === undefined) {
        use_author = 1;
    }

    var author = '';
    if (use_author == 1 && defDict['has_author'] == 1 && defDict['use_author'] == 1) {
        author = document.getElementById(prefix + "_author_" + taxon_group + "_" + seq).value;
    }

    var name = document.getElementById(prefix + "_value_" + taxon_group + "_" + seq).value;

    name = name.replace(/^\\s+|\\s+\$/g,'');
	
	if (name == '') {
        var default_value = defDict['default_value'];
		name = default_value;
	}
	
    if (name == '') {
		return '';
	}

    // apply all formatters
    for (f in formatters) {
        var value = defDict[f];

        if (value) {
            if (formatters[f][value]) {
                name = formatters[f][value](name);
            }
        }
    }

    name = defDict['prefix'] + name + defDict['suffix'];

    if ((author != '') && (defDict['use_author'] == 1)) { 
        name += ' ' + author;
    }

    return name;
}

function applySciName() {
    var taxon_group = document.getElementById("taxon_group");
    var id_taxon_group = taxon_group.options[taxon_group.selectedIndex].value;
    var defDict = sciname_dict[id_taxon_group];
    
    var hitaxa  = document.getElementById("higher_taxa");
    var sciname = document.getElementById("sciname");
    var hitaxa_html = document.getElementById("higher_taxa_html");
    var sciname_html = document.getElementById("sciname_html");
    var sciname_no_auth = document.getElementById("sciname_no_auth");
    
    if (!defDict) {
        return;
    }
    
    var scinameStr = "";
    var hitaxaStr = "";
    var scinameNoAuthStr = "";
	for (i in defDict) {
        var item = defDict[i];
		
        if (item['hi_tax'] == 1) {
			var this_sciname = trim(formatSciName(id_taxon_group, item['seq']));
			if (this_sciname && this_sciname.length > 0) {
                hitaxaStr += this_sciname + ' ';
			}
        }
        else {
            var in_sciname = item['in_sciname'];
			var this_sciname = trim(formatSciName(id_taxon_group, item['seq']));
			var this_sciname_no_author = trim(formatSciName(id_taxon_group, item['seq'], 0));

			if (in_sciname && this_sciname && this_sciname.length > 0) {
                scinameStr += this_sciname + ' ';
			}
			if (in_sciname && this_sciname_no_author && this_sciname_no_author.length > 0) {
                scinameNoAuthStr += this_sciname_no_author + ' ';
			}
        }
    }
    
    hitaxaStr = hitaxaStr.replace(/^\s+|\s+$/g,"");
    scinameStr = scinameStr.replace(/^\s+|\s+$/g,"");
    
    hitaxa.innerHTML = hitaxaStr;
    sciname.innerHTML = scinameStr;
    
    hitaxa_html.value = hitaxaStr;
    sciname_html.value = scinameStr;

    sciname_no_auth.value = scinameNoAuthStr;
}

function displaySciNameBuilder() {
    var taxon_group = document.getElementById("taxon_group");
    var id_taxon_group = taxon_group.options[taxon_group.selectedIndex].value;
    var options = taxon_group.options;
    
    for (var i = 0; i < options.length; i++) {
        var item = taxon_group.options[i];
        var builder_div = document.getElementById("sciname_builder_" + item.value);
        if (builder_div) {
            builder_div.style.display = (item.value == id_taxon_group ? 'block' : 'none');
        }
    }
        
    applySciName();
}

function validateSciNameFields() {
    var taxon_group = document.getElementById("taxon_group");
    var id_taxon_group = taxon_group.options[taxon_group.selectedIndex].value;
    var defDict = sciname_dict[id_taxon_group];
    var valid = true;
    
    for (key in defDict) {
        var item = defDict[key];
        if (item['required'] == 1) {
            var prefix = item['type_prefix'];
            var seq = item['seq'];
        
            var ctrlId = prefix + "_value_" + id_taxon_group + "_" + seq;
            var scinameControl = document.getElementById(ctrlId);
            var scinameLabel = document.getElementById("label_" + ctrlId);
            
            if (isEmpty(scinameControl, scinameLabel)) {
                valid = false;
            }
        }
    }
    
    return valid;
}