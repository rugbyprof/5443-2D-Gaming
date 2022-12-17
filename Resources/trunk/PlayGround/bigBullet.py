# This code calculates
# 1. Time taken by a projectile,
# 2. location where it impacts with ground/ship
# 3. angle of impact
# 4. joules of energy it carries at impact

import math
import random
import json
import sys, os
from rich import print
from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
import numpy as np
from time import sleep

sys.path.append("..")
from module import DBQuery

ENERGY_TO_MASS_RATIO = 5
LLPRECISION = 8
PRECISION = 3

DATAFOLDER = "/root/battleship/api/module/data/"
HOMEFOLDER = "/root/battleship/api/"
DISTANCECAP = 40

conn = DBQuery(os.path.join(DATAFOLDER, "mq_config.json"))


def error(e):
    print(e)
    sys.exit()


def deg2rad(theta):
    return np.divide(np.dot(theta, np.pi), np.float32(180.0))


def rad2deg(theta):
    return np.divide(np.dot(theta, np.float32(180.0)), np.pi)


def projectPoint(lng, lat, theta, distance, kilometers=True):
    """
    Displace a LatLng theta degrees counterclockwise and some
    meters in that direction.
    Notes:
        http://www.movable-type.co.uk/scripts/latlong.html
        0 DEGREES IS THE VERTICAL Y AXIS! IMPORTANT!
    Args:
        theta:    A number in degrees.
        distance: A number in meters.
    Returns:
        A new LatLng.
    """
    theta = np.float32(theta)

    units = 6371
    if not kilometers:
        units = 3959

    delta = np.divide(np.float32(distance), np.float32(units))

    theta = deg2rad(theta)
    lat1 = deg2rad(lat)
    lng1 = deg2rad(lng)

    lat2 = np.arcsin(
        np.sin(lat1) * np.cos(delta) + np.cos(lat1) * np.sin(delta) * np.cos(theta)
    )

    lng2 = lng1 + np.arctan2(
        np.sin(theta) * np.sin(delta) * np.cos(lat1),
        np.cos(delta) - np.sin(lat1) * np.sin(lat2),
    )

    lng2 = (lng2 + 3 * np.pi) % (2 * np.pi) - np.pi

    return [rad2deg(lng2), rad2deg(lat2)]


class BigBullet:
    def __init__(
        self,
        mps,
        bearing,
        lonA,
        latA,
        altitude,
        elevation,
        payload_mass,
    ):
        """
        Calculates where a BigBullet will land and how much energy created with proper inputs.
        Params:
            mps (float) : meters per second
            bearing (float): degree in which the gun points
            lonA (float): starting longitude of gun
            latA (float): starting latitude of gun
            altitude (float): altitude of gun (usually 10m on ship deck)
            elevation (float): the barrels vertical angle from -1 degrees to 45 degrees
            payload_mass (float): weight of BigBullet in kg
        """
        self.mps = 50 * round(float(mps) / 50.0)
        # if self.mps < 970 or self.mps > 1055:
        #     error({"Error": "MPS is out of range."})

        self.bearing = math.radians(bearing)
        if self.bearing < 0 or self.bearing > 360:
            error({"Error": "Gun bearing is not between 0 and 360 inclusive."})

        self.lonA = lonA
        if self.lonA < -179 or self.lonA > 179:
            error({"Error": "Gun latitude is not in range -179 to 179."})

        self.latA = latA
        if self.latA < -89 or self.latA > 89:
            error({"Error": "Gun latitude is not in range -89 to 89."})

        self.altitude = altitude
        if self.altitude < 0 or self.altitude > 20:
            error({"Error": "Gun altitude is not in range 0m to 20m."})

        self.elevation = float(elevation)

        if self.elevation < 0 or self.elevation > 45:
            error({"Error": "Gun elevation is not in range 0deg to 45deg."})

        self.mass = payload_mass
        self.lonB = None
        self.latB = None

        self.vf_y = 0
        self.vf_x = 0

        # calc x-component and y-component of the velocity
        self.v_x = self.mps * math.cos(self.elevation * math.pi / 180)
        self.v_y = self.mps * math.cos(self.elevation * math.pi / 180)

        self.totFlightTime = self.calcFlightTime()
        self.distanceTraveled = self.getDistanceTraveled()
        self.lonB, self.latB = self.getDestCoords()
        self.impactAngle = self.getImpactAngle()
        self.impactEnergy = self.getEnergy()

    def __str__(self):
        a = f"============================================\n"
        a += f"totFlightTime      ::   {str(round(self.totFlightTime,PRECISION))}"
        a += f"\ndistanceTraveled   ::   {str(round(self.distanceTraveled,PRECISION))}"
        a += f"\nlonA,LatA          ::  {str(round(self.lonA,LLPRECISION))},{str(round(self.latA,LLPRECISION))}"
        a += f"\nlonB,LatB          ::  {str(round(self.lonB,LLPRECISION))},{str(round(self.latB,LLPRECISION))}"
        a += f"\nimpactAngle        ::   {str(round(self.impactAngle,PRECISION))}"
        a += f"\njoulesAtImpact     ::   {str(round(self.impactEnergy,PRECISION))}"
        a += f"\nmegaJoulesAtImpact ::   {str(round(self.impactEnergy/1000000,PRECISION))}"
        a += f"\ngunElevation       ::   {str(self.elevation)}"
        return a

    def calcFlightTime(self):
        tot_disp = -1 * self.altitude
        # using v^2 - u^2 = 2as
        v = (((self.v_y**2) + 2 * (-9.8) * tot_disp) ** 0.5) * -1

        # using v = u + at
        t = (v - self.v_y) / (-9.8)

        self.vf_y = v
        return t

    def getDistanceTraveled(self):
        sql = f"""SELECT distance FROM public.fire_table
                  WHERE ms = '{self.mps}' and degrees = '{self.elevation}';
               """
        res = conn.query(sql, nopagination=True, singleVal=True)
        return res * DISTANCECAP

    def getDestCoords(self):
        self.lonB, self.latB = projectPoint(
            self.lonA, self.latA, self.bearing, self.distanceTraveled
        )
        return (self.lonB, self.latB)

    def getImpactAngle(self):

        return abs(
            float(self.elevation) + (3.0 * random.random()) * random.choice([1.0, -1.0])
        )

    def getEnergy(self):
        return (
            0.5
            * self.mass
            * ((self.vf_y**2) + (self.vf_x**2))
            * ENERGY_TO_MASS_RATIO
        )

    def results(self):
        return {
            "totFlightTime": round(self.totFlightTime, PRECISION),
            "distanceTraveled": round(self.distanceTraveled, PRECISION),
            "lonB": round(self.lonB, LLPRECISION),
            "latB": round(self.latB, LLPRECISION),
            "impactAngle": round(self.impactAngle, PRECISION),
            "joulesAtImpact": round(self.impactEnergy, PRECISION),
            "megaJoulesAtImpact": round(self.impactEnergy / 1000000, PRECISION),
        }


def usage():
    print(
        """BigBullet(
        meters_per_second, 
        gun bearing,
        lonA, 
        latA,
        altitude (in meters), 
        elevation (in degrees)
        projectile_mass (in kg)
        )
        """
    )


def makePoint(lon, lat):
    import random
    import copy

    color = "%06x" % random.randint(0, 0xFFFFFF)
    return copy.deepcopy(
        {
            "type": "Feature",
            "properties": {"marker-color": f"#{color}"},
            "geometry": {"coordinates": [lon, lat], "type": "Point"},
        }
    )


if __name__ == "__main__":
    """My tests to make sure things didn't go crazy at different bearings."""

    with open("./data/data.json") as f:
        data = json.load(f)

    data = data["ammo"]

    while True:
        for name, ammo in data["cartridge"].items():
            # print(ammo)

            elevation = [x for x in range(0, 45)]
            for ele in elevation:
                proj = BigBullet(
                    ammo["ms"], 0, -4.660736864, 44.54346084, 10, ele, ammo["kg"]
                )
                res = proj.results()
                # print(res)

                os.system("clear")
                print(proj)
                print(name)
                sleep(0.01)

    # bearings = [x for x in range(0, 360, 15)]
    # landingLocs = []
    # for i in range(100):
    #     bearing = random.randrange(0, 359)
    #     proj = BigBullet(
    #         random.randrange(500, 1000),
    #         bearing,
    #         -4.660736864,
    #         44.54346084,
    #         10,
    #         random.randrange(10, 40),
    #         500,
    #     )
    #     res = proj.results()
    #     landingLocs.append(makePoint(res["lonB"], res["latB"]))

    # with open("test.json", "w") as f:
    #     json.dump(landingLocs, f, indent=4)
