from extensions import db 

from sqlalchemy.exc import SQLAlchemyError

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    author = db.relationship('User', back_populates='posts')
    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def data(self):
        return{
            'id':self.id,
            'title':self.title,
            'created_at':self.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
            'updated_at':self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'author':self.author_data,
            'category':self.category_data, 
            'comments': [comment.data for comment in self.comments.all()]
        }

    @property
    def author_data(self):
        return {
            'id':self.author.id, 
            'username':self.author.username, 
            'email':self.author.email
        }if self.author else None
    
    @property
    def categrory_data(self):
        return {
            'id': self.category.id,
            'name':self.category.name 
        }if self.category else None
    @property
    def summary(self):
        return f"{self.content[:100]}..." if len(self.content) > 100 else self.content
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e: 
            db.session.rollback()
            print (f"Error saving to the database: {e}")
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting from the database: {e}")
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
