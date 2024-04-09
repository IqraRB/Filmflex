#Import connect module 
from connect import *

# create a function to add/insert record in table 
def filmflex2_search_report():
    try:
        dbCon, dbCursor = db_filmflex2_access()

        #ask for a search field
        search_field = input("Search by filmID or title or yearReleased or rating or duration or genre: ")

        # check if search_field value entered is FilmID, year released or duration 
        if search_field.lower() in ["filmid", "yearreleased", "duration"]:
            #search by "filmID" "YearReleased" "Duration"
            int_input = int(input(f"Enter the vaue for {search_field}: "))
            dbCursor.execute(f"SELECT * FROM tblfilms WHERE {search_field} like ?", (f'%{int_input}%',))
            row = dbCursor.fetchone()

            if row is None:
                print(f"No record with field {search_field} matching {int_input} exists in the film table.")
            else:
                print("*" * 100)

                #format the heading using field names: #filmID, title, yearReleased, rating, duration, genre
                print(f"FilmID{'':<1}|Title{'':<40}|Year Released{'':<1}|Rating{'':<1}|Duration{'':<1}|Genre{'':<5}")
                print("*" * 100)
                print(f"{row[0]:<7}|{row[1]:<45}|{row[2]:<14}|{row[3]:<7}|{row[4]:<9}|{row[5]:<10}")
                print("-" * 100)

        elif search_field.lower() in ["title", "rating" ,"genre"]:
            #Search by FilmID, Title, Rating, Genre
            str_input = input(f"Enter the value for {search_field}: ")

            dbCursor.execute(f'SELECT * FROM tblfilms where {search_field} LIKE ?',(f'%{str_input}%',))
            rows = dbCursor.fetchall()
            if not rows:
                print(f"No record with the field {search_field} matching {str_input} in the film table.")
            else: 
                for films in rows:
                    #format the heading using field names: #filmID, title, yearReleased, rating, duration, genre
                    print(f"FilmID{'':<1}|Title{'':<40}|Year Released{'':<1}|Rating{'':<1}|Duration{'':<1}|Genre{'':<5}")
                    print("*" * 100)

                    print(f"{films[0]:<7}|{films[1]:<45}|{films[2]:<14}|{films[3]:<7}|{films[4]:<9}|{films[5]:<10}")
                    print("-" * 100)
        else:
            print(f"Search field {search_field} value is invalid.")
            # print(type(f'%{str_input}%,'))
     
    except sql.ProgrammingError as e:
        print(f"Search error: {e}")
    except sql.OperationalError as f: 
        print(f"Connection failed: {f}")

if __name__ == "__main__":
    filmflex2_search_report()