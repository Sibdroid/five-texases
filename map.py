import utils
import charts
import parsing
import typing as t
import pandas as pd
import json
import sys
from time import time
STATES = ["El Norte", "Gulfland", "New Texas", "Plainland", "Trinity"]
YEARS = [i for i in range(2000, 2024, 4)]

    
def main() -> None:
    start_time = time()
    pd.options.mode.chained_assignment = None
    geojson = utils.read_json("tx-geojson.json")
    data = pd.read_excel("tx-data.xlsx", header=0, index_col=0)
    for state in STATES:
        state_data = parsing.get_data(data, state)
        state_results = parsing.get_results(data, state)
        file_names = []
        for i, year in enumerate(YEARS):
            charts.draw_map(geojson, state_data, "code", f"{year}",
                            f"{year}-map.png")
            charts.create_chart(state_results, i, f"{year}-chart.png")
            utils.combine_images([f"{year}-map.png", f"{year}-chart.png"],
                                 f"{year}.png")
            utils.add_text(f"{year}.png", (1100, 50), f"{state}, {year}",
                           "Roboto-Regular.ttf", 40, fill=(0, 0, 0))
            file_names += [f"{year}.png"] 
        utils.make_gif(file_names, f"{state}.gif")  
        print(f"{state} done")
    print(f"{time()-start_time} seconds")
    
        
if __name__ == "__main__":
    main()
