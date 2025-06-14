from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Pokemon(Base):
    __tablename__ = "pokemon"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), unique=True, index=True)  # Name with max 15 characters
    height = Column(Integer)
    weight = Column(Integer)
    xp = Column(Integer)
    image_url = Column(String(150))  # URL with max 150 characters
    pokemon_url = Column(String(150))  # URL with max 150 characters
    abilities = relationship(
        "Ability", back_populates="pokemon", cascade="all, delete-orphan"
    )
    stats = relationship("Stat", back_populates="pokemon", cascade="all, delete-orphan")
    types = relationship("Type", back_populates="pokemon", cascade="all, delete-orphan")

class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String(15))  # Name with max 15 characters
    is_hidden = Column(Boolean)
    pokemon = relationship("Pokemon", back_populates="abilities")

class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String)
    base_stat = Column(Integer)
    pokemon = relationship("Pokemon", back_populates="stats")

class Type(Base):
    __tablename__ = "types"
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id", ondelete="CASCADE"))
    name = Column(String(10))  # Name with max 10 characters
    pokemon = relationship("Pokemon", back_populates="types")



