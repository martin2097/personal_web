import dash
from dash import html, Output, Input, State, callback
import dash_mantine_components as dmc
import itertools

dash.register_page(__name__)

layout = dmc.LoadingOverlay(
    dmc.Grid([
        dmc.Col([
            dmc.Grid([
                dmc.Col([
                    dmc.Text("Type A:")
                ], span="content"),
                dmc.Col([
                    dmc.TextInput(id="group-creator-list-input-type-a", label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):", value="500x4, 750x1, 850x5, 350x8"),
                ], span="auto")
            ]),
            dmc.Grid([
                dmc.Col([
                    dmc.Text("Type B:")
                ], span="content"),
                dmc.Col([
                    dmc.TextInput(id="group-creator-list-input-type-b", label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):"),
                ], span="auto")
            ]),
            dmc.Grid([
                dmc.Col([
                    dmc.Text("Type C:")
                ], span="content"),
                dmc.Col([
                    dmc.TextInput(id="group-creator-list-input-type-c", label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):"),
                ], span="auto")
            ]),
            dmc.Grid([
                dmc.Col([
                    dmc.Text("Type D:")
                ], span="content"),
                dmc.Col([
                    dmc.TextInput(id="group-creator-list-input-type-d", label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):"),
                ], span="auto")
            ]),
            dmc.Grid([
                dmc.Col([
                    dmc.Text("Type E:")
                ], span="content"),
                dmc.Col([
                    dmc.TextInput(id="group-creator-list-input-type-e", label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):"),
                ], span="auto")
            ]),
            dmc.NumberInput(
                id="group-creator-group-max",
                label="Set maximal size of each group",
                value=1100,
                style={"width": 250},
            ),
            dmc.Button("Calculate", id="group-creator-calculate-btn"),
            dmc.Grid(id="group-creator-output")
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
                if full >= best:
                    best = full
                    best_results = out
    return best_results


def final_algo(lst, maxsum):
    result = []
    for uni in set(lst):
        if maxsum//uni > 1:
            for times in range((lst.count(uni))//(maxsum//uni)):
                result.append([uni] * (maxsum//uni))
                for i in ([uni] * (maxsum//uni)):
                    lst.remove(i)
    while max(lst)+min(lst) > maxsum:
        result.append([max(lst)])
        lst.remove(max(lst))
        if len(lst) == 0:
            break
    scrubbs = fast_solution(lst, maxsum)
    return result+scrubbs


def list_from_input(lst):
    out_lst = []
    if len(lst) == 0:
        return out_lst
    for x in list(lst.split(",")):
        tp, cnt = x.split("x")
        out_lst += [int(tp)] * int(cnt)
    return out_lst


@callback(
    Output("group-creator-output", 'children'),
    Input("group-creator-calculate-btn", 'n_clicks'),
    State("group-creator-list-input-type-a", 'value'),
    State("group-creator-list-input-type-b", 'value'),
    State("group-creator-list-input-type-c", 'value'),
    State("group-creator-list-input-type-d", 'value'),
    State("group-creator-list-input-type-e", 'value'),
    State("group-creator-group-max", "value"),
    prevent_initial_call=True
)
def update_output_div(n_clicks, lst_type_a, lst_type_b, lst_type_c, lst_type_d, lst_type_e, group_max):
    lst_type_a = list_from_input(lst_type_a)
    lst_type_b = list_from_input(lst_type_b)
    lst_type_c = list_from_input(lst_type_c)
    lst_type_d = list_from_input(lst_type_d)
    lst_type_e = list_from_input(lst_type_e)
    out = []
    # A
    if len(lst_type_a) > 0:
        solution = final_algo(lst_type_a, group_max)
        if solution is None:
            out.append(dmc.Col(dmc.Text("Type A solution does not exist"), span="content"))
        else:
            inout = []
            inout.append(dmc.Text("Type A Solution:"))
            for groups in solution:
                text_group = ""
                for i in groups:
                    text_group = text_group + "A" + str(i) + " "
                text_group = text_group + "   (sum " + str(sum(groups)) + ")"
                inout.append(dmc.Text(text_group))
            out.append(dmc.Col(inout, span="content"))
    # B
    if len(lst_type_b) > 0:
        solution = final_algo(lst_type_b, group_max)
        if solution is None:
            out.append(dmc.Col(dmc.Text("Type B solution does not exist"), span="content"))
        else:
            inout = []
            inout.append(dmc.Text("Type B Solution:"))
            for groups in solution:
                text_group = ""
                for i in groups:
                    text_group = text_group + "B" + str(i) + " "
                text_group = text_group + "   (sum " + str(sum(groups)) + ")"
                inout.append(dmc.Text(text_group))
            out.append(dmc.Col(inout, span="content"))
    # C, D, E
    if len(lst_type_c) + len(lst_type_d) + len(lst_type_e) > 0:
        solution = final_algo(lst_type_c+lst_type_d+lst_type_e, group_max)
        if solution is None:
            out.append(dmc.Col(dmc.Text("Type C,D,E solution does not exist"), span="content"))
        else:
            inout = []
            inout.append(dmc.Text("Type C,D,E Solution:"))
            lst_type_c_fo = lst_type_c.copy()
            lst_type_d_fo = lst_type_d.copy()
            lst_type_e_fo = lst_type_e.copy()
            for groups in solution:
                text_group = ""
                for i in groups:
                    if i in lst_type_c_fo:
                        part = "C"
                        lst_type_c_fo.remove(i)
                    elif i in lst_type_d_fo:
                        part = "D"
                        lst_type_d_fo.remove(i)
                    elif i in lst_type_e_fo:
                        part = "E"
                        lst_type_e_fo.remove(i)
                    text_group = text_group + part + str(i) + " "
                text_group = text_group + "   (sum " + str(sum(groups)) + ")"
                inout.append(dmc.Text(text_group))
            out.append(dmc.Col(inout, span="content"))
    return out
