import utils
import typing as t
import pandas as pd
THRESH_MARGIN = [50, 60, 70, 80, 90, 100]
YEARS = [i for i in range(2000, 2024, 4)]


def get_data(data: pd.DataFrame,
             state: str) -> pd.DataFrame:
    """Filters data by an individual state. 

    Args:
        data (pd.DataFrame): data for all counties and states.
        state (str): the state.

    Returns:
        The filtered data, with only counties of the state provided left,
        and other states greyed out.
    """
    conditions = ((data["state"] == state) | (data["is_state"] == 1)) & (data["unit"] != state)
    state_data = data[conditions]
    for year in YEARS:
        data_year = state_data[f"{year}"].apply(lambda x: utils.get_color(x, THRESH_MARGIN))
        state_data[f"{year}"] = data_year
        state_data[f"{year}"] = state_data.apply(lambda x: utils.grey_out(x["state"],
                                                                          x[f"{year}"],
                                                                          state), axis = 1)
    return state_data


def get_results(data: pd.DataFrame,
                state: str) -> t.List[t.List[float]]:
    """Gets state results.

    Args:
        data (pd.DataFrame): data for all counties and states.
        state (str): the state.

    Returns:
        The results, transformed to be used by create_chart().
    """ 
    results = data[data["unit"] == state].iloc[0].tolist()
    results = [float(i) for i in results[-6:]]
    d_results = [abs(i) if i < 0 else 100-i for i in results]
    r_results = [100+i if i < 0 else i for i in results]
    return [d_results, r_results]    
