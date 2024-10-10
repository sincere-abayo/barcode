import sys
import msvcrt
import sqlite3

def getch():
    return msvcrt.getch().decode()

def check_barcode(conn, barcode):
    c = conn.cursor()
    c.execute("SELECT * FROM scans WHERE barcode = ?", (barcode,))
    result = c.fetchone()
    if result:
        return f"Barcode: {result[0]}\nName: {result[1]}\nDetails: {result[2]}\nTimestamp: {result[3]}"
    else:
        return "Error: Barcode not found in the database."

conn = sqlite3.connect('barcodes.db')
print("Scan a barcode to check (press 'q' to quit):")

barcode = ""
while True:
    char = getch()
    if char == 'q':
        print("\nExiting...")
        break
    elif char == '\r' or char == '\n':
        if barcode:
            print(f"\nChecking barcode: {barcode}")
            result = check_barcode(conn, barcode)
            print(result)
            barcode = ""
    else:
        barcode += char
        sys.stdout.write(char)
        sys.stdout.flush()

conn.close()
