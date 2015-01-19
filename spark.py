from pyspark import SparkContext, SparkConf, StorageLevel
from CSVLoader import CSVLoader
import re, os, uuid, datetime, json, argparse, math

def Dedupe(a, b):
    return a

def DistanceBetweenSystems(a, b):
    return math.sqrt((a['SystemX'] - b['SystemX']) ** 2 + (a['SystemY'] - b['SystemY']) ** 2 + (a['SystemZ'] - b['SystemZ']) ** 2)

def Main(maxJumpDistance):
    conf = SparkConf().setMaster('local[8]')
    sc = SparkContext(conf=conf)

    systems = CSVLoader('data/headers/System.hcsv').loadMap(sc, 'data/System.csv')
    stationCommodities = CSVLoader('data/headers/SC.hcsv').loadMap(sc, 'data/SC.csv')
    commodities = CSVLoader('data/headers/Commod.hcsv').loadMap(sc, 'data/Commod.csv')

    def MapSystems(a):
        del a['SystemSize']
        del a['SystemId']
        a['SystemX'] = float(a['SystemX'])
        a['SystemY'] = float(a['SystemY'])
        a['SystemZ'] = float(a['SystemZ'])
        return a

    systems = systems.map(MapSystems)

    currentSystemName = 'Brani'
    currentSystem = systems.filter(lambda x: x['SystemName'] == currentSystemName).collect()[0]

    systemsWithStations = sc.broadcast(stationCommodities.map(lambda x: x['SCStationSystem']).distinct().collect())
    systems = systems.filter(lambda x: DistanceBetweenSystems(currentSystem, x) < 100).filter(lambda x: x['SystemName'] in systemsWithStations.value)

    systemPairs = systems.cartesian(systems).filter(lambda x: DistanceBetweenSystems(x[0], x[1]) < maxJumpDistance)

    def TokenizeSystem(systems):
        a = systems[0]['SystemName']
        b = systems[1]['SystemName']

        token = min(a, b) + '__' + max(a, b)

        return (token, systems)

    def ReduceSystemPair(x):
        return (x[0]['SystemName'], x[1]['SystemName'])

    systemPairs = systemPairs.map(TokenizeSystem).reduceByKey(Dedupe).map(lambda x: x[1]).map(ReduceSystemPair)

    inrangeSystems = sc.broadcast(systems.map(lambda x: x['SystemName']).distinct().collect())
    stationCommodities = stationCommodities.filter(lambda a: a['SCStationSystem'] in inrangeSystems.value)

    def StationCommodityMap(a):
        return (a['SCStationSystem'], {
            'Station': a['SCStationName'],
            'Commodity': a['SCStationCommod'],
            'BuyPrice': int(a['SCStationPrice']),
            'SellPrice': int(a['SCStationSell']),
            'Stock': int(float(a['SCStationStock']))
        })

    def StationMap(a):
        results = {}
        for stationcommod in a[1]:
            if stationcommod['Station'] in results:
                results[stationcommod['Station']].append(stationcommod)
            else:
                results[stationcommod['Station']] = [stationcommod]

        return (a[0], results)

    stationCommoditiesTable = {system[0]: system[1] for system in stationCommodities.map(StationCommodityMap).groupByKey().map(StationMap).collect()}
    stationCommoditiesTable = sc.broadcast(stationCommoditiesTable)

    def MapSystemPairToSystems(pair):
        return ({
                'Name': pair[0],
                'Stations': stationCommoditiesTable.value[pair[0]]
            },
            {
                'Name': pair[1],
                'Stations': stationCommoditiesTable.value[pair[1]]
            })
    

    systemPairs = systemPairs.map(MapSystemPairToSystems)

    def GetStationPairs(syspair):
        origin_sys = syspair[0]['Stations']
        dest_sys = syspair[1]['Stations']

        station_pairs = []

        for origin_station, origin_commods in origin_sys.iteritems():
            for dest_station, dest_commods in dest_sys.iteritems():
                station_pairs.append(((origin_station, origin_commods), (dest_station, dest_commods)))

        return station_pairs

    def BestCommodityTrade(sellingCommodities, buyingCommodities):
        a_max_profit = 0
        a_max_price = 0
        a_max_profit_commodity = None

        for k, v in sellingCommodities.iteritems():
            profit = buyingCommodities[k]['SellPrice'] - v['BuyPrice']
            if profit > a_max_profit or (profit == a_max_profit and v['BuyPrice'] < a_max_price):
                a_max_profit = profit
                a_max_price = v['BuyPrice']
                a_max_profit_commodity = k

        return {
            'Profit': a_max_profit,
            'BuyPrice': a_max_price,
            'Commodity': a_max_profit_commodity
        } if a_max_profit_commodity != None else None

    def BestSystemRoute(pair):
        station_pairs = GetStationPairs(pair)
        origin_sys = pair[0]['Name']
        dest_sys = pair[1]['Name']

        trade_pairs = []

        for stations in station_pairs:
            station_a_commodities = {a['Commodity']: a for a in stations[0][1]}
            station_b_commodities = {a['Commodity']: a for a in stations[1][1]}
            common_commodities = set(station_a_commodities.keys()).intersection(station_b_commodities.keys())

            station_a_sold = {k: station_a_commodities[k] for k in common_commodities if station_a_commodities[k]['BuyPrice'] > 0 and station_a_commodities[k]['Stock'] > 0}
            station_b_sold = {k: station_b_commodities[k] for k in common_commodities if station_b_commodities[k]['BuyPrice'] > 0 and station_b_commodities[k]['Stock'] > 0}

            station_a_trade = BestCommodityTrade(station_a_sold, station_b_commodities)
            station_b_trade = BestCommodityTrade(station_b_sold, station_a_commodities)

            if station_a_trade != None and station_b_trade != None:
                trade_pairs.append(({
                    'System': origin_sys,
                    'Station': stations[0][0],
                    'Trade': station_a_trade
                }, {
                    'System': dest_sys,
                    'Station': stations[1][0],
                    'Trade': station_b_trade
                }))

        if len(trade_pairs) > 0:
            max_profit = 0
            best_trade = None
            for pair in trade_pairs:
                total_profit = pair[0]['Trade']['Profit'] + pair[1]['Trade']['Profit']
                if total_profit > max_profit:
                    max_profit = total_profit
                    best_trade = pair

            return {
                'Trade': best_trade,
                'Profit': max_profit
            }
        else:
            return None

    routes = systemPairs.map(BestSystemRoute).filter(lambda a: a != None).map(lambda x: (x['Profit'], x)).sortByKey().map(lambda x: x[1]).collect()
    print routes

    #print stationCommodities.collect()
    #print commodities.collect()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Determine best trade routes between locations')
    parser.add_argument('maxjumpdistance', type=int, help='Maximum single jump distance', nargs='?', default=30)

    args = parser.parse_args()
    Main(args.maxjumpdistance)