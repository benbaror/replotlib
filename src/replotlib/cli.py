"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later,
  but that will cause problems:
  the code will get executed twice:

  - When you run `python -mreplotlib` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``replotlib.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``replotlib.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import json
from collections import OrderedDict

import click
import matplotlib.pyplot as plt

from . import Axes


def replot(file_name, file_type, style={}, savefig=False, **kargs):
    plt.figure()
    Axes(file_name, file_type=file_type, style=style,
         erase=False).replot()
    if savefig:
        plt.savefig(savefig, **kargs)
    else:
        plt.show()


@click.command()
@click.argument('file_name', nargs=1)
@click.option('--savefig', '-s', help="save the figure to 'savefig'.")
@click.option('--bb', is_flag=True,
              help="make figure compatible with black background")
@click.option('--file_type', '-t', default='json',
              help="file type 'json' or 'hdf5'")
@click.option('--style_file', default=None,
              help="Style file in json format")
def main(file_name, savefig, file_type, style_file, bb):
    if style_file:
        with open(style_file) as f:
            style = json.load(f, object_pairs_hook=OrderedDict)
    else:
        style = {}

    if bb:
        from matplotlib.colors import colorConverter
        colorConverter.cache = {}
        colorConverter.colors['w'], colorConverter.colors['k']\
            = (colorConverter.colors['k'], colorConverter.colors['w'])
        colorConverter.cache['black'] = colorConverter.colors['k']
        colorConverter.cache['wight'] = colorConverter.colors['w']
        plt.rcParams['savefig.transparent'] = True
    try:
        replot(file_name=file_name, file_type=file_type,
               savefig=savefig, style=style)
    except IOError as err:
        print("Cannot read '{}': {}"
              .format(file_name, err))
    except ValueError:
        replot(file_name=file_name, file_type='hdf5',
               savefig=savefig, style=style)
