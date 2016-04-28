import datetime
import json

gid = "1285"

with open('gas_car_trip') as fgas_car_trip:    
    gas_car_trip = json.load(fgas_car_trip)
gas_car_trip[gid] = {}
cars = ["221", "1389", "5390", "1890", "313", "2056", "433",
        "311", "460", "312", "1797", "1889", "323", "5753"]
gas_station = {"lat": 55.8115, "lng": 37.6901}
#trip_car_f = open('point_trip_result/trip_car', 'a')
for cid in cars:
    gas_car_trip_tmp = []
    times = {}
    try:
        f = open('../cars/' + cid + '.txt')
        # f = open('cars_in_gas/' + cid + '.txt')
    except IOError:
        print '!!!' + cid
        continue
    empty = False
    for i in xrange(0, 999000):
    # for i in xrange(0, 3):
        line = f.readline()
        line = line.strip()
        if not line:
            if empty:
                break
            else:
                empty = True
                continue
        else:
            empty = False
        data = line.split()
        try:
            int(line[0])
        except ValueError:
            continue
        d1 = datetime.datetime.strptime(data[2] + data[3][0:5], "%Y-%m-%d%H:%M")
        times[d1] = line
    f.close()

    empty = False
    f_trip = open('1/' + cid + '.txt')
    # for i in xrange(3):
    for i in xrange(9999999):
        line = f_trip.readline()
        line = line.strip()
        if not line:
            if empty:
                break
            else:
                empty = True
                continue
        else:
            empty = False
        data = line.split()
        try:
            int(line[0])
        except ValueError:
            continue
        # open_flag = False
        d1 = datetime.datetime.strptime(data[2] + data[3][0:5], "%Y-%m-%d%H:%M")
        d2 = datetime.datetime.strptime(data[4] + data[5][0:5], "%Y-%m-%d%H:%M")
        flag_write = False
        buffer_trip = []
        for t in times:
            if d1 <= t and t <= d2:
                # if not open_flag:
                    # open_flag = True
                poi = times[t]
                buffer_trip.append(poi)
                poi_data = poi.split()
                lat = poi_data[4].split(',')
                lat = '.'.join(lat)
                lng = poi_data[5].split(',')
                lng = '.'.join(lng)
                tmp = {'lat': round(float(lat), 4),
                       'lng': round(float(lng), 4)}
                if tmp == gas_station:
                    flag_write = True
        if flag_write:
            gas_car_trip_tmp.append(data[0])
################################################
            trip_points_f = open('trips_point/' + data[0], 'w')
            for r in buffer_trip:
                trip_points_f.write(r + '\n')
            trip_points_f.close()
################################################
    f_trip.close()
    if gas_car_trip_tmp:
        gas_car_trip[gid][cid] = gas_car_trip_tmp

fgas_car_trip = open('gas_car_trip', 'w')
gas_car_trip = json.dumps(gas_car_trip)
fgas_car_trip.write(gas_car_trip)
fgas_car_trip.close()
