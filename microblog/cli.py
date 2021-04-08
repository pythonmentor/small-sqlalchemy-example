"""Module responsible of defining the command-line interface of the program."""

import click
from sqlalchemy import func, desc
from sqlalchemy.orm.exc import NoResultFound

from .models import Article, Tag
from .database import Session, drop_and_create


@click.group()
def main():
    """This short example aims at demonstrating how to query a many to many
    relationship using sqlalchemy."""


@main.command()
def initdb():
    """Initialize the sqlite3 database with demo data."""
    # Drop and create tables again
    drop_and_create()

    # Create a new session
    with Session() as session:
        # Create a few articles and add them to the current session
        first = Article(title="mon premier article sur python")
        second = Article(title="mon second article sur python")
        third = Article(title="mon troisième article sur python")
        fourth = Article(title="mon quatrième article sur python")
        fifth = Article(title="mon cinquième article sur python")

        session.add_all([first, second, third, fourth, fifth])

        # Create a few tags, add them to the current session
        # and add them to articles
        python = Tag(name='python')
        web = Tag(name='web')
        flask = Tag(name='flask')
        django = Tag(name='django')

        session.add_all([python, web, flask, django])

        first.tags.extend([python, web, django])
        second.tags.append(python)
        third.tags.extend([python, web, flask])
        fifth.tags.extend([python, web, django])

        # Commit the session modifications to database
        session.commit()


def get_or_create(session, model, **attributes):
    """Gets the corresponding instance of the model if exists or creates it."""
    filter_args = []
    for attribute, value in attributes.items():
        filter_args.append(getattr(model, attribute) == value)

    try:
        instance = session.query(model).filter(*filter_args).one()
    except NoResultFound:
        instance = model(**attributes)
        session.add(instance)
        session.commit()

    return instance


@main.command()
@click.argument('title')
@click.argument('tags', nargs=-1)
def article(title, tags):
    """Create a new article with the given title and tags. If the article
    exists, it is updated."""
    title = title.lower()
    tags = [tag.lower() for tag in tags]

    with Session() as session:
        article = get_or_create(session, Article, title=title)
        article.tags = []
        for tag_name in tags:
            tag = get_or_create(session, Tag, name=tag_name)
            article.tags.append(tag)
        session.commit()


@main.command()
@click.argument('tags', nargs=-1)
def show(tags):
    """Shows articles with spectified tags in order of pertinence."""
    with Session() as session:
        if not tags:
            articles = session.query(Article).order_by(desc(Article.id)).all()
            click.echo('Voici les articles demandés:')
            for article in articles:
                article_tags = (
                    f" ({', '.join(str(tag) for tag in article.tags)})"
                    if article.tags
                    else ""
                )
                click.echo(f"- {article}{article_tags}")
        else:
            articles = (
                session.query(
                    Article, func.count(Article.id).label('tag_count')
                )
                .join(Article.tags)
                .filter(Tag.name.in_(tags))
                .group_by(Article)
                .order_by(desc('tag_count'), Article.title)
                .all()
            )

            click.echo('Voici les articles demandés:')
            for article, tag_count in articles:
                click.echo(
                    f"- {article} ({', '.join(str(tag) for tag in article.tags)}) [{tag_count} tag(s) recherché(s)]"
                )
