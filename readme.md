# How to make the masks

## Prep the data

- Put the PNGs of the sources you want to measure in a directory.
- Put the corresponding fits files in a sub-directory named *fits*.
- Create a sub-directory named *masks*.

The naming scheme should be *object_id*.png, fits/*object_id*_g.fits, fits/*object_id*_r.fits, etc.

## Run the macro in ImageJ

- Install and run ImageJ.
- From the menu, select plugins, edit, and choose savemask.ijm
- Edit the path in the file to point to your images
- Optionally, edit the zoom level
- Install the macro - Macros/install macro from the menu, or *ctrl-i*.

The macro installs some key commands:

- "a" - loads the file list, initializes the process
- "w" - prints the first file (a sanity check)
- "z" - load the next image
- "q" - save the mask 

When the image is loaded, use any of the ImageJ tools (rectangle, oval, polygon) to draw the mask. When done, hit 'q'.

# How to do the photometry

- Repeat the process to make separate masks for the lens and source if required (rename the masks directory in between)
- Run *mags.py*, as follows: `python mags.py directory_name`

Where *directory_name* is the directory containing the pngs. The output will appear in a file called `mags.csv` in that directory.

If the sub-directories masks_lens and mask_source are present, then it will include both; otherwise, just the mags for the single masks directory will be present.

