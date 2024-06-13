import pymssql
from typing import Literal
import csv


def execute_query(code: str, sqlmode: str):
    params = {
        "server": "10.166.168.127",
        "database": "HYCX.Noise.ShunDe",
        "user": "sa",
        "password": "1a2b3c4D",
        "name": 1235
    }

    conn = pymssql.connect(**params, charset="utf8")
    cursor = conn.cursor()

    if sqlmode == "声压级":
        sql = f"SELECT COUNT(DISTINCT FORMAT(TimePoint, 'yyyy-MM-dd HH')) AS TimeFormatted FROM T_GaoLing_Minute WHERE Code = '{code}'"
    elif sqlmode == "音频":
        sql = f"SELECT COUNT(DISTINCT FORMAT(StartTime, 'yyyy-MM-dd HH')) AS TimeFormatted FROM T_GaoLing_IdentifyData WHERE Code = '{code}'"
    elif sqlmode == "定位":
        sql = f"SELECT COUNT(DISTINCT FORMAT(TimePoint, 'yyyy-MM-dd HH')) AS TimeFormatted FROM T_GaoLing_LocationData WHERE Code = '{code}'"

    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0] if row else None


def noise_data_sql(
    sqlmode: Literal["声压级", "音频", "定位"],
    stations_code: list,
    stations_name: list,
    *args,
):
    res = {}
    for code, name in zip(stations_code, stations_name):
        res[name] = execute_query(params, code, sqlmode)
    return res


def save_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # 写入标题行
        writer.writerow(["站点名称", "小时数据(条)"])
        # 写入数据行
        for key, value in data.items():
            writer.writerow([key, value])
        print(f"数据已保存至{filename}")
def sum(*args):
    n = 0
    for i in args:
        n+=i
    return n
if __name__ == "__main__":
    params = {
    "server": "10.166.168.127",
    "database": "HYCX.Noise.ShunDe",
    "user": "sa",
    "password": "1a2b3c4D",
}
    station = {
        "name": [
            "赛纳科技中心",
            "佛山生态环境监测站",
            "德胜广场",
            "T21创意产业园",
            "新宁公园",
            "中新科技文化艺术中心",
            "测试站点1",
        ],
        "code": [
            "0756168807",
            "075616880901",
            "0756168810",
            "075616881002",
            "075616881003",
            "0756168811",
            "station1",
        ],
    }
    sqlmode = "声压级"
    res = noise_data_sql(
        sqlmode="声压级", stations_code=station["code"], stations_name=station["name"]
    )
    save_to_csv(res, f"{sqlmode}.csv")
