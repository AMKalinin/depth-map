import stereo

l = 'img/L.jpg'
r = 'img/R.jpg'



dm = stereo.depth_map(l, r, 21, 5)
dm.calc_depth_map()
dm.show_map()