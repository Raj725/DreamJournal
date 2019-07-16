from datetime import datetime

from dream_journal import db


class Dreams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    dream_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Dreams('{self.title}', '{self.dream_date}')"
