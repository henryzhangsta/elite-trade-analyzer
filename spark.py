from pyspark import SparkContext, SparkConf, StorageLevel
from CSVLoader import CSVLoader
import re, os, uuid, datetime, json

if __name__ == '__main__':
    conf = SparkConf().setMaster('local[8]')
    sc = SparkContext(conf=conf)

    systems = CSVLoader('data/headers/System.hcsv').loadMap(sc, 'data/System.csv')
    stationCommodities = CSVLoader('data/headers/SC.hcsv').loadMap(sc, 'data/SC.csv')
    commodities = CSVLoader('data/headers/Commod.hcsv').loadMap(sc, 'data/Commod.csv')
