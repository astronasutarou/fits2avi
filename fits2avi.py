#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (print_function, absolute_import)

import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits

from argparse import ArgumentParser as ap

if __name__ == '__main__':
  parser = ap(description='Convert 3D FITS into a movie file.')
  parser.add_argument(
    'fits', type=str,
    help='source a FITS image.')
  parser.add_argument(
    'avi', type=str,
    help='converted a movie file.')
  parser.add_argument(
    '-f','--fps', dest='fps', type=float, default=24,
    help='frame rate of the movie')
  parser.add_argument(
    '-r', '--dpi', dest='dpi', type=float, default=200.,
    help='resolution of the movie')
  parser.add_argument(
    '-l','--limits', dest='limits', nargs=2, type=float,
    default=[None,None],
    help='(lower, upper) limits of coloamap. If not specified, the minimum and maximum values are assigned.')
  parser.add_argument(
    '--vflip', dest='vflip', action='store_true',
    help='vertically flip the movie')
  parser.add_argument(
    '--hflip', dest='hflip', action='store_true',
    help='horizontally flip the movie')

  args = parser.parse_args()

  hdu = fits.open(args.fits)
  img = hdu[0].data
  if len(img.shape)==4: img = img[0]
  nz = img.shape[0]
  sz = img[0].shape

  if args.hflip: img = img[:,:,::-1]
  if args.vflip: img = img[:,::-1,:]

  fig = plt.figure()
  fig.set_size_inches([sz[1]/args.dpi, sz[0]/args.dpi])

  ax = plt.Axes(fig,[0.,0.,1.,1.])
  ax.set_axis_off()
  fig.add_axes(ax)

  im = ax.imshow(np.zeros_like(img[0]),
                 cmap='gray', interpolation='nearest')
  im.set_clim([0,1])

  clim = args.limits
  if clim[0] is None: clim[0] = np.min(img)
  if clim[1] is None: clim[1] = np.max(img)

  def update_img(n):
    im.set_data(np.clip((img[n]-clim[0])/(clim[1]-clim[0]),0,1))
    return im

  avi = anim.FuncAnimation(fig, update_img, nz, interval=int(args.fps))
  writer = anim.writers['avconv'](fps=args.fps,codec='h264')

  avi.save(args.avi, writer=writer, dpi=int(args.dpi))
