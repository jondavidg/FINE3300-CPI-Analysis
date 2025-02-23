#Import required libraries
import pandas as pd

#Create a dictionary which contains jurisdiction names (as keys) and the file paths to their associated datasets (as values)
filepaths = {'Canada' : 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/Canada.CPI.1810000401.csv',
              'Alberta': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/AB.CPI.1810000401.csv',
              'British Columbia': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/BC.CPI.1810000401.csv',
              'Manitoba': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/MB.CPI.1810000401.csv',
              'New Brunswick': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/NB.CPI.1810000401.csv',
              'Newfoundland and Labrador': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/NL.CPI.1810000401.csv',
              'Nova Scotia': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/NS.CPI.1810000401.csv',
              'Ontario': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/ON.CPI.1810000401.csv',
              'Prince Edward Island': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/PEI.CPI.1810000401.csv',
              'Quebec': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/QC.CPI.1810000401.csv',
              'Saskatchewan': 'C:/Users/jdgie/Desktop/FINE3300 Assignments/Assignment #2/Dataset/SK.CPI.1810000401.csv'
              }

#PART 1

#Create an empty list which will support the dataframe combination process
jurisdictionset = []

#Create a for loop to execute a series of steps on each individual (jurisdiction-specific) dataset
for jurisdiction in filepaths:
    #Access the filepath associated with the selected jurisdiction, read it into a dataframe object
    df = pd.read_csv(filepaths[jurisdiction])
    #Unpivot the dataframe, fixing the item column as the identifier, and unpivoting all other columns (24-Jan to 24-Dec). This yields a variable column titled "Month" which holds the month names and a value column titled "CPI" which holds their corresponding CPI figures
    df_unpivot = df.melt(id_vars=['Item'], var_name='Month', value_name='CPI')
    #Insert a new column called 'Jurisdiction' in the required position, storing the name of the selected jurisdiction as the value for all rows
    df_unpivot.insert(2, 'Jurisdiction', jurisdiction)
    #Append the formatted dataframe to the list created above
    jurisdictionset.append(df_unpivot)

#Concatenate the individual dataframes of all jurisdictions, as stored in the list, into one dataframe 
df_combined = pd.concat(jurisdictionset, ignore_index=True)

#PART 2

#Print the first 12 lines of the new combined dataframe, using the head() method to access the desired rows
print(f"Print the first 12 lines of the new dataframe: \n{df_combined.head(12)} ")

#PART 3

#Filter the combined dataframe, returning only rows where the value for Item is 'Food', 'Shelter', or 'All-items excluding food and energy'
df_combined_part3 = df_combined[df_combined['Item'].isin(['Food','Shelter','All-items excluding food and energy'])].reset_index(drop=True)
#Group the selected dataframe by Jurisdiction and Item, and compute the month-to-month (chronological row-over-row) percentage change in CPI using the 'CPI' column. Store this computation as a new column 'Change' added to the dataframe.
df_combined_part3['Change'] = df_combined_part3.groupby(['Jurisdiction', 'Item'])['CPI'].pct_change()
#Group the selected dataframe by Jurisdiction and Item, and compute the average change in CPI for each group (called 'Average Change (float)') using the 'Change' column calculated above. Then, reset the index (return a dataframe)
df_combined_part3 = df_combined_part3.groupby(['Jurisdiction', 'Item'])['Change'].mean().rename('Average Change (Float)').reset_index()
#Create a new column called 'Average Change', which converts the above 'Average Change (Float)' column into the desired format (percent up to one decimal place)
df_combined_part3['Average Change'] = df_combined_part3['Average Change (Float)'].map('{:.1%}'.format)
#Report the desired results, printing only the columns of interest
print(f"\nAverage Month-to-Month Change by Jurisdiction and Item: \n{df_combined_part3[['Jurisdiction', 'Item', 'Average Change']]}\n")

#PART 4

#Using the filtered data from part 3, apply an additional constraint to retain only province-specific data (per the requirements of question 4)
df_combined_part4 = df_combined_part3[df_combined_part3['Jurisdiction'] != 'Canada'].reset_index(drop=True)
#Create a new column which will hold the absolute values of the formerly calculated average change figures
df_combined_part4['Absolute Average Change (Float)'] = abs(df_combined_part4['Average Change (Float)'])
#Return the row labels corresponding with the highest absolute average change for each Item group
row_label_max_avg_per_group = df_combined_part4.groupby(['Item'])['Absolute Average Change (Float)'].idxmax()
#Store the specific rows from the dataframe corresponding with the labels selected above (use loc for label based indexing, since idxmax returns row labels)
row_max_avg_per_group = df_combined_part4.loc[row_label_max_avg_per_group]
#Iterate through each row (which contains the maximum absolute average change for a given category), printing the name of the category and the associated province
print("Province with Highest Average Change by Category: ")
for ind, rw in row_max_avg_per_group.iterrows():
    print(f"Highest Average Change for {rw['Item']}: {rw['Jurisdiction']}")

#PART 5

#Filter the combined dataframe, returning only rows where the value for Item is 'Services'
df_combined_part5 = df_combined[df_combined['Item'].isin(['Services'])].reset_index(drop=True)
#Group the selected dataframe by Jurisdiction and compute the annual percentage change in CPI (Dec - Jan / Jan) for services, called 'Annual Change (Float)', using the 'CPI' column. Then, reset the index (return a dataframe)
df_combined_part5 = ((df_combined_part5.groupby(['Jurisdiction'])['CPI'].last() - df_combined_part5.groupby(['Jurisdiction'])['CPI'].first())
                        / (df_combined_part5.groupby(['Jurisdiction'])['CPI'].first())).rename('Annual Change (Float)').reset_index()
#Create a new column called 'Annual Change', which converts the above 'Annual Change (Float)' column into the desired format (percent up to one decimal place)
df_combined_part5['Annual Change'] = df_combined_part5['Annual Change (Float)'].map('{:.1%}'.format)
#Report the desired results, printing only the columns of interest
print(f"\nAnnual Change in CPI for Services by Jurisdiction: \n{df_combined_part5[['Jurisdiction', 'Annual Change']]}\n")

#PART 6

#Using the filtered data from part 5, return the row label corresponding with the highest inflation (maximum annual change) in services
row_label_max_inflation_for_services = df_combined_part5['Annual Change (Float)'].idxmax()
#Print the jurisdiction name and annual change value of the row with the highest inflation in services (use loc for label based indexing, since idxmax returns row labels)
print(f"Region with Highest Inflation in Services: \n{df_combined_part5.loc[row_label_max_inflation_for_services, 'Jurisdiction']} has experienced the highest inflation in services, at {df_combined_part5.loc[row_label_max_inflation_for_services, 'Annual Change']}")