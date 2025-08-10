import click
from .service import run_prompt_test

@click.command()
@click.option("--payload", prompt=True, help="Prompt to test against the LLM")
def main(payload):
    res = run_prompt_test(payload)
    click.echo(res)

if __name__ == "__main__":
    main()
