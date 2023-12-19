import stereo

l = 'img/L.jpg'
r = 'img/R.jpg'


dm = stereo.depth_map(l, r, strob_size=21, step=1)
dm.calc_depth_map()
dm.show_map()