import click
from .service import detect_deepfake

@click.command()
@click.option("--url", prompt=True, help="Media URL to scan")
def main(url):
    click.echo(detect_deepfake(url))

if __name__ == "__main__":
    main()
