import pandas as pd
import matplotlib.pyplot as plt

# load rankings data
wood_winners = pd.read_csv('Golden_Ticket_Award_Winners_Wood.csv')
steel_winners = pd.read_csv('Golden_Ticket_Award_Winners_Steel.csv')
print("wood winners: ")
# print(wood_winners.head())
print("steel winners: ")
# print(steel_winners.head())

# function to plot rankings over time for 1 roller coaster
def rank_history(name, park):
    # select data corresponding to the query
    wood_rank = wood_winners[(wood_winners.Name == name) & (wood_winners.Park == park)]
    steel_rank = steel_winners[(steel_winners.Name == name) & (steel_winners.Park == park)]
    # select the ranking the roller coaster in question is featured in
    if len(wood_rank.index) != 0:
        ro_co_rank = wood_rank
    elif len(steel_rank.index) != 0: 
        ro_co_rank = steel_rank
    else:
        print(name + "is a looser")
    # the years will be the x-axis and the ranks the y-axis
    years = range(2013, 2019)
    rank_list = ro_co_rank.Rank.tolist()
    # plot the line graph
    plt.plot(years, rank_list, color = 'purple', marker = 'o')
    # improve readability of graph
    plt.title("Rank of " + name + "roller coaster, " + park + " park (2013-2018)")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.subplot().set_yticks(rank_list)
    # invert the y-axis
    plt.gca().invert_yaxis()
    plt.show()
    
rank_history('El Toro', 'Six Flags Great Adventure')
plt.clf()
