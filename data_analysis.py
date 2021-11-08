import pandas as pd
import matplotlib.pyplot as plt
import math

#load data from csv to dataframe in pandas
df = pd.read_csv('shots_data.csv')

#create squared x and y columns to calculate non-corner threes
df['x_sqd'] = df['x'].pow(2)
df['y_sqd'] = df['y'].pow(2)

#create column with distance from basketball hoop
df['dist'] = (df['x_sqd'] + df['y_sqd'])**(1/2)

#Helper Function section
def get_team_fg(df,team):
    return df[df['team'] == team]

def calculate_noncorner_threes(df):
    #to find approximation for beginning of arc I used pythagorean theorem to calculate the y coordinate (approx. 8.95ft)
    #non-corner threes are defined by either:
    # 1) x,y coordinates [x<=-22 or x>=22, y>7.8] (i.e. area before arc)
    # 2) 23.75 ft away from the basket (Euclidean distance)
    return df.loc[(((df['x'] >= 22) | (df['x'] <= -22)) & (df['y']>7.8)) | ((df['dist'] >= 23.75) & (df['y']>8.95))]

def calculate_corner_threes(df):
    #corner threes are defined by x,y coordinates [x<=-22 or x>=22, y<=7.8]
    return df[(df['y'] <= 7.8) & ((df['x'] >= 22) |(df['x'] <= -22))]

def calculate_two_pointers(df):
    #two pointers are defined by shots by the coordinates [-22<x<22 , y < 8.95] 
    #and with distance less than 23.75 feet and y>8.95 (shots within arc)
    return df.loc[((df['x'] < 22) & (df['x'] >= 0) | (df['x'] > -22) & (df['x'] <= 0)) & (df['y']<8.95) |((df['y'] > 8.95) & (df['dist'] < 23.75))]

def calculate_eFG(fgm,threes_made,fga):
    egper_float = ((fgm +(.5*threes_made))/fga) *100

    #round to nearest hundreth
    return round(egper_float,2)

def calculate_fgper(fgm,fga):
    fg_float = (fgm/fga) * 100
    #round to nearest hundreth
    return round(fg_float,2)

def calculate_made_plus_total(df):
    #.shape returns a tuple with the rows and columns, respectively
    total_shots = df.shape[0]

    #grab all row where fgmade equals 1
    made_shots = df.loc[df['fgmade'] == 1].shape[0]

    return (total_shots,made_shots)

#Let's get down to business!

#seperate teams by name
team_a_fgs = get_team_fg(df,'Team A')
team_b_fgs = get_team_fg(df,'Team B')

#calculate each team's corner three efg%
team_a_corner_3s = calculate_corner_threes(team_a_fgs)
team_a_corner_3s_total, team_a_corner_3s_made = calculate_made_plus_total(team_a_corner_3s)
team_a_corner_3s_efper = calculate_eFG(team_a_corner_3s_made,team_a_corner_3s_made,team_a_corner_3s_total)

team_b_corner_3s = calculate_corner_threes(team_b_fgs)
team_b_corner_3s_total, team_b_corner_3s_made = calculate_made_plus_total(team_b_corner_3s)
team_b_corner_3s_efper = calculate_eFG(team_b_corner_3s_made,team_b_corner_3s_made,team_b_corner_3s_total)

#calculate each team's corner three fg%
team_a_corner_3s_fgper = calculate_fgper(team_a_corner_3s_made,team_a_corner_3s_total)
team_b_corner_3s_fgper = calculate_fgper(team_b_corner_3s_made,team_b_corner_3s_total)

#calculate each team's non-noncorner three efg%
team_a_noncorner_3s = calculate_noncorner_threes(team_a_fgs)
team_a_noncorner_3s_total, team_a_noncorner_3s_made = calculate_made_plus_total(team_a_noncorner_3s)
team_a_noncorner_3s_efper = calculate_eFG(team_a_noncorner_3s_made,team_a_noncorner_3s_made,team_a_noncorner_3s_total)

team_b_noncorner_3s = calculate_noncorner_threes(team_b_fgs)
team_b_noncorner_3s_total, team_b_noncorner_3s_made = calculate_made_plus_total(team_b_noncorner_3s)
team_b_noncorner_3s_efper = calculate_eFG(team_b_noncorner_3s_made,team_b_noncorner_3s_made,team_b_noncorner_3s_total)

#calculate each team's non-corner three fg%
team_a_noncorner_3s_fgper = calculate_fgper(team_a_noncorner_3s_made,team_a_noncorner_3s_total)
team_b_noncorner_3s_fgper = calculate_fgper(team_b_noncorner_3s_made,team_b_noncorner_3s_total)

#calculate each team's 2 pointer efg%
team_a_2ptrs = calculate_two_pointers(team_a_fgs)
team_a_2ptrs_total, team_a_2ptrs_made = calculate_made_plus_total(team_a_2ptrs)
team_a_2ptrs_efper = calculate_eFG(team_a_2ptrs_made,0,team_a_2ptrs_total)

team_b_2ptrs = calculate_two_pointers(team_b_fgs)
team_b_2ptrs_total, team_b_2ptrs_made = calculate_made_plus_total(team_b_2ptrs)
team_b_2ptrs_efper = calculate_eFG(team_b_2ptrs_made,0,team_b_2ptrs_total)

#calculate each team's 2 pointer fg%
team_a_2ptrs_fgper = calculate_fgper(team_a_2ptrs_made,team_a_2ptrs_total)
team_b_2ptrs_fgper = calculate_fgper(team_b_2ptrs_made,team_b_2ptrs_total)

def generate_plots(team_a_efper,team_b_efper,xlabel,ylabel,title,color):
    # Dataset generation
    data_dict = {'Team A':team_a_efper, 'Team B':team_b_efper}
    teams = list(data_dict.keys())
    values = list(data_dict.values())
    fig = plt.figure(figsize = (10, 5))

    # Add labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    #create bars and put both team's ef% in a list for looping
    bars = plt.bar(teams, values, color =color,width = 0.5)
    efpers = [team_a_efper,team_b_efper]
    
    # access the bar attributes to place the text in the appropriate location
    for bar,efper in zip(bars,efpers):
        yval = bar.get_height()
        plt.text(bar.get_x()+.20, yval + .01, str(efper) + "%")

#plot teams fg% from two pointer (we expect this to be the same as eFG%)
generate_plots(team_a_2ptrs_fgper,team_b_2ptrs_fgper,"Teams two pointers fg%","fg% (FGM/FGA) *100","Two Pointers FG%","orange")

#plot teams eFG% for two pointers
generate_plots(team_a_2ptrs_efper,team_b_2ptrs_efper,"Teams two pointers efg%","Efg% ((FGM +(0.5 *3pt))/FGA))","Two Pointers eFG%","orange")

#plot teams FG% for corner threes pointers
generate_plots(team_a_corner_3s_fgper,team_b_corner_3s_fgper,"Teams corner 3 pointers fg%","fg% (FGM/FGA) *100","Corner Threes Pointers FG%","blue")

#plot teams eFG% for corner threes pointers
generate_plots(team_a_corner_3s_efper,team_b_corner_3s_efper,"Teams corner 3 pointers efg%","Efg% ((FGM +(0.5 *3pt))/FGA))","Corner Threes Pointers eFG%","blue")

#plot teams FG% for noncorner threes pointers
generate_plots(team_a_noncorner_3s_fgper,team_b_noncorner_3s_fgper,"Teams non-corner 3 pointers fg%","fg% (FGM/FGA) *100","Non-corner Threes Pointers FG%","blue")

#plot teams eFG% for noncorner threes pointers
generate_plots(team_a_noncorner_3s_efper,team_b_noncorner_3s_efper,"Teams non-corner 3 pointers efg%","Efg% ((FGM +(0.5 *3pt))/FGA))","Non-corner Threes Pointers eFG%","orange")