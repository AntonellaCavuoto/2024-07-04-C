from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as year
                        from sighting s 
                        order by year(s.`datetime`) desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct s.shape as shape
                        from sighting s 
                        where year(s.`datetime`) = %s
                        having s.shape != ""
                        order by s.shape asc"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getSitingsYear(year, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from sighting s 
                        where year (s.`datetime`) = %s and s.shape = %s """
            cursor.execute(query, (year, shape))

            for row in cursor:
                result.append(Sighting(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdges(year, shape, year2, shape2, idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as id1, s2.id as id2, s2.longitude - s.longitude as peso
                        from (select *
                        from sighting s 
                        where year (s.`datetime`) = %s and s.shape = %s) s, 
                        (select *
                        from sighting s 
                        where year (s.`datetime`) = %s and s.shape = %s) s2
                        where s.id != s2.id and s.state = s2.state and s.longitude < s2.longitude"""
            cursor.execute(query, (year, shape, year2, shape2))

            for row in cursor:

                result.append((idMap[row["id1"]], idMap[row["id2"]], row["peso"]))

            cursor.close()
            cnx.close()
        return result