from flask import Flask, render_template, request, redirect
import sqlite3
import shortuuid

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT NOT NULL,
        short_code TEXT NOT NULL UNIQUE
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    # Render the main page where users can enter a long URL
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    # Shorten the submitted long URL and return the shortened URL
    long_url = request.form['long_url']

    # Check if the URL already exists in the database
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT short_code FROM urls WHERE long_url = ?', (long_url,))
    result = cursor.fetchone()

    if result:
        # If the long URL already has a short code, reuse it
        short_code = result[0]
    else:
        # Generate a unique short code using shortuuid
        short_code = shortuuid.uuid()[:8]

        # Save the mapping in the database
        cursor.execute('INSERT INTO urls (long_url, short_code) VALUES (?, ?)', (long_url, short_code))
        conn.commit()

    conn.close()

    # Construct the shortened URL
    short_url = f'http://localhost:5000/{short_code}'
    return render_template('shorten.html', short_url=short_url)

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    # Redirect to the original long URL associated with the short code
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_code = ?', (short_code,))
    result = cursor.fetchone()

    if result:
        # If short code found, redirect to the original long URL
        long_url = result[0]
        conn.close()
        return redirect(long_url)
    else:
        # If short code not found, return a 404 error
        conn.close()
        return 'Short URL not found.', 404

if __name__ == '__main__':
    # Run the Flask app in debug mode on http://localhost:5000
    app.run(debug=True)
