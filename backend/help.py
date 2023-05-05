from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from config import config

config.setup("development")
# create the engine and session

Session = sessionmaker(bind=config.settings.database_url)
session = config.db.SessionLocal()


# create the base class for declarative models
Base = declarative_base()


# define your models
class Table1(Base):
    __tablename__ = "table1"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    table2 = relationship("Table2", uselist=False, back_populates="table1")


class Table2(Base):
    __tablename__ = "table2"
    id = Column(Integer, primary_key=True)
    table1_id = Column(Integer, ForeignKey("table1.id"))
    name = Column(String)
    table1 = relationship("Table1", back_populates="table2")


class Table3(Base):
    __tablename__ = "table3"
    id = Column(Integer, primary_key=True)
    table1_id = Column(Integer, ForeignKey("table1.id"))
    name = Column(String)


# create the tables
Base.metadata.create_all(config.db.engine)

# add some initial data
t1_1 = Table1(name="A")
t1_2 = Table1(name="B")
t1_3 = Table1(name="C")
t2_1 = Table2(name="X", table1_id=t1_1.id)
t2_2 = Table2(name="Y", table1_id=t1_2.id)
t3_1 = Table3(name="M", table1_id=t1_1.id)

session.add_all([t1_1, t1_2, t1_3, t2_1, t2_2, t3_1])
session.commit()

# query the database
results = (
    session.query(Table1)
    .outerjoin(Table2)
    .outerjoin(Table3)
    .filter(Table1.name.in_(["A", "B"]))
    .all()
)

print(results)

# print the results
for result in results:
    print(result.table2)
    # print(
    #     f"Table1({result.id}, {result.name}) -> "
    #     f"Table2({result.table2.id if result.table2 else None}, {result.table2.name if result.table2 else None}) -> "
    #     f"Table3({result.table3.id if result.table3 else None}, {result.table3.name if result.table3 else None})"
    # )
