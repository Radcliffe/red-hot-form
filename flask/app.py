# all the imports
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import csv
from fdfgen import forge_fdf
import os
import sys

# configuration
DATABASE = '/tmp/redhotform.db'
DEBUG = True
SECRET_KEY = 'asidonhopo'
USERNAME = 'admin'
PASSWORD = 'default'
pdf_file = "static/form.pdf"
tmp_file = "static/tmp%s.fdf"
output_file = "static/filled%s.pdf"

field_names = ['msp', 'name_first', 'name_mi', 'name_last', 'dob',
               'sex', 'ssn', 'marital_status', 'phone', 'phone_other',
               'address', 'city', 'state', 'zip', 'county', 'mailing_address',
               'mailing_city', 'mailing_zip', 'mailing_county', 'homeless',
               'applying', 'voterreg', 'language', 'interpreter', 'race_asian',
               'race_black', 'race_aina', 'race_pinh', 'race_white',
               'hispanic', 'reservation']
N = len(field_names)
               
insert_cmd = "insert into entries (" + ", ".join(field_names) + ") values (?" + ',?'*(N-1) + ")"

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config['USERNAME'] = 'dave'
app.config['PASSWORD'] = 'redwing'
        
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, name_first, name_mi, name_last from entries order by id desc')
    entries = [dict(Id=row[0], name_first=row[1], name_mi=row[2], name_last=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    values = []
    for field in field_names:
        values.append(request.form.get(field, None))
    cur.execute(insert_cmd, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    flash('New entry was successfully posted')
    return redirect('/show/%d' % id)

@app.route('/show/<Id>')
def show_entry(Id):
    cur = g.db.execute('select * from entries where id = ?', [Id])
    entries = cur.fetchall()
    for entry in entries:
        return render_template('show_entry.html', entry=entry)
    return "Not found" 

@app.route('/edit/<Id>')
def edit(Id):
    cur = g.db.execute('select * from entries where id = ?', [Id])
    rows = cur.fetchall()
    for row in rows:
        return "Found"
    return "Not found"

@app.route('/fill/<Id>')
def fill_form(Id):
    cur = g.db.execute('select * from entries where id = ?', [Id])
    rows = cur.fetchall()
    for row in rows:
        fields = {}
        for i, field in enumerate(field_names):
            fields["1_" + field] = row[i+1]
        fdf = forge_fdf("", fields.items(), [], [], [])
        fdf_file = open(tmp_file % Id, "w")
        fdf_file.write(fdf)
        fdf_file.close()
        cmd = 'pdftk {0} fill_form {1} output {2} dont_ask'.format(pdf_file, tmp_file % Id, output_file % Id)
        os.system(cmd)
        os.remove(tmp_file % Id)
        return redirect(url_for('static', filename="filled%s.pdf" % Id))    
    return "Not found"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()
