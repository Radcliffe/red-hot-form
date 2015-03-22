import csv
from fdfgen import forge_fdf
import os
import sys

pdf_file = "form.pdf"
tmp_file = "tmp.fdf"
output_file = "filled_form.pdf"

fields = {}
fields = {
    "1_msp"             : "Yes",
    "1_name_first"      : "Dave",
    "1_name_mi"         : "G",
    "1_name_last"       : "Radcliffe",
    "1_dob"             : "11/21/1966",
    "1_sex"             : "Male",
    "1_ssn"             : "999-99-9999",
    "1_marital_status"  : "Single",
    "1_phone"           : "651-484-5676",
    "1_phone_other"     : "651-245-8720",
    "1_address"         : "806 Carla Ln",
    "1_city"            : "Little Canada",
    "1_state"           : "MN",
    "1_zip"             : "55109",
    "1_county"          : "Ramsey",
    "1_mailing_address" : "",
    "1_mailing_city"    : "",
    "1_mailing_state"   : "",
    "1_mailing_zip"     : "",
    "1_mailing_county"  : "",
    "1_homeless"        : "No",
    "1_applying"        : "Yes",
    "1_voterreg"        : "No",
    "1_language"        : "English",
    "1_interpreter"     : "No",
    "1_race_asian"      : "No",
    "1_race_black"      : "No",
    "1_race_aina"       : "No",
    "1_race_pinh"       : "No",
    "1_race_white"      : "Yes",
    "1_hispanic"        : "No"
}

fdf = forge_fdf("", fields.items(), [], [], [])
fdf_file = open(tmp_file, "w")
fdf_file.write(fdf)
fdf_file.close()

cmd = 'pdftk "{0}" fill_form "{1}" output "{2}" dont_ask'.format(pdf_file, tmp_file, output_file)
os.system(cmd)
os.remove(tmp_file)
