import sys
import msvcrt
import sqlite3
from datetime import datetime
from database_setup import setup_database

def getch():
    return msvcrt.getch().decode()

def get_input(prompt):
    print(prompt, end='', flush=True)
    return input()

def register_barcode(conn, barcode):
    name = get_input("Enter name: ")
    details = get_input("Enter details: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = conn.cursor()
    c.execute("INSERT INTO scans VALUES (?, ?, ?, ?)", (barcode, name, details, timestamp))
    conn.commit()

setup_database()
conn = sqlite3.connect('barcodes.db')
print("Barcode scanner ready. Scan a barcode or press 'q' to quit:")

barcode = ""
while True:
    char = getch()
    if char == 'q':
        print("\nExiting...")
        break
    elif char == '\r' or char == '\n':
        if barcode:
            print(f"\nScanned barcode: {barcode}")
            register_barcode(conn, barcode)
            print("Barcode registered successfully.")
            barcode = ""
    else:
        barcode += char
        sys.stdout.write(char)
        sys.stdout.flush()

conn.close()
