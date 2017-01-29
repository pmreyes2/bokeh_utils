"""Utility and application modules for web development

bokeh_utils.py	--- functions useful when working with bokeh

Typical usage:
1) Getting all the matplotlib colormaps and translate it to bokeh format.


"""
from create_map_colorbar import create_map
from get_all_mpl_palettes import get_all_mpl_palettes
from get_all_mpl_palettes import valid_mpl_palettes
from create_cmap_selection import create_cmap_selection
from create_low_high_sliders import create_low_high_sliders
from create_low_high_input_button import create_low_high_input_button

__all__=['get_all_mpl_palettes','create_map','valid_mpl_palettes','create_low_high_sliders','create_cmap_selection',
        'create_low_high_input_button']
