# -*- coding: utf-8 -*-
import math
import random
import datetime


class KCluster(object):
    def __init__(self, data, k):
        self.rotatematrix(data)
        self.k = k

    def rotatematrix(self, data):
        self.data = []
        for i in xrange(len(data[0])):
            newrow = [data[j][i] for j in range(len(data))]
            self.data.append(newrow)

    def get_distance(self, v1, v2):
        d = 0.0
        for i in xrange(len(v1)):
            d += (v1[i] - v2[i]) ** 2
        return math.sqrt(d)

    def clustering(self):
        ranges = [(min([row[i] for row in self.data]),
                   max([row[i] for row in self.data])) for i in
                  xrange(len(self.data[0]))]

        clusters = [[(random.random() *
                      (ranges[i][1] - ranges[i][0]) +
                      ranges[i][0]) for i in xrange(len(self.data[0]))]
                    for j in xrange(self.k)]
        lastmatches = None
        for t in xrange(100):
            bestmatches = [[] for i in xrange(self.k)]
            for j in range(len(self.data)):
                row = self.data[j]
                bestmatch = 0
                for i in xrange(self.k):
                    d = self.get_distance(clusters[i], row)
                    if d < self.get_distance(clusters[bestmatch], row):
                        bestmatch = i
                bestmatches[bestmatch].append(j)
            if bestmatches == lastmatches:
                break
            lastmatches = bestmatches
            for i in xrange(self.k):
                avgs = [0.0] * len(self.data[0])
                if len(bestmatches[i]) > 0:
                    for rowid in bestmatches[i]:
                        for m in xrange(len(self.data[rowid])):
                            avgs[m] += self.data[rowid][m]
                    for j in xrange(len(avgs)):
                        avgs[j] /= len(bestmatches[i])
                    clusters[i] = avgs
        # clusters = []
        # bestmatches = []
        # already_in = []
        # for i in range(len(self.data)):
        #     cl = self.data[i]
        #     tmp = [round(cl[0], 4), round(cl[1], 4)]
        #     tmp_best = []
        #     for j in range(i + 1, len(self.data)):
        #         cl2 = self.data[j]
        #         tmp2 = [round(cl2[0], 4), round(cl2[1], 4)]
        #         if tmp == tmp2:
        #             if j not in already_in:
        #                 already_in.append(j)
        #                 tmp_best.append(j)
        #                 self.data[j] = self.data[i]
        #     clusters.append(self.data[i])
        #     if tmp_best:
        #         bestmatches.append(tmp_best)
        #     else:
        #         bestmatches.append([i])
        # print clusters

        return clusters, bestmatches


def read_data():
    rownames = ['lon', 'lat']
    colnames = []
    arrlon = []
    arrlat = []
    ftrips = open('trips')
    trip_count = ftrips.readline().strip()
    trip_ids = []
    for i in xrange(int(trip_count)):
        trip_id = ftrips.readline().strip()
        trip_ids.append(trip_id)
        f = open('trips_point/' + trip_id)
        for i in xrange(0, 100):
            line = f.readline()
            line = line.strip()
            if not line:
                break
            line_sp = line.split()
            lat = line_sp[4].split(',')
            lat = '.'.join(lat)
            lng = line_sp[5].split(',')
            lng = '.'.join(lng)
            arrlon.append(float(lng))
            arrlat.append(float(lat))
            colnames.append(trip_id + ' ' + line_sp[2] + ' ' + line_sp[3])
    ftrips.close()
    data = [arrlon,
            arrlat]
    return colnames, rownames, data, trip_ids


point_info, lon_lat, data, trip_ids = read_data()
gid = "1285"
# gid = "372"
# gid = "688"

k = 50
centroids, kclust = KCluster(data, k).clustering()
result = {}
diff = 0
f = open('k_means_result.txt', 'w')
fcentroids = open('centroids.txt', 'w')

fcentroidsall = open('centroids/' + gid + '.txt', 'w')

for i in xrange(k):
    trips = {}
    if not kclust[i]:
        diff += 1
        continue
    f.write(str(i - diff) + '\n')

    for cl in kclust[i]:
        f.write(point_info[cl])
        f.write('\n')
        line = point_info[cl].split()
        d1 = datetime.datetime.strptime(line[1] + line[2][0:5],
                                        "%Y-%m-%d%H:%M")
        trips[line[0]] = d1
    fcentroidsall.write(str(centroids[i][0]) + ' ' +
                        str(centroids[i][1]) + '\n')
    fcentroids.write(str(centroids[i][0]) + ' ' + str(centroids[i][1]) + '\n')
    result[str(i - diff)] = {'point': centroids[i],
                             'trip': trips}
f.close()
fcentroids.close()
fcentroidsall.close()
k -= diff
matrix = []
newmatrix = []
for a in xrange(0, k):
    matrix.append([0 for i in range(0, k)])
    newmatrix.append([0 for i in range(0, k)])

for tid in trip_ids:
    tmp = {}
    for i in xrange(k):
        if tid in result[str(i)]['trip']:
            tmp[result[str(i)]['trip'][tid]] = str(i)
    ittmp = sorted(tmp.items())
    for i in xrange(len(ittmp) - 1):
        matrix[int(ittmp[i][1])][int(ittmp[i + 1][1])] += 1

# for i in xrange(k):
#     if sum(matrix[i]) == 0:
#         check = True
#         for j in xrange(k):
#            if matrix[j][i] != 0:
#             check = False
#         if check:
#             print 'TRUE!'
max_el = 0
max_el2 = 0
ind = [0, 0]
# count = 0
# groups = []
for i in xrange(0, k):
    for j in xrange(0, k):
        el = matrix[i][j]
        if el > max_el:
            max_el = el
            max_el2 = el
            ind = [i, j]
print k

for j in xrange(k):
    tmpcount = 0.0
    for i in xrange(k):
        tmpcount += float(matrix[i][j])
    if tmpcount == 0.0:
        tmpcount = 1.0
    for i in xrange(k):
        newmatrix[i][j] = matrix[i][j]/tmpcount

newmatrix[ind[0]][ind[1]] = 2.0

matrix[ind[0]][ind[1]] = 0
# matrix[ind[0]] = [0 for i in xrange(k)]
# for i in xrange(k):
#     matrix[i][ind[1]] = 0


path = [ind[0], ind[1]]
i = ind[1]
while(max_el):
    max_el = 0
    nj = 0
    count = float(sum(matrix[i]))
    if count != 0:
        # count = 1.0
        for j in xrange(0, k):
            if j not in path:
                el = matrix[i][j]
                # newmatrix[i][j] = el/count
                if el > max_el:
                    max_el = el
                    nj = j
        if max_el:
            matrix[i][nj] = 0
            path.append(nj)
            i = nj
#################################
# v druguyu storonu
max_el = max_el2
npath = []
j = ind[0]
while(max_el):
    max_el = 0
    ni = 0
    count = 0
    for i in xrange(0, k): 
        count += float(matrix[i][j])
    print count
    if count != 0:
        # count = 1.0
        for i in xrange(0, k):
            if i not in path:
                el = matrix[i][j]
                # newmatrix[i][j] = el / count
                if el > max_el:
                    max_el = el
                    ni = i
        if max_el:
            matrix[ni][j] = 0
            npath.append(ni)
            j = ni
path = npath[::-1] + path
#######################
print path

fmatr = open('matrixs/' + gid + '.txt', 'w')
for i in xrange(0, k):
    fmatr.write(' '.join([str(j) for j in newmatrix[i]]) + '\n')
fmatr.close()


fgraph = open('graphs/' + gid + '.txt', 'w')
for p in path:
    fgraph.write(str(result[str(p)]['point'][0]) + ' ' +
                 str(result[str(p)]['point'][1]) + '\n')
fgraph.close()
