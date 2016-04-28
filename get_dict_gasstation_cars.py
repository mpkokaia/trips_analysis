# -*- coding: utf-8 -*-
import json
gas_station = {}
old_gas_st = []
id_gas = 0
with open('../gas_station') as f:
    for i in xrange(10000):
        line = f.readline()
        if not line:
            break
        jsline = json.loads(line)
        jsline['lng'] = round(jsline['lng'], 4)
        jsline['lat'] = round(jsline['lat'], 4)
        old_gas_st.append(jsline)
        gas_station[str(id_gas)] = jsline
        id_gas += 1
f.closed
gas_file = open('gas_station', 'w')
gas_file.write(json.dumps(gas_station))
gas_file.close()
cf = open('../foo.txt')

coor = []
result = {}

for j in xrange(0, 1460):
    print j
    already = False
    cid = cf.readline().strip()
    if not cid:
        break
    latitudes = []
    longitudes = []
    try:
        f = open('../cars/' + cid + '.txt')
    except IOError:
        continue
    empty = False
    for i in xrange(0, 999000):
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
        lat = data[4].split(',')
        lat = '.'.join(lat)
        lng = data[5].split(',')
        lng = '.'.join(lng)
        tmp = {'lat': round(float(lat), 4),
               'lng': round(float(lng), 4)}
        if tmp in old_gas_st:
            for gas_id in gas_station:
                if tmp == gas_station[gas_id]:
                    if gas_id in result:
                        if cid not in result[gas_id]:
                            result[gas_id].append(cid)
                    else:
                        result[gas_id] = [cid]
    f.close()
cf.close()
gas_filer = open('result', 'w')
gas_filer.write(json.dumps(result))
gas_filer.close()
