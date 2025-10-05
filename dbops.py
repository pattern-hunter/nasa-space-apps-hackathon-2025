import sqlite3 as sql
import csv

with open("nasa_kepler_exoplanet.csv", "r") as datafile:
    X, y = [], []
    csvlines = list(csv.DictReader(datafile))

    accepted_keys = []
    
    m = csvlines[0]
    for key, val in m.items():
        if key != "rowid":
            try:
                t = float(val)
                accepted_keys.append(key)
            except ValueError:
                pass
    
    conn = sql.connect("database.sqlite")
    cur = conn.cursor()

########################################## Create SQLite Table ##########################################
    # columns = []
    # for key in accepted_keys:
    #     columns.append(f"{key} REAL")

    # query = f"""
    # CREATE TABLE exoplanet_data(
    #     result TEXT,
    #     {",".join(columns)}
    # );
    # """
    # cur.execute(query)
#########################################################################################################

###################################### Insert planetary data ############################################
    # values = []
    # for line in csvlines:
    #     result = line["koi_disposition"]
    #     value = [f"'{result}'"]
    #     for key in accepted_keys:
    #         if line[key] == "":
    #             value.append(0.0)
    #         else:
    #             value.append(float(line[key]))
    #     values.append(f"({','.join(map(lambda x: str(x), value))})")
    # query = f"""
    # INSERT INTO exoplanet_data (result,{",".join(accepted_keys)})
    # VALUES {",".join(values)}
    # """
    # # print(query)
    # cur.execute(query)
    # conn.commit()
#########################################################################################################


    conn.close()

