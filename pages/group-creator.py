import dash
from dash import html, Output, Input, State, callback
import dash_mantine_components as dmc
import itertools

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


def first_group(previous_ele, len_rema):
    output = []
    if len_rema == 0:
        output = previous_ele
    if len_rema >= 3:
        output += next_group(previous_ele+[3], len_rema-3)
    if len_rema >= 2:
        output += next_group(previous_ele+[2], len_rema-2)
    if len_rema >= 1:
        output += next_group(previous_ele+[1], len_rema-1)
    return output


def next_group(previous_ele, len_rema):
    output = []
    if len_rema == 0:
        output.append(previous_ele)
    if (previous_ele[-1] in (1, 2, 3)) and (len_rema >= 3):
        output += next_group(previous_ele+[3], len_rema-3)
    if (previous_ele[-1] in (1, 2)) and (len_rema >= 2):
        output += next_group(previous_ele+[2], len_rema-2)
    if (previous_ele[-1] == 1) and (len_rema >= 1):
        output += next_group(previous_ele+[1], len_rema-1)
    return output





def get_combs(candidate, input_list, maxsum, groups):
    output = []
    for comb in list(itertools.combinations(input_list, groups[0])):
        local_candidate = candidate.copy()
        if sum(comb) <= maxsum:
            if len(groups) == 1:
                local_candidate.append(list(comb))
                output.append(local_candidate)
            else:
                local_candidate.append(list(comb))
                new_input = input_list.copy()
                for ele in comb:
                    new_input.remove(ele)
                output += get_combs(local_candidate, new_input, maxsum, groups[1:])
    return output


def fast_solution(lst, maxsum):
    least_groups = 1000
    best = 0
    best_results = []
    for groups in first_group([], len(lst)):
        if len(groups) <= least_groups:
            for out in get_combs([], lst, maxsum, groups):
                if len(groups) < least_groups:
                    best_results = []
                    best = 0
                    least_groups = len(groups)
                full = 0
                for g in out:
                    if sum(g) == maxsum:
                        full += 1
                if full > best:
                    best = full
                    best_results = out
    return best_results


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
