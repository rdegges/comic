"""
comic
~~~~~

A static site generator built to render webcomics.

Usage:
    comic create
      [<name> | -n <name> | --name <name>]
    comic start
      [<file> | -f <file> | --file <file>]
    comic stop
    comic build
      [<file> | -f <file> | --file <file>]
    comic
      (-h | --help)
    comic
      (-v | --version)

Options:
    -h --help       Show this screen.
    -v --version    Show version.

Written by Randall Degges (@rdegges): http://www.rdegges.com
"""


from codecs import open
from glob import glob
from os import getcwd, mkdir
from os.path import abspath, basename, dirname, exists, splitext
from sys import exit, path

from docopt import docopt
from jinja2 import Environment, FileSystemLoader
from yaml import load

from . import __version__

path.append(getcwd())


# GLOBALS
OUT_DIR = 'out'
TEMPLATES_DIR = 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def fetch_globals():
    """
    Create a dictionary of all globals specified in this comic's configuration
    file.

    :rtype: dict
    :returns: A dictionary of configuration variables.
    """
    import conf

    globals = {}
    for var in [v for v in dir(conf) if not v.startswith('__')]:
        globals[var] = getattr(conf, var)

    return globals


def slugify(file):
    """
    Given a comic's file path, return the slug.

    Slugs will be calculated as a lowercase version of the file's basename
    (*without any extension*).

    :param str file: The filename to slugify.
    """
    name, ext = splitext(file)
    return basename(name).lower()


def fetch_comics():
    """
    Create a dictionary of all comics found in this directory structure.

    :rtype: dict
    :returns: A dictionary of comic data
    """
    comics = {}

    for f in glob('comics/meta/*.yaml'):
        slug = slugify(f)

        # If there is no matching image, we'll skip it.
        if not glob(f.replace('meta', 'images', 1)[:-4] + '*'):
            continue

        # Load all comic data.
        yaml = load(open(f, 'rb', 'utf-8').read())
        html = yaml['long']
        yaml['date'] = yaml['date'].isoformat()
        del yaml['long']

        comics[slug] = {
            'image': glob(f.replace('meta', 'images', 1)[:-4] + '*')[0],
            'meta': yaml,
            'html': html,
        }

    from json import dumps
    print dumps(comics, indent=2, sort_keys=True)
    return comics


def render_page(page, context=None):
    """
    Render static pages.

    :param str page: The page to render, eg: 'index.html'.
    :param dict context: The context to use when rendering the page.

    :rtype: str
    :returns: The HTML page.
    """
    if not exists(OUT_DIR):
        mkdir(OUT_DIR)

    if context:
        return env.get_template(page).render(**context)
    else:
        return env.get_template(page).render()


def create(name):
    """
    Create a new webcomic!

    This command will create a new webcomic by creating the proper directory
    structure and populating it with some defaults.

    :param str name: (optional) The name of the comic.
    """
    while not name:
        name = raw_input("Enter your new comic's name: ")

    dir_name = name.lower()
    if not exists(dir_name):
        mkdir(dir_name)
        mkdir(dir_name + '/comics')
        mkdir(dir_name + '/templates')

        open(dir_name + '/conf.py', 'wb').close()
        open(dir_name + '/templates/base.html', 'wb').close()
        open(dir_name + '/templates/comic.html', 'wb').close()
        open(dir_name + '/templates/index.html', 'wb').close()

    print 'Finished creating your webcomic directory:', dir_name


def build(file):
    """
    Build an existing webcomic.

    This works by compiling the comic into HTML templates, and outputting a
    static website.

    :param str file: (optional) An absolute file path to the comic's
      configuration file.  If not specified, we'll assume the file is named
      ``conf.py`` and exists in the current directory.
    """
    if not file:
        file = getcwd() + '/conf.py'

    if not exists(file):
        print 'ERROR! No configuration file found.'
        exit(1)

    comic_dir = dirname(abspath(file))

    env.globals.update(fetch_globals())
    page = render_page('index.html')
    print page

    for comic_image, data in fetch_comics().iteritems():
        data['image'] = comic_image
        print render_page('comic.html', data)
    #print dumps(fetch_comics(), indent=2, sort_keys=True)


def main():
    """
    Our CLI entry point.

    This is where the *magic* actually happens.  When a users runs `comic` on
    the command line, this is the function that will get run.

    What we'll do here is just basic dispatching: we'll figure out what the
    user wants to do, then make the appropriate dispatch call to actually do
    stuff.
    """
    args = docopt(__doc__, version=__version__)

    if args['create']:
        create(args['<name>'])
    elif args['build']:
        build(args['<file>'])
