import click
from .service import run_prompt_test

@click.command()
@click.option("--payload", prompt=True, help="Prompt to test against the LLM")
def main(payload):
    result = run_prompt_test(payload)
    click.echo(result)

if __name__ == "__main__":
    main()
