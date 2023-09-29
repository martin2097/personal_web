import dash
from dash import html, Output, Input, State, callback, dcc, no_update
import dash_mantine_components as dmc
import itertools
from datetime import datetime
from time import time
import math
import copy
import base64
import io
import pandas as pd
import numpy as np
import re
from lib.page_templates import page_template

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)

connection_height_df = pd.read_excel(
    "swep_data.xlsx",
    sheet_name="connection_height",
)

type_group_df = pd.read_excel(
    "swep_data.xlsx",
    sheet_name="type_group",
)


def layout(language):
    return page_template(
        dmc.LoadingOverlay(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                dcc.Upload(
                                                    id="upload-data",
                                                    children=html.Div(
                                                        [
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ]
                                                    ),
                                                    style={
                                                        "width": "100%",
                                                        "height": "60px",
                                                        "lineHeight": "60px",
                                                        "borderWidth": "1px",
                                                        "borderStyle": "dashed",
                                                        "borderRadius": "5px",
                                                        "textAlign": "center",
                                                        "margin": "10px",
                                                    },
                                                ),
                                            ],
                                            span=12,
                                        )
                                    ]
                                ),
                                dmc.Grid(dmc.Col(id="group-creator-output")),
                            ]
                        )
                    ],
                    style={
                        "width": "calc(100vw - 60px)",
                        "padding-top": "40px",
                        "margin": "0px",
                    },
                    gutter=40,
                ),
                dcc.Store(id="input-excel"),
                dcc.Download(id="download-xlsx"),
            ]
        ),
        language=language,
    )


dash.register_page(
    module="group-creator-sk",
    path="/sk/group-creator",
    redirect_from=["/group-creator"],
    title="Martin Rapavý - Group Creator",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Toto je projekt pre konkrétnu firmu.",
    image="personal-page-view.png",
    layout=layout("sk"),
)


dash.register_page(
    module="group-creator-en",
    path="/en/group-creator",
    title="Martin Rapavý - Group Creator",
    description="I am passionate about data, Python and especially Dash. This is a project for specific company.",
    image="personal-page-view.png",
    layout=layout("en"),
)


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        return no_update

    return df


@callback(
    Output("input-excel", "data"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    prevent_initial_call=True,
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = parse_contents(list_of_contents, list_of_names, list_of_dates)
        return children.to_json(date_format="iso", orient="split")


def find_pattern(in_str):
    if in_str is None:
        return None
    elif in_str == " ":
        return None
    extracted_number = re.findall(r"\d+", in_str)[0]
    if in_str[0:3] == "B30":
        return "B30"
    elif in_str[1:4] == "35H":
        return "35H"
    elif in_str[1:4] == "35T":
        return "35T"
    elif in_str[0:5] == "B315M":
        return "B315M"
    elif in_str[0:3] == "B56":
        return "B56"
    elif "120T" in in_str:
        return "120T"
    elif "200TH" in in_str:
        return "200TH"
    elif "320HT" in in_str:
        return "320HT"
    elif "320LT" in in_str:
        return "320LT"
    elif "250ASH" in in_str:
        return "250ASH"
    elif "BDW35TDW" in in_str:
        return "BDW35TDW"
    elif extracted_number == "300":
        return "300"
    elif extracted_number == "310":
        return "310"
    elif extracted_number == "50":
        return "50"
    elif extracted_number == "185":
        return "185"
    elif extracted_number == "220":
        return "220"
    elif extracted_number == "57":
        return "57"
    else:
        return "XNA"


def calculate_plate_height(type_a, type_b, type_c, nop):
    if type_a == "B30":
        if type_c == "SC-H":
            if type_b == "D":
                return 18.3 + 2.12 * nop
            else:
                return 14 + 2.12 * nop
        elif type_c == "SC-Y":
            return 6 + 2.12 * nop
        else:
            return None
    elif type_a == "35H":
        if type_c == "SC-S":
            if type_b == "D":
                return 12.7 + 2.34 * nop
            else:
                return 8 + 2.34 * nop
        else:
            return None
    elif type_a == "35T":
        if type_c == "SC-S":
            if type_b == "D":
                return 14.6 + 2.26 * nop
            else:
                return 10 + 2.26 * nop
        elif type_c == "SC-M":
            if type_b == "D":
                return 31.2 + 2.26 * nop
            else:
                return 22 + 2.26 * nop
        else:
            return None
    elif type_a == "BDW35TDW":
        return 18 + 2.53 * nop
    elif type_a == "B315M":
        if type_c == "SC-S":
            if type_b == "D":
                return 15.8 + 2.86 * nop
            else:
                return 10 + 2.86 * nop
        else:
            return None
    elif type_a == "B56":
        if type_c[0:2] == "SC":
            if type_b == "D":
                return 23.8 + 2.44 * nop
            else:
                return 14 + 2.44 * nop
        else:
            return None
    elif type_a == "120T":
        if type_b == "D":
            return 14.6 + 2.29 * nop
        else:
            if type_c == "SC-E":
                return 18 + 2.29 * nop
            elif type_c == "SC-H":
                return 14 + 2.29 * nop
            elif type_c == "SC-F":
                return 14 + 2.29 * nop
            else:
                return 10 + 2.29 * nop
    elif type_a == "200TH":
        if type_b == "D":
            return 19.4 + 2.29 * nop
        else:
            if type_c == "SC-H":
                return 22 + 2.29 * nop
            else:
                return 10 + 2.29 * nop
    elif type_a == "300":
        if type_c == "SC-M":
            return 10 + 1.89 * nop
        elif type_c == "SC-H1":
            return 14 + 1.89 * nop
        else:
            return None
    elif type_a == "310":
        if type_c == "SC-H":
            return 10 + 1.91 * nop
        else:
            return None
    elif type_a == "320HT":
        if type_b == "D":
            if type_c == "SC-S":
                return 10 + 1.98 * nop + 2
            elif type_c == "SC-M":
                return 14 + 1.98 * nop + 4
            else:
                return None
        else:
            if type_c == "SC-S":
                return 10 + 1.98 * nop
            elif type_c == "SC-M":
                return 14 + 1.98 * nop
            else:
                return None
    elif type_a == "320LT":
        if type_b == "D":
            if type_c == "SC-S":
                return 15.14 + 2.57 * nop
            elif type_c == "SC-M":
                return 24.28 + 2.57 * nop
            else:
                return None
        else:
            if type_c == "SC-S":
                return 10 + 2.57 * nop
            elif type_c == "SC-M":
                return 14 + 2.57 * nop
            else:
                return None
    elif type_a == "50":
        if type_b == "D":
            return 21.4 + 2.34 * nop
        else:
            return 12 + 2.34 * nop
    elif type_a == "185":
        return 18 + 2 * nop
    elif type_a == "220":
        if type_b == "D":
            if type_c == "SC-M":
                return 17 + 1.73 * nop
            elif type_c == "SC-H":
                return 21 + 1.73 * nop
            elif type_c == "SC-S":
                return 13 + 1.73 * nop
            else:
                return None
        else:
            if type_c == "SC-H":
                return 14 + 1.73 * nop
            elif type_c == "SC-M":
                return 10 + 1.73 * nop
            elif type_c == "SC-S":
                return 6 + 1.73 * nop
            else:
                return None
    elif type_a == "250ASH":
        if type_c == "NSC-M1":
            return 14 + 2.11 * nop
        else:
            return 14 + 1.91 * nop
    elif type_a == "57":
        if type_b == "D":
            if type_c == "SC-S":
                return 25.8 + 2.44 * nop
            else:
                return None
        else:
            if type_c == "SC-S":
                return 16 + 2.44 * nop
            else:
                return None
    else:
        return None


def first_non_empty(list_of_string):
    try:
        return int(next(s for s in list_of_string if s))
    except:
        return np.NaN


def calculate_nop(input_string):
    if input_string is None:
        return 0
    try:
        if math.isnan(input_string):
            return 0
    except:
        return sum([int(i) for i in re.findall(r"\d+", input_string)])


def calculate_final_height(connection_p_height, connection_f_height, plate_height):
    try:
        if (connection_p_height in (20, 30)) & (connection_f_height in (20, 30)):
            return 60 + plate_height + 60
        elif (connection_p_height in (20, 30)) & (math.isnan(connection_f_height)):
            return 20 + plate_height + 60
        elif (math.isnan(connection_p_height)) & (connection_f_height in (20, 30)):
            return 20 + 60 + plate_height
        elif connection_p_height in (20, 30):
            return 60 + plate_height + connection_f_height + 18
        elif connection_f_height in (20, 30):
            return 20 + 18 + connection_p_height + plate_height + 60
        elif math.isnan(connection_f_height):
            return 20 + 18 + connection_p_height + plate_height
        elif math.isnan(connection_p_height):
            return 20 + plate_height + connection_f_height + 18
        else:
            return (
                20 + 18 + connection_p_height + plate_height + connection_f_height + 18
            )
    except:
        return None


def find_type_b(in_str):
    if in_str is None:
        return None
    try:
        if math.isnan(in_str):
            return None
    except:
        if "D" in in_str:
            return "D"
        else:
            return "XNA"


@callback(
    Output("group-creator-output", "children", allow_duplicate=True),
    Output("download-xlsx", "data"),
    Input("input-excel", "data"),
    prevent_initial_call=True,
)
def run_from_excel(stored_df_as_json):
    stored_df = pd.read_json(stored_df_as_json, orient="split")
    df = stored_df.copy()
    df = df[["Job No", "Item description", "CONNECTIONS F", "CONNECTIONS P"]]
    df["TYPE_A"] = (
        df["Item description"]
        .str.split(n=1, pat="/")
        .str.get(0)
        .str.split(n=1, pat="x")
        .str.get(0)
        .apply(find_pattern)
    )
    df["TYPE_B"] = (
        df["Item description"]
        .str.split(n=1, pat="/")
        .str.get(1)
        .str.split(n=1, pat=" ")
        .str.get(0)
        .apply(find_type_b)
    )
    df["TYPE_C"] = (
        df["Item description"]
        .str.split(n=1, pat="/")
        .str.get(1)
        .str.split(n=1, pat=" ")
        .str.get(0)
        .str.split(n=1, pat="-")
        .str.get(1)
    )
    df["TYPE_FOR_GROUP"] = (
        df["Item description"]
        .str.split(n=1, pat="/")
        .str.get(0)
        .str.split(n=1, pat="x")
        .str.get(0)
    )
    df["NOP"] = (
        df["Item description"]
        .str.split(n=1, pat="/")
        .str.get(0)
        .str.split(n=1, pat="x")
        .str.get(1)
        .apply(lambda x: calculate_nop(x))
        .astype("int")
    )
    df["PLATE_HEIGHT"] = df.apply(
        lambda x: calculate_plate_height(x.TYPE_A, x.TYPE_B, x.TYPE_C, x.NOP), axis=1
    )
    df["CONNECTION_P"] = (
        df["CONNECTIONS P"].str.split(pat="*").apply(lambda x: first_non_empty(x))
    )
    df["CONNECTION_F"] = (
        df["CONNECTIONS F"].str.split(pat="*").apply(lambda x: first_non_empty(x))
    )
    df = (
        df.merge(
            connection_height_df,
            how="left",
            left_on="CONNECTION_P",
            right_on="Connection",
        )
        .drop(columns=["Connection"])
        .rename(columns={"Height": "CONNECTION_P_HEIGHT"})
    )
    df = (
        df.merge(
            connection_height_df,
            how="left",
            left_on="CONNECTION_F",
            right_on="Connection",
        )
        .drop(columns=["Connection"])
        .rename(columns={"Height": "CONNECTION_F_HEIGHT"})
    )
    df = (
        df.merge(
            type_group_df,
            how="left",
            left_on="TYPE_FOR_GROUP",
            right_on="Type",
        )
        .drop(columns=["Type"])
        .rename(columns={"Group": "GROUP"})
    )
    df["FINAL_HEIGHT"] = df.apply(
        lambda x: calculate_final_height(
            x.CONNECTION_P_HEIGHT, x.CONNECTION_F_HEIGHT, x.PLATE_HEIGHT
        ),
        axis=1,
    )
    return "Done", dcc.send_data_frame(
        df.to_excel, "ouput_excel.xlsx", sheet_name="Sheet_1"
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
