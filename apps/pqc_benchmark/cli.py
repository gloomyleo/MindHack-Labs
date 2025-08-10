import click
from .service import run_benchmarks

@click.command()
def main():
    res = run_benchmarks()
    click.echo(res)

if __name__ == "__main__":
    main()
