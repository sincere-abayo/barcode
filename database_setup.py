import sqlite3

def setup_database():
    conn = sqlite3.connect('barcodes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (barcode TEXT,name TEXT, details TEXT ,timestamp TEXT)''')
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

if __name__ == "__main__":
    setup_database()
