function openLocationDialog(id_coll, id_pres_method, operation, id_strain, strain, currentLocations, callback) { 
   var reqData = {
        'action': 'main', 
        'id_coll': id_coll, 
        'id_pres_method' : id_pres_method,
        'operation' : operation,
        'id_strain': id_strain,
        'strain': strain
   };
   
   $.get("location.callback.py", reqData,
      function(data, textStatus) {
         //console.debug("returned");
         $('img.new').attr('src', '../img/pick.png');
         showDialog($(data), reqData, callback, currentLocations);
      }, 'html');
}

function showDialog(html, reqData, callback, currentLocations) {
    //console.debug("openLocation");
    var boxy = new Boxy(
         $(html), { 
            title: _("Stock Location"), 
            modal: true, 
            confirmHtml: "<img alt='" 
                + _('CONFIRM') + "' title='"
                + _('CONFIRM') + "' id='saveConfirm' src='../img/record_save_disabled.png'/>",
            closeText: "<img alt='    " 
                    + _('CANCEL') + "' title='"
                    + _('CANCEL') + "' src='../img/record_cancel.png'/>",
            show: false
    });
    
    boxy.getLocations = function() {
        var locations = {};
        $("td.lookupCell").each(function(i) {
            if ($(this).find("input.location").val()) {
                locations[get_key($(this))] = reqData['strain'];
            }
        });
        return locations;
    };

    boxy.cloneId = 0;    
    boxy.addRow = function() {
        // clones the container combo
        var new_combo = $("div#location" + this.cloneId).clone(true);
        $(new_combo).find("span").remove();
        $(new_combo).find(".lookupCell").remove();

        show_delete($("div#location" + this.cloneId + " img.remove"));
        
        // increases the current clone id and applies new id
        this.cloneId++;
        $(new_combo).attr("id", "location" + this.cloneId);
        
        // creates the new container combo
        setup_combo($(this), "div#location" + this.cloneId + " select#container", this.cloneId);
        
        // and appends it to the main div
        $("div.main").append(new_combo);
        
        return new_combo;
    }
    
    prepare(boxy, $(html), callback);
    $(boxy).remove('tr.locationRow');
    
    boxy.show();

//   if (currentLocations) {
//        var locs = eval(currentLocations);
//        for (var i = 0; i < locs.length; i++) {
//            var loc = locs[i];
////          id_strain: $("#id_strain").val(),
////          id_container: $(ctrl).find('#id_container').val(),
////          id_container_hierarchy: $(ctrl).find("#id_container_hierarchy").val(),
////          row: $(ctrl).find("#row").val(),
////          col: $(ctrl).find("#col").val()
//            var combo = boxy.addRow();
//            
//            $(combo).find('option').each(function(i) {
//                if ($(this).val() == loc['id_container']) {
//                    $(this).attr('selected', 'selected');
//                }
//            });
//            $(combo).val(loc['id_container']);
//            container_combo_change(boxy, combo);
//        } 
//   }
}

function prepare(main_boxy, html, callback) {
    $("img.remove").hide();
    
    // debug button
    $("input.debug").click(function() {
      // console.debug(main_boxy.getLocations());
    });

    // hides the AJAX loading image
    $("#loading").hide();
    
    // tells AJAX to show the loading div when starting background load
    $("#loading").ajaxStart(function(){
        $(this).show();
    });
    
    // tells AJAX to hide the loading div when loading completes
    $("#loading").ajaxStop(function(){
        $(this).hide();
    });
    
    // sets up the close button
    $("#save").click(function() {
      // console.debug('closing0');
        
        if (!document.locationDict) {
            document.locationDict = {};
        }

        var retDict = [];
        $("td.lookupCell").each(function(i) {
            if ($(this).find("input.location").val()) {
              // console.debug('get_json ' + i);
                retDict[i] = get_json($(this));
              // console.debug(retDict[i]);
                
                document.locationDict[get_key($(this))] = {
                    id_strain: retDict['id_strain'],
                    strain: $('#strain').val()
                };  
            }
        });
        
        console.debug(retDict);
        
        if (callback) {
          // console.debug('callbacker');
            console.debug(retDict);
            callback(retDict);
        }
        
        main_boxy.hideAndUnload();
    });
    
    setup_combo(main_boxy, $("div#location0 select#container"), 0);
}

function container_combo_change(main_boxy, combo) {
  // console.debug($(combo));
  // console.debug($(combo).val());
    if (!$(combo).val()) {
      // console.debug("entered");
      // console.debug($(combo));
        if ($(combo).parents('tr').find('td.delete img.remove').css('display') != 'none') {
            remove_row($(combo).parents('div.location'));
        }
        else {
            disable_save();
        }
    }
    
    // determines parent (div)
    var parent = $(combo).parent();

    // removes all children spans with combos
    $(parent).children("span.location_attributes").remove();
        
    var c = $(parent);
    while (!$(c).is("tr")) {
        c = $(c).parent();
        //console.debug($(c));
    }       
    $(c).find(".lookupCell").remove();

    // for each selected option on the combo (only one)
    $(parent).children("select#container option:selected").each(function() {
        // if the option value doesn't have a value (empty), returns
        if (!$(combo).val()) {
            return;
        }
        
        // assembles the JSON for the AJAX request 
        var data = {
            'action': 'select_container',
            'id_container': $(combo).val()
        };
   
        // requests the location callback script with 
        // the parameters determined above and,
        // when the response comes, treats it as html
        // and calls build_combo function
        $.get("location.callback.py", data,
              function(data, textStatus) {
                 build_combo(main_boxy, parent, data);
              }, 'html');
    })
}

function setup_combo(main_boxy, combo, id) {
    // when the container select (first-level) changes
    $(combo).change(function() {
        container_combo_change(main_boxy, $(this));
    })
    .change(); // ... and forces the change event to occur
}

function build_combo(main_boxy, the_parent, data) {
    // html for the combo, comes from AJAX call
    var ctrl = $(data);
    
    // if a combo changed, cannot save until picking
    // the whole tree and the final location
    $('#save').attr('disabled', 'true');
        
    if ($(ctrl).find("input[@type=image]").length > 0) {
        var c = $(the_parent);
        
        while (!$(c).is("tr")) {
            c = $(c).parent();
        }

        var newCtrl = $("<td class='lookupCell' align='right'>" + $(ctrl).html() + "</td>");
        $(c).append(newCtrl);
    }
    else {
        // appends the new combo to its parent control (span)
        $(the_parent).append(ctrl);
    }    
    
    // if the added control was a the location, not
    // the combo, it's because we reached a final level
    // and we need to add the click event handler 
    if ($(ctrl).find('select.location').length < 1) {
        //console.debug($(c));
        //console.debug($(c).find('input.location_lookup'));
        // when user clicks the lookup button
        $(c).find('input.location_lookup').click(function() {
            // creates the modal dialog box
            var boxy = new Boxy(
                 "", { 
                    title: "Mapa de Estoque", 
                    modal: true, 
                    closeText: "Fechar",
                    show: false
            });

            // figure out what's the container and container_hierarchy
            // that was selected by the user
            var query_json = determine_location($(this));
            
            // gets current row and col value, if set
            var row = $(this).siblings('#row').val();
            var col = $(this).siblings('#col').val();

            var locations = main_boxy.getLocations();
            console.debug(locations);
            var locationsStr = '';
            if (locations) {
                locationsStr = JSON.stringify(locations);
            }
          // console.debug(locationsStr);

            // assembles the JSON for the AJAX request 
            var data = {
                'action': 'select_location',
                'id_container': query_json.id_container,
                'id_container_hierarchy' : query_json.id_container_hierarchy,
                'selectedLocations': locationsStr,
                'row': row, 'col': col
            };
            
            $(this).siblings('#id_container').val(query_json.id_container);
            $(this).siblings('#id_container_hierarchy').val(query_json.id_container_hierarchy);
            
            // calls the AJAX callback page passing the 
            // parameters for assembling the dialog box
            // for location selection
            $.get("location.callback.py", data,
                  function(data, textStatus) {
                          // gets the returned HTML and
                        // inserts it on our dialog box
                          var controls = $(data);
                        boxy.setContent($(controls));
                        boxy.mainBoxy = main_boxy;
                        console.debug(boxy);
                        console.debug(boxy.mainBoxy);
                        
                        // sets up each cell of the table
                        var tds = $(controls).find('td');
                        for (var i = 0; i < tds.length; i++) {
                            // when we go over the cell, we
                            // need to make the cursor a pointer
                            // so user know it's clickable
                            $(tds[i]).not($(".unav_location")).hover(function() {
                                $(this).css('cursor', 'pointer');
                            }, 
                            function() {
                                $(this).css('cursor', 'default');
                            });

                            // when user clicks one cell to select, we
                            // should enable the "Select" button,
                            // move the selection icon into it, and
                            // also display the helper message with
                            // selected location
                            $(tds[i]).not($(".unav_location")).click(function() {
                                console.log("Click: %o", $(this));
                              // console.log($('#message'));
                                $(controls).find('input[@type=button]').removeAttr('disabled');
                                var selectedLocation = $(controls).find(".selectedCell");
                                if (selectedLocation) {
                                    $(selectedLocation).html('<div style="width: 16px; height: 16px"></div>');
                                    $(selectedLocation).toggleClass("selectedCell");
                                }
                                $(this).html('<img src="../img/inserting.gif" alt="X" title="Selecionado">');
                                $(this).toggleClass("selectedCell");
                                console.log("Message: %o - %s", $('#message'), $('#message').html());
                              // console.log("Selected: %o - %s", $(this), $(this).attr('name'));
                                $('#message').html('Selecionado: ' + $(this).attr('name'));
                              // console.log("Message: %o - %s", $('#message'), $('#message').html());
                            });
                        }
                        
                        // centers the dialog on the screen with new contents
                        boxy.center();
                        // ... and displays it
                        boxy.show();

                        // if no current selected cell, we'll disable the "Select"
                        // button, so it will only get enabled when user click 
                        // one location
                        if ($(controls).find(".selectedCell").length < 1) {
                            $(controls).find('input[@type=button]').attr('disabled', 'disabled');
                        }
                        
                        // sets up what happens when user clicks the "Select" button
                        $(controls).find('input[@type=button]').click(function() {
                            boxy.hide(function() {
                                //console.debug($(c));
                                // finds the current selected table cell "name"
                                // that contains the friendly location name (eg, "B2")
                                $(c).find("input.location").val($('td.selectedCell').attr('name'));
                            
                                // finds the current table cell "id" that contains
                                // the location in row_col format
                                var row_col;
                                $(controls).find('td.selectedCell').each(function() {
                                    row_col = $(this).attr('id');
                                });
                                
                                if (row_col) {
                                    $(c).find("#row").val(row_col.split("_")[0]);
                                    $(c).find("#col").val(row_col.split("_")[1]);
                                }
                                
                                // clears the dialog contents for next time
                                $(controls).empty();

                              // console.debug(boxy.mainBoxy);

                                // enables the save button
                                $("#save").removeAttr('disabled');
                                      
                                // automagically adds a new row
                                if ($('select.container').filter(':last').val()) {
                                    boxy.mainBoxy.addRow();
                                }
                            });
                        });
                        
                        // clicks the selected cell for initial setup
                        $(controls).find('td.selectedCell').click();
                  }, 'html');
          
        });
        $(c).find('input.location_lookup').click();
        return;
    }

    $(ctrl).find('select#location').change(function() {
        location_combo_change(main_boxy, $(this));
    })
    .change();
}

function location_combo_change(main_boxy, combo) {
    var c = $(combo).parent();
    
    while (!$(c).is("tr")) {
        c = $(c).parent();
        //console.debug($(c));
    }       
    $(c).find(".lookupCell").remove();

    if (!$(combo).val()) {
        return;
    }
    
    $(combo).parent().children("span.location_attributes").remove();
    var parent = $(combo).parent();

    var data = {
        'action': 'select_hierarchy',
        'id_parent': $(combo).val()
    };

    $.get("location.callback.py", data,
          function(data, textStatus) {
             build_combo(main_boxy, parent, data);
          }, 'html');
}

function determine_location(control) {
    var ctrl = control;
    var hier = '';
    var containerCell = $(control).parent().parent().children('td.selection');
    var containerCombo = $(containerCell).children('select');
    
    var allLocationCombos = $(containerCell).find('select.location')
    var lastLocationCombo = $(allLocationCombos)[$(allLocationCombos).length-1]

  // console.debug(containerCombo);
    console.debug(lastLocationCombo);
    
    var id_container_hierarchy = $(lastLocationCombo).val();
    var id_container = $(containerCombo).val();
    
    return { 'id_container': id_container, 'id_container_hierarchy': id_container_hierarchy };
}

function show_delete(ctrl) {
    $(ctrl).fadeIn('normal', function() {
        $(this).click(function() {
            if (confirm("Deseja realmente excluir esta localizacao?")) {
                remove_row($(this).parents('div.location'));
            }
        });
    });
}

function remove_row(div) {
    $(div).slideUp('normal', function() {
        $(this).remove();
        disable_save();
    });
}

function disable_save() {
    if ($('tr.locationRow').length == 1) {
        $('#save').attr('disabled', 'true');
    }
    else {
        $('#save').removeAttr('disabled');
    }
}

function get_key(ctrl) {
    return $(ctrl).find("#id_container_hierarchy").val() + "," + $(ctrl).find("#row").val() + "," + $(ctrl).find("#col").val()    
}

function get_json(ctrl) {
    return {
        id_strain: $("#id_strain").val(),
        id_container: $(ctrl).find('#id_container').val(),
        id_container_hierarchy: $(ctrl).find("#id_container_hierarchy").val(),
        row: $(ctrl).find("#row").val(),
        col: $(ctrl).find("#col").val()
    };  
}
