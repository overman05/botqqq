from src import db
import config
import click


@click.group()
def cli():
    pass


@click.command()
def initdb():
    db.init_db(config)


cli.add_command(initdb)

if __name__ == "__main__":
    cli()
