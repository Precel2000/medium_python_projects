import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load rankings data
wood_winners = pd.read_csv('Golden_Ticket_Award_Winners_Wood.csv')
steel_winners = pd.read_csv('Golden_Ticket_Award_Winners_Steel.csv')

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
    plt.figure()
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

# function to plot rankings over time for 2 roller coasters in the same ranking
def rank_hist_2(name1, park1, name2, park2, ranking):

    #select data corresponding to the query
    ro_co_1_rank = ranking[(ranking.Name == name1) & (ranking.Park == park1)]
    ro_co_2_rank = ranking[(ranking.Name == name2) & (ranking.Park == park2)]

    #check if the roller coaster appeared in the specified ranking
    if len(ro_co_1_rank.index) == 0:
        print(name1 + "is a looser")
    if len(ro_co_2_rank.index) == 0:
        print(name2 + "is a looser")  

    #the years will be the x-axis and the ranks the y-axis
    years = range(2013, 2019)

    #select the endpoints of the rankings (ie the y-axis)
    lowest_rank_1 = int(np.max(ro_co_1_rank.Rank.tolist()))
    lowest_rank_2 = int(np.max(ro_co_2_rank.Rank.tolist()))
    highest_rank_1 = int(np.min(ro_co_1_rank.Rank.tolist()))
    highest_rank_2 = int(np.min(ro_co_2_rank.Rank.tolist()))

    max_rank = np.maximum(lowest_rank_1, lowest_rank_2)
    min_rank = np.minimum(highest_rank_1, highest_rank_1)
    rank_list = range((min_rank),(max_rank + 1))

    #plot the line graph
    plt.figure()
    plt.plot(years, ro_co_1_rank.Rank.tolist(), color = 'purple', marker = 'o')
    plt.plot(years, ro_co_2_rank.Rank.tolist(), color = 'blue', marker = 'o', linestyle = ":")

    #improve readability of graph
    plt.title("Ranks of " + name1 + " and " + name2 + " (2013-2018)")
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.subplot().set_yticks(rank_list)
    plt.legend([name1, name2])

    #invert the y-axis
    plt.gca().invert_yaxis()
    plt.show()

#rank_hist_2('El Toro', 'Six Flags Great Adventure', 'Boulder Dash' ,'Lake Compounce', wood_winners)
plt.clf()

# function to plot top n rankings over time
def rank_hist_n (n, ranking):
    #select the coasters with the desired rank
    interested_ro_cos = ranking[ranking.Rank <= n]

    #create figure
    plt.figure()
    #this empty list will be our legend
    legend = []
    
    #set is a collection that eliminates repetitions, 
    #so we iterate through the unique coaster names
    for coaster in set(interested_ro_cos['Name']):
        #we select the rows where out coaster exists
        coaster_rankings = ranking[ranking['Name'] == coaster]
        years = coaster_rankings['Year of Rank']
        ranks = coaster_rankings['Rank']
        legend.append(coaster)
        plt.plot(years, ranks, label = coaster)

    #label the graph
    plt.xlabel("Year")
    plt.ylabel("Rank")
    plt.title("History of rankings of the top " + str(n) + " coasters")
    plt.legend(legend)

    #invert the y-axis
    plt.gca().invert_yaxis()
    plt.show()

#rank_hist_n(2, steel_winners)
plt.clf()

# load roller coaster data
ro_co_cap = pd.read_csv('roller_coasters.csv')

# function to plot histogram of a column's values
def histogram (column):
    #the height column contains outliers, which are eliminated here
    if column != 'height':
        dataset = ro_co_cap[column].dropna()
    else:
        dataset = ro_co_cap[ro_co_cap.height <= 140].height 
    
    #plot graph
    plt.figure()
    plt.hist(dataset, bins=15, color='purple')

    #label the graph
    plt.ylabel("number of such roller coasters")
    plt.xlabel(column + " of a rollercoaster")
    plt.title("distribution of " + column + " amongst roller coasters")
    plt.show()

#histogram('height')
plt.clf()

# function to plot inversions by coaster at a park
def inv_num (park):
    #select all coasters in the queried park
    coasters = ro_co_cap[ro_co_cap['park'] == park]
    inversions = coasters['num_inversions']
    names = coasters['name'].tolist()

    #we specify the size of the figure as we want it bigger than the default
    plt.figure(figsize=(15,10))
    #plot the bar chart
    plt.bar(range(len(names)), inversions)
    
    #customize the chart, improve readability
    ax=plt.subplot()
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=40)
    #label the graph
    ax.set_title('Inversions per coaster in ' + park)
    plt.xlabel('Coaster Name')
    plt.ylabel("Number of Inversions")
    plt.show()

#inv_num('Walibi Belgium')

plt.clf()

#function to plot pie chart of operating status
def open_stat(df):
    #select desired data
    operating_df = df[df['status']=='status.operating']
    closed_df = df[df['status'] == 'status.closed.definitely']
    #count number of operating and permanently closed coasters
    operating = len(operating_df)
    closed = len(closed_df)
    count = [operating, closed]
    #these will become the chart's labels
    labels = ['Operating', 'Closed definitely']

    #create graph
    plt.figure()
    plt.pie(count, labels = labels, autopct='%0.1f%%')
    #improve visials
    plt.axis('equal')
    plt.title('operating status of coasters')
    plt.show()
    
#open_stat(ro_co_cap)
plt.clf()

#function to create scatter plot of any two numeric columns
def scatter(col1, col2):
    #get the data from the input columns
    values1 = ro_co_cap[col1]
    values2 = ro_co_cap[col2]

    plt.figure(figsize=(10, 8))
    plt.scatter(values1, values2, c='purple', marker='*')
    plt.title(col1 + ' as related to ' + col2 + " of coasters")
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.show()

#scatter('speed', 'length')
plt.clf()
