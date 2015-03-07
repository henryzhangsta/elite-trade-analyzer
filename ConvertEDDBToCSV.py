import json
import csv

def WriteSystems(systems, stations):
    systems_with_station = {x['system_id'] for x in stations}

    with open('data/csv/System.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for system in systems:
            if system['id'] in systems_with_station:
                writer.writerow([system['id'], system['name'], system['x'], system['y'], system['z'], ''])

def WriteStations(stations, systems_lookup, commodity_lookup):
    with open('data/csv/SC.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for station in stations:
            station_name = station['name']
            
            station_system_name = systems_lookup[station['system_id']]

            for listing in station['listings']:
                commodity = commodity_lookup[listing['commodity_id']]

                writer.writerow([
                    listing['id'],
                    station_system_name,
                    '',
                    station_name,
                    commodity['category']['name'],
                    commodity['name'],
                    commodity['average_price'],
                    listing['buy_price'],
                    listing['sell_price'],
                    '',
                    listing['demand'],
                    '',
                    listing['supply'],
                    '',
                    listing['supply'],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ''
                    ])

# SCId,SCStationSystem,SCStationLocal,SCStationName,SCStationCommodGroup,SCStationCommod,SCStationCommodAvg,
# SCStationPrice,SCStationSell,SCStationFence,SCStationDemand,SCStationDemandCode,SCStationSupply,SCStationSupplyCode,
# SCStationStock,SCStationIllegal,SCStationConsumer,SCStationProducer,SCStationLastUpdate,SCStationForSale,
# S1,S2,S3,S4,N1,N2,N3,N4,B1,B2,SCUNIQUE


if __name__ == '__main__':
    commodities = json.loads(open('data/commodities.json', 'r').read())
    stations = json.loads(open('data/stations.json', 'r').read())
    systems = json.loads(open('data/systems.json', 'r').read())

    WriteSystems(systems, stations)

    commodity_lookup = {commodity['id']: commodity for commodity in commodities}
    systems_lookup = {system['id']: system['name'] for system in systems}

    WriteStations(stations, systems_lookup, commodity_lookup)