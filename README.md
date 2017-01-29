# bokeh_utils
Utilities for interactive scientific plots using python, bokeh and javascript.
# Overview
Python, bokeh , and JavaScript are put together to create an interactive Map to 
manipulate on the client side the lower and upper limits of the 2D color map, 
as well as the colormap/palette used in the MAP and in the colorbar.
## Requirements

*  [numpy](http://www.numpy.org/)
  
*  [scipy](http://www.scipy.org/)
  
*  [matplotlib](http://matplotlib.org/)
  
*  [Bokeh](http://bokeh.pydata.org/en/latest/).

## Example
This creates a simple 2D map with controls for vmin, vmax, and selection of palette from matplotlib library to use in bokeh.
```python
import bokeh
import bokeh.plotting
import numpy as np
import calendar
import bokeh_utils

x0 = calendar.timegm((2016,11,22,14,35,25))*1000.
x1 = calendar.timegm((2016,11,22,15,40,13))*1000.
y0 = 60
y1 = 1000
vmin,vmax = -1,1.

N = 200
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

cmaps = bokeh_utils.get_all_mpl_palettes(allmaps=['Accent','CMRmap','Greys','viridis'])
# if allmaps is None, then all the possible matplotlib palettes will be loaded
# bokeh_utils.valid_mpl_palettes() gives a list of all possible matplotlib palettes
p_width = 400
p_height = 250
map_title = "MAP"
initial_cmap = "viridis"

p,im = bokeh_utils.create_map(data2plot=d,palette_name=initial_cmap,
        fig_width_pxls=p_width, fig_height_pxls=p_height,x_range=(x0,x1),
        y_range=(y0,y1),title=map_title,x_axis_type="datetime",
        cmaps=cmaps,vmin=vmin,vmax=vmax)

# Controls
vabsmin,vabsmax = -2,2
low_slider,high_slider = bokeh_utils.create_low_high_sliders(vabsmin,vabsmax,vmin,vmax,im=im)
input_vmin,input_vmax,button_update = bokeh_utils.create_low_high_input_button(vmin,vmax,im=im,width=450)
select_cm = bokeh_utils.create_cmap_selection(im,cmaps=cmaps, value=initial_cmap)

# Layout
layout = bokeh.plotting.gridplot([[p],[input_vmin,input_vmax],[button_update],
                                  [low_slider],[high_slider],[select_cm]])

fname = "RTI_cb_slider_cmap_select.html"
bokeh.io.output_file(fname, title="RTI and select",mode='inline') # use inline instead of cdn for independent page
bokeh.io.save(layout)
```
### output

<img src="https://github.com/pmreyes2/bokeh_utils/blob/master/MAP_cb_controls.png" width="800">

This is similar to the previous example, but with crosshair and tap tools included for display of coordinates:
This creates a simple 2D map with controls for vmin, vmax, and selection of palette from matplotlib library to use in bokeh.
```python
import bokeh
import bokeh.plotting
import numpy as np
import calendar
import bokeh_utils
reload(bokeh_utils)

x0 = calendar.timegm((2016,11,22,14,35,25))*1000.
x1 = calendar.timegm((2016,11,22,15,40,13))*1000.
y0 = 60
y1 = 1000
vmin,vmax = -1,1.

N = 200
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

lmem_source = bokeh.models.ColumnDataSource(data=dict(state=[1]))


callback_tap = bokeh.models.CustomJS(args=dict(lmem_source=lmem_source), code="""
            if(lmem_source.data['state'][0] < 1){
                lmem_source.data['state'][0] += 1;
            }else{
                lmem_source.data['state'][0] = 0;
            }
            lmem_source.trigger('change'); // to update value of state
    """)

callback_hover = bokeh.models.CustomJS(args=dict(lmem_source=lmem_source),code="""
    if (lmem_source.data['state'][0] == 1){
        var x = cb_data['geometry'].x;
        var y = cb_data['geometry'].y;

        var d = new Date(x);
        var sHours = d.getUTCHours()+"";        // +"" converts it to string
        var sMinutes = d.getUTCMinutes()+"";
        var sSeconds = d.getUTCSeconds()+"";
        var sMilliseconds = d.getUTCMilliseconds()+"";
        while (sHours.length<2)        sHours = "0" + sHours;
        while (sMinutes.length<2)      sMinutes = "0" + sMinutes;
        while (sSeconds.length<2)      sSeconds = "0" + sSeconds;
        while (sMilliseconds.length<3) sMilliseconds = "0" + sMilliseconds;
        var sHeight = y.toFixed(2)+"";
        while (sHeight.length<7)       sHeight = "&nbsp;" + sHeight;
        
        var cursor_time = sHours+":"+sMinutes+":"+sSeconds+"."+sMilliseconds;
        var cursor_height = sHeight + " km";
        
        divtime.text = 'Time:'+cursor_time;
        divheight.text = 'Height:'+cursor_height;
        crosshair_tool.active = true;
        crosshair_tool.disabled =false;
    }else{
        crosshair_tool.active = false;
        crosshair_tool.disabled =true;
    }
    """)

cmaps = bokeh_utils.get_all_mpl_palettes(allmaps=['Accent','CMRmap','Greys','viridis'])
# if allmaps is None, then all the possible matplotlib palettes will be loaded
# bokeh_utils.valid_mpl_palettes() gives a list of all possible matplotlib palettes
p_width = 400
p_height = 250
map_title = "MAP"
initial_cmap = "viridis"

p,im = bokeh_utils.create_map(data2plot=d,palette_name=initial_cmap,
        fig_width_pxls=p_width, cb_title="", fig_height_pxls=p_height,x_range=(x0,x1),
        y_range=(y0,y1),title=map_title,x_axis_type="datetime",
        cmaps=cmaps,vmin=vmin,vmax=vmax)


divtime = bokeh.models.Div(text="Time:")
divheight = bokeh.models.Div(text="Height:")
crosshair_tool = bokeh.models.CrosshairTool()
hover_tool = bokeh.models.HoverTool(callback=callback_hover,tooltips=None)
tap_tool = bokeh.models.TapTool(callback=callback_tap)

callback_hover.args.update(dict(divtime=divtime,divheight=divheight,
                                crosshair_tool=crosshair_tool))

p.add_tools(crosshair_tool)
p.add_tools(hover_tool)
p.add_tools(tap_tool)

vabsmin,vabsmax = -2,2
low_slider,high_slider = bokeh_utils.create_low_high_sliders(vabsmin,vabsmax,vmin,vmax,im=im)
input_vmin,input_vmax,button_update = bokeh_utils.create_low_high_input_button(vmin,vmax,im=im,width=450)

select_cm = bokeh_utils.create_cmap_selection(im,cmaps=cmaps, value=initial_cmap)

layout = bokeh.plotting.gridplot([[p],[divtime],[divheight],[input_vmin,input_vmax],
                                  [button_update],[low_slider],[high_slider],[select_cm]])

fname = "RTI_cb_slider_cmap_select_crosshair.html"
bokeh.io.output_file(fname, title="RTI and select",mode='cdn') # use inline instead of cdn for independent page
bokeh.io.save(layout)
```
### output

<img src="https://github.com/pmreyes2/bokeh_utils/blob/master/MAP_cb_controls_crosshair.png" width="800">


