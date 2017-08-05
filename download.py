# -------------------------------------------------------------------
# - NAME:        download.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2017-08-04
# -------------------------------------------------------------------
# - DESCRIPTION:
# -------------------------------------------------------------------
# - EDITORIAL:   2017-08-04, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2017-08-05 10:13 on thinkreto
# -------------------------------------------------------------------

import logging
logging.basicConfig(format="# %(levelname)s %(message)s",level=logging.DEBUG)
log = logging.getLogger()

# -------------------------------------------------------------------
# Main part of the script
# -------------------------------------------------------------------
if __name__ == "__main__":

   # ----------------------------------------------------------------
   # Requires one single input argument
   # ----------------------------------------------------------------
   import argparse, sys, os
   helptext = """
   This is the python package for downloading GFS reforecast V2 grib
   file data from the NOAA CDC data server. This script is used to
   download pre-specified sets of data wherefore a config file has
   to be given!"""

   parser = argparse.ArgumentParser(description=helptext)
   parser.add_argument("-c","--config", default=None,
         help="String, config file which has to be read.")
   args = parser.parse_args()
   if args.config is None:
      parser.print_help(); sys.exit(1)
   else:
      if not os.path.isfile( args.config ):
         log.error("Sorry, cannot find file \"{:s}\". Please check if file exists.")
         sys.exit(1)
   

   # ----------------------------------------------------------------
   # Read config file now
   # ----------------------------------------------------------------
   import datetime as dt
   from GFSV2 import *

   # Read confg file
   config = readConfig( args.config )

   # Looping over dates
   loopdate = config.main_from
   while loopdate <= config.main_to:

      # Check whether we have to download this file or not
      loopdate_mon = int(loopdate.strftime("%m"))
      if not config.main_only is None:
         if not loopdate_mon == config.main_only:
            # Increase loopdate and continue
            loopdate = loopdate + dt.timedelta(1)
            continue

      # Proccessing
      log.info("Processing date {:s}".format(loopdate.strftime("%Y-%m-%d %HZ")))

      download( config, loopdate )

      # Increase date
      loopdate = loopdate + dt.timedelta(1)

