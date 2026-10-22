#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This file contains a mapping from the values in the fields retrieved by the reports
to translatable strings.
'''


label_values_dict = {
    
    "status":{"":"", "active":"label_active", "inactive":"label_inactive","pending":"label_pending"},
    "gps_latitude_mode":{"":"", "decimal":"label_decimal","dms":"label_dms"},
    "gps_longitude_mode":{"":"", "decimal":"label_decimal","dms":"label_dms"},
    "hiv":{"":"", "yes":"label_yes","no":"label_no"},
    "ogm":{"":"", "0":"label_ogm_0","1":"label_ogm_1","2":"label_ogm_2"},
    "is_ogm":{"":"", 0:"label_is_ogm_0",1:"label_is_ogm_1"},
    "go_catalog":{"":"", 1:"label_go_catalog_1", 0:"label_go_catalog_0"},
    "coll_month":{"":"", 1:"label_january",2:"label_february",3:"label_march",4:"label_april",5:"label_may",6:"label_june",7:"label_july",8:"label_august",9:"label_september",10:"label_october",11:"label_november",12:"label_december"},
    "iso_month":{"":"", 1:"label_january",2:"label_february",3:"label_march",4:"label_april",5:"label_may",6:"label_june",7:"label_july",8:"label_august",9:"label_september",10:"label_october",11:"label_november",12:"label_december"},
    "ident_month":{"":"", 1:"label_january",2:"label_february",3:"label_march",4:"label_april",5:"label_may",6:"label_june",7:"label_july",8:"label_august",9:"label_september",10:"label_october",11:"label_november",12:"label_december"},
    "dep_month":{"":"", 1:"label_january",2:"label_february",3:"label_march",4:"label_april",5:"label_may",6:"label_june",7:"label_july",8:"label_august",9:"label_september",10:"label_october",11:"label_november",12:"label_december"},
    "aut_month":{"":"", 1:"label_january",2:"label_february",3:"label_march",4:"label_april",5:"label_may",6:"label_june",7:"label_july",8:"label_august",9:"label_september",10:"label_october",11:"label_november",12:"label_december"},
    "hazard_group":{"":"", "1":"label_1","2":"label_2","3":"label_3","4":"label_4"},
    "alt_states_type":{"":"", "ANA":"label_ana","TELEO":"label_teleo"}
}

values_dict = {
                       "":"", 
    "label_active"       : _("Active"),
    "label_inactive"     : _("Inactive"),
    "label_pending"      : _("Pending"),
    "label_decimal"      : _("Decimal"),
    "label_dms"          : _("DMS"),
    "label_yes"          : _("Yes"),
    "label_no"           : _("No"),
    "label_ogm_0"        : _("Unknown"),
    "label_ogm_1"        : _("Group I"),
    "label_ogm_2"        : _("Group II"),
    "label_is_ogm_0"        : _("False"),
    "label_is_ogm_1"        : _("True"),
    "label_go_catalog_1" : _("True"),
    "label_go_catalog_0" : _("False"),
    "label_january"      : _("January"),
    "label_february"      : _("February"),
    "label_march"      : _("March"),
    "label_april"      : _("April"),
    "label_may"      : _("May"),
    "label_june"      : _("June"),
    "label_july"      : _("July"),
    "label_august"      : _("August"),
    "label_september"      : _("September"),
    "label_october"      : _("October"),
    "label_november"      : _("November"),
    "label_december"      : _("December"),
    "label_1"      : _("1"),
    "label_2"      : _("2"),
    "label_3"      : _("3"),
    "label_4"      : _("4"),
    "label_ana"      : _("Anamorfic"),
    "label_teleo"      : _("Teleomorfic")
}