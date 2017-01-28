"""Utility and application modules for web development

bokeh_utils.py	--- functions useful when working with bokeh

Typical usage:
1) Getting all the matplotlib colormaps and translate it to bokeh format.


"""
from create_map_colorbar import create_map_colorbar
from get_all_mpl_palettes import get_all_mpl_palettes
from get_all_mpl_palettes import valid_mpl_palettes
from create_cmap_selection import create_cmap_selection
from create_low_high_sliders import create_low_high_sliders

__all__=['get_all_mpl_palettes','create_map_colorbar','valid_mpl_palettes','create_low_high_sliders','create_cmap_selection']
