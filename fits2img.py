#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (print_function, absolute_import)

from matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits

from argparse import ArgumentParser as ap

if __name__ == '__main__':
  parser = ap(description='Convert a 2D FITS into a movie file.')
  parser.add_argument(
    'fits', type=str,
    help='a source FITS image.')
  parser.add_argument(
    'img', type=str,
    help='a converted image file.')
  parser.add_argument(
    '-r', '--dpi', dest='dpi', type=float, default=200.,
    help='resolution of the image')
  parser.add_argument(
    '-l','--limits', dest='limits', nargs=2, type=float,
    default=[None,None],
    help='(lower, upper) limits of coloamap. If not specified, the minimum and maximum values are assigned.')
  parser.add_argument(
    '-z', '--zrange', dest='zr', action='store_true',
    help='limits are automatically calculated. This override the "-l" option.')
  parser.add_argument(
    '--vflip', dest='vflip', action='store_true',
    help='vertically flip the image')
  parser.add_argument(
    '--hflip', dest='hflip', action='store_true',
    help='horizontally flip the image')

  args = parser.parse_args()

  hdu = fits.open(args.fits)
  img = hdu[0].data
  if len(img.shape)==4: img = img[0]
  if len(img.shape)==3: img = img[0]
  nx,ny = img[0].shape

  if args.hflip: img = img[:,::-1]
  if args.vflip: img = img[::-1,:]

  cmap = plt.cm.hot
  clim = args.limits
  if clim[0] is None: clim[0] = np.min(img)
  if clim[1] is None: clim[1] = np.max(img)
  if args.zr is True:
    med = np.median(img)
    std = np.std(img[img>0])
    clim[0] = med - std
    clim[1] = med + 3*std

  imdata = cmap(plt.Normalize(vmin=clim[0], vmax=clim[1])(img))
  plt.imsave(args.img, imdata)
