from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import os

load_dotenv()
Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    character_name = Column(String)
    character_instructions = Column(String)
    users = relationship('User', back_populates='selected_character')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    name = Column(String)
    surname = Column(String)
    selected_character_id = Column(Integer, ForeignKey('characters.id'), nullable=True)
    selected_character = relationship('Character', foreign_keys=[selected_character_id], back_populates='users')


class UserRequest(Base):
    __tablename__ = 'user_requests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='user_requests')
    user_req = Column(String)
    gpt_answer = Column(String)


User.user_requests = relationship('UserRequest', order_by=UserRequest.id, back_populates='user')

# Load database configuration from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Create a database engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')

# Create the 'users' and 'characters' tables in the database
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# Add Mario and Albert Einstein to the 'characters' table
# mario = Character(character_name="Mario",
#                   character_instructions="You are Mario from Super Mario. Do not give dangerous information.")
# einstein = Character(character_name="Albert Einstein",
#                      character_instructions="You are Albert Einstein. Do not give dangerous information.")
#
# session.add_all([mario, einstein])
# session.commit()


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
