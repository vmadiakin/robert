from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    name = Column(String)
    surname = Column(String)


# Load database configuration from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Create a database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')

# Create the 'users' table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# Function to interact with the database
async def interact_with_db(message):
    # Check if the user already exists in the database
    user = session.query(User).filter_by(user_id=message.from_user.id).first()

    if user is None:
        # If the user doesn't exist, add them to the database
        new_user = User(user_id=message.from_user.id,
                        username=message.from_user.username,
                        name=message.from_user.first_name,
                        surname=message.from_user.last_name)

        session.add(new_user)
        session.commit()
        print("User added to the database.")
    else:
        print("User already exists in the database.")