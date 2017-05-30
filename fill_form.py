import csv
from fdfgen import forge_fdf
import codecs
import os
import sys

pdf_file = "form.pdf"
tmp_file = "tmp.fdf"
output_file = "filled_form.pdf"

fields = {}
fields = {
    "1_msp"             : "",
    "1_name_first"      : "",
    "1_name_mi"         : "",
    "1_name_last"       : "",
    "1_dob"             : "",
    "1_sex"             : "","
    "1_ssn"             : "",
    "1_marital_status"  : "",
    "1_phone"           : "",
    "1_phone_other"     : "",
    "1_address"         : "",
    "1_city"            : "",
    "1_state"           : "",
    "1_zip"             : "",
    "1_county"          : "",
    "1_mailing_address" : "",
    "1_mailing_city"    : "",
    "1_mailing_state"   : "",
    "1_mailing_zip"     : "",
    "1_mailing_county"  : "",
    "1_homeless"        : "",
    "1_applying"        : "",
    "1_voterreg"        : "",
    "1_language"        : "",
    "1_interpreter"     : "",
    "1_race_asian"      : "",
    "1_race_black"      : "",
    "1_race_aina"       : "",
    "1_race_pinh"       : "",
    "1_race_white"      : "",
    "1_hispanic"        : ""
}

fdf = forge_fdf("", fields.items(), [], [], [])
fdf_file = open(tmp_file, "w")
fdf_file.write(fdf)
fdf_file.close()

cmd = 'pdftk {0} fill_form {1} output {2} dont_ask'.format(pdf_file, tmp_file, output_file)
os.system(cmd)
os.remove(tmp_file)
