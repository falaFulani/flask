from extensions import db
# from models import User, Category, Comment, Post
from models import User
from models import Category
from models import Comment
from models import Post
from sqlalchemy.exc import SQLAlchemyError
from faker import Faker
def seed_users():
    fake = Faker()  # Create an instance of Faker
    for _ in range(10):  # Create 10 fake users
        new_user = User(
            name=fake.name(),          # Generates a full name
            email=fake.email(),        # Generates a fake email
            password=fake.password(),  # Generates a fake password
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error saving user: {e}")

def seed_comments():
    fake = Faker()
    users = User.query.all()
    posts = Post.query.all()
    for _ in range(20):
        new_comment = Comment(
            content=fake.text(),
            user_id=fake.random_element(users).id,
            post_id=fake.random_element(posts).id
        )
        try:
            db.session.add(new_comment)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error Saving Comment: {e}")

def seed_categories():
    fake = Faker()
    for _ in range(13):
        new_category = Category(name=fake.word())
        try:
            db.session.add(new_category)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error Saving Category: {e}")

def seed_posts():
    fake = Faker()
    users = User.query.all()
    categories = Category.query.all()
    for _ in range(50):
        new_post = Post(
            title=fake.sentence(),
            content=fake.text(),
            user_id=fake.random_element(users).id,
            category_id=fake.random_element(categories).id
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error Saving Post: {e}")
def seed_database():
    from app import create_app
    app = create_app()
    with app.app_context():
        print("Seeding database...")
        seed_users()
        seed_categories()
        seed_posts()
        seed_comments()
        print("Database Seeded Successfully!")

