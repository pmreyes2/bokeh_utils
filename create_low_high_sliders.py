import bokeh
import bokeh.plotting
import numpy as np

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

