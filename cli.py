import json
import click
from sc2_extract import sc2_extract
from sc2_transform import sc2_transform


@click.command()
@click.argument('file')
@click.option('--flag', '-f', multiple=True,
              default=['header', 'details', 'initdata', 'gameevents', 'messageevents', 'trackerevents', 'attributeevents'],
              help='Limit output to certain flags. ex: -f header -f details')
@click.option('--details', '-d', is_flag=True)
def cmd_extract(file, flag, details):
    extract = sc2_extract(file, flag)
    if details:
        extract = sc2_transform(extract)
    extract_utf8 = convert(extract)
    extract_json = json.dumps(extract_utf8)
    return click.echo(extract_json)


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        try:
            return unicode(input, errors='ignore').encode('utf-8')
        except:
            return input


if __name__ == '__main__':
    cmd_extract()
