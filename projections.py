import unicodedata
import NBA_TEAMS
import pandas as pd
from unidecode import unidecode
from pydfs_lineup_optimizer import get_optimizer, Site, Sport, Player, CSVLineupExporter, TeamStack


def combine_stats(df_team_stats, df_player_stats, df_boxscores):
    player_stats = df_player_stats[
        ['slug', 'name', 'team', 'MIN/G', 'FPS/G', 'FPS/M', 'Fouls/G', 'player_efficiency_rating', 'win_shares',
         'total_rebound_percentage',
         'assist_percentage', 'offensive_box_plus_minus', 'box_plus_minus']]
    # df_boxscores = pd.merge(df_boxscores, player_stats, on=['slug'])

    # numerical_columns = [col for col in df_player_stats.columns if
    #                      (df_player_stats[col].dtype == 'int64' or df_player_stats[col].dtype == 'float64')]
    # numerical_data = df_player_stats[numerical_columns].describe().loc[['min', 'max', 'mean', '50%'], :]

    players_playing = df_boxscores['slug'].unique()
    temp_df = pd.DataFrame()
    for player in players_playing:
        player_boxscores = (df_boxscores.loc[df_boxscores['slug'] == player]).sort_values(by=['date'], ascending=True)
        player_boxscores = player_boxscores.set_index('date')
        if len(player_boxscores.index) >= 3:
            player_avg_last3 = player_boxscores.tail(3)
            player_avg_last3_points = player_avg_last3['Fantasy Points Scored'].mean()
            player_avg_last3_min = player_avg_last3['minutes_played'].mean()
            player_avg_last3_ATO = player_avg_last3['A/TO'].mean()
            player_avg_last3_Three = player_avg_last3['ThreePointRate'].mean()

            df = pd.DataFrame({'slug': player,
                               'avg_points_last3': player_avg_last3_points, 'avg_min_last3': player_avg_last3_min,
                               'avg_ato_last3': player_avg_last3_ATO, 'avg_three_last3': player_avg_last3_Three},
                              index=[0])
            temp_df = temp_df.append(df)

    player_stats = pd.merge(player_stats, temp_df, on=['slug'])
    return player_stats


def set_starter_minutes(df, starters):
    # removing accents and other characters in name column of dataframe
    df['name'] = df['name'].str.normalize('NFKD') \
        .str.encode('ascii', errors='ignore') \
        .str.decode('utf-8')
    players = list()
    # print(starters)
    for team in starters.keys():
        team_starters = starters[team].starters
        for player in team_starters:
            # print(player)
            players.append(player)
    # SET STARTERS
    # df = df[df['name'].isin(players)]
    df['minutes'] = df.apply(lambda row: round(row.avg_min_last3), axis=1)
    df = df.loc[df['minutes'] >= 15]
    df['Projected Score'] = df.apply(
        lambda row: round(0.30 * row['FPS/G'] + 0.45 * (row['avg_points_last3']) + (
                0.25 * (row['minutes'] * row['FPS/M'])), 2), axis=1)

    df = df.groupby(['name', 'team']).mean()
    df = df.reset_index()
    df.to_excel("fantasy_players_table.xlsx", sheet_name='Sheet_name_1')
    print("Fantasy Players Table exported!")
    return df


def set_boosters(df, team_stats, df_matchup):
    # Rating Player Season Attributes and assigning grading score of 'MVP', 'ALL STAR', 'POTENTIAL', 'AVERAGE', 'MEH', 'TRASH'
    df['fantasy_grade'] = pd.cut(x=df['FPS/G'], bins=4, labels=[5, 4, 1, 0])
    df['fantasy_per_min_grade'] = pd.cut(x=df['FPS/M'], bins=4, labels=[5, 4, 1, 0])
    df['efficiency_grade'] = pd.cut(x=df['player_efficiency_rating'], bins=4, labels=[4, 3, 1, 0])
    df['win_shares_grade'] = pd.cut(x=df['win_shares'], bins=4, labels=[4, 3, 1, 0])
    df['rebound_grade'] = pd.cut(x=df['total_rebound_percentage'], bins=4, labels=[4, 3, 2, 1])
    df['assist_grade'] = pd.cut(x=df['assist_percentage'], bins=4, labels=[4, 3, 2, 1])
    df['o_box_pm_grade'] = pd.cut(x=df['offensive_box_plus_minus'], bins=4, labels=[4, 3, 2, 1])
    df['box_plus_minus_grade'] = pd.cut(x=df['box_plus_minus'], bins=4, labels=[4, 3, 1, 0])
    df['min_per_game_grade'] = pd.cut(x=df['MIN/G'], bins=4, labels=[5, 4, 1, 0])
    df['Overall Score'] = df.apply(
        lambda row: (row['fantasy_grade'] + row['fantasy_per_min_grade'] + row['efficiency_grade'] + row[
            'win_shares_grade'] + row['rebound_grade'] + row['assist_grade'] +
                     row['o_box_pm_grade'] + row['box_plus_minus_grade'] + row['min_per_game_grade']), axis=1)

    df['Overall Grade'] = pd.cut(x=df['Overall Score'], bins=6,
                                 labels=['MVP', 'ALL STAR', 'POTENTIAL', 'AVERAGE', 'MEH', 'TRASH'])
    df = df.loc[(df['Overall Grade'] != 'TRASH')]

    df['Projected Score'] = df.apply(
        lambda row: round(row['Projected Score'] * (1 + 0.05), 2) if row['Overall Grade'] == 'MVP' else row[
            'Projected Score'], axis=1)
    df['Projected Score'] = df.apply(
        lambda row: round(row['Projected Score'] * (1 + 0.08), 2) if row['Overall Grade'] == 'ALL STAR' else row[
            'Projected Score'], axis=1)
    df['Projected Score'] = df.apply(
        lambda row: round(row['Projected Score'] * (1 + 0.06), 2) if row['Overall Grade'] == 'POTENTIAL' else row[
            'Projected Score'], axis=1)
    df['Projected Score'] = df.apply(
        lambda row: round(row['Projected Score'] * (1 + 0.03), 2) if row['Overall Grade'] == 'AVERAGE' else row[
            'Projected Score'], axis=1)
    df['Projected Score'] = df.apply(
        lambda row: round(row['Projected Score'] * (1 - 0.05), 2) if row['Overall Grade'] == 'MEH' else row[
            'Projected Score'], axis=1)

    # HOT OR COOL PLAYER GRADING

    df['points_streak'] = df.apply(lambda row: row['avg_points_last3'] - row['FPS/G'], axis=1)
    df['points_streak_grade'] = df.apply(lambda row: 2 if row['points_streak'] >= 1 else 0, axis=1)
    df['points_streak_grade'] = df.apply(lambda row: 1 if 0 <= row['points_streak'] < 1 else row['points_streak_grade'],
                                         axis=1)
    df['minutes_streak'] = df.apply(lambda row: row['avg_min_last3'] - row['MIN/G'], axis=1)
    df['minutes_streak_grade'] = df.apply(lambda row: 1 if row['minutes_streak'] >= 0 else 0, axis=1)
    df['minutes_streak_grade'] = df.apply(
        lambda row: 1 if 0 <= row['minutes_streak'] < 1 else row['points_streak_grade'], axis=1)
    df['temp_score'] = df.apply(lambda row: row['points_streak_grade'] + row['minutes_streak_grade'], axis=1)
    df['player_temp'] = pd.cut(x=df['temp_score'], bins=3, labels=['COLD', 'NEUTRAL', 'HOT'])

    remove_meh = df.loc[
        (df['player_temp'] == 'COLD') & ((df['Overall Grade'] == 'MEH') | (df['Overall Grade'] == 'AVERAGE'))].index
    df.drop(remove_meh, inplace=True)

    df['Projected Score'] = df.apply(
        lambda row: round(
            (row['Projected Score'] * (1 + 0.05)) if row['player_temp'] == 'HOT' else row['Projected Score'], 2),
        axis=1)
    # Matchup boosters
    final_columns = ['MOV', 'ORtg', 'DRtg', 'Pace', 'FTr', '3PAr', 'EFG%', 'TOV%', 'ORB%', 'FT/FGA', 'oppEFG%',
                     'oppTOV%',
                     'DRB%', 'oppFT/FGA']

    team_stats['Pace Rank'] = team_stats['Pace'].rank(method='max')
    team_stats['Offensive Rank'] = team_stats['ORtg'].rank(method='max')
    team_stats['Defensive Rank'] = team_stats['DRtg'].rank(method='max')
    team_stats['MOV Rank'] = team_stats['MOV'].rank(method='max', ascending=False)
    team_stats['Freethrow Rank'] = team_stats['FTr'].rank(method='max')
    team_stats['Threepoint Rank'] = team_stats['3PAr'].rank(method='max')
    team_stats['Forced EFG Rank'] = team_stats['oppEFG%'].rank(method='max', ascending=False)
    team_stats['Turnover Rank'] = team_stats['TOV%'].rank(method='max', ascending=False)
    team_stats['Forced Turnover Rank'] = team_stats['oppTOV%'].rank(method='max', ascending=False)
    team_stats['Rebound Rank'] = team_stats['DRB%'].rank(method='max', ascending=False)

    team_stats['O_Rank'] = team_stats.apply(
        lambda row: row['Pace Rank'] + row['Offensive Rank'] + row['Freethrow Rank'] + row[
            'Threepoint Rank'], axis=1)

    team_stats['D_Rank'] = team_stats.apply(
        lambda row: row['Defensive Rank'] + row['MOV Rank'] + row['Forced EFG Rank'] + row[
            'Forced Turnover Rank'], axis=1)

    team_rankings = team_stats[['Team', 'O_Rank', 'D_Rank']]

    df_matchup = pd.merge(df_matchup, team_rankings, left_on='home_team', right_on='Team', how='left')
    df_matchup = pd.merge(df_matchup, team_rankings, left_on='away_team', right_on='Team', suffixes=('_team', '_opp'),
                          how='left')
    # print(df_matchup)
    df_matchup['Heat_Rank'] = df_matchup.apply(
        lambda row: (row['O_Rank_team'] + row['O_Rank_opp']), axis=1)

    df_matchup['home_vs_opp'] = df_matchup.apply(lambda row: (row['O_Rank_team'] + row['D_Rank_opp']), axis=1)
    df_matchup['opp_vs_home'] = df_matchup.apply(lambda row: (row['O_Rank_opp'] + row['D_Rank_team']), axis=1)
    df_matchup['Matchup_Rank'] = df_matchup.apply(lambda row: abs(row['home_vs_opp'] - row['opp_vs_home']), axis=1)
    df_matchup['Closeness Number Rank'] = df_matchup['Matchup_Rank'].rank(method='max', ascending=True)
    df_matchup['Overall_Rank'] = df_matchup['Heat_Rank'].rank(method='max', ascending=False)

    df_matchup['Final_Rank_number'] = df_matchup.apply(lambda row: row['Closeness Number Rank'] + row['Overall_Rank'],
                                                       axis=1)
    df_matchup['Final_Rank'] = pd.cut(df_matchup['Final_Rank_number'], bins=3, labels=['GOOD', 'ALRIGHT', 'MEH'])

    df_matchup['home_team'] = df_matchup.apply(lambda row: str.upper(row['home_team']), axis=1)
    df_matchup['away_team'] = df_matchup.apply(lambda row: str.upper(row['away_team']), axis=1)

    good_list = df_matchup.loc[(df_matchup['Final_Rank'] == 'GOOD')]
    alright_list = df_matchup.loc[(df_matchup['Final_Rank'] == 'ALRIGHT')]
    meh_list = df_matchup.loc[(df_matchup['Final_Rank'] == 'MEH')]

    final_good_list = (good_list['home_team'].tolist()) + (good_list['away_team'].tolist())
    final_alright_list = (alright_list['home_team'].tolist()) + (alright_list['away_team'].tolist())
    final_meh_list = (meh_list['home_team'].tolist()) + (meh_list['away_team'].tolist())

    final_meh_list = set_abreviation(final_meh_list)
    final_alright_list = set_abreviation(final_alright_list)
    final_good_list = set_abreviation(final_good_list)

    # df = df[(df['team'].isin(final_team_opp)) | (df['team'].isin(final_team_home))]
    # print(df)

    return df, final_good_list, final_alright_list, final_meh_list


def set_abreviation(lst):
    final_list = list()
    for matchup in lst:
        final_list.append(NBA_TEAMS.get_NBA_abrev(matchup))
    return final_list


def optimize_lineup(df, good_list, alright_list, meh_list):
    optimizer = get_optimizer(Site.FANDUEL, Sport.BASKETBALL)
    optimizer.load_players_from_csv("fanduel.csv")

    df['name'] = df.apply(lambda row: (str.split(row['name'], ' Jr.')[0]), axis=1)
    for player in optimizer.players:
        if player.full_name in df['name'].unique():
            projected_score = df.loc[
                (df['name'] == player.full_name) & (df['team'] == NBA_TEAMS.find_NBA_abrev(player.team))][
                'Projected Score'].tolist()
            if len(projected_score) > 0:
                player.fppg = projected_score[0]
            else:
                player.fppg = 0

            # print(f"{player.full_name:}{projected_score}")
        else:
            player.fppg = 0

    optimizer.set_min_salary_cap(60000)
    optimizer.set_max_repeating_players(2)
    optimizer.add_stack(TeamStack(2, for_teams=good_list))
    optimizer.add_stack(TeamStack(2, for_teams=alright_list))
    optimizer.add_stack(TeamStack(1, for_teams=meh_list))
    # for lineup in optimizer.optimize(n=50):
    #     print(lineup)
    #     print(lineup.players)  # list of players
    #     print(lineup.fantasy_points_projection)
    #     print(lineup.salary_costs)

    exporter = CSVLineupExporter(optimizer.optimize(n=50))
    exporter.export('lineups.csv')
    print("Lineups optimized and exported!")
