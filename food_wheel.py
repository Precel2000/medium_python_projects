import pandas as pd 
from matplotlib import pyplot as plt 

#load and inspect data
restaurants=pd.read_csv('restaurants.csv')
print(restaurants.head(10))

#count no of cuisines offered
cuisine_options_count = restaurants.cuisine.nunique()
print(cuisine_options_count)

#get number of restaurants associated with each cuisine type
cuisine_counts = restaurants.groupby('cuisine').name.count().reset_index()
cuisines = cuisine_counts['cuisine'].values 
counts = cuisine_counts.name.values

#plot the pie chart
plt.figure(figsize=(10,8))
plt.pie(counts, labels=cuisines, autopct='%d%%')
plt.axis('equal')
plt.title('Number of restaurants per cuisine type')
plt.show()

#investigate the 'orders' in each month
orders = pd.read_csv('orders.csv')
#create the new 'month' column
orders['month'] = orders.date.apply(lambda x: x.split('-')[0])
avg_order = orders.groupby('month').price.mean().reset_index()
std_order = orders.groupby('month').price.std().reset_index()

ax = plt.subplot()

#get the desired data
bar_heights = avg_order.price
bar_errors = std_order.price
#plot the data
plt.bar(range(len(bar_heights)),
  			bar_heights,
        yerr=bar_errors,
        capsize=5)

#label and customize the graph
ax.set_xticks(range(len(bar_heights)))
ax.set_xticklabels(['April', 'May', 'June', 'July', 'August', 'September'])
plt.ylabel('Average Order Amount')
plt.title('Order Amount over Time')

#render the visualisation
plt.show()
