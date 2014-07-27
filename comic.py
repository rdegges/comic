"""
    comic
    ~~~~~

    A static site generator built to render webcomics.
"""


from codecs import open
from glob import glob
from json import dumps
from os import getcwd, mkdir
from os.path import exists
from sys import path

from jinja2 import Environment, FileSystemLoader
from markdown import Markdown

path.append(getcwd())


# GLOBALS
OUT_DIR = 'out'
TEMPLATES_DIR = 'templates'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
markdown = Markdown(extensions=['meta'])


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


def fetch_comics():
    """
    Create a dictionary of all comics found in this directory structure.

    :rtype: dict
    :returns: A dictionary of comic data
    """
    comics = {}

    for f in glob('comics/meta/*.md'):

        # If there is no matching image, we'll skip it.
        if not glob(f.replace('meta', 'images', 1)[:-2] + '*'):
            continue

        # Otherwise, let's do this.
        html = markdown.convert(open(f, 'rb', 'utf-8').read())

        # Combine meta lines to remove nastiness in templates.
        for k, v in markdown.Meta.iteritems():
            markdown.Meta[k] = ' '.join(v)

        comics[glob(f.replace('meta', 'images', 1)[:-2] + '*')[0]] = {
            'meta': markdown.Meta,
            'html': html,
        }

        markdown.reset()

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


if __name__ == '__main__':
    env.globals.update(fetch_globals())
    page = render_page('index.html')
    print page

    for comic_image, data in fetch_comics().iteritems():
        data['image'] = comic_image
        print render_page('comic.html', data)
    #print dumps(fetch_comics(), indent=2, sort_keys=True)
