# poate scrie in roiu.json - 0 credite
import json, datetime
def publica(problema, J):
    data = {"de_la": "Hydra", "problema": problema, "J": J, "t": str(datetime.datetime.now())}
    open("roiul/roiu.json", "a", encoding="utf-8").write(json.dumps(data)+"\n")