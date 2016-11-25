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
```python
import bokeh
import bokeh.plotting
import numpy as np
import calendar
from bokeh_utils import bokeh_utils

x0 = calendar.timegm((2016,11,22,14,35,25))*1000.
x1 = calendar.timegm((2016,11,22,15,40,13))*1000.
y0 = 60
y1 = 1000
vmin,vmax = -1,1.

N = 500
x = np.linspace(0, 10, N)
y = np.linspace(0, 10, N)
xx, yy = np.meshgrid(x, y)
d = np.sin(xx)*np.cos(yy)

cmaps = bokeh_utils.get_all_palettes()
p_width = 800
p_height = 500
map_title = "MAP"
initial_cmap = "viridis"

p,im,pcb,imcb = bokeh_utils.create_map_colorbar(data2plot=d,palette_name=initial_cmap,
        fig_width_pxls=p_width, cb_title="", fig_height_pxls=p_height,x_range=(x0,x1),
        y_range=(y0,y1),title=map_title,x_axis_type="datetime",
        cmaps=cmaps,vmin=vmin,vmax=vmax)
vabsmin,vabsmax = -2,2
low_slider,high_slider = bokeh_utils.create_low_high_sliders(vabsmin,vabsmax,vmin,vmax,
        im=im,pcb=pcb,imcb=imcb)
select_cm = bokeh_utils.create_cmap_selection(im,imcb,cmaps=cmaps, value=initial_cmap)

layout = bokeh.plotting.gridplot([[p,pcb],[low_slider,high_slider],[select_cm]])

fname = "RTI_cb_slider_cmap_select.html"
bokeh.io.output_file(fname, title="RTI and select",mode='cdn') # use inline instead of cdn for independent page
bokeh.io.save(layout)
```
### output

<img src="https://github.com/pmreyes2/bokeh_utils/blob/master/MAP_cb_controls.png" width="800">
