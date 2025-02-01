import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name='jobs.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            # Таблица объявлений
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    end_date DATE,
                    telegram_link TEXT,
                    status TEXT DEFAULT 'new',
                    post_style INTEGER DEFAULT 1
                )
            ''')

            # Таблица откликов
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY,
                    job_id INTEGER,
                    applicant_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    apply_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (job_id) REFERENCES jobs (id)
                )
            ''')

    def insert_job(self, job_data):
        query = '''INSERT INTO jobs (title, description, company, location, end_date)
                  VALUES (?, ?, ?, ?, ?)'''
        with self.conn:
            cursor = self.conn.execute(query, (
                job_data['title'],
                job_data['description'],
                job_data['company'],
                job_data['location'],
                job_data['end_date']
            ))
            return cursor.lastrowid

    def update_job_status(self, job_id, telegram_link):
        query = '''UPDATE jobs SET status = ?, telegram_link = ? WHERE id = ?'''
        with self.conn:
            self.conn.execute(query, ('published', telegram_link, job_id))

    def get_expired_jobs(self):
        today = datetime.now().date()
        query = '''SELECT id, telegram_link FROM jobs 
                  WHERE end_date <= ? AND status = 'published' '''
        with self.conn:
            return self.conn.execute(query, (today,)).fetchall()

    def save_application(self, job_id, name, email):
        query = '''INSERT INTO applications (job_id, applicant_name, email)
                  VALUES (?, ?, ?)'''
        with self.conn:
            self.conn.execute(query, (job_id, name, email))