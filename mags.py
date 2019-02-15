from PIL import Image
import astropy.io.fits as pyfits
from astropy.coordinates import SkyCoord
import glob
import numpy as np
import sys
import os

FLIPUD = True # Important: PNGs are inverted from fits

hdu = 0
bands_des = "griz"
magzps_des = [30, 30, 30, 30]
bands_cfhtls = "ugriz"
pixel_scale = .263  # DES
scale = 4
bands = bands_des

def main(args):
    indir = args[0]
    doboth = False
    mags = {}
    outputfile = "mags.csv"

    if not os.path.isdir(indir):
        print("Directory %s not found.")
        sys.exit(0)
    if os.path.exists(indir + "/masks_lens") and os.path.exists(indir + "/masks_source"):
        doboth = True
    else:
        if not os.path.exists(indir + "/masks"):
            print("Masks directory not found.")
            sys.exit(0)

    if doboth:
        columns = ["lens", "source"]
        mags['lens'] = getmags(indir, masksdir="masks_lens")
        mags['source'] = getmags(indir, masksdir="masks_source")
    else:
        columns = ["mag"]
        mags['mag'] = getmags(indir, masksdir="masks")

    # output
    with open(indir + "/" + outputfile, "w") as f:
        f.write("objid,")
        for column in columns:
            f.write(",".join(
                [b + "_mag_" + column for b in bands])
            )
            f.write(",")
            f.write(",".join(
                [b + "_sb_" + column for b in bands]) 
            )
            if column != columns[-1]:
                f.write(",")
        f.write("\n")

        objids = list(mags[columns[0]].keys())
        for obj in objids:
            line = ""
            f.write("%s," % obj)
            for column in columns:
                for band in bands:
                    line += "%.2f," % mags[column][obj][0][band]
                for band in bands:
                    line += "%.2f," % mags[column][obj][1][band]
            f.write(line[:-1] + "\n")

def getmags(indir, bands=bands, masksdir="masks"):
    output_mags = {}
    mask_files = glob.glob(indir + "/" + masksdir + "/*.bmp")
    for mask in mask_files:
        objid = mask.replace("-mask", "").split(".")[0].split("/")[-1]
        mask = np.array(Image.open(mask))
        mask = mask / 255.
        if FLIPUD:
            mask = np.flipud(mask)
        fits_files = glob.glob(indir + "/fits/*" + objid + "*.fits")
        mags = {}
        sb = {}
        for band in bands:
            mags[band] = 99
            ff = [f for f in fits_files if "_" + band + "." in f]
            if len(ff) != 1:
                print("No FITS files found for " + objid)
                break
            hdulist = pyfits.open(ff[0])
            data = hdulist[hdu].data
            try:
                masked = data * mask
            except Error as e:
                # print(e)
                continue

            magzp = None
            header = hdulist[hdu].header
            if "MAGZP" in header:
                magzp = float(hdulist[hdu].header['MAGZP'])
            elif "MAGZERO" in header:
                magzp = float(hdulist[hdu].header['MAGZERO'])
            if magzp is None:
                magzp = 30
                print("Warning: No zero point found, using default")
            mag = -2.5 * np.log10(masked.sum()) + magzp
            mags[band] = mag

            A = mask.sum() * pixel_scale**2
            surf_bri = mag + 2.5 * np.log10(A)  # flux_pixel * (1./pixel_scale)**2
            sb[band] = surf_bri

        output_mags[objid] = (mags, sb)

    return output_mags


if __name__ == "__main__":
    main(sys.argv[1:])
