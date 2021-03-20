from functions import Functions
import logging
from hc_ga import Algorithm, AlgorithmBihc, AlgorithmGa, AlgorithmGaBihc, solve_with_GA
from lshade import solve_with_LSHADE

# structure for method output
common_output = {
    'f_value': None,
    'solution': None,
}


def check_method_output(method, output):
    """Checks that a method outputs every information we need"""
    for key in common_output.keys():
        val_in_output = output.get(key)
        if not val_in_output:
            logging.warning(
                f"Method {method} did not add information about {key}")


def _get_f_name(common_params):
    return common_params['function'].__name__


def main():
    common_params = {
        "function": [Functions.bent_cigar],
        "ndim": 5
    }

    GA_params = common_params.copy()
    GA_params.update({
    })

    LSHADE_params = common_params.copy()
    LSHADE_params.update({
    })

    output_GA = solve_with_GA(GA_params)
    output_LSHADE = solve_with_LSHADE(LSHADE_params)

    check_method_output("GA", output_GA)
    check_method_output("LSHADE", output_LSHADE)

    print(f"GA vs LSHADE for {_get_f_name(common_params)}:",output_GA['f_value'], output_LSHADE['f_value'])


if __name__ == "__main__":
    main()
