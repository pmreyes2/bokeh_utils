import bokeh
import bokeh.plotting
import numpy as np

def create_low_high_input_button(vmin,vmax,im,width=450):
    JS_code_vmin_vmax = """
        var vmin = parseFloat(input_vmin.value);
        var vmax = parseFloat(input_vmax.value);
        im.glyph.color_mapper.high = vmax;
        im.glyph.color_mapper.low = vmin;
        im.data_source.trigger('change');
    """
    callback_update = bokeh.models.CustomJS(code=JS_code_vmin_vmax)
    input_vmin = bokeh.models.widgets.TextInput(value="%d"%vmin,title="vmin",width=int(width/3.))
    input_vmax = bokeh.models.widgets.TextInput(value="%d"%vmax,title="vmax",width=int(width/3.))
    button_update =  bokeh.models.Button(label="Update vmin/vmax", callback=callback_update,width=int(width/3.))

    callback_update.args['input_vmin'] = input_vmin
    callback_update.args['input_vmax'] = input_vmax
    callback_update.args['im'] = im

    return input_vmin,input_vmax,button_update

