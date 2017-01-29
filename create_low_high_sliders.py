import bokeh
import bokeh.plotting
import numpy as np

def create_low_high_sliders(vabsmin,vabsmax,vmin,vmax,im,step=0.1):
    JS_code_slider = """
        var vmin = low_slider.value;
        var vmax = high_slider.value;
        im.glyph.color_mapper.high = vmax;
        im.glyph.color_mapper.low = vmin;
        im.data_source.trigger('change');
    """
    callback_slider = bokeh.models.CustomJS(args=dict( im=im),
                                        code=JS_code_slider)

    low_slider = bokeh.models.Slider(title="low limit",start=vabsmin,end=vabsmax,step=step,
                             value=vmin,callback=callback_slider,orientation="horizontal")
    high_slider = bokeh.models.Slider(title="high limit",start=vabsmin,end=vabsmax,step=step,
                             value=vmax,callback=callback_slider,orientation="horizontal")
    callback_slider.args['low_slider'] = low_slider
    callback_slider.args['high_slider'] = high_slider

    return low_slider,high_slider

