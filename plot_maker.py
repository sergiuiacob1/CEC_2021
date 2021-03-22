import matplotlib.pyplot as plt
import json


hc_path = "./output/"
lshade_path = "./output/LSHADE_21_03_2021_21_34_26.json"

# read fitnesses for each method
with open(lshade_path, "r") as f:
    lshade_json = json.loads(f.read())

# plot fitnesses
plt.title(f"HC vs LSHADE\nfunction={lshade_json['function']}, ndim={lshade_json['ndim']}, MaxFES={lshade_json['maxFes']}")
plt.plot(lshade_json['fitnesses'])
plt.show()