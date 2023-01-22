import uuid

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from src.database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')

    submenus = relationship('SubMenu', back_populates='menus', cascade='all')

    def __repr__(self) -> str:
        return f"{self.title}"


class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')
    menu_id = Column('Menu', ForeignKey('menus.id', ondelete='CASCADE'))

    menus = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenus', cascade='all', lazy='joined')

    def __repr__(self) -> str:
        return f"{self.title}"


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column('id', UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column('title', String(80), nullable=False)
    description = Column('description', String(200), nullable=False, default='test description')
    price = Column('price', Float(precision=2), nullable=False)
    submenu_id = Column('SubMenu', ForeignKey('submenus.id', ondelete='CASCADE'))

    submenus = relationship('SubMenu', back_populates='dishes')

    def __repr__(self) -> str:
        return f"{self.title}"
