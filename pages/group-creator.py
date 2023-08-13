import dash
from dash import html, Output, Input, State, callback
import dash_mantine_components as dmc
import itertools
from datetime import datetime
from time import time
import math
import copy

dash.register_page(__name__)

layout = dmc.LoadingOverlay(
    dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Grid(
                        [
                            dmc.Col([dmc.Text("Type A:")], span="content"),
                            dmc.Col(
                                [
                                    dmc.TextInput(
                                        id="group-creator-list-input-type-a",
                                        label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):",
                                        value="500x4, 750x1, 850x5, 350x8",
                                    ),
                                ],
                                span="auto",
                            ),
                        ]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col([dmc.Text("Type B:")], span="content"),
                            dmc.Col(
                                [
                                    dmc.TextInput(
                                        id="group-creator-list-input-type-b",
                                        label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):",
                                    ),
                                ],
                                span="auto",
                            ),
                        ]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col([dmc.Text("Type C:")], span="content"),
                            dmc.Col(
                                [
                                    dmc.TextInput(
                                        id="group-creator-list-input-type-c",
                                        label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):",
                                    ),
                                ],
                                span="auto",
                            ),
                        ]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col([dmc.Text("Type D:")], span="content"),
                            dmc.Col(
                                [
                                    dmc.TextInput(
                                        id="group-creator-list-input-type-d",
                                        label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):",
                                    ),
                                ],
                                span="auto",
                            ),
                        ]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col([dmc.Text("Type E:")], span="content"),
                            dmc.Col(
                                [
                                    dmc.TextInput(
                                        id="group-creator-list-input-type-e",
                                        label="Enter the list of numbers (i.e. 500x4, 750x1, 850x5, 350x8):",
                                    ),
                                ],
                                span="auto",
                            ),
                        ]
                    ),
                    dmc.NumberInput(
                        id="group-creator-group-max",
                        label="Set maximal size of each group",
                        value=1100,
                        style={"width": 350},
                    ),
                    dmc.NumberInput(
                        id="group-creator-group-max-cnt",
                        label="Set maximal number of elements in each group",
                        value=20,
                        style={"width": 350},
                    ),
                    dmc.Text("Choose algorithm type: "),
                    dmc.SegmentedControl(
                        id="group-creator-algorithm-type",
                        value="best",
                        data=[
                            {"value": "fast", "label": "Fast"},
                            {"value": "best", "label": "Best"},
                        ],
                    ),
                    dmc.Grid(
                        dmc.Col(
                            dmc.Button("Calculate", id="group-creator-calculate-btn"),
                            span="auto",
                        )
                    ),
                    dmc.Grid(id="group-creator-output"),
                ]
            )
        ],
        style={"width": "calc(100vw - 60px)", "padding-top": "40px", "margin": "0px"},
        gutter=40,
    )
)


def first_group(previous_ele, len_rema, max_len):
    output = []
    if len_rema == 0:
        output = previous_ele
    for r in range(max_len, 0, -1):
        if len_rema >= r:
            output += next_group(previous_ele + [r], len_rema - r, max_len)
    return output


def next_group(previous_ele, len_rema, max_len):
    output = []
    if len_rema == 0:
        output.append(previous_ele)
    for r in range(max_len, 0, -1):
        if (previous_ele[-1] in range(r, 0, -1)) and (len_rema >= r):
            output += next_group(previous_ele + [r], len_rema - r, max_len)
    return output


def get_combs(candidate, input_list, maxsum, groups):
    output = []
    for comb in list(set(itertools.combinations(input_list, groups[0]))):
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


def best_solution(lst, maxsum, max_len):
    least_groups = 1000
    best = 0
    best_results = []
    groups_opt = first_group([], len(lst), max_len)
    groups_opt.sort(key=len)
    for groups in groups_opt:
        if len(groups) <= least_groups:
            groups.sort(reverse=True)
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


def fast_solution(lst, maxsum, max_len):
    out = []
    groups_opt = first_group([], len(lst), max_len)
    groups_opt.sort(key=len)
    for groups in groups_opt:
        groups.sort(reverse=True)
        for out in get_combs([], lst, maxsum, groups):
            return out


def final_algo(lst, maxsum, max_len, alg_type):
    result = []
    for uni in set(lst):
        if maxsum // uni > 1:
            for times in range((lst.count(uni)) // (maxsum // uni)):
                result.append([uni] * (maxsum // uni))
                for i in [uni] * (maxsum // uni):
                    lst.remove(i)
    while max(lst) + min(lst) > maxsum:
        result.append([max(lst)])
        lst.remove(max(lst))
        if len(lst) == 0:
            break
    if alg_type == "fast":
        scrubbs = fast_solution(lst, maxsum, max_len)
    elif alg_type == "best":
        scrubbs = best_solution(lst, maxsum, max_len)
    return result + scrubbs


def final_algo_with_splitting(lst, maxsum, max_len, alg_type):
    result = []
    half_list = []
    for i in set(lst):
        cnt = lst.count(i)
        half_list += [i] * math.floor(cnt / 2)
    solution = final_algo(half_list, maxsum - 20, max_len, alg_type)
    rest_of_list = lst.copy()
    for i in solution:
        result.append(i)
        result.append(i)
        for j in i:
            rest_of_list.remove(j)
            rest_of_list.remove(j)
    rest_solution = final_algo(rest_of_list, maxsum, max_len, alg_type)
    return result + rest_solution


def list_from_input(lst):
    out_lst = []
    if len(lst) == 0:
        return out_lst
    for x in list(lst.split(",")):
        tp, cnt = x.split("x")
        out_lst += [int(tp)] * int(cnt)
    return out_lst


def one_by_one_solution(lst, maxsum):
    ordered_unique_lst = list(set(lst))
    print(ordered_unique_lst)
    ordered_unique_lst.sort(reverse=True)
    comb = []
    for val in ordered_unique_lst:
        for _ in range(lst.count(val)):
            added = 0
            i = 0
            for c in comb:
                if maxsum - sum(c) >= val:
                    comb[i] += [val]
                    added = 1
                    break
                i += 1
            if added == 0:
                comb.append([val])
    return comb


def get_remot(lst_of_lst):
    unique_list = list(set([item for sublist in lst_of_lst for item in sublist]))
    tot_rem = 0
    for val in unique_list:
        min_ind = 1000000
        max_ind = 0
        pos = 0
        for i in lst_of_lst:
            if val in i:
                if pos < min_ind:
                    min_ind = pos
                if pos > max_ind:
                    max_ind = pos
            pos += 1
        tot_rem += max_ind - min_ind
    return tot_rem


def best_one_by_one_solution(lst, maxsum):
    ordered_unique_lst = list(set(lst))
    best_sol = []
    shortest_len = 10000
    smallest_sums = 1000000
    for order in itertools.permutations(ordered_unique_lst):
        comb = []
        for val in order:
            for _ in range(lst.count(val)):
                added = 0
                i = 0
                for c in comb:
                    if maxsum - sum(c) >= val:
                        comb[i] += [val]
                        added = 1
                        break
                    i += 1
                if added == 0:
                    comb.append([val])
        if len(comb) < shortest_len:
            best_sol = comb
            shortest_len = len(comb)
            smallest_sums = get_remot(comb)
        elif len(comb) == shortest_len:
            if get_remot(comb) < smallest_sums:
                smallest_sums = get_remot(comb)
                best_sol = comb
    return best_sol


def one_by_one_with_splitting(lst, maxsum):
    result = []
    half_list = []
    for i in set(lst):
        cnt = lst.count(i)
        half_list += [i] * math.floor(cnt / 2)
    solution = one_by_one_solution(half_list, maxsum)
    rest_of_list = lst.copy()
    for i in solution:
        result.append(i.copy())
        result.append(i.copy())
        for j in i:
            rest_of_list.remove(j)
            rest_of_list.remove(j)
    for r in rest_of_list:
        added = 0
        i = 0
        for c in result:
            if maxsum - sum(c) >= r:
                result[i] += [r]
                added = 1
                break
            i += 1
        if added == 0:
            result.append([r])
    return result


def best_one_by_one_with_splitting(lst, maxsum):
    result = []
    half_list = []
    for i in set(lst):
        cnt = lst.count(i)
        half_list += [i] * math.floor(cnt / 2)
    solution = best_one_by_one_solution(half_list, maxsum)
    rest_of_list = lst.copy()
    for i in solution:
        result.append(i.copy())
        result.append(i.copy())
        for j in i:
            rest_of_list.remove(j)
            rest_of_list.remove(j)
    best_sol = []
    shortest_len = 10000
    smallest_sums = 1000000
    for order in itertools.permutations(list(set(rest_of_list))):
        comb = copy.deepcopy(result)
        for val in order:
            for _ in range(rest_of_list.count(val)):
                added = 0
                i = 0
                for c in comb:
                    if maxsum - sum(c) >= val:
                        comb[i] += [val]
                        added = 1
                        break
                    i += 1
                if added == 0:
                    comb.append([val])
        if len(comb) < shortest_len:
            best_sol = comb.copy()
            shortest_len = len(comb)
            smallest_sums = get_remot(comb)
        elif len(comb) == shortest_len:
            if get_remot(comb) < smallest_sums:
                smallest_sums = get_remot(comb)
                best_sol = comb.copy()
    return best_sol


def one_by_one_final(lst, maxsum, splitting, alg_type):
    if splitting:
        if alg_type == "fast":
            return one_by_one_with_splitting(lst, maxsum)
        elif alg_type == "best":
            return best_one_by_one_with_splitting(lst, maxsum)
    else:
        if alg_type == "fast":
            return one_by_one_solution(lst, maxsum)
        elif alg_type == "best":
            return best_one_by_one_solution(lst, maxsum)


@callback(
    Output("group-creator-output", "children"),
    Input("group-creator-calculate-btn", "n_clicks"),
    State("group-creator-list-input-type-a", "value"),
    State("group-creator-list-input-type-b", "value"),
    State("group-creator-list-input-type-c", "value"),
    State("group-creator-list-input-type-d", "value"),
    State("group-creator-list-input-type-e", "value"),
    State("group-creator-group-max", "value"),
    State("group-creator-group-max-cnt", "value"),
    State("group-creator-algorithm-type", "value"),
    prevent_initial_call=True,
)
def update_output_div(
    n_clicks,
    lst_type_a,
    lst_type_b,
    lst_type_c,
    lst_type_d,
    lst_type_e,
    group_max,
    max_len,
    alg_type,
):
    lst_type_a = list_from_input(lst_type_a)
    lst_type_b = list_from_input(lst_type_b)
    lst_type_c = list_from_input(lst_type_c)
    lst_type_d = list_from_input(lst_type_d)
    lst_type_e = list_from_input(lst_type_e)
    out = []
    start = time()
    # A
    if len(lst_type_a) > 0:
        # solution = final_algo(lst_type_a, group_max, max_len, alg_type)
        solution = one_by_one_final(lst_type_a, group_max, False, alg_type)
        if solution is None:
            out.append(
                dmc.Col(dmc.Text("Type A solution does not exist"), span="content")
            )
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
        # solution = final_algo(lst_type_b, group_max, max_len, alg_type)
        solution = one_by_one_final(lst_type_b, group_max, False, alg_type)
        if solution is None:
            out.append(
                dmc.Col(dmc.Text("Type B solution does not exist"), span="content")
            )
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
        # solution = final_algo_with_splitting(lst_type_c+lst_type_d+lst_type_e, group_max, max_len, alg_type)
        solution = one_by_one_final(
            lst_type_c + lst_type_d + lst_type_e, group_max - 20, True, alg_type
        )
        if solution is None:
            out.append(
                dmc.Col(dmc.Text("Type C,D,E solution does not exist"), span="content")
            )
        else:
            inout = []
            inout.append(dmc.Text("Type C,D,E Solution:"))
            lst_type_c_fo = lst_type_c.copy()
            lst_type_d_fo = lst_type_d.copy()
            lst_type_e_fo = lst_type_e.copy()
            inc = 0
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
                if ((inc % 2) == 1) & (solution[inc - 1] == solution[inc]):
                    inout.append(dmc.Text("---"))
                inc += 1
            out.append(dmc.Col(inout, span="content"))
    end = time()
    out.append(
        dmc.Col(
            [
                dmc.Text("Last Update:"),
                dmc.Text(datetime.now()),
                dmc.Text("Evaluation Time:"),
                dmc.Text(end - start),
            ],
            span="content",
            offset=1,
        )
    )
    return out
