import sqlite3

def main():
    create_table()
    insert_image("smile", "input.png")
    retrieve_image("smile", "ouput.png")
    

#create the table 
def create_table():
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        image BLOB NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

#insert image
def insert_image(name, filename):
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    image_data = convert_to_binary_data(filename)
    cursor.execute('''
    INSERT INTO images (name, image) VALUES (?, ?)
    ''', (name, image_data))
    conn.commit()
    conn.close()

#convert the image into binary data ----- INSERT IMAGE FUNCTION will call this function
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data

# retrieve data from database
def retrieve_image(image_name, output_filename):
    conn = sqlite3.connect('images.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, image FROM images WHERE name = ?
    ''', (image_name,))
    record = cursor.fetchone()
    conn.close()
    if record:
        id, image_data = record
        with open(output_filename, 'wb') as file:
            file.write(image_data)
        print(f"Image {image_name} and ID {id} SUCCESSFULLY saved as {output_filename}")
    else:
        print("No image found with the given name.")

if __name__ == "__main__":
    main()