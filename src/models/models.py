import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from src.database import Base


class Bill(Base):
    __abstract__ = True

    id = Column("id", UUIDType(binary=False), primary_key=True, default=uuid.uuid4)


class Menu(Bill):
    __tablename__ = "menus"

    title = Column("title", String(80), nullable=False)
    description = Column(
        "description", String(200), nullable=False, default="test description"
    )

    submenus = relationship("SubMenu", back_populates="menus", cascade="all")

    def __repr__(self) -> str:
        return f"{self.title}"


class SubMenu(Bill):
    __tablename__ = "submenus"

    title = Column("title", String(80), nullable=False)
    description = Column(
        "description", String(200), nullable=False, default="test description"
    )
    menu_id = Column("Menu", ForeignKey("menus.id", ondelete="CASCADE"))

    menus = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenus", cascade="all", lazy="joined"
    )

    def __repr__(self) -> str:
        return f"{self.title}"


class Dish(Bill):
    __tablename__ = "dishes"

    title = Column("title", String(80), nullable=False)
    description = Column(
        "description", String(200), nullable=False, default="test description"
    )
    price = Column("price", Float(precision=2), nullable=False)
    submenu_id = Column("SubMenu", ForeignKey("submenus.id", ondelete="CASCADE"))

    submenus = relationship("SubMenu", back_populates="dishes")

    def __repr__(self) -> str:
        return f"{self.title}"
