# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:04:49 2019

@author: Ravikanth Tadikonda
"""
import pandas as pd

import os

os.chdir('D:\\Public Health Data')

districtua_data = pd.read_csv('DistrictUA.csv')
countyua_data = pd.read_csv('CountyUA.csv')
region_data = pd.read_csv('Region.csv')

def get_overview_grouped_data(input_data):
    grouped_data_frame = pd.DataFrame(input_data.groupby(['Indicator Name','Time period','Area Name'])['Value'].mean())
    grouped_data_frame['Indicator_Area']=grouped_data_frame.index.tolist()
    indicator= grouped_data_frame['Indicator_Area'].apply(lambda x:x[0] )
    period= grouped_data_frame['Indicator_Area'].apply(lambda x:x[1] )
    area= grouped_data_frame['Indicator_Area'].apply(lambda x:x[2] )
    grouped_data_frame['Area_Name']=area
    grouped_data_frame['Time_period']=period
    grouped_data_frame['Indicator_Name']=indicator
    return grouped_data_frame
    
def get_all_regions(input_dataset):
    return input_dataset.loc[input_dataset['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

def get_entire_dataset(area_type):
    if(area_type=='DistrictUA'):
        return districtua_data
    elif(area_type=='CountyUA'):
        return countyua_data
    elif(area_type=='Region'):
        return region_data
    else:
        return None

def get_entire_data_for_area(input_dataset, region):
    output_dataset  = input_dataset.loc[input_dataset['Area Name']==region]
    return output_dataset

def get_entire_data_for_region(input_dataset, region):
    output_dataset  = input_dataset.loc[input_dataset['Parent Name']==region]
    print("inside get entire data for region.....")
    print(output_dataset.head())
    return output_dataset

def get_entire_data_for_timeperiod(input_dataset, timeperiod):
    output_dataset = input_dataset.loc[input_dataset['Time period']==timeperiod]
    print("inside get entire data for time period.....")
    #print(output_dataset.head())
    return output_dataset

def get_overview_indicators_list(area_type, region, timeperiod):
    return get_new_data_populated(area_type, region, timeperiod)['Indicator'].tolist()

def get_entire_indicators_list(area_type,timeperiod):
    return get_entire_dataset(area_type)['Indicator Name'].dropna().unique().tolist()

def get_overview_data_for_region_timeperiod(area_type, region, timeperiod):
    input_dataset = get_entire_dataset(area_type)
    input_dataset = get_entire_data_for_region(input_dataset,region)
    input_dataset = get_entire_data_for_timeperiod(input_dataset,timeperiod)
    output_dataset = input_dataset.loc[input_dataset['Indicator Name'].isin(input_dataset['Indicator Name'].dropna().unique().tolist()[0:5])]
    return output_dataset

def get_entire_data_for_region_timeperiod(area_type, region, timeperiod):
    input_dataset = get_entire_dataset(area_type)
    input_dataset = get_entire_data_for_region(input_dataset,region)
    input_dataset = get_entire_data_for_timeperiod(input_dataset,timeperiod)
    return input_dataset.loc[input_dataset['Indicator Name'].isin(input_dataset['Indicator Name'].dropna().unique().tolist())]

def get_overview_data_for_area_timeperiod(area_type, area, timeperiod):
    input_dataset = get_entire_dataset(area_type)
    output_dataset = get_entire_data_for_area(input_dataset,area)
    output_dataset = get_entire_data_for_timeperiod(output_dataset,timeperiod)
    return output_dataset.loc[output_dataset['Indicator Name'].isin(output_dataset['Indicator Name'].dropna().unique().tolist()[0:5])]

def get_overview_empty_list(input_dataset, region,timeperiod):
    area_list = input_dataset['Area Name'].dropna().unique().tolist()
    return pd.DataFrame(columns=area_list)

def get_new_data_populated(area_type, region, timeperiod):
    input_dataset = get_overview_data_for_region_timeperiod(area_type, region, timeperiod)
    grouped_data_frame = get_overview_grouped_data(input_dataset)
    new_dataframe =  get_overview_empty_list(input_dataset, region,timeperiod) 
    column_names =new_dataframe.columns.tolist()
    column_names.append(region)
    column_names.append('England ')
    for column_name in new_dataframe.columns:
        new_dataframe[column_name] = pd.to_numeric(grouped_data_frame.loc[grouped_data_frame['Area_Name']== column_name]['Value'].values)
    new_dataframe = new_dataframe.sort_index(axis=1)
    new_dataframe.insert(loc=0, column='Period', value='2015 - 17')
    new_dataframe.insert(loc=1, column='England ', value=pd.to_numeric(get_overview_grouped_data(get_overview_data_for_area_timeperiod(area_type, 'England',timeperiod))['Value'].values))
    new_dataframe.insert(loc=2, column=region, value=pd.to_numeric(get_overview_grouped_data(get_overview_data_for_area_timeperiod(area_type, region, timeperiod))['Value'].values))
    #empty_list[region] =  pd.to_numeric(get_overview_grouped_data(get_overview_data_for_area_timeperiod(area_type, region, timeperiod))['Value'].values)
    new_dataframe['Indicator'] = grouped_data_frame['Indicator_Name'].unique()
    new_dataframe.set_index('Indicator', inplace = True)
    new_dataframe.reset_index( inplace = True)
    for index, row in new_dataframe.iterrows():
        for col_name in column_names:
            if(int(row['England '])-int(row[col_name])>=1):
                new_dataframe.loc[index,col_name] = str(row[col_name])+','+col_name+',Worse'
            elif(int(row['England '])-int(row[col_name])<=-1):
                new_dataframe.loc[index,col_name] = str(row[col_name])+','+col_name+',Better'
            else:
                new_dataframe.loc[index,col_name] = str(row[col_name])+','+col_name+',Similar'
    return new_dataframe


def get_compare_indicators_data(area_type,region,indicator_name_x,indicator_name_y,timeperiod):
    input_dataset = get_entire_data_for_region_timeperiod(area_type,region,timeperiod)
    output_dataset = pd.DataFrame()
    input_dataset = input_dataset.loc[input_dataset['Indicator Name'].isin([indicator_name_x,indicator_name_y])]
    input_indicator_x_dataset = input_dataset.loc[input_dataset['Indicator Name']==indicator_name_x]
    input_indicator_y_dataset = input_dataset.loc[input_dataset['Indicator Name']==indicator_name_y]
    grouped_x_dataset = input_indicator_x_dataset.groupby(['Area Name'])['Value'].mean()
    grouped_y_dataset = input_indicator_y_dataset.groupby(['Area Name'])['Value'].mean()
    output_dataset['Area']=grouped_x_dataset.index.tolist()
    output_dataset['X']=[round(element, 2) for element in pd.to_numeric(grouped_x_dataset).tolist()]
    output_dataset['Y']=[round(element, 2) for element in pd.to_numeric(grouped_y_dataset).tolist()]
    return output_dataset

def get_compare_areas_data(area_type,region,indicator_name,timeperiod):
    input_dataset = get_entire_data_for_region_timeperiod(area_type,region,timeperiod)
    output_dataset = pd.DataFrame()
    england_dataset = get_overview_data_for_area_timeperiod(area_type ,'England',timeperiod)
    england_dataset = england_dataset.loc[england_dataset['Indicator Name']==indicator_name]
    region_dataset = get_overview_data_for_area_timeperiod(area_type ,region, timeperiod)
    region_dataset = region_dataset.loc[region_dataset['Indicator Name']==indicator_name]
    input_indicator_dataset = input_dataset.loc[input_dataset['Indicator Name']==indicator_name]
    grouped_area_dataset = input_indicator_dataset.groupby(['Area Name'])['Value'].mean()
    output_dataset['Area']=['England',region]+grouped_area_dataset.index.tolist()
    output_dataset['Count']=pd.to_numeric(england_dataset.groupby(['Area Name']).size()).tolist()+pd.to_numeric(region_dataset.groupby(['Area Name']).size()).tolist()+pd.to_numeric(input_indicator_dataset.groupby(['Area Name']).size()).tolist()
    output_dataset['Value']=[round(element, 2) for element in pd.to_numeric(england_dataset.groupby(['Area Name'])['Value'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(region_dataset.groupby(['Area Name'])['Value'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(grouped_area_dataset).tolist()]
    output_dataset['95% Lower CI'] = [round(element, 2) for element in pd.to_numeric(england_dataset.groupby(['Area Name'])['Lower CI 95.0 limit'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(region_dataset.groupby(['Area Name'])['Lower CI 95.0 limit'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(input_indicator_dataset.groupby(['Area Name'])['Lower CI 95.0 limit'].mean()).tolist()]
    output_dataset['95% Upper CI'] = [round(element, 2) for element in pd.to_numeric(england_dataset.groupby(['Area Name'])['Upper CI 95.0 limit'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(region_dataset.groupby(['Area Name'])['Upper CI 95.0 limit'].mean()).tolist()]+[round(element, 2) for element in pd.to_numeric(input_indicator_dataset.groupby(['Area Name'])['Upper CI 95.0 limit'].mean()).tolist()]
    return output_dataset

def get_entire_data_for_indicator(input_dataset,indicator_name):
    return input_dataset.loc[input_dataset['Indicator Name']==indicator_name]

def get_grouped_region_indicator_data(input_data):
    grouped_quantile_data = input_data.groupby(['Time period'])['Value']
    return grouped_quantile_data

def get_boxplot_indicator_data(area_type, region, indicator_name):
    input_dataset = get_entire_dataset(area_type)
    input_dataset = get_entire_data_for_region(input_dataset,region)
    input_dataset = get_entire_data_for_indicator(input_dataset,indicator_name)
    return get_grouped_region_indicator_data(input_dataset)

def get_boxplot_data_table(grouped_quantile_data):
    quantile_data_frame = pd.DataFrame()
    quantile_data_frame['Time Period'] = pd.DataFrame(grouped_quantile_data)[0].tolist()
    quantile_data_frame['Minimum'] = grouped_quantile_data.quantile(q=0.00).tolist()
    quantile_data_frame['5th Percentile'] = grouped_quantile_data.quantile(q=0.05).tolist()
    quantile_data_frame['25th Percentile'] = grouped_quantile_data.quantile(q=0.25).tolist()
    quantile_data_frame['Median'] = grouped_quantile_data.quantile(q=0.5).tolist()
    quantile_data_frame['75th Percentile'] = grouped_quantile_data.quantile(q=0.75).tolist()
    quantile_data_frame['95th Percentile'] = grouped_quantile_data.quantile(q=0.95).tolist()
    quantile_data_frame['Maximum'] = grouped_quantile_data.quantile(q=1.00).tolist()
    return quantile_data_frame.dropna()

def get_areas_for_region(area_type, region, timeperiod):
    input_dataset = get_entire_data_for_region_timeperiod(area_type,region,timeperiod)
    return input_dataset['Area Name'].dropna().unique().tolist()
    
def get_area_profiles_data(area_type,area_name,timeperiod):
    temp_dataset = get_overview_data_for_area_timeperiod(area_type ,area_name,timeperiod)
    temp_dataset = get_overview_grouped_data(temp_dataset)
    output_dataset = pd.DataFrame()
    output_dataset['Indicator'] =  temp_dataset['Indicator_Name']
    output_dataset.insert(loc=1, column='Period', value='2015 - 17') 
    output_dataset['Value'] = temp_dataset['Value']
    return output_dataset

