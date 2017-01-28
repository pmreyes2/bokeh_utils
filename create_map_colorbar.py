import bokeh
import bokeh.plotting
import numpy as np

def create_map_colorbar(data2plot=None,palette_name="jet",fig_width_pxls=800,fig_height_pxls=500,x_range=(0,1),y_range=(0,1),
            title="MAP",x_axis_type="linear", cmaps=None,cb_title="",cb_min_border_left=40,cb_min_border_right=40,
            cb_fig_width_pxls=100,
            min_border_left=20,min_border_right=10,min_border_top=30, min_border_bottom=10,title_font_size="12pt",
            title_align="center",vmin="auto",vmax="auto",
            tools= ["box_zoom,wheel_zoom,pan,reset,previewsave,resize,crosshair"],
            cb_tools = ["box_zoom,wheel_zoom,pan,reset,previewsave,resize"]):
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
    p.quad(top=[y1], bottom=[y0], left=[x0], right=[x1],alpha=0) # This is used for hover and taptool



    pcb = bokeh.plotting.figure(x_range=(0,1), y_range=(vmin,vmax) ,plot_width=cb_fig_width_pxls,
                plot_height=fig_height_pxls,
                min_border_left=cb_min_border_left,min_border_right=cb_min_border_right,title=cb_title,
                min_border_top=min_border_top, min_border_bottom=min_border_bottom,
                                tools=cb_tools)
    pcb.title.text_font_size = title_font_size
    pcb.title.align = title_align
    cb_data = np.linspace(vmin,vmax,256).reshape(256,1)
    imcb = pcb.image(image = [cb_data],x=[0],y=[vmin],dw=[1],dh=[vmax-vmin],
                     palette=cmaps["palettes_dict"][palette_name])
    pcb.xaxis.major_label_text_color = None
    pcb.yaxis.major_label_text_color = None
    pcb.yaxis.major_tick_line_color = None
    pcb.yaxis.minor_tick_line_color = None
    pcb.xaxis.major_tick_line_color = None
    pcb.xaxis.minor_tick_line_color = None
    pcb.extra_y_ranges = {"right_ticks": bokeh.models.Range1d(start=vmin, end=vmax)}
    pcb.add_layout(bokeh.models.LinearAxis(y_range_name="right_ticks"),'right')


    return p,im,pcb,imcb


