import json
import csv

def WriteCommodities(commodities):
    with open('data/csv/Commod.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for commodity in commodities:
            writer.writerow([commodity['name'], commodity['category']['name'], commodity['average_price']])

def WriteSystems(systems):
    with open('data/csv/System.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for system in systems:
            if len(system['stations']) > 0:
                writer.writerow([system['id'], system['name'], system['x'], system['y'], system['z'], ''])

def WriteStations(stations, systems_lookup, commodity_lookup):
    with open('data/csv/SC.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for station in stations:
            station_id = station['id']
            station_name = station['name']
            station_orbital_dist = station['distance_to_star']
            station_system_id = station['system_id']
            station_system_name = systems_lookup[station_system_id]

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

    WriteCommodities(commodities)
    WriteSystems(systems)

    commodity_lookup = {commodity['id']: commodity for commodity in commodities}
    systems_lookup = {system['id']: system['name'] for system in systems}

    WriteStations(stations, systems_lookup, commodity_lookup)