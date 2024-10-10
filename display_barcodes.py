import sqlite3

def display_barcodes():
    conn = sqlite3.connect('barcodes.db')
    c = conn.cursor()
    
    c.execute("SELECT barcode, name, details, timestamp FROM scans ORDER BY timestamp DESC")
    rows = c.fetchall()
    
    if not rows:
        print("No barcodes found in the database.")
    else:
        print("Barcode\t\tName\t\tDetails\t\t\tTimestamp")
        print("-" * 80)
        for row in rows:
            barcode, name, details, timestamp = row
            print(f"{barcode}\t{name}\t\t{details}\t{timestamp}")
    
    conn.close()

if __name__ == "__main__":
    display_barcodes()
