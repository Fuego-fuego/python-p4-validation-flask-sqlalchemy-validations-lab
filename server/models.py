from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self,key,name):
        if not name:
            raise ValueError('Name required')
        author = db.session.query(Author.id).filter_by(name=name).first()
        if author:
            raise ValueError("Name must be unique.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) !=10 or not phone_number.isdigit():
            raise ValueError("Phone number must be of length 10,and must be digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validates_title(self,key,title):
        if not title:
            raise ValueError("Title is required.")
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(string in title for string in clickbait):
            raise ValueError("Clickbait not found")
        return title
    
    @validates('content','summary')
    def validate_length(self,key,string):
        if len(string)< 250:
            raise ValueError("post content must be greater than or equal 250 character long.")
        if (key =='summary'):
            if len(string)>250:
                raise ValueError("Post summary must be less than or equal to 250 characters long.")
            return string
        
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction','Non-Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
