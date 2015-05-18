__author__ = 'simone.decristofaro'

import psycopg2
from psycopg2 import extras
import logging

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.DEBUG)

MAX_GEOMETRY_AREA = 25
QUERY_ON_WITHIN = "SELECT id,area FROM geographies where st_within(st_geomfromtext('POLYGON((%s))'), geometry) order by area limit 1"

QUERY_ON_OVERLAPS = "select *" \
                   ",t4.intersection_area_on_bbox_area*2+t4.bbox_area_on_geometry_area as rate" \
                   " from(" \
                   " select * from " \
                   "(" \
                   "select *" \
                   ",ST_Intersection(t2.bbox,t2.geometry) as intersection" \
                   ",st_area(ST_Intersection(t2.bbox,t2.geometry)) as intersection_area " \
                   ",st_area(ST_Intersection(t2.bbox,t2.geometry)) / st_area(t2.bbox) * 100 as intersection_area_on_bbox_area" \
                   ",st_area(t2.bbox)/st_area(t2.geometry)*100 as bbox_area_on_geometry_area" \
                   " from " \
                   "(" \
                   " select id,name,area as geometry_area,bbox,geometry from geographies," \
                   "(" \
                   " select " \
                   "st_geomfromtext('POLYGON((%s))') " \
                   "as bbox" \
                   ") as t1" \
                   " where ST_Overlaps(t1.bbox,geometry)" \
                   ") as t2 " \
                   ") as t3" \
                   ") as t4" \
                   " order by rate desc"


def buildPolygonFromPoints(bl, tr):
    """
    Args:
    bl is the bottomleft point (min_lon,min_lat)
    tr the the top right point (max_lon,max_lat)
    """

    return "%s %s,%s %s,%s %s,%s %s,%s %s" % (bl[0], bl[1],
                                              bl[0], tr[1],
                                              tr[0], tr[1],
                                              tr[0], bl[1],
                                              bl[0], bl[1])


def getGeoIdFromPolygon(polygon):
    conn = psycopg2.connect("dbname='inrix' user='postgres' host='172.16.3.171' password='postgres'")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        cur.execute(QUERY_ON_WITHIN % polygon)
    except Exception, e:
        log.exception("Can't load geoid from polygon ")
        return

    geoID = None
    area = None
    try:
        rows = cur.fetchall()
        if len(rows) > 0:
            area=rows[0]['area']
            if  area<= MAX_GEOMETRY_AREA:
                geoID = rows[0]['id']
                log.info("WITHIN QUERY SUCCESS: geoID = " + str(geoID) + "; area = " + str(area))
            else:
                log.warn("WITHIN QUERY FAILED: the inrix geometry " + str(rows[0]['id']) + " has an area of: " + str(
                    area) + ", grater than the limit: " + str(MAX_GEOMETRY_AREA) + ", ")
        if not geoID:
            cur.execute(QUERY_ON_OVERLAPS % polygon)
            rows = cur.fetchall()
            if len(rows) > 0:
                for r in rows:
                    area = r['geometry_area']
                    if area <= MAX_GEOMETRY_AREA:
                        geoID = r['id']
                        break
            if geoID:
                log.info("TOUCHES QUERY SUCCESS: geoID = " + str(geoID) + "; area = " + str(area))
            else:
                log.error("TOUCHES QUERY FAILED: No data found for given polygon")
                return

        return geoID
    except Exception, e:
        log.exception("No data found for given polygon")
        return


def getGeoId(bl, tr):
    polygon = buildPolygonFromPoints(bl, tr)
    return getGeoIdFromPolygon(polygon)


# When the Python interpreter reads a source file, it executes all of the code found in it. Before executing the code, it will define a few special
# variables. For example, if the python interpreter is running that module (the source file) as the main program, it sets the special __name__ variable to
# have a value "__main__". If this file is being imported from another module, __name__ will be set to the module's name.
if __name__ == "__main__":
    print getGeoId((-115.580838, 35.757702), (-114.211166, 36.614982))
