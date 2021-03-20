import os
import logging
import json
import numpy as np
from datetime import datetime

from functions import Functions
from hc_ga import Algorithm, AlgorithmBihc, AlgorithmGa, AlgorithmGaBihc, solve_with_HC
from lshade import solve_with_LSHADE

# structure for method output
common_output = {
    'f_value': None,
    'solution': None,
}


def _check_method_output(method, output):
    """Checks that a method outputs every information we need"""
    for key in common_output.keys():
        val_in_output = output.get(key)
        if val_in_output is None:
            logging.warning(
                f"Method {method} did not add information about {key}")


def _get_f_name(common_params):
    return common_params['function'].__name__


def _save_method_output(method_name, input_params, method_output):
    """Saves the result (`method_output`) for running `method_name` with parameters `input_params`."""
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

    # remove/adapt keys to be serializable
    input_params = input_params.copy()
    method_output = method_output.copy()
    input_params.pop('bounds')
    input_params['function'] = _get_f_name(input_params)
    if 'solution' in method_output:
        method_output['solution'] = np.array2string(method_output['solution'])

    output = {
        **input_params,
        **method_output
    }

    try:
        os.makedirs('./output', exist_ok=True)
        file_path = f'./output/{method_name}_{dt_string}.json'
        with open(file_path, 'w+') as f:
            json.dump(output, f)
    except Exception as e:
        logging.error(f'Failed to save method output: {e}')


def main():
    ndim = 20
    common_params = {
        "function": Functions.bent_cigar,
        "ndim": ndim,
        # range for each parameter of the function
        "bounds": [[-100, 100] for _ in range(ndim)],
    }

    HC_params = common_params.copy()
    LSHADE_params = common_params.copy()

    HC_params.update({
    })
    LSHADE_params.update({
    })

    output_HC = solve_with_HC(HC_params)
    _check_method_output("HC", output_HC)
    _save_method_output("HC", common_params, output_HC)

    output_LSHADE = solve_with_LSHADE(LSHADE_params)
    _check_method_output("LSHADE", output_LSHADE)
    _save_method_output("LSHADE", common_params, output_LSHADE)

    print(f"HC vs LSHADE for {_get_f_name(common_params)}:",
          output_HC['f_value'], output_LSHADE['f_value'])


if __name__ == "__main__":
    main()
