"""Module responsible of defining the models for the application."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association table used to link articles and tags in their many to many
# relationship
article_tag = Table(
    'article_tag',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
)


class Article(Base):
    """Represents a very simple article with only a title."""

    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    tags = relationship(
        'Tag', secondary='article_tag', back_populates='articles'
    )

    def __str__(self):
        return self.title.title()

    def __repr__(self):
        return f'Article(id={self.id}, title="{self.title}")'


class Tag(Base):
    """Represents a tag to categorize articles."""

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    articles = relationship(
        'Article', secondary='article_tag', back_populates='tags'
    )

    def __str__(self):
        return self.name.capitalize()

    def __repr__(self):
        return f'Tag(id={self.id}, name="{self.name}")'