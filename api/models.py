from sqlalchemy import DateTime, Table, Column, Integer, String, ForeignKey, MetaData, Sequence


metadata = MetaData()

users = Table('py_users', metadata,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('email', String(100), nullable=False),
    Column('password', String(100), nullable=False),
    Column('fullname', String(50), nullable=False),
    Column('created_on', DateTime),
    Column('status', String(1))
)

codes = Table(
    "py_codes", metadata,
    Column("id", Integer, Sequence("code_id_seq"), primary_key = True),
    Column("email", String(100)),
    Column("reset_code", String(50)),
    Column("status", String(1)),
    Column("expired_in", DateTime)
    
)
    
    
    

