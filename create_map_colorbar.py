import bokeh
import bokeh.plotting
import numpy as np

def create_map(data2plot=None,palette_name="jet",fig_width_pxls=800,fig_height_pxls=500,x_range=(0,1),y_range=(0,1),
            title="MAP",x_axis_type="linear", cmaps=None,cb_title="",create_colorbar=True,
            min_border_left=20,min_border_right=10,min_border_top=30, min_border_bottom=10,title_font_size="12pt",
            title_align="center",vmin="auto",vmax="auto",output_quad=False,
            tools= ["box_zoom,wheel_zoom,pan,reset,previewsave,resize"]):
    """
    x_axis_type: "linear", "log", "datetime", "auto"
    """
    if type(cmaps)==type(None):
        cmaps = get_all_palettes()
    if vmin=="auto":
        vmin = np.nanmin(data2plot)
    if vmax=="auto":
        vmax = np.nanmax(data2plot)
    try:
        x0=x_range[0]
        x1=x_range[1]
    except:
        x0 = x_range.start
        x1 = x_range.end
    try:
        y0=y_range[0]
        y1=y_range[1]
    except:
        y0 = y_range.start
        y1 = y_range.end
    p = bokeh.plotting.figure(x_range=x_range, y_range=y_range,x_axis_type=x_axis_type,plot_width=fig_width_pxls,
        plot_height=fig_height_pxls, min_border_left=min_border_left,min_border_right=min_border_right,title=title,
        min_border_top=min_border_top,min_border_bottom=min_border_bottom,
        tools= tools)
    p.title.text_font_size = title_font_size
    p.title.align = title_align
    im = p.image(image=[data2plot],dw=[x1-x0],dh=[y1-y0],x=[x0],y=[y0],palette=cmaps["palettes_dict"][palette_name])
    im.glyph.color_mapper.high = vmax
    im.glyph.color_mapper.low = vmin
    imquad = p.quad(top=[y1], bottom=[y0], left=[x0], right=[x1],alpha=0) # This is used for hover and taptool
    if create_colorbar:
        color_bar = bokeh.models.ColorBar(color_mapper=im.glyph.color_mapper, label_standoff=12, location=(0,0))
        p.add_layout(color_bar, 'right')
    if output_quad:
        return p,im,imquad
    else:
        return p,im


