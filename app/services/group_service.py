import pandas as pd

def create_balanced_groups(df, num_groups):
    df = df.sort_values(by="Grade in pre", ascending=False).reset_index(drop=True)
    groups = [[] for _ in range(num_groups)]

    direction = 1
    group_index = 0

    for _, row in df.iterrows():
        groups[group_index].append(row.to_dict())

        if direction == 1:
            group_index += 1
            if group_index == num_groups:
                group_index -= 1
                direction = -1
        else:
            group_index -= 1
            if group_index < 0:
                group_index += 1
                direction = 1

    return groups


def calculate_stats(group):
    df = pd.DataFrame(group)
    avg_marks = round(df["Grade in pre"].mean(), 2)
    male_count = len(df[df["Gender"] == "Male"])
    female_count = len(df[df["Gender"] == "Female"])
    return avg_marks, male_count, female_count