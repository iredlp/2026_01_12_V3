from database.DB_connect import DBConnect
from model.constructors import Constructors


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct c.*
                    from constructors c , results r , races ra 
                    where r.constructorId =c.constructorId 
                    and ra.raceId =r.raceId 
                    and ra.`year` between %s and %s
                    and r.`position` is not null ;  """

        cursor.execute(query, (anno1,anno2))

        for row in cursor:
            results.append(Constructors(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPilotiPerCostr(idCostr,anno1, anno2):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select r.driverId as driverId 
                    from constructors c , results r , races ra 
                    where r.constructorId =c.constructorId and c.constructorId =%s
                    and ra.raceId =r.raceId and ra.raceId =r.raceId 
                    and ra.`year` between %s and %s
                    and r.`position` is not null ; """

        cursor.execute(query, (idCostr,anno1, anno2))

        for row in cursor:
            results.append(row["driverId"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getOldestDriverDob(constructorId, anno1, anno2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor()

        query = """
            SELECT MIN(d.dob) AS oldest_dob
            FROM results r, drivers d, races ra
            WHERE r.driverId = d.driverId
              AND r.raceId = ra.raceId
              AND r.constructorId = %s
              AND ra.year BETWEEN %s AND %s
              AND d.dob IS NOT NULL
        """

        cursor.execute(query, (constructorId, anno1, anno2))
        result = cursor.fetchone()

        cursor.close()

        if result is None:
            return None
        conn.close()

        return result[0]

