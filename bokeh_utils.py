import bokeh
import bokeh.plotting
import numpy as np

def get_all_palettes():
    """
    map_names, palettes_dict, palette_nums_dict = get_all_palettes()
    """
    import matplotlib.cm
    allmaps = sorted(matplotlib.cm.cmaps_listed.keys() + matplotlib.cm.datad.keys())
    palette_nums = []
    palettes = []
    map_names = []
    for cmap_name in allmaps:
        palette_nums += [[]]
        palettes += [[]]
        cmap = matplotlib.cm.get_cmap(cmap_name)
        if cmap.N < 256:
            pts = np.linspace(0,255,cmap.N).round()
            rr = np.interp(np.arange(256),pts,np.array(cmap.colors)[:,0])
            gg = np.interp(np.arange(256),pts,np.array(cmap.colors)[:,1])
            bb = np.interp(np.arange(256),pts,np.array(cmap.colors)[:,2])
            palette = []
            for i in range(256):
                palette += [matplotlib.colors.rgb2hex((rr[i],gg[i],bb[i]))]
            palettes[-1] += palette
            palette_nums[-1] += [int(m[1:],16) for m in palette]
            map_names += [cmap_name+"_smooth"]
            palette_nums += [[]]
            palettes += [[]]
        cmap = matplotlib.cm.get_cmap(cmap_name,256)
        palette = [matplotlib.colors.rgb2hex(m) for m in cmap(np.arange(cmap.N))]  # always 256 pts!!!
        palettes[-1] += palette
        palette_nums[-1] += [int(m[1:],16) for m in palette]
        map_names += [cmap_name]
    palettes_dict = dict(zip(map_names, palettes))
    palette_nums_dict = dict(zip(map_names, palette_nums))
    return {"map_names":map_names,"palettes_dict":palettes_dict,"palette_nums_dict":palette_nums_dict}


def create_map_colorbar(data2plot=None,palette_name="jet",fig_width_pxls=800,fig_height_pxls=500,x_range=(0,1),y_range=(0,1),
            title="MAP",x_axis_type="linear", cmaps=None,cb_title="dB",cb_min_border_left=40,cb_min_border_right=40,
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
    x0=x_range[0]
    x1=x_range[1]
    y0=y_range[0]
    y1=y_range[1]
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

def create_low_high_sliders(vabsmin,vabsmax,vmin,vmax,im,pcb,imcb,step=0.1):
    JS_code_slider = """
        var vmin = low_slider.value;
        var vmax = high_slider.value;
        im.glyph.color_mapper.high = vmax;
        im.glyph.color_mapper.low = vmin;

        imcb.data_source.data['y'][0]= vmin;
        imcb.data_source.data['dh'][0]= vmax-vmin;

        pcb.y_range.start = vmin;
        pcb.y_range.end = vmax;
        pcb.y_range['_initial_start'] = vmin;
        pcb.y_range['_initial_end'] = vmax;

        var right_ticks = pcb.extra_y_ranges['right_ticks'];
        right_ticks.start = vmin;
        right_ticks.end = vmax;
        right_ticks['_initial_start'] = vmin;
        right_ticks['_initial_end'] = vmax;

        imcb.data_source.trigger('change');
        im.data_source.trigger('change');
    """
    callback_slider = bokeh.models.CustomJS(args=dict( im=im,pcb=pcb,imcb=imcb),
                                        code=JS_code_slider)

    low_slider = bokeh.models.Slider(title="low limit",start=vabsmin,end=vabsmax,step=step,
                             value=vmin,callback=callback_slider,orientation="horizontal")
    high_slider = bokeh.models.Slider(title="high limit",start=vabsmin,end=vabsmax,step=step,
                             value=vmax,callback=callback_slider,orientation="horizontal")
    callback_slider.args['low_slider'] = low_slider
    callback_slider.args['high_slider'] = high_slider

    return low_slider,high_slider

def create_cmap_selection(im,imcb,cmaps=None,value="jet"):
    if type(cmaps)==type(None):
        cmaps = get_all_palettes()
    bmem_cmaps = bokeh.models.ColumnDataSource(data=cmaps["palette_nums_dict"])
    call_cm = bokeh.models.CustomJS(args=dict(im=im,imcb=imcb,bmem_cmaps=bmem_cmaps),code="""
        sel_map = select_cm.value; // select_cm will be added to the args dictionary after creating the widget!!
        numpalette = bmem_cmaps.data[sel_map];  // needs to be added if a list of list
        // first the image:

        var numglyph_palette1 = im.glyph.color_mapper["palette"];
        var numglyph_palette12 = im.glyph.color_mapper["_palette"];
        for (var i=0; i<numpalette.length; i++){
            numglyph_palette1[i] = numpalette[i];   // changing values of the palette with those of selected one
            numglyph_palette12[i] = numpalette[i];   // changing values of the palette with those of selected one
        }
        // now the colorbar:

        var numglyph_palette2 = imcb.glyph.color_mapper["palette"];
        var numglyph_palette22 = imcb.glyph.color_mapper["_palette"];
        for (var i=0; i<numpalette.length; i++){
            numglyph_palette2[i] = numpalette[i];
            numglyph_palette22[i] = numpalette[i];
        }

        imcb.data_source.trigger('change');
        im.data_source.trigger('change');
        //console.log(im)
        //console.log(imcb)
        """)
    select_cm = bokeh.models.Select(title="Color Map:", value =value, options=cmaps["map_names"],callback=call_cm)
    call_cm.args.update(dict(select_cm=select_cm))

    return select_cm

