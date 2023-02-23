from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()

# таблиця для зв'язку many-to-many між таблицями notes та tags
note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)

# Таблиця notes, де зберігатимуться назви завдань
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    # backref -> дозволяє автоматично генерувати нове відношення, яке буде автоматично додано до порівняння ORM для пов'язаного класу.
    records = relationship("Record", cascade="all, delete", backref="note")
    # Параметр passive_deletes вказує на поведінку завантаження під час операцій видалення. Значення True вказує, 
    # що вивантажені дочірні елементи не повинні завантажуватись під час операції видалення батьківського елемента.
    tags = relationship("Tag", secondary=note_m2m_tag, backref="notes", passive_deletes=True)
    '''Іншими словами, в таблиці Note ми створили відносини relationship для того, 
    щоб отримувати записи records з таблиці Record. За допомогою 
    таблиці secondary=note_m2m_tag здійснили зв'язок багато до багатьох, 
    щоб отримувати доступ до тегів завдання.'''

# Таблиця records, де зберігатимуться записи справ для конкретного завдання з таблиці notes - зв'язок one-to-many, поле note_id
class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    # ondelete="CASCADE" -> при видаленні запису з таблиці notes ми видалимо автоматично всі пов'язані записи у таблиці records
    note_id = Column(Integer, ForeignKey(Note.id, ondelete="CASCADE"))

# Таблиця tags, де зберігається набір тегів для списку справ.
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)
