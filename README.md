Elite Trade Analyzer
====================

This tool will analyze and find the best routes for trade data persuant to several parameters:

+ Proximity to current location
+ Distance between trade stations
+ Current commodity prices and supplies

Requirements
------------

+ Apache Spark 1.2.0
+ Python 2.7+
+ Data source (EDDB and Slopey's BPC are currently supported)

Usage
-----

1. Download current market data. This can be done by exporting the ED4.db file from Slopey's BPC tool using a SQLLite editor to CSV format. The tables required are Commod, SC, and System. Place these files in data/csv. Alternatively, run DownloadEDDB.sh to get the necessary data files from EDDB.io, and run ConvertEDDBToCSV.py to convert them into usable format.
2. Run `spark-submit spark.py` to generate the routes. The results will be displayed in JSON format at the end of the output.
