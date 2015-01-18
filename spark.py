from pyspark import SparkContext, SparkConf, StorageLevel
from CSVLoader import CSVLoader
import re, os, uuid, datetime, json

if __name__ == '__main__':
    conf = SparkConf().setMaster('local[8]')
    sc = SparkContext(conf=conf)

    systems = CSVLoader('data/headers/System.hcsv').loadMap()
    stationCommodities = CSVLoader('data/headers/SC.hcsv').loadMap()
    commodities = CSVLoader('data/headers/Commod.hcsv').loadMap()
