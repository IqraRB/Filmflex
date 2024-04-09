from flask import Flask, render_template, url_for, request, redirect, abort
import sqlite3 as sql
# Import all CRUD modules

app = Flask(__name__)

def db_filmflex2_access():
    try:
        with sql.connect("filmflix 2.db") as dbCon:
            #dbCursor = dbCon.cursor()
            dbCon.row_factory = sql.Row
            return dbCon
    
    except sql.OperationalError as e: 
        print(f"Connection failed: {e}")

def get_film(film_id):
    conn = db_filmflex2_access()
    film = conn.execute('SELECT * FROM tblFilms WHERE filmID = ?',
    (film_id,)).fetchone()
    conn.close()
    if film is None:
        abort(404)
    return film

@app.route('/')
def index():
    conn = db_filmflex2_access()
    films = conn.execute('SELECT * FROM tblFilms').fetchall()
    conn.close()
    return render_template('index.html', title='home', films = films)

@app.route('/insert_film', methods = ('GET','POST'))
def insert():
    if request.method == 'POST':
        film = {
            "filmID":request.form.get('filmID'),
            "title":request.form.get('title'),
            "yearReleased":request.form.get('yearReleased'),
            "rating":request.form.get('rating'),
            "duration":request.form.get('duration'),
            "genre":request.form.get('genre')
        }
        conn = db_filmflex2_access()
        conn.execute("INSERT INTO tblFilms (filmID, title, yearReleased, rating, duration, genre) VALUES(:filmID, :title, :yearReleased, :rating, :duration, :genre)", film)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('insert.html')

@app.route('/update/int:<film_id>', methods = ('GET', 'POST'))
def update(film_id):
    film = get_film(film_id)
    if request.method == 'POST':
        film = {
            "filmID": film_id,
            "title":request.form['title'],
            "yearReleased":request.form['yearReleased'],
            "rating":request.form['rating'],
            "duration":request.form['duration'],
            "genre":request.form['genre']
        }
        conn = db_filmflex2_access()
        conn.execute('UPDATE tblFilms SET title = ? , yearReleased = ?, rating = ?, duration = ?, genre = ? WHERE filmID = ?',
        (film['title'], film['yearReleased'], film['rating'], film['duration'], film['genre'], film['filmID']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('update.html', film = film)


@app.route('/<int:film_id>/delete', methods=('POST',))
def delete(film_id):    
    film = get_film(film_id)    
    conn = db_filmflex2_access() 
    conn.execute('DELETE FROM tblFilms WHERE filmID = ?', (film_id,))    
    conn.commit()    
    conn.close()   
    return redirect(url_for('index'))







"""
# Create a function to read from a text file

def read_file(file_path):
    try:
        with open(file_path) as open_file:
            rf = open_file.read()

            return rf
    except FileNotFoundError as nf:
        print(f"file not found : {nf}")
    except FileExistsError as ne:
        print(f"file does not exist : {ne}")

def film_menu():
    try:
        option= 0
        optionList = ["1","2","3","4","5","6"]

        menu_choice = read_file("/ff2Menu.txt")

        while option not in optionList:
            print(menu_choice)

            option = input("Enter an option from the menu above")

            if option not in optionList:
                print(f"{option} is not a valid choice") 
        return option
    except FileNotFoundError as e:
        print(f"Add error: {e}")

#create a boolean variable 
mainPrograme = True 

while mainPrograme: #same as while True
    #call/invoke the songs_menu and assign it to a variable 
    main_menu = film_menu()

    if main_menu == "1":
        #call the readrecords.read_records()
        readrecords.filmflex2_read_records()
    elif main_menu == "2":
        addrecord.filmflex2_insert_record()
    elif main_menu == "3":
        updaterecord.filmflex2_update_record()
    elif main_menu == "4":
        deleterecord.filmflex2_delete_record()
    elif main_menu == "5":
        report.filmflex2_search_report()
    
    else: #to exit the menu re-assign the value of mainProgramme to False 
        mainPrograme = False
input("Press Enter to exit...")

"""

if __name__ == "__main__":
    app.run(debug=True)