"""Provide the basic Axes class."""
import json
import os
from collections import OrderedDict
from functools import wraps

import h5py
import matplotlib.pyplot as plt


class HDF5IO(object):
    """
    """

    def __init__(self, data_file):
        """
        """
        self.data_file = data_file

    def read(self):
        """Read the hdf5 file."""
        with h5py.File(self.data_file, 'r') as h5_file:
            dct = OrderedDict(
                sorted([(plot_function,
                         {arg_name: OrderedDict(
                             sorted([(str(key), value[()])
                                     for key, value in arg.items()]))
                          for arg_name, arg in args.items()})
                        for plot_function, args in h5_file.items()
                        if plot_function != 'rcParams']))
            if 'rcParams' in h5_file:
                dct['rcParams'] = dict((key, val[()])
                                       for key, val in
                                       h5_file['rcParams'].items())
        return dct

    def save(self, name, plot_object):
        """Save a plot object to the hdf5 file."""
        with h5py.File(self.data_file) as h5_file:
            plot_object_group = h5_file.require_group(name)
            if name == 'rcParams':
                for param, value in plot_object.items():
                    plot_object_group[param] = value

            elif name == 'style':
                for style, dct in plot_object.items():
                    style_group = plot_object_group.require_group(style)
                    for key, value in dct.items():
                        style_group[key] = value
            else:
                args_group = plot_object_group.require_group('args')
                kwargs_group = plot_object_group.require_group('kwargs')
                for key, arg in plot_object['args'].items():
                    args_group[str(key)] = arg
                for key, value in plot_object['kwargs'].items():
                    kwargs_group[str(key)] = value


class JsonIO(object):
    """
    """

    def __init__(self, data_file):
        """
        """
        self.data_file = data_file

    def read(self):
        with open(self.data_file) as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
        return data

    def save(self, name, dct_obj):
        if name not in ('style', 'rcParams'):
            for key, value in dct_obj['args'].items():
                try:
                    dct_obj['args'][key] = value.tolist()
                except AttributeError:
                    pass
            for key, value in dct_obj['kwargs'].items():
                try:
                    dct_obj['kwargs'][key] = value.tolist()
                except AttributeError:
                    pass

        dct = {name: dct_obj}
        try:
            data = self.read()
        except IOError:
            data = {}
        data.update(dct)
        with open(self.data_file, 'w') as json_file:
            json.dump(data, json_file, sort_keys=True,
                      indent=0, separators=(',', ': '))


class Axes(object):

    """
    Save matplotlib command for later reuse.

    Holds and `matplotlib.axes.Axes` object which saves the operations done on
    it for latter re-plotting.
    """

    def __init__(self, data_file, ax=None, file_type='json', style=None,
                 rcParams=None, erase=True):
        """
        Save matplotlib command for later reuse.

        Arguments:

        `data_file` -- the file on which the plotting functions and
                       data are stored

        `ax` -- an `matplotlib.axes.Axes` instance (default: the
                       current `matplotlib.axes.Axes` instance)

        """
        self._action_number = 0
        self.file_type = file_type
        self.data_file = data_file
        self._style = style if style else {}
        self._rcParams = rcParams if rcParams else {}

        if erase:
            try:
                os.remove(self.data_file)
            except OSError:
                pass

        if file_type == 'json':
            self.io = JsonIO(self.data_file)
        elif file_type == 'hdf5':
            self.io = HDF5IO(self.data_file)
        else:
            raise NotImplementedError(self.file_type)

        try:
            style = self.io.read()['style']
            style.update(self._style)
            self._style = style
        except (IOError, KeyError):
            pass

        try:
            rcParams = self.io.read()['rcParams']
            rcParams.update(self._rcParams)
            self._rcParams = rcParams
        except (IOError, KeyError):
            pass

        plt.rcParams.update(self.rcParams)
        self._ax = ax if ax else plt.gca()

    @property
    def action_number(self):
        """Number of action called."""
        self._action_number += 1
        return '{:03d}'.format(self._action_number)

    def __getattr__(self, attr):
        """Pass the plotting function to the parser."""
        if attr[1] == '_':
            raise AttributeError
        try:
            return self.parse_func(getattr(self._ax, attr))
        except AttributeError:
            return self.parse_func(getattr(self, '_' + attr))

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, dct):
        self._style.update(dct)
        self.io.save('style', self.style)

    @property
    def rcParams(self):
        return self._rcParams

    @rcParams.setter
    def rcParams(self, dct):
        self._rcParams.update(dct)
        self.io.save('rcParams', self.rcParams)

    def replot(self):
        """Replot using the recorded ploting funtions."""
        for key, plot_object in self.io.read().items():
            if key not in ('style', 'rcParams'):
                attr = '_'.join(key.split('_')[1:])
                kwargs = plot_object['kwargs']
                self.apply_style(kwargs, attr)
                try:
                    getattr(self._ax, attr)(
                        *plot_object['args'].values(), **kwargs)
                except AttributeError:
                    getattr(self, attr)(
                        *plot_object['args'].values(), **kwargs)

        plt.draw_if_interactive()

    def _to_dict(self, name, *args, **kwargs):
        return self.action_number + '_' + name, {'args': dict(enumerate(args)),
                                                 'kwargs': kwargs}

    def parse_func(self, func):
        """Create and save a plot object by parsing the ploting function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.io.save(*self._to_dict(func.__name__, *args, **kwargs))
            self.apply_style(kwargs, func.__name__)
            return func(*args, **kwargs)
        return wrapper

    def apply_style(self, kwargs, extra_styles=None):
        if extra_styles:
            kwargs['style'] = (extra_styles + ' ' +
                               kwargs.get('style', ' ')).strip()
        try:
            for style in kwargs.pop('style').split(' '):
                try:
                    kwargs.update(self.style[style])
                except KeyError:
                    pass

        except KeyError:
            pass
