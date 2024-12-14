import pandas as pd
import sqlite3 as sql
import streamlit as st


conn = sql.connect("railway.db")
pen = conn.cursor()

def create_db():
  pen.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
  pen.execute("CREATE TABLE IF NOT EXISTS employees (employee_id TEXT, password TEXT, designation TEXT)")
  pen.execute("CREATE TABLE IF NOT EXISTS trains (train_number TEXT, train_name TEXT, departure_date TEXT, start_destination TEXT, end_destination TEXT)")

create_db()


def search_train(train_number):
  query = pen.execute(__sql: "SELECT * FROM trains WHERE train_number=?", __parameters: (train_number,))
  return query.fetchone()
  
def search_train(start_destination, end_destination):
  query = pen.execute(__sql: "SELECT * FROM trains WHERE start_destination=?, end_destination=?", __parameters: (start_destination, end_destination,))
  return query.fetchall()
  
  
def add_train(train_number, train_name, departure_date, start_destination, end_destination):
  query = pen.execute(__sql: "INSERT INTO trains (train_number, train_name, departure_date, start_destination, end_destination) VALUES(?, ?, ?, ?, ?)", __parameters: (train_number, train_name, departure_date, start_destination, end_destination))
  conn.commit()
  
