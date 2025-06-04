import pandas as pd
import sqlite3 as sql
import streamlit as st


conn = sql.connect("railway.db")
current_page = "Login or Sign up"
pen = conn.cursor()

def create_db():
  pen.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
  pen.execute("CREATE TABLE IF NOT EXISTS employees (employee_id TEXT, password TEXT, designation TEXT)")
  pen.execute("CREATE TABLE IF NOT EXISTS trains (train_number TEXT, train_name TEXT, departure_date TEXT, start_destination TEXT, end_destination TEXT)")

create_db()


def search_train(train_number):
  query = pen.execute("SELECT * FROM trains WHERE train_number=?", (train_number,))
  return query.fetchone()
  
def train_destination(start_destination, end_destination):
  query = pen.execute("SELECT * FROM trains WHERE start_destination=?, end_destination=?", (start_destination, end_destination,))
  return query.fetchall()
  
  
def add_train(train_number, train_name, departure_date, start_destination, end_destination):
  query = pen.execute("INSERT INTO trains (train_number, train_name, departure_date, start_destination, end_destination) VALUES(?, ?, ?, ?, ?)", (train_number, train_name, departure_date, start_destination, end_destination))
  conn.commit()


def create_seat_table(train_number):
  pen.execute(f"CREATE TABLE IF NOT EXISTS seats_{train_number} (seat_number INTEGER PRIMARY KEY, seat_type TEXT, booked INTEGER, passenger_name TEXT, passenger_age INTEGER, passenger_gender TEXT)")

  for i in range(1, 51):
    val = categorize_seat(i)
    pen.execute(f"INSERT INTO seas_{train_number} (seat_number, seat_type, booked, passenger_name, passenger_age, passenger_gender)"
                f"VALUES(?,?,?,?,?,?);", (i, val, 0, ''','''))
    
def allocate_next_available_train(train_number, seat_type):
  query = pen.execute(f"SELECT seat_number FROM seats_{train_number} WHERE booked=0 and seat_type=?"
                      f"ORDER BY seat_number ASC", (seat_type))
  
  result = query.fetchall()
  if result:
    return result[0]
  
def categorize_seat(seat_number):
  if (seat_number % 10) in [0, 4, 5, 9]:
    return "Window"
  elif (seat_number % 10) in [2, 3, 4, 6, 7]:
    return "Asile"
  else:
    return "Middle"
  
def view_seats(train_number):
  query = pen.execute("SELECT *  FROM train WHERE train_number=? ", (train_number))

  train_data = query.fetchone()
  if train_data:
    seat_query = pen.execute(f'''SELECT 'Number '|| seat_number, '\n type: '||seat_type,  '\n  Name: '|| passenger_name, \n Age: '|| passenger_age '\n Gender: '|| paseenger_gender as Details, booked from seats_{train_number}
                                    ORDER BY seat_number ASC''')
  result = seat_query.fetchall()
  if result:
    st.dataframe(data=result)

def book_tickets(train_number, passenger_name, passenger_age, passenger_gender, seat_type):
  query = pen.execute("SELECT * FROM trains WHERE train_number=?", (train_number))
  train_data = query.fetchone()
  if train_data:
    seat_number = allocate_next_available_train(train_number, seat_type)

    if seat_number:
      pen.execute(f"UPDATE seats_{train_number} SET booked=1, seat_type=?, pasenger_name=?, passenger_age=?, passenger_gender=?"
                  f"WHERE seat_number=?", (seat_type, passenger_name, passenger_age, passenger_gender, seat_number))
      
      conn.commit()

      st.success("BOOKED SUCCESSFULLY !!")

def cancel_tickets(train_number, seat_number):
  query = pen.execute("SELECT * FROM trains WHERE train_number=?", (train_number))
  train_data = query.fetchone()
  if train_data:
    pen.execute(f"UPDATE seats_{train_number} SET booked=0, passenger_name='', passenger_age='', passenger_gender='' WHERE seat_number=?", (seat_number))

    conn.commit()

    st.success("cancel successfully")

def delete_train(train_number, departure_date):
  query = pen.execute("SELECT * FROM trains WHERE train_number=?", (train_number))

  train_data = query.fetchone()
  if train_data:
    pen.execute("DELETE FROM trains WHERE train_number=? AND departure_date=?", (train_number, departure_date))

    conn.commit()

    st.success("train delete successfully")




def train_function():
  st.title("Train System")

  functions = st.sidebar.selectbox('select train functions', ['Add train', 'View train', 'Delete train','Book ticket', 'Cancel ticket', 'View seats'])

  if functions == 'Add train':
    st.header('Add new train')
    with st.form(key="new_train-details"):
      train_number=st.text_input("train number")
      train_name = st.text_input("train name")
      departure_date = st.date_input('date')
      start_destination = st.text_input("start destination")
      end_destination = st.text_input("end destination")
      submited = st.form_submit_button('add train')

      if submited and train_name!='' and train_number !='' and departure_date !='' and start_destination !='' and end_destination !='':
        add_train(train_number, train_name, departure_date, start_destination, end_destination)

        st.success("train added successfully")
  if functions == "View train":
    st.title("View all train")
    query = pen.execute("SELECT * FROM trains")

    trains = query.fetchall()

  if functions == "Book ticket":
    st.title("Book train ticket")
    train_number = st.text_input("enter train number")
    seat_type = st.selectbox("seat_type", ["asile", "middle", "window"], index=0)
    passenger_name = st.text_input("passenger name")
    passenger_age = st.number_input('passenger age', min_value=1)
    passenger_gender = st.selectbox("passenger gender", ["male", "female"], index=0)

    if st.button('book ticket'):
      if train_number and passenger_name and passenger_gender and passenger_age:
        book_tickets(train_number, passenger_name, passenger_age, passenger_gender, seat_type)
  if functions == "Cancel ticket":
    st.title("Cancel ticket")
    train_number = st.text_input("train number")
    seat_number = st.number_input("enter seat number", min_value=1)
    if st.button("Cancel ticket"):
      if train_number and seat_number:
        cancel_tickets(train_number, seat_number)

  if functions == "View seats":
    st.title("View seats")
    train_number = st.text_input("enter train number")
    if st.button('View seats') and train_number:
      view_seats(train_number)

  if functions == "Delete train":
    st.title("Delete train")
    train_number = st.text_input("enter train number")
    departure_date = st.date_input('enter date')
    if st.button("Delete train"):
      if train_number:
        pen.execute(f"DROP TABLE IF EXISTS seat_{train_number}")
        delete_train(train_number, departure_date)
 
train_function()