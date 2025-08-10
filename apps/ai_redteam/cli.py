import click
from .service import plan_attack

@click.command()
@click.option("--system", default="Windows Server 2019", help="Target system description")
@click.option("--ttps", default="T1059,T1547", help="Comma-separated MITRE techniques")
def main(system, ttps):
    plan = plan_attack(system, [t.strip() for t in ttps.split(",") if t.strip()])
    click.echo(plan)

if __name__ == "__main__":
    main()
