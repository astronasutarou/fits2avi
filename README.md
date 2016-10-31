# FITS2AVI
This provides a Python script to convert a 3D FITS cube file into a movie.

In a certain region, a 3D FITS cube file contains a set of sequential images,
which is usually recognized as a movie. This script convert the FITS cube into
a movie encoded with the `H.264` codec.

## How to Install
Create a symbolic link in `/usr/local/bin/`.

~~~sh
sudo ln -s ${PWD}/fits2avi.py /usr/local/bin/fits2avi
~~~


## Usage
`fits2avi` requires, at least, two arguments: The first argument is the name
of the FITS cube file; The second argument is the name of the output movie.

~~~sh
fits2avi source.fits output.avi
~~~

`fits2avi` accepts several options as follows:

- `-f`, `--fps`:
    specify the frame per second of the movie.
- `r`, `--dpi`:
    specify the resolution (dpi) of the movie.
- `-l`, `--limits`:
    specify the lower and upper limits of colormap. If this option is not
    specified, the minimum and maximum values of the FITS data are assigned.
- `--vflip`:
    vertically flip the movie.
- `--hflip`:
    horizontally flip the movie.


## Dependence
This script depends on `matplotlib`, `numpy`, `pyfits`, and `argparse`.
