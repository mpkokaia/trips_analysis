from bottle import route, run, template
import datetime


@route('/hello')
def hello():
    coor = []
    ftrips = open('trips')
    for i in range(22):
        trip_id = ftrips.readline().strip()
        f = open('trips_point/' + trip_id)
        tmp = {}
        tmpcoor = []
        for i in range(0, 100):
            line = f.readline()
            line = line.strip()
            if not line:
                break
            line_sp = line.split()
            lat = line_sp[4].split(',')
            lat = '.'.join(lat)
            lng = line_sp[5].split(',')
            lng = '.'.join(lng)
            d1 = datetime.datetime.strptime(line_sp[2] +
                                            line_sp[3][0:5], "%Y-%m-%d%H:%M")
            tmp[d1] = [float(lat), float(lng)]
        tmpi = sorted(tmp.items())
        for j in range(len(tmpi) - 1):
            tmpcoor.append([[tmpi[j][1][0], tmpi[j][1][1]],
                            [tmpi[j + 1][1][0], tmpi[j + 1][1][1]]])
        coor.append(tmpcoor)
        f.close()
    ftrips.close()
    f = open('../centroids.txt')
    point = []
    for i in range(300):
        line = f.readline()
        if not line:
            break
        line_sp = line.split()
        lat = line_sp[0].split(',')
        lat = '.'.join(lat)
        lng = line_sp[1].split(',')
        lng = '.'.join(lng)
        point.append([float(lng), float(lat)])
    f.close()
    f = open('../graph.txt')
    tmp = []
    for i in range(300):
        line = f.readline()
        if not line:
            break
        line_sp = line.split()
        lat = line_sp[0]
        lng = line_sp[1]
        tmp.append([float(lng), float(lat)])
    f.close()
    graph = []
    for j in range(len(tmp) - 2):
        graph.append([[tmp[j], tmp[j + 1]]])
    return template('1.html', coordinates=coor, point=point, graph=graph)
run(host='localhost', port=8080, debug=True)
