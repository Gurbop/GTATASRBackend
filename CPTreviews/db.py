import sqlite3

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('reviews.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        review TEXT NOT NULL,
                        rate INTEGER NOT NULL
                    )''')
    conn.commit()
    conn.close()

def populate_data():
    conn = db_connection()
    cursor = conn.cursor()
    # Sample data with four reviews per name
    sample_data = [
        ('San Diego Refugee Tutoring', 'Excellent program!', 5),
        ('San Diego Refugee Tutoring', 'Helped me a lot', 4),
        ('San Diego Refugee Tutoring', 'Great experience', 5),
        ('San Diego Refugee Tutoring', 'Amazing work', 5),
        ('Youth Court', 'Good initiative', 4),
        ('Youth Court', 'Very beneficial', 5),
        ('Youth Court', 'Needs improvement', 3),
        ('Youth Court', 'Fantastic idea', 5),
        ('Balboa Natural History Museum', 'Educational and fun', 5),
        ('Balboa Natural History Museum', 'Loved the exhibits', 5),
        ('Balboa Natural History Museum', 'Great for families', 4),
        ('Balboa Natural History Museum', 'Informative displays', 4),
        ('Step Up', 'Helpful resources', 4),
        ('Step Up', 'Impressive organization', 5),
        ('Step Up', 'Changed my life', 5),
        ('Step Up', 'Could do more', 3),
        ('Children Rising', 'Making a difference', 5),
        ('Children Rising', 'Top-notch program', 5),
        ('Children Rising', 'Inspiring work', 5),
        ('Children Rising', 'Supportive staff', 4),
        ('Seattle Animal Shelter', 'Caring staff', 5),
        ('Seattle Animal Shelter', 'Adopted my best friend', 5),
        ('Seattle Animal Shelter', 'Great facilities', 4),
        ('Seattle Animal Shelter', 'Could use more volunteers', 3),
        ("God's Love We Deliver", 'Life-saving service', 5),
        ("God's Love We Deliver", 'Heartwarming work', 5),
        ("God's Love We Deliver", 'Volunteered here', 4),
        ("God's Love We Deliver", 'Needs more funding', 3),
        ('Horse Play Therapy Center', 'Therapeutic experience', 5),
        ('Horse Play Therapy Center', 'Helped my child', 4),
        ('Horse Play Therapy Center', 'Trained staff', 5),
        ('Horse Play Therapy Center', 'Wonderful facility', 5),
        ('Community Servings Food Heals', 'Providing essential services', 5),
        ('Community Servings Food Heals', 'Great food!', 5),
        ('Community Servings Food Heals', 'Volunteered here', 4),
        ('Community Servings Food Heals', 'Improvements needed', 3),
        ('Emmaus', 'Fantastic organization', 5),
        ('Emmaus', 'Grateful for their help', 5),
        ('Emmaus', 'Volunteered here', 4),
        ('Emmaus', 'Supportive community', 4)
    ]
    # Execute insert queries
    for data in sample_data:
        cursor.execute("INSERT INTO reviews (name, review, rate) VALUES (?, ?, ?)", data)
    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    populate_data()    