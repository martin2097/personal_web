import dash
from dash import html, Output, Input, State, callback
import dash_mantine_components as dmc
import math

dash.register_page(__name__)

layout = dmc.LoadingOverlay(
    dmc.Grid([
        dmc.Col([
            dmc.TextInput(id="group-creator-list-input", label="Enter the list of numbers (i.e. 40, 40, 20, 70, 30):"),
            dmc.NumberInput(
                id="group-creator-group-max",
                label="Set maximal size of each group",
                value=110,
                style={"width": 250},
            ),
            dmc.Button("Calculate", id="group-creator-calculate-btn"),
            html.Div(id="group-creator-output")
        ])
    ])
)


def sorted_k_partitions(seq, k):
    """Returns a list of all unique k-partitions of `seq`.

    Each partition is a list of parts, and each part is a tuple.

    The parts in each individual partition will be sorted in shortlex
    order (i.e., by length first, then lexicographically).

    The overall list of partitions will then be sorted by the length
    of their first part, the length of their second part, ...,
    the length of their last part, and then lexicographically.
    """
    n = len(seq)
    groups = []  # a list of lists, currently empty

    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()

            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()

    result = generate_partitions(0)

    # Sort the parts in each partition in shortlex order
    result = [sorted(ps, key=lambda p: (len(p), p)) for ps in result]
    # Sort partitions by the length of each part, then lexicographically.
    result = sorted(result, key=lambda ps: (*map(len, ps), ps))

    return result


def fast_solution(lst, maxsum):
    output = None
    for n_size in range(math.ceil(sum(lst)/maxsum), len(lst)+1):
        for split in sorted_k_partitions(lst, n_size):
            correct = True
            for group in split:
                if sum(group) > maxsum:
                    correct = False
            if correct:
                output = split
                return output
    return output


@callback(
    Output("group-creator-output", 'children'),
    Input("group-creator-calculate-btn", 'n_clicks'),
    State("group-creator-list-input", 'value'),
    State("group-creator-group-max", "value"),
    prevent_initial_call=True
)
def update_output_div(n_clicks, number_list, group_max):
    number_list = [int(x) for x in list(number_list.split(","))]
    out = []
    solution = fast_solution(number_list, group_max)
    if solution is None:
        return dmc.Text("Solution does not exist")
    for groups in solution:
        text_group = ""
        for i in groups:
            text_group = text_group + str(i) + " "
        text_group = text_group + "   (sum " + str(sum(groups)) + ")"
        out.append(dmc.Text(text_group))
    return out
