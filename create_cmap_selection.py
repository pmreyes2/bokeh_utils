import bokeh
import bokeh.plotting
import numpy as np

def create_cmap_selection(im,cmaps=None,value="jet"):
    if type(cmaps)==type(None):
        cmaps = get_all_palettes()
    bmem_cmaps = bokeh.models.ColumnDataSource(data=cmaps["palette_nums_dict"])
    call_cm = bokeh.models.CustomJS(args=dict(im=im,bmem_cmaps=bmem_cmaps),code="""
        sel_map = select_cm.value; // select_cm will be added to the args dictionary after creating the widget!!
        numpalette = bmem_cmaps.data[sel_map];  // needs to be added if a list of list

        var numglyph_palette1 = im.glyph.color_mapper["palette"];
        var numglyph_palette12 = im.glyph.color_mapper["_palette"];
        for (var i=0; i<numpalette.length; i++){
            numglyph_palette1[i] = numpalette[i];   // changing values of the palette with those of selected one
            numglyph_palette12[i] = numpalette[i];   // changing values of the palette with those of selected one
        }

        im.data_source.trigger('change');
        """)
    select_cm = bokeh.models.Select(title="Color Map:", value =value, options=cmaps["map_names"],callback=call_cm)
    call_cm.args.update(dict(select_cm=select_cm))

    return select_cm

