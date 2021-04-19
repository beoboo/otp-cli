import os

import click
import pyotp
import yaml


def print_usage():
    click.secho('Usage: totp generate TOKEN')


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.group(invoke_without_command=True, cls=AliasedGroup)
@click.pass_context
def cli(context):
    subcommand = context.invoked_subcommand

    if subcommand is None:
        print_usage()


@click.command()
def list():
    home = os.environ.get('HOME')

    with open('{}/totp.yaml'.format(home)) as file:
        contents = yaml.full_load(file.read())

        for name, item in contents['totp'].items():
            click.secho(name)


@click.command()
@click.argument('issuer')
def generate(issuer):
    home = os.environ.get('HOME')

    with open('{}/totp.yaml'.format(home)) as file:
        contents = yaml.full_load(file.read())

        generator = pyotp.parse_uri(contents['totp'][issuer]['url'])
        click.secho(generator.now())


cli.add_command(list)
cli.add_command(generate)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
