import bokeh
import bokeh.plotting
import numpy as np
import matplotlib.cm

def valid_mpl_palettes():
    return sorted(matplotlib.cm.cmaps_listed.keys() + matplotlib.cm.datad.keys())

def get_all_mpl_palettes(allmaps=None):
    """
    map_names, palettes_dict, palette_nums_dict = get_all_palettes()
    """
    if type(allmaps)==type(None):
        # Getting all the map names available in matplotlib
        allmaps = valid_mpl_palettes()
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

