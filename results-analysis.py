import pandas as pd
import sys

reservoir = sys.argv[1]

df = pd.read_csv('results_'+reservoir+'.csv')

df['Elapsed_Time(s)'] = (df['End_Timestamp']-df['Start_Timestamp'])*10e-9

df.to_csv('results_'+reservoir+'.csv', index=False)

grouped_elapsed = df.groupby('Kernel_Name')['Elapsed_Time(s)'].agg(
    Total_Elapsed='sum',
    Average_Elapsed='mean',
    Std_Elapsed='std'
).reset_index()

Total_Time = grouped_elapsed['Total_Elapsed'].sum()

grouped_elapsed['Percentage'] = (grouped_elapsed['Total_Elapsed']/Total_Time)*100

grouped_elapsed.to_csv('results_stat_'+reservoir+'.csv', index=False)
