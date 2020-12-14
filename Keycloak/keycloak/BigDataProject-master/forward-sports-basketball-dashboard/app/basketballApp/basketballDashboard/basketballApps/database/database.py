import pandas as pd
import numpy as np
import sqlalchemy as sql
import yaml
import os
import datetime
from datetime import datetime as dt


### these are configurations to connect to the database server eventually
# cfg = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), os.pardir, 'config.yaml')))
# sql_engine = sql.create_engine(cfg['mysql'])

####################################

## This first part is loading in the csv file and doing certain data transformations on it, which eventually should not be necessary

####################################
session_summary_df = pd.read_csv(
    "app/basketballApp/basketballDashboard/basketballApps/database/full_session_summary.csv",
    delimiter=";",
)

# turn date string into datetime
session_summary_df["datetime"] = pd.to_datetime(session_summary_df["date"])
session_summary_df["datetime"] = session_summary_df["datetime"].dt.date

# create total counts for acc, dec, left, right (always using mid and high)
session_summary_df["leftTurnMidAndHighCount"] = (
    session_summary_df["leftTurnMidCount"] + session_summary_df["leftTurnHighCount"]
)
session_summary_df["rightTurnMidAndHighCount"] = (
    session_summary_df["rightTurnMidCount"] + session_summary_df["rightTurnHighCount"]
)
session_summary_df["accMidAndHighCount"] = (
    session_summary_df["accMidCount"] + session_summary_df["accHighCount"]
)
session_summary_df["decMidAndHighCount"] = (
    session_summary_df["decMidCount"] + session_summary_df["decHighCount"]
)

# convert duration to minutes
session_summary_df["duration"] = session_summary_df["duration"] / 60000

# change the df to a per 10 minutes calculation
calculation_columns = [
    "distance",
    "highSpeedDistance",
    "sprintSpeedDistance",
    "calories",
    "exerciseLoad",
    "maxHR",
    "maxSpeed",
    "maxVO2",
    "accLowCount",
    "accMidCount",
    "accHighCount",
    "decLowCount",
    "decMidCount",
    "decHighCount",
    "leftTurnLowCount",
    "leftTurnMidCount",
    "leftTurnHighCount",
    "rightTrunLowCount",
    "rightTurnMidCount",
    "rightTurnHighCount",
    "leftTurnMidAndHighCount",
    "rightTurnMidAndHighCount",
    "accMidAndHighCount",
    "decMidAndHighCount",
]

# keep basic info and merge again after doing the calculation
basic_info = session_summary_df[
    session_summary_df.columns.difference(calculation_columns)
]

# do the per 10 minute division and keep in new df
session_per_10_df = session_summary_df[calculation_columns].divide(
    session_summary_df["duration"] / 10, axis="index"
)

# merge the two dfs again
session_per_10_df = pd.concat([session_per_10_df, basic_info], axis=1)

# create summary per training df per 10 Minutes
summary_per_training_per_10 = (
    session_per_10_df.groupby(["datetime", "name"]).mean().reset_index()
)
summary_per_training_per_10["id"] = "Total_Training"
summary_per_training_per_10["datetime"] = pd.to_datetime(
    summary_per_training_per_10["datetime"], errors="raise"
)
summary_per_training_per_10["num_week"] = summary_per_training_per_10[
    "datetime"
].dt.week

# create summary per training df
summary_per_training_player = (
    session_summary_df.groupby(["datetime", "name"]).sum().reset_index()
)
summary_per_training_player["id"] = "Total_Training"
summary_per_training_player["datetime"] = pd.to_datetime(
    summary_per_training_player["datetime"], errors="raise"
)
summary_per_training_player["weekday"] = summary_per_training_player[
    "datetime"
].dt.weekday
summary_per_training_player["num_week"] = summary_per_training_player[
    "datetime"
].dt.week


###################
#### RPE data #####
# This is RPE data that eventually should be read by an Google API since this is a google questionaire
###################
full_rpe_df = pd.read_csv(
    "app/basketballApp/basketballDashboard/basketballApps/database/rpe_data.csv",
    delimiter=";",
    encoding="latin1",
)

full_rpe_df["Tijdstempel"] = pd.to_datetime(full_rpe_df["Tijdstempel"])
full_rpe_df["Gestart om"] = pd.to_datetime(full_rpe_df["Gestart om"], errors="raise")

# extract RPE score
full_rpe_df["RPE score"] = full_rpe_df["RPE score"].str.extract("(\d+)", expand=False)
full_rpe_df["RPE score"] = full_rpe_df["RPE score"].astype(int)

# extract tevredenheid
new = full_rpe_df["Tevredenheid over training"].str.split(".", expand=True)
new[1] = pd.to_numeric(new[1], errors="coerce")
new = new.fillna(0)
new[1] = new[1].astype(int)
new[2] = new[0].astype(str) + "." + new[1].astype(str)
new[2] = pd.to_numeric(new[2], errors="coerce")
full_rpe_df["Tevredenheid over training"] = new[2]

# replace names dictionary
abbreviations = {
    "EF": "Esther FOKKE",
    "FK": "Fleur KUIJT",
    "IK": "Ilse KUIJT",
    "JBe": "Jill BETTONVIL",
    "KK": "Karin Kuijt",
    "KF": "Kiki FLEUREN",
    "LB": "Loyce BETTONVIL",
    "ND": "Noor DRIESSEN",
    "ZS": "Zoë SLAGTER",
    "CvK": "Charlotte VAN KLEEF",
}

session_types = [
    "Skills",
    "Shooting",
    "Kracht & Shooting",
    "Skills & Shooting",
    "Kracht & Skills",
    "Team",
]

full_rpe_df = full_rpe_df[full_rpe_df["Sessie type"].isin(session_types)]

full_rpe_df["Naam"] = full_rpe_df["Naam"].replace(abbreviations)

full_rpe_df.rename(
    columns={
        "Naam": "name",
        "Gestart om": "datetime",
        "Sessie type": "session_type",
        "RPE score": "rpe_score",
    },
    inplace=True,
)
full_rpe_df = full_rpe_df[["datetime", "name", "session_type", "rpe_score"]]
full_rpe_df.drop_duplicates(inplace=True)


#############

### Right Eye data is not something to worry about at the moment

#############
right_eye_df = pd.read_csv(
    "app/basketballApp/basketballDashboard/basketballApps/database/rightEyeTransformed.csv",
    delimiter=";",
    encoding="latin1",
)  # encoding="latin1")
right_eye_df["LAST_NAME"] = right_eye_df["LAST_NAME"].str.upper()
right_eye_df["name"] = right_eye_df["FIRST_NAME"] + " " + right_eye_df["LAST_NAME"]


#############

### Shooting data is not something to worry about at the moment

#############
shooting_df = pd.DataFrame(
    {
        "name": [
            "Charlotte VAN KLEEF",
            "Emese HOF",
            "Esther FOKKE",
            "Fleur KUIJT",
            "Ilse KUIJT",
            "Jill BETTONVIL",
            "Karin KUIJT",
            "Kiki FLEUREN",
            "Loyce BETTONVIL",
            "Natalie VAN DEN ADEL",
            "Noor DRIESSEN",
            "Rowie JONGELING",
            "Zoë SLAGTER",
            "Richelle VAN DER KEIJL",
        ],
        "shooting_percentage": [34, 26, 31, 29, 28, 33, 30, 28, 30, 27, 22, 25, 23, 25],
    }
)


# define todays data that the calculations should be based on
# has to be changed manually rn but later will be automatic based on the database
DATE_STR = "08-31-2020"


def overview_performance_metrics(players, df=summary_per_training_per_10):
    """
    Calculates the five performance metrics for the overview page
    """
    df2 = df.copy()

    # check if there is only one player
    if isinstance(players, str):
        selected_players = [players]
    else:
        selected_players = players

    df2 = df2[df2["name"].isin(selected_players)]

    df2["datetime"] = pd.to_datetime(df2["datetime"], errors="raise")
    df2["datetime"] = df2["datetime"].dt.date

    # return a df that has sums per week or per day
    week_sums_df = (
        df2.groupby("datetime")[
            [
                "exerciseLoad",
                "leftTurnMidCount",
                "leftTurnHighCount",
                "rightTurnMidCount",
                "rightTurnHighCount",
                "leftTurnMidAndHighCount",
                "rightTurnMidAndHighCount",
                "accMidAndHighCount",
                "decMidAndHighCount",
                "accMidCount",
                "accHighCount",
                "decMidCount",
                "decHighCount",
            ]
        ]
        .mean()
        .reset_index()
    )

    # usually should select the current data and go back to the latest monday
    current_date = dt.strptime(DATE_STR, "%m-%d-%Y")
    current_week_num = current_date.isocalendar()[1]
    current_date = current_date.date()

    # define last monday data
    last_monday = current_date - datetime.timedelta(days=current_date.weekday())

    # select all data from that monday on
    current_week_df = df2[df2["datetime"] >= last_monday]
    current_week_by_player_df = (
        current_week_df.groupby("name")[
            [
                "exerciseLoad",
                "leftTurnMidCount",
                "leftTurnHighCount",
                "rightTurnMidCount",
                "rightTurnHighCount",
                "leftTurnMidAndHighCount",
                "rightTurnMidAndHighCount",
                "accMidAndHighCount",
                "decMidAndHighCount",
                "accMidCount",
                "accHighCount",
                "decMidCount",
                "decHighCount",
            ]
        ]
        .mean()
        .reset_index()
    )

    # round the numeric values
    current_week_by_player_df = current_week_by_player_df.round(2)

    # get a sum per parameter for the display metrics
    sum_current_week_df = current_week_df.mean().reset_index().transpose()
    sum_current_week_df.columns = sum_current_week_df.loc["index"]
    sum_current_week_df = sum_current_week_df.iloc[1:, :]
    sum_current_week_df = sum_current_week_df.round(0)

    # get previous week averages
    means_per_weeknum = df2.groupby("num_week").mean().reset_index()
    means_per_weeknum = means_per_weeknum.round(2)
    means_per_weeknum.sort_values(by="num_week", inplace=True)

    return (
        week_sums_df,
        sum_current_week_df,
        current_week_by_player_df,
        means_per_weeknum,
    )


def load_management_current_physical_load(players, df=summary_per_training_player):
    """
    Calculates the current physical load, monotony, and strain for load management tab
    These are sports science metrics
    """
    df2 = df.copy()

    # usually should select the current data
    date = datetime.datetime.strptime(DATE_STR, "%m-%d-%Y").date()

    # check if there is only one player
    if isinstance(players, str):
        selected_players = [players]
    else:
        selected_players = players

    df2["datetime"] = pd.to_datetime(df2["datetime"], errors="raise")
    df2["datetime"] = df2["datetime"].dt.date

    # find unique player
    players = df2["name"].unique().tolist()
    players_df = pd.DataFrame({"name": players})
    players_df["key"] = 1

    # define the length of acute and chronic period
    num_days_acute = 6
    num_days_chronic = 21

    # find the start dates for acute load and chronic load
    start_date_acute = date - pd.to_timedelta(num_days_acute - 1, unit="d")
    start_date_chronic = date - pd.to_timedelta(num_days_chronic - 1, unit="d")

    # set up filters based on the time dates
    mask_acute = (df2["datetime"] >= start_date_acute) & (df2["datetime"] <= date)
    mask_chronic = (df2["datetime"] >= start_date_chronic) & (df2["datetime"] <= date)

    # since there might not be data for every day we set up a df that includes all days
    date_range_acute = pd.date_range(start_date_acute, date)
    date_range_acute_df = pd.DataFrame({"datetime": date_range_acute})
    date_range_acute_df["key"] = 1
    date_range_acute_df = pd.merge(
        date_range_acute_df, players_df, how="left", left_on="key", right_on="key"
    )

    # filter the acute data
    acute_df = df2.loc[mask_acute]
    acute_df["datetime"] = pd.to_datetime(acute_df["datetime"], errors="raise")
    acute_df = pd.merge(
        date_range_acute_df,
        acute_df,
        how="left",
        left_on=["datetime", "name"],
        right_on=["datetime", "name"],
    )
    acute_df.fillna(0, inplace=True)

    # calculate the mean of the acute load per player
    acute_df_mean = acute_df.groupby("name")["exerciseLoad"].mean().reset_index()

    ### need to look into acute std agian because std should also include the zeroes when no training is present
    acute_df_std = acute_df.groupby("name")["exerciseLoad"].std().reset_index()
    acute_df_mean.rename(columns={"exerciseLoad": "exerciseLoadAcute"}, inplace=True)
    acute_df_std.rename(columns={"exerciseLoad": "stdLoad"}, inplace=True)
    acute_df = pd.merge(
        acute_df_mean, acute_df_std, how="left", left_on="name", right_on="name"
    )

    # repeat the same process for chronic load
    date_range_chronic = pd.date_range(start_date_chronic, date)
    date_range_chronic_df = pd.DataFrame({"datetime": date_range_chronic})
    date_range_chronic_df["key"] = 1
    date_range_chronic_df = pd.merge(
        date_range_chronic_df, players_df, how="left", left_on="key", right_on="key"
    )

    chronic_df = df2.loc[mask_chronic]
    chronic_df["datetime"] = pd.to_datetime(chronic_df["datetime"], errors="raise")
    chronic_df = pd.merge(
        date_range_chronic_df,
        chronic_df,
        how="left",
        left_on=["datetime", "name"],
        right_on=["datetime", "name"],
    )
    chronic_df.fillna(0, inplace=True)
    chronic_df = chronic_df.groupby("name")["exerciseLoad"].mean().reset_index()
    chronic_df.rename(columns={"exerciseLoad": "exerciseLoadChronic"}, inplace=True)

    # calculate ac_ratio, monotony, and strain
    acute_chronic_df = pd.merge(
        acute_df, chronic_df, how="left", left_on="name", right_on="name"
    )

    acute_chronic_df["ac_ratio"] = (
        acute_chronic_df["exerciseLoadAcute"] / acute_chronic_df["exerciseLoadChronic"]
    )
    acute_chronic_df["monotony"] = (
        acute_chronic_df["exerciseLoadAcute"] / acute_chronic_df["stdLoad"]
    )
    acute_chronic_df["strain"] = (
        acute_chronic_df["exerciseLoadAcute"] * acute_chronic_df["monotony"]
    )

    acute_chronic_df.fillna(0, inplace=True)
    acute_chronic_df = acute_chronic_df.round(2)

    # only return data for selected players
    acute_chronic_df = acute_chronic_df[acute_chronic_df["name"].isin(selected_players)]

    return acute_chronic_df


def load_management_week_periodization(
    individual_player, players, df=summary_per_training_player
):
    """
    Calculates the periodization or spikes in training for the last seven days
    """
    df2 = df.copy()
    # check if there is only one player
    if isinstance(players, str):
        selected_players = [players]
    else:
        selected_players = players

    # only select selected players
    df2 = df2[df2["name"].isin(players)]

    # usually should select the current data
    date = datetime.datetime.strptime(DATE_STR, "%m-%d-%Y").date()

    # set up the time range for periodization data
    future_date = date + pd.to_timedelta(1, unit="d")
    back_date = date - pd.to_timedelta(5, unit="d")

    df2["datetime"] = pd.to_datetime(df2["datetime"], errors="raise")
    df2["datetime"] = df2["datetime"].dt.date

    # define number of days for the period as well as filter mask
    num_days_week = 7
    start_date_week = date - pd.to_timedelta(num_days_week - 1, unit="d")
    mask_week = (df2["datetime"] >= back_date) & (df2["datetime"] <= future_date)

    date_range = pd.date_range(back_date, future_date)
    date_range_df = pd.DataFrame({"datetime": date_range})

    # filter data for that week and calculate average per day
    one_week_df = df2.loc[mask_week]
    one_week_df = one_week_df.groupby("datetime")["exerciseLoad"].mean().reset_index()

    one_week_df["datetime"] = pd.to_datetime(one_week_df["datetime"], errors="raise")
    one_week_df = pd.merge(
        date_range_df, one_week_df, how="left", left_on="datetime", right_on="datetime"
    )

    # filter data for that week and only use it for the specified individual player
    player_one_week_df = df2.loc[mask_week]
    player_one_week_df = player_one_week_df[
        player_one_week_df["name"] == individual_player
    ]
    player_one_week_df = player_one_week_df[["datetime", "exerciseLoad"]].reset_index(
        drop=True
    )
    player_one_week_df["name"] = player
    player_one_week_df["datetime"] = pd.to_datetime(
        player_one_week_df["datetime"], errors="raise"
    )

    # merge team and individual player data
    one_week_df = pd.merge(
        one_week_df,
        player_one_week_df,
        how="left",
        left_on="datetime",
        right_on="datetime",
    )

    one_week_df.fillna(0, inplace=True)

    # get weekdays for plotting purposes
    one_week_df["weekday"] = one_week_df["datetime"].dt.strftime("%A")
    one_week_df.sort_values(by="datetime", inplace=True)

    one_week_df.rename(
        columns={
            "exerciseLoad_x": "exerciseLoadMean",
            "exerciseLoad_y": "exerciseLoadPlayer",
        },
        inplace=True,
    )

    return one_week_df


def load_management_individual_player_load_rpe(
    player, df=summary_per_training_player, rpe_df=full_rpe_df
):
    """
    calculates all the needed data for a single player selection in the load management tab
    """
    df2 = df.copy()
    rpe_df2 = rpe_df.copy()

    # select player data
    player_df = df2[df2["name"] == player]
    player_df.sort_values(by="datetime", ascending=True, inplace=True)

    load_df = player_df[["datetime", "name", "exerciseLoad"]]
    load_df["datetime"] = pd.to_datetime(load_df["datetime"], errors="raise")
    load_df["datetime"] = load_df["datetime"].dt.date

    # select rpe data for player
    rpe_player_df = rpe_df2[rpe_df2["name"] == player]
    rpe_player_df["datetime"] = pd.to_datetime(
        rpe_player_df["datetime"], errors="raise"
    )
    rpe_player_df["datetime"] = rpe_player_df["datetime"].dt.date

    rpe_player_df = rpe_player_df.groupby("datetime").mean().reset_index()
    rpe_player_df["name"] = player

    # merge load and rpe data
    merged_rpe_df = pd.merge(
        load_df,
        rpe_player_df,
        how="left",
        right_on=["name", "datetime"],
        left_on=["name", "datetime"],
    )

    # get data for monotony, strain, load chart
    current_date = datetime.datetime.strptime(DATE_STR, "%m-%d-%Y").date()
    start_date = current_date - pd.to_timedelta(30, unit="d")
    date_range = pd.date_range(start_date, current_date)

    # we need to calculate the ac_ratio, monotony and strain on a rolling bases per day
    num_days_week = 6
    num_days_chronic = 21

    ac_monotony_dict = {}
    for date in date_range:

        # filter load_df by the dates
        start_date_week = date - pd.to_timedelta(num_days_week - 1, unit="d")
        date_range = pd.date_range(start_date_week, date)
        date_range_df = pd.DataFrame({"datetime": date_range})
        date_range_df["datetime"] = date_range_df["datetime"].dt.date

        player_week_load_df = pd.merge(
            date_range_df, load_df, how="left", left_on="datetime", right_on="datetime"
        )
        player_week_load_df["exerciseLoad"].fillna(0, inplace=True)
        player_week_load_df["name"].fillna(player, inplace=True)

        mean_load_week = player_week_load_df["exerciseLoad"].mean()
        std_load_week = player_week_load_df["exerciseLoad"].std()

        # rolling AC Ratio
        start_date_chronic = date - pd.to_timedelta(num_days_chronic - 1, unit="d")
        date_range_chronic = pd.date_range(start_date_chronic, date)
        date_range_chronic_df = pd.DataFrame({"datetime": date_range_chronic})
        date_range_chronic_df["datetime"] = date_range_chronic_df["datetime"].dt.date

        player_chronic_df = pd.merge(
            date_range_chronic_df,
            load_df,
            how="left",
            left_on="datetime",
            right_on="datetime",
        )
        player_chronic_df["exerciseLoad"].fillna(0, inplace=True)
        player_chronic_df["name"].fillna(player, inplace=True)

        mean_load_chronic = player_chronic_df["exerciseLoad"].mean()

        ac_monotony_dict[date] = [mean_load_week, std_load_week, mean_load_chronic]

    # turn dictionary into df and rename columns
    ac_monotony_df = pd.DataFrame.from_dict(ac_monotony_dict, orient="index")
    ac_monotony_df.reset_index(inplace=True)
    ac_monotony_df.rename(
        columns={
            "index": "datetime",
            0: "mean_load_week",
            1: "std_load_week",
            2: "mean_load_chronic",
        },
        inplace=True,
    )

    # calculate final statistics
    ac_monotony_df["monotony_week"] = (
        ac_monotony_df["mean_load_week"] / ac_monotony_df["std_load_week"]
    )
    ac_monotony_df["strain"] = (
        ac_monotony_df["mean_load_week"] * ac_monotony_df["monotony_week"]
    )
    ac_monotony_df["ac_ratio"] = (
        ac_monotony_df["mean_load_week"] / ac_monotony_df["mean_load_chronic"]
    )
    ac_monotony_df = ac_monotony_df.round(2)
    ac_monotony_df.sort_values(by="datetime", ascending=False, inplace=True)

    return merged_rpe_df, ac_monotony_df


def load_management_individual_player_ima(
    player, per_10_bit, dfs=[summary_per_training_player, summary_per_training_per_10]
):
    """
    Retrieves the ima events depending on whether per_10_bit is 0 or not
    """
    if per_10_bit == 0:
        df = dfs[0].copy()
    else:
        df = dfs[1].copy()

    player_df = df[df["name"] == player]
    player_df.sort_values(by="datetime", ascending=True, inplace=True)

    acc_dec_df = player_df[
        ["datetime", "name", "accMidAndHighCount", "decMidAndHighCount"]
    ]
    acc_dec_df = acc_dec_df.round(2)

    left_right_turns_df = player_df[
        ["datetime", "name", "leftTurnMidAndHighCount", "rightTurnMidAndHighCount"]
    ]
    left_right_turns_df = left_right_turns_df.round(2)

    return acc_dec_df, left_right_turns_df


def compose_groupby_session_df(df=session_summary_df):
    """
    Takes the session_per_10_df as a parameter and returns a groupby per session_name with means
    """
    df2 = df.copy()
    final_df = df2.groupby("session_name").mean().reset_index()

    # only keep relevant columns
    final_df = final_df[
        [
            "session_name",
            "exerciseLoad",
            "leftTurnMidAndHighCount",
            "rightTurnMidAndHighCount",
            "accMidAndHighCount",
            "decMidAndHighCount",
        ]
    ]

    # round numbers
    final_df = final_df.round(2)

    return final_df


def compose_groupby_session_and_player_df(session_names, df=session_summary_df):
    """
    Takes the session_per_10_df as a parameter and returns a groupby per session_name and player with means.
    Takes a list of parameters, which are the selected session_names from the table and returns data for those sessions

    """
    df2 = df.copy()
    groupby_df = df2.groupby(["name", "session_name"]).mean().reset_index()

    # selection based on session_names
    final_df = groupby_df[groupby_df["session_name"].isin(session_names)]

    return final_df


def compose_current_optimal_load(
    ac_lower_bound, ac_upper_bound, date, selected_players, df=session_summary_df
):
    """
    Calculates the current optimal load per player
    """
    df2 = df.copy()

    players = [
        "Kiki FLEUREN",
        "Zoë SLAGTER",
        "Fleur KUIJT",
        "Karin KUIJT",
        "Richelle VAN DER KEIJL",
        "Esther FOKKE",
        "Noor DRIESSEN",
        "Loyce BETTONVIL",
        "Ilse KUIJT",
        "Jill BETTONVIL",
        "Emese HOF",
        "Natalie VAN DEN ADEL",
        "Jacobien KLERX",
        "Charlotte VAN KLEEF",
        "Rowie JONGELING",
        "Janine Guijt",
    ]

    common_players = [p for p in players if p in selected_players]

    optimal_load = np.full((1, len(common_players)), 100).flatten()

    optimal_load_df = pd.DataFrame(
        {
            "name": common_players,
            "optimal_load": optimal_load,
            "optimal_acc": optimal_load,
            "optimal_dec": optimal_load,
            "optimal_left": optimal_load,
            "optimal_right": optimal_load,
        }
    )

    daily_optimal_load = daily_optimal_load_calculation(
        ac_lower_bound, ac_upper_bound, date
    )
    daily_optimal_load = daily_optimal_load[
        ["name", "optimal_load_upper", "optimal_load_lower"]
    ]
    optimal_load_df = pd.merge(
        optimal_load_df, daily_optimal_load, how="left", left_on="name", right_on="name"
    )

    optimal_load_df.fillna(0, inplace=True)

    return optimal_load_df


def daily_optimal_load_calculation(
    ac_lower_bound, ac_upper_bound, date_str, df=summary_per_training_player
):
    """
    Calculates the optimal load for each player based on the AC ratio for each player
    """
    df2 = df.copy()
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()

    df2["datetime"] = pd.to_datetime(df2["datetime"], errors="raise")
    df2["datetime"] = df2["datetime"].dt.date

    # define acute and chronic day intervals
    num_days_acute = 6
    num_days_chronic = 21

    # find the dates
    start_date_acute = date - pd.to_timedelta(num_days_acute - 1, unit="d")
    start_date_chronic = date - pd.to_timedelta(num_days_chronic - 1, unit="d")

    # setup filter masks
    mask_acute = (df2["datetime"] >= start_date_acute) & (df2["datetime"] <= date)
    mask_chronic = (df2["datetime"] >= start_date_chronic) & (df2["datetime"] <= date)

    # filter acute data
    acute_df = df2.loc[mask_acute]
    acute_df = acute_df.groupby("name")["exerciseLoad"].sum().reset_index()
    acute_df.rename(columns={"exerciseLoad": "exerciseLoadAcute"}, inplace=True)

    # filter chronic data
    chronic_df = df2.loc[mask_chronic]
    chronic_df = chronic_df.groupby("name")["exerciseLoad"].sum().reset_index()
    chronic_df.rename(columns={"exerciseLoad": "exerciseLoadChronic"}, inplace=True)

    # merge acute and chronic
    acute_chronic_df = pd.merge(
        acute_df, chronic_df, how="left", left_on="name", right_on="name"
    )

    # this is a specific calculation to define the upper and lower bounds of suggested load
    acute_chronic_df["analytical_numerator_upper"] = (
        num_days_acute / num_days_chronic
    ) * ac_upper_bound * acute_chronic_df["exerciseLoadChronic"] - acute_chronic_df[
        "exerciseLoadAcute"
    ]
    acute_chronic_df["optimal_load_upper"] = (
        acute_chronic_df["analytical_numerator_upper"]
        / (1 - (num_days_acute / num_days_chronic) * ac_upper_bound)
    ).where(acute_chronic_df["analytical_numerator_upper"] >= 0, 0)

    acute_chronic_df["analytical_numerator_lower"] = (
        num_days_acute / num_days_chronic
    ) * ac_lower_bound * acute_chronic_df["exerciseLoadChronic"] - acute_chronic_df[
        "exerciseLoadAcute"
    ]
    acute_chronic_df["optimal_load_lower"] = (
        acute_chronic_df["analytical_numerator_lower"]
        / (1 - (num_days_acute / num_days_chronic) * ac_lower_bound)
    ).where(acute_chronic_df["analytical_numerator_lower"] >= 0, 0)

    return acute_chronic_df


def compose_expected_monotony(date_str, load_df, df=summary_per_training_player):
    """
    Parameter is a df with the current load that is being done by players, for those players it goes back and calculates current monotony
    """
    df2 = df.copy()
    df2 = df2[["name", "datetime", "exerciseLoad"]]

    df2["datetime"] = pd.to_datetime(df2["datetime"], errors="raise")
    df2["datetime"] = df2["datetime"].dt.date

    date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
    players = load_df["name"].tolist()

    load_df["datetime"] = date
    load_df.rename(columns={"base_load": "exerciseLoad"}, inplace=True)
    load_df = load_df[["name", "datetime", "exerciseLoad"]]

    num_days_week = 6

    start_date_monotony = date - pd.to_timedelta(num_days_week - 1, unit="d")

    mask_monotony = (df2["datetime"] >= start_date_monotony) & (df2["datetime"] <= date)

    date_df = df2.loc[mask_monotony]
    date_df = date_df[date_df["name"].isin(players)]

    date_df = pd.concat([date_df, load_df], ignore_index=True)
    date_df.fillna(0, inplace=True)

    std_df = date_df.groupby("name")["exerciseLoad"].std().reset_index()
    std_df.rename(columns={"exerciseLoad": "std_load"}, inplace=True)
    mean_load_df = date_df.groupby("name")["exerciseLoad"].mean().reset_index()
    mean_load_df.rename(columns={"exerciseLoad": "mean_load"}, inplace=True)

    monotony_df = pd.merge(
        std_df, mean_load_df, how="left", left_on="name", right_on="name"
    )
    monotony_df["monotony"] = monotony_df["mean_load"] / monotony_df["std_load"]

    return monotony_df


def compare_find_latest_and_earliest_date(df=session_per_10_df):
    """
    Finds the earliest and latest available date in the data to update the calendar selection in comparison tab
    """
    df2 = df.copy()
    min_date = df2["datetime"].min()
    max_date = df2["datetime"].max()
    return min_date, max_date


def compare_find_drills_from_date(date, df=session_per_10_df):
    """
    Returns a list of the drills that happened on that day
    """
    df2 = df.copy()
    df_by_date = df2[df2["datetime"].astype(str) == date]
    drill_names = df_by_date["session_name"].unique().tolist()

    return drill_names


def compare_find_data_for_selected_drills(date, drills, players, df=session_per_10_df):
    """
    Returns the data for the selected drills
    """
    df2 = df.copy()

    # check if there is only one drill
    if isinstance(drills, str):
        selected_drills = [drills]
    else:
        selected_drills = drills

    # check if there is only one player
    if isinstance(players, str):
        selected_players = [players]
    else:
        selected_players = players

    df_by_date = df2[df2["datetime"].astype(str) == date]
    df_by_drills = df_by_date[df_by_date["session_name"].isin(selected_drills)]

    df_by_drills_and_players = df_by_drills[df_by_drills["name"].isin(selected_players)]

    parameters = [
        "name",
        "session_name",
        "exerciseLoad",
        "leftTurnMidAndHighCount",
        "rightTurnMidAndHighCount",
        "accMidAndHighCount",
        "decMidAndHighCount",
    ]

    df_by_drills_and_players = df_by_drills_and_players[parameters]

    return df_by_drills_and_players


def select_data_table(
    start_date_str,
    end_date_str,
    per_10_bit,
    dfs=[summary_per_training_player, summary_per_training_per_10],
):
    """
    queries data for the player table in the select tab based on time and absolute or per 10 minute data
    """
    if per_10_bit == 0:
        df = dfs[0].copy()
    else:
        df = dfs[1].copy()

    df["datetime"] = pd.to_datetime(df["datetime"], errors="raise")
    df["datetime"] = df["datetime"].dt.date

    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # select df by time
    mask_time = (df["datetime"] >= start_date) & (df["datetime"] <= end_date)

    time_df = df.loc[mask_time]

    player_data_df = (
        time_df.groupby("name")[
            [
                "exerciseLoad",
                "accMidCount",
                "accHighCount",
                "decMidCount",
                "decHighCount",
                "leftTurnMidCount",
                "leftTurnHighCount",
                "rightTurnMidCount",
                "rightTurnHighCount",
                "leftTurnMidAndHighCount",
                "rightTurnMidAndHighCount",
                "accMidAndHighCount",
                "decMidAndHighCount",
            ]
        ]
        .mean()
        .reset_index()
    )

    player_data_df["total_Acc_Dec"] = (
        player_data_df["accMidAndHighCount"] + player_data_df["accMidAndHighCount"]
    )
    player_data_df["totalTurns"] = (
        player_data_df["leftTurnMidAndHighCount"]
        + player_data_df["rightTurnMidAndHighCount"]
    )

    player_data_df = player_data_df.round(2)

    return player_data_df


## don't have to worry about this one
def shooting_right_eye_data(
    eye_df=right_eye_df, shooting_df=shooting_df, df=summary_per_training_per_10
):
    """
    merges the shooting and right eye data
    """
    df2 = df.copy()
    df2 = df2[
        [
            "name",
            "leftTurnMidCount",
            "leftTurnHighCount",
            "rightTurnMidCount",
            "rightTurnHighCount",
            "accMidCount",
            "accHighCount",
            "decMidCount",
            "decHighCount",
        ]
    ]
    player_mean_df = df2.groupby("name").mean().reset_index()

    eye_shooting_df = pd.merge(
        shooting_df, eye_df, how="left", left_on="name", right_on="name"
    )

    # ONCE THERE IS MORE DATA NEED TO CHANGE IT TO GROUPBY DATE MEAN #
    eye_shooting_df.loc["mean"] = eye_shooting_df.mean()
    eye_shooting_df.loc["mean", "name"] = "mean"

    eye_shooting_df["TEST_DATE"] = pd.to_datetime(
        eye_shooting_df["TEST_DATE"], errors="raise"
    )

    eye_shooting_df = pd.merge(
        eye_shooting_df, player_mean_df, how="left", left_on="name", right_on="name"
    )
    # eye_shooting_df['TEST_DATE'] = eye_shooting_df['TEST_DATE'].date()

    return eye_shooting_df
