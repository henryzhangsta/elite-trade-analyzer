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

Note on Spark
-------------

This is a Spark program, and thus requires Spark. Tips to simplify installation are listed below.

Linux
-----

It is recommended that you download Apache Spark from Cloudera's repositories. Instructions can be found at [http://www.cloudera.com/content/cloudera/en/documentation/core/latest/topics/cdh_ig_spark_install.html]

Mac
---

It is recommended to download the `apache-spark` package from Homebrew.

Windows
-------

Manual installation is required.
Locations listed here are used for simplicity and completely optional. You can use your prefered locations.

Download the Pre-Built Spark for Hadoop 2.4+ from [https://spark.apache.org/downloads.html]. Extract it to "C:\spark". Download Hadoop from [https://www.apache.org/dyn/closer.cgi/hadoop/common/] and extract it to "C:\hadoop". It is also necessary to get the Windows runtimes, which can be downloaded here [http://www.srccodes.com/p/article/39/error-util-shell-failed-locate-winutils-binary-hadoop-binary-path]. Unpack them and copy to "C:\hadoop\bin". Overwrite only older files. Before running Spark, you must set the `%HADOOP_HOME%` environment variable to point at "C:\hadoop". Also add "C:\spark\bin" and "C:\hadoop\bin" to `%Path%` environment variable.

Usage
-----

1. Download current market data. This can be done by exporting the ED4.db file from Slopey's BPC tool using a SQLLite editor to CSV format. The tables required are Commod, SC, and System. Place these files in data/csv. Alternatively, run DownloadEDDB.sh to get the necessary data files from EDDB.io, and run ConvertEDDBToCSV.py to convert them into usable format.
2. Run `spark-submit spark.py` to generate the routes. The results will be displayed in JSON format at the end of the output.
