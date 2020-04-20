import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load rankings data
wood_winners = pd.read_csv('Golden_Ticket_Award_Winners_Wood.csv')
steel_winners = pd.read_csv('Golden_Ticket_Award_Winners_Steel.csv')
print("wood winners: ")
#print(wood_winners.head())
print("steel winners: ")
#print(steel_winners.head())

# function to plot rankings over time for 1 roller coaster
def rank_history(name, park):
    
    #select data corresponding to the query
    wood_rank = wood_winners[(wood_winners.Name == name) & (wood_winners.Park == park)]
    steel_rank = steel_winners[(steel_winners.Name == name) & (steel_winners.Park == park)]
    
    #select the ranking the roller coaster in question is featured in
    if len(wood_rank.index) != 0:
        ro_co_rank = wood_rank
    elif len(steel_rank.index) != 0: 
        ro_co_rank = steel_rank
    else:
        print(name + "is a looser")
        
    #the years will be the x-axis and the ranks the y-axis
    years = range(2013, 2019)
    rank_list = ro_co_rank.Rank.tolist()
    
    #plot the line graph
    plt.plot(years, rank_list, color = 'purple', marker = 'o')
    
    #improve readability of graph
    plt.title("Rank of " + name + "roller coaster, " + park + " park (2013-2018)")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.subplot().set_yticks(rank_list)
    
    #invert the y-axis
    plt.gca().invert_yaxis()
    plt.show()
    
#rank_history('El Toro', 'Six Flags Great Adventure')
plt.clf()

# write function to plot rankings over time for 2 roller coasters here:
def rank_hist_2(name1, park1, name2, park2, ranking):
    
    #select data corresponding to the query
    ro_co_1_rank = ranking[(ranking.Name == name1) & (ranking.Park == park1)]
    ro_co_2_rank = ranking[(ranking.Name == name2) & (ranking.Park == park2)]

    #select the ranking the roller coaster in question is featured in
    if len(ro_co_1_rank.index) == 0:
        print(name1 + "is a looser")
    if len(ro_co_2_rank.index) == 0:
        print(name2 + "is a looser")  

    #the years will be the x-axis and the ranks the y-axis
    years = range(2013, 2019)

    #select the endpoints of the rankings
    lowest_rank_1 = int(np.max(ro_co_1_rank.Rank.tolist()))
    lowest_rank_2 = int(np.max(ro_co_2_rank.Rank.tolist()))
    highest_rank_1 = int(np.min(ro_co_1_rank.Rank.tolist()))
    highest_rank_2 = int(np.min(ro_co_2_rank.Rank.tolist()))

    max_rank = np.maximum(lowest_rank_1, lowest_rank_2)
    min_rank = np.minimum(highest_rank_1, highest_rank_1)
    rank_list = range((min_rank),(max_rank + 1))

    #plot the line graph
    plt.plot(years, ro_co_1_rank.Rank.tolist(), color = 'purple', marker = 'o')
    plt.plot(years, ro_co_2_rank.Rank.tolist(), color = 'blue', marker = 'o', linestyle = ":")

    #improve readability of graph
    plt.title("Ranks of " + name1 + " and " + name2 + " (2013-2018)")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.subplot().set_yticks(rank_list)
    
    #invert the y-axis
    plt.gca().invert_yaxis()
    plt.show()

rank_hist_2('El Toro', 'Six Flags Great Adventure', 'Ravine Flyer II' ,'Waldameer', wood_winners)

plt.clf()
