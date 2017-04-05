import numpy as np
import os
from replotlib import Axes
import matplotlib.pyplot as plt
from contextlib import contextmanager

from click.testing import CliRunner

from replotlib.cli import main

PATH = os.path.dirname(os.path.realpath(__file__))


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


def diff(file1, file2, ignore=None):
    if isinstance(ignore, str):
        ignore = [ignore]
    with open(file1) as f1, open(file2) as f2:
        for lineno, (line1, line2) in enumerate(zip(f1, f2), 1):
            ignoreline = False
            if ignore:
                for ig in ignore:
                    if ig in line1 and ig in line2:
                        ignoreline = True
                        break
            if not ignoreline and line1 != line2:
                return lineno
    return None


	# def test_json():
	#     gen_orig()
	#     runner = CliRunner()
	#     runner.invoke(main, ['test.rplt'])
	#     runner.invoke(main, ['-s', 'test.eps', 'test.rplt'])
	#     assert diff('test.eps', 'test_orig.eps', 'CreationDate') is None
	#     assert diff('test.eps', 'test_orig.eps',
	#                 ['CreationDate', 'Can Ignore more than one item']) is None


# def test_hdf5():
#     gen_orig('test_h5.rplt', 'hdf5')
#     runner = CliRunner()
#     runner.invoke(main, ['test.rplt'])
#     runner.invoke(main, ['-s', 'test.eps', 'test.rplt'])
#     assert diff('test.eps', 'test_orig.eps', 'CreationDate') is None
#     assert diff('test.eps', 'test_orig.eps',
#                 ['CreationDate', 'Can Ignore more than one item']) is None


def test_main():
    runner = CliRunner()
    runner.invoke(main, [PATH + '/test.rplt'])


def test_main_save():
    runner = CliRunner()
    runner.invoke(main, ['-s', PATH + '/test.eps', PATH + '/test.rplt'])


def test_main_style():
    runner = CliRunner()
    runner.invoke(main, ['--style_file', PATH + '/style.json', '-s',
                         PATH + '/test_styl.eps', PATH + '/test.rplt'])

def test_main_bb():
    runner = CliRunner()
    runner.invoke(main, ['--bb', '-s', PATH + '/test_bb.eps', 
                         PATH + '/test.rplt'])




# def gen_orig(test_file='test.rplt', file_type='json'):
#     style = {'nice_color': {'color': 'green'}}
#     with ignored(OSError):
#         os.remove(test_file)
#     print(test_file, file_type)
#     plt.rcParams['lines.linewidth'] = 3
#     plt.rcParams['lines.color'] = 'k'
#     ax = Axes(test_file, file_type=file_type, style=style)
#     ax.rcParams = {'lines.linewidth': 3,
#                    'lines.color': 'k'}
#     style = {'strong_color': {'color': 'blue'},
#              'errorbar': {'fmt': 'o'}}
#     ax.style = style
#     x = np.linspace(0, 1)
#     ax.plot(x, x**2, color='c', label=r'$x^2$')
#     ax.errorbar(x, x**2, x**2*0.1)
#     ax.plot(x, x**3, style='strong_color')
#     ax.plot(x, x**4, style='nice_color')
#     ax.set_xlabel('x')
#     ax.set_ylabel('y')
#     ax.legend()
#     plt.savefig('test_orig.eps')
