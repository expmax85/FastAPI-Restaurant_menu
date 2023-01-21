from sqlalchemy import create_engine, Column, \
    Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src import config as settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(bind=engine)


class Menu(Base):
    __tablename__ = 'menus'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')

    submenus = relationship('SubMenu', back_populates='menus', cascade='all')

    def __repr__(self) -> str:
        return f"{self.title}"


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')
    menu_id = Column('Menu', ForeignKey('menus.id', ondelete='CASCADE'))

    menus = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenus', cascade='all', lazy='joined')

    def __repr__(self) -> str:
        return f"{self.title}"


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')
    price = Column('price', Float(precision=2), nullable=False)
    submenu_id = Column('SubMenu', ForeignKey('submenus.id', ondelete='CASCADE'))

    submenus = relationship('SubMenu', back_populates='dishes')

    def __repr__(self) -> str:
        return f"{self.title}"
