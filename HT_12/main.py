import requests
from csv import writer, QUOTE_NONNUMERIC
from bs4 import BeautifulSoup
from datetime import datetime
from sqlite3 import Error
from sqlite3 import connect

URL = 'https://quotes.toscrape.com'
DB_FILE = "quotes_and_authors.db"

CREATE_AUTHORS_TABLE_SQL = """ CREATE TABLE IF NOT EXISTS authors (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    born_date text NOT NULL,
                                    born_location text NOT NULL,
                                    bio text NOT NULL
                                ); """

CREATE_QUOTES_TABLE_SQL = """CREATE TABLE IF NOT EXISTS quotes (
                                id integer PRIMARY KEY,
                                text text NOT NULL,
                                author_id integer NOT NULL,
                                page integer not null,
                                FOREIGN KEY (author_id) REFERENCES authors(id)
                            );"""

INSERT_AUTHOR_SQL = """INSERT INTO authors(name, born_date, born_location, bio) 
                        VALUES (?,?,?,?)
                    ;"""

INSERT_QUOTE_SQL = """INSERT INTO quotes(text, author_id, page) 
                        VALUES (?,?,?)
                    ;"""

DROP_AUTHORS_TABLE_SQL = """ DROP TABLE authors """
DROP_QUOTES_TABLE_SQL = """ DROP TABLE quotes """


def fetch_data():
    quotes, authors = {}, {}
    next_page_url = URL
    page_number = 1
    while next_page_url:
        print("Processing page number:", page_number)
        quotes_page_response = requests.get(next_page_url)
        soup = BeautifulSoup(quotes_page_response.text, 'lxml')
        update_quotes(soup, page_number, quotes, authors)

        next_page_url = get_next_page_link(soup)
        page_number += 1
    return quotes, authors


def update_quotes(soup, page_number, quotes, authors):
    raw_quotes = soup.find_all('div', class_='quote')
    for raw_quote in raw_quotes:
        quote_text = clear_string(raw_quote.find('span', class_='text').text)
        quote_author_name = clear_string(raw_quote.find('small', class_='author').text)
        quotes[quote_text] = [None, quote_text, quote_author_name, page_number]
        update_authors(raw_quote, quote_author_name, authors)


def update_authors(raw_quote, quote_author_name, authors):
    if quote_author_name not in authors.keys():
        author_page_link = raw_quote.find('small', class_='author').next_sibling.next_sibling["href"]
        author_page_response = requests.get(URL + author_page_link)
        author_soup = BeautifulSoup(author_page_response.text, 'lxml')
        author_born_date = author_soup.find('span', class_='author-born-date').text
        parsed_author_born_date = datetime.strptime(author_born_date, "%B %d, %Y").date()
        author_born_location = clear_string(author_soup.find('span', class_='author-born-location').text.lstrip("in "))
        author_bio = clear_string(author_soup.find('div', class_='author-description').text)
        authors[quote_author_name] = \
            [None, quote_author_name, parsed_author_born_date, author_born_location, author_bio]


def clear_string(string):
    return string.strip("\"").strip("”").strip("“").strip().replace("\n", "");


def get_next_page_link(soup):
    next_page_link = soup.select_one('li.next a')
    if next_page_link:
        return URL + next_page_link["href"]
    else:
        return


def fetch_and_save_data():
    quotes, authors = fetch_data()
    save_data_to_csv(authors, quotes)
    save_data_to_db(authors, quotes)


def save_data_to_csv(authors, quotes):
    with open("quotes_and_authors.csv", "w") as output_file:
        csv_writer = writer(output_file, delimiter=";", quoting=QUOTE_NONNUMERIC)
        csv_writer.writerow(["Quote", "Author", "Page"])
        for quote in quotes.values():
            csv_writer.writerow([quote[1], quote[2], quote[3]])
        csv_writer.writerow([])
        csv_writer.writerow(["Name", "Born Date", "Born Location", "Bio"])
        for author in authors.values():
            csv_writer.writerow([author[1], author[2], author[3], author[4]])


def save_data_to_db(authors, quotes):
    with connect(DB_FILE) as conn:
        try:
            recreate_tables(conn)
            for author in authors.values():
                author_id = add_author(conn, author[1:])
                author[0] = author_id
            for quote in quotes.values():
                quote_copy = list(quote)
                quote_copy[2] = authors[quote[2]][0]
                add_quote(conn, quote_copy[1:])
            conn.commit()
        except Error as e:
            print("Error occurred in DB during the save:", e)
            conn.rollback()


def recreate_tables(conn):
    drop_quotes_table(conn)
    drop_authors_table(conn)
    create_table(conn, CREATE_AUTHORS_TABLE_SQL)
    create_table(conn, CREATE_QUOTES_TABLE_SQL)


def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)


def add_author(conn, author):
    c = conn.cursor()
    c.execute(INSERT_AUTHOR_SQL, author)
    return c.lastrowid


def add_quote(conn, quote):
    c = conn.cursor()
    c.execute(INSERT_QUOTE_SQL, quote)
    return c.lastrowid


def drop_authors_table(conn):
    c = conn.cursor()
    c.execute(DROP_AUTHORS_TABLE_SQL)


def drop_quotes_table(conn):
    c = conn.cursor()
    c.execute(DROP_QUOTES_TABLE_SQL)


fetch_and_save_data()
