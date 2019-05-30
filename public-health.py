# -*- coding: utf-8 -*-
"""
Created on Wed May 22 11:06:07 2019

@author: Ravikanth Tadikonda
"""
import os
os.chdir('D:\\Public Health Data')
from expectancy_causes_of_death_data import get_new_data_populated, get_entire_dataset,get_overview_indicators_list, get_entire_indicators_list,get_compare_indicators_data,get_compare_areas_data, get_area_profiles_data,get_areas_for_region,get_boxplot_indicator_data, get_boxplot_data_table
#entire_dataframe = get_exp_causes_of_death_data()

#template = """
#     <span href="#" data-toggle="tooltip" title='<%= value %> Years \nLife Exp'><%= value %></span>

template="""
            <div style="background:<%= 
                (function colorfromint(){
                    if(value.split(",")[2]=="Worse"){
                            return("#C70039")}
                    if(value.split(",")[2]=="Better"){
                            return("#B0EC6F")}
                    if(value.split(",")[2]=="Similar"){
                            return("#FFC300")}
                    }()) %>; 
                color: black;font-size:15px;"> 
                <% if(value!='2015 - 17'){
                     if (Indicator=='Life expectancy at birth') {%>
                        <span href="#" class ="highlightme" data-toggle="tooltip" title="<%=value.split(",")[1] %> \n <%= value.split(",",1) %> Years\n\n<%= Indicator %>"><a href="" target=""><%= value.split(",",1) %> </a></span>
                        <%}
                         else {%>
                                  <span href="#" class ="highlightme" data-toggle="tooltip" title="<%=value.split(",")[1] %> \n <%= value.split(",",1) %> per 100,000\n\n<%= Indicator %>"><a href="" target=""><%= value.split(",",1) %> </a></span>
                                  <%}
                         }  
                             else {%>
                                   <span href="#" class ="highlightme"><%= value%> </span>
                                   <%}%>
                    </div>
            """

#from bokeh.io import output_file, show
#from bokeh.models import TableColumn, ColumnDataSource
#from bokeh.models.widgets.tables import DataTable,HTMLTemplateFormatter
from bokeh.models.widgets import Panel, Tabs
from bokeh.layouts import layout
#from bokeh.models import CustomJS, Column
from bokeh.plotting import curdoc
from bokeh.models.widgets import Select, CheckboxButtonGroup
from bokeh.models import ColumnDataSource, TableColumn,  DataTable, HTMLTemplateFormatter, HoverTool,ResetTool, PanTool, BoxZoomTool, SaveTool
from bokeh.plotting import figure
from sklearn.linear_model import LinearRegression

import pandas as pd

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("x", "@x per 100,000"),
    ("y", "@y per 1000"),
    ('desc', '@desc'),
])

tools = [hover, BoxZoomTool(), PanTool(), ResetTool(), SaveTool()]

def overview_area_type_on_change(attr, old, new):
    print(overview_area_type_select.value)
    if(overview_area_type_select.value=='Region'):
        overview_areas_in_region_select.visible = False
        return None
    else:
        overview_areas_in_region_select.visible = True
        region_areas = get_entire_dataset(overview_area_type_select.value)
        areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()
        print(areas_list)
        overview_areas_in_region_select.value = areas_list[0]
        overview_areas_in_region_select.options = areas_list
        temp_dataset = get_new_data_populated(overview_area_type_select.value, overview_areas_in_region_select.value,'2015 - 17')
        print(temp_dataset)
        Columns = [TableColumn(field=Ci, title=Ci, width=50, formatter=HTMLTemplateFormatter(template=template)) for Ci in temp_dataset.columns]
        overview_data_table.columns = Columns
        overview_data_table.source = ColumnDataSource(temp_dataset)
        overview_data_table.update()
 
def overview_areas_grouped_by_on_change(attr, old, new):
    print(overview_area_grouped_by_select.value)
    
def overview_areas_in_region_on_change(attr, old, new):
    temp_dataset = get_new_data_populated(overview_area_type_select.value, overview_areas_in_region_select.value,'2015 - 17')
    print(temp_dataset)
    Columns = [TableColumn(field=Ci, title=Ci, width=100, formatter=HTMLTemplateFormatter(template=template)) for Ci in temp_dataset.columns]
    overview_data_table.columns = Columns
    overview_data_table.source = ColumnDataSource(temp_dataset)
    overview_data_table.update()
    
def compare_indicators_area_type_on_change(attr, old, new):
    print(compare_indicators_area_type_select.value)
    if(compare_indicators_area_type_select.value=='Region'):
        compare_indicators_areas_in_region_select.visible = False
        return None
    else:
        compare_indicators_areas_in_region_select.visible = True
        region_areas = get_entire_dataset(compare_indicators_area_type_select.value)
        areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()
        print(areas_list)
        compare_indicators_areas_in_region_select.value = areas_list[0]
        compare_indicators_areas_in_region_select.options = areas_list  
        result_dataset = get_compare_indicators_data(compare_indicators_area_type_select.value, 
                                compare_indicators_areas_in_region_select.value, 
                                compare_x_indicator_select.value,
                                compare_y_indicator_select.value,
                                '2015 - 17')
        print("inside compare_indicators_area_type_on_change....")
        # add a circle renderer with a size, color, and alpha
        regressor = LinearRegression()
        regressor.fit([result_dataset['X']], [result_dataset['Y']])
        y_predict = regressor.predict([result_dataset['X']])
        #regression_plot = figure(plot_width=800, plot_height=400, tools=tools,title="Compare Indicators" )
        print("result set....")
        print(y_predict.flatten())
        # add a circle renderer with a size, color, and alpha
        regression_plot.x_range = None
        regression_plot.y_range = None
        regression_plot.circle(result_dataset['X'], result_dataset['Y'], size=10, color="navy", alpha=0.5)
        regression_plot.line(result_dataset['X'],y_predict.flatten(), color='red')
     
def compare_indicator_areas_grouped_by_on_change(attr, old, new):
    print(compare_indicators_area_grouped_by_select.value)
    
def compare_indicators_areas_in_region_on_change(attr, old, new):
    print(compare_indicators_areas_in_region_select.value)
    result_dataset1 = get_compare_indicators_data(compare_indicators_area_type_select.value, 
                                compare_indicators_areas_in_region_select.value, 
                                compare_x_indicator_select.value,
                                compare_y_indicator_select.value,
                                '2015 - 17')
    print("inside compare_indicator_areas_grouped_by_on_change")
    print(result_dataset1)
    # add a circle renderer with a size, color, and alpha
    regressor = LinearRegression()
    regressor.fit([result_dataset1['X']], [result_dataset1['Y']])
    y_predict = regressor.predict([result_dataset1['X']])
    #fig = figure(plot_width=800, plot_height=400, tools=tools,title="Compare Indicators" )
    print("result set....")
    print(y_predict.flatten())
    # add a circle renderer with a size, color, and alpha
    regression_plot.circle(result_dataset1['X'], result_dataset1['Y'], size=10, color="navy", alpha=0.5)
    regression_plot.line(result_dataset1['X'],y_predict.flatten(), color='red')
    

def compare_areas_area_type_on_change(attr, old, new):
    print(compare_indicators_area_type_select.value)
    if(compare_areas_area_type_select.value=='Region'):
        compare_areas_areas_in_region_select.visible = False
        return None
    else:
        compare_areas_areas_in_region_select.visible = True
        region_areas = get_entire_dataset(compare_indicators_area_type_select.value)
        areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()
        print(areas_list)
        compare_areas_areas_in_region_select.value = areas_list[0]
        compare_areas_areas_in_region_select.options = areas_list  
        result_dataset1 = get_compare_areas_data(compare_areas_area_type_select.value, 
                                    compare_areas_areas_in_region_select.value, 
                                    compare_areas_indicator_select.value,
                                    '2015 - 17')
        Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in result_dataset1.columns] # bokeh columns
        compare_areas_data_table.columns = Columns
        compare_areas_data_table.source = ColumnDataSource(result_dataset1)
        compare_areas_data_table.update()

def compare_areas_areas_in_region_on_change(attr, old, new):
    result_dataset = get_compare_areas_data(compare_areas_area_type_select.value, 
                                compare_areas_areas_in_region_select.value, 
                                compare_areas_indicator_select.value,
                                '2015 - 17')
    Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in result_dataset.columns] # bokeh columns
    compare_areas_data_table.columns = Columns
    compare_areas_data_table.source = ColumnDataSource(result_dataset)
    compare_areas_data_table.update()

   
def compare_areas_indicator_on_change(attr, old, new):
    result_dataset = get_compare_areas_data(compare_areas_area_type_select.value, 
                                compare_areas_areas_in_region_select.value, 
                                compare_areas_indicator_select.value,
                                '2015 - 17')
    Columns = [TableColumn(field=Ci, title=Ci, width=50, formatter=HTMLTemplateFormatter(template=template)) for Ci in result_dataset.columns] # bokeh columns
    compare_areas_data_table.columns = Columns
    compare_areas_data_table.source = ColumnDataSource(result_dataset)
    compare_areas_data_table.update()
    

    
def compare_y_indicator_on_change(attr, old, new):
    print(compare_y_indicator_select.value)
    result_dataset1 = get_compare_indicators_data(compare_indicators_area_type_select.value, 
                                compare_indicators_areas_in_region_select.value, 
                                compare_x_indicator_select.value,
                                compare_y_indicator_select.value,
                                '2015 - 17')
    print("inside compare_y_indicator_on_change")
    print(result_dataset1)
    # add a circle renderer with a size, color, and alpha
    regressor1 = LinearRegression()
    regressor1.fit([result_dataset['X']], [result_dataset['Y']])
    y_predict = regressor1.predict([result_dataset['X']])
    #regression_plot = figure(plot_width=800, plot_height=400, tools=tools,title="Compare Indicators" )
    print("result set....")
    print(y_predict.flatten())
    regression_plot.x_range = None
    regression_plot.y_range = None
    # add a circle renderer with a size, color, and alpha
    regression_plot.circle(result_dataset1['X'], result_dataset1['Y'], size=10, color="navy", alpha=0.5)
    regression_plot.line(result_dataset1['X'],y_predict.flatten(), color='red')
    
def compare_x_indicator_on_change(attr, old, new):
    print(compare_x_indicator_select.value)
    result_dataset1 = get_compare_indicators_data(compare_indicators_area_type_select.value, 
                                compare_indicators_areas_in_region_select.value, 
                                compare_x_indicator_select.value,
                                compare_y_indicator_select.value,
                                '2015 - 17')
    print("inside compare_indicator_areas_grouped_by_on_change")
    print(result_dataset1)
    # add a circle renderer with a size, color, and alpha
    regressor1 = LinearRegression()
    regressor1.fit([result_dataset1['X']], [result_dataset1['Y']])
    y_predict = regressor1.predict([result_dataset1['X']])  
    #regression_plot = figure(plot_width=800, plot_height=400, tools=tools,title="Compare Indicators" )
    print("result set....")
    print(y_predict.flatten())
    regression_plot.x_range = None
    regression_plot.y_range = None
    # add a circle renderer with a size, color, and alpha
    regression_plot.circle(result_dataset1['X'], result_dataset1['Y'], size=10, color="navy", alpha=0.5)
    regression_plot.line(result_dataset1['X'],y_predict.flatten(), color='red')

    
def area_profiles_area_type_on_change(attr, old, new):
    if(area_profiles_area_type_select.value=='Region'):
        area_profiles_areas_in_region_select.visible = False
        return None
    else:
        area_profiles_areas_in_region_select.visible = True
        area_profiles_dataset = get_area_profiles_data(area_profiles_area_type_select.value,area_profiles_areas_of_region_select.value,'2015 - 17')
        Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in area_profiles_dataset.columns] # bokeh columns
        area_profiles_data_table.columns = Columns
        area_profiles_data_table.source = ColumnDataSource(area_profiles_dataset)
        area_profiles_data_table.update()

def area_profiles_areas_in_region_on_change(attr, old, new):
    area_profiles_dataset = get_area_profiles_data(area_profiles_area_type_select.value,area_profiles_areas_of_region_select.value,'2015 - 17')
    Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in area_profiles_dataset.columns] # bokeh columns
    area_profiles_data_table.columns = Columns
    area_profiles_data_table.source = ColumnDataSource(area_profiles_dataset)
    area_profiles_data_table.update()

def area_profiles_areas_of_region_on_change(attr, old, new):
    area_profiles_dataset = get_area_profiles_data(area_profiles_area_type_select.value,area_profiles_areas_of_region_select.value,'2015 - 17')
    Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in area_profiles_dataset.columns] # bokeh columns
    area_profiles_data_table.columns = Columns
    area_profiles_data_table.source = ColumnDataSource(area_profiles_dataset)
    area_profiles_data_table.update()    
    
def england_area_type_on_change(attr, old, new):
    temp_dataset = get_new_data_populated(england_area_type_select.value,'England','2015 - 17').iloc[:,[0,10]]
    Columns = [TableColumn(field=Ci, title=Ci, width=50, formatter=HTMLTemplateFormatter(template=template)) for Ci in temp_dataset.columns] # bokeh columns
    england_data_table.columns = Columns
    england_data_table.source = ColumnDataSource(temp_dataset)
    england_data_table.update()
    
def box_plots_area_type_on_change(attr, old, new):
    print("inside box_plots_area_type_on_change....")
    print(box_plots_area_type_select.value)
    print(box_plots_areas_in_region_select.value)
    print(box_plots_indicator_select.value)
    if(box_plots_area_type_select.value=='Region'):
        box_plots_areas_in_region_select.visible = False
        return None
    else:
        box_plots_areas_in_region_select.visible = True
        region_areas = get_entire_dataset(box_plots_area_type_select.value)
        areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()
        print(areas_list)
        box_plots_areas_in_region_select.value = areas_list[0]
        box_plots_areas_in_region_select.options = areas_list  
        grouped_quartile_data1 = get_boxplot_indicator_data(box_plots_area_type_select.value,box_plots_areas_in_region_select.value,box_plots_indicator_select.value)
        box_plot_dataset1 = get_boxplot_data_table(grouped_quartile_data1)
        print(box_plot_dataset1['Minimum'])       
        quantile_min = pd.DataFrame(grouped_quartile_data1.quantile(q=0.00).dropna())
        quantile_1 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.25).dropna())
        quantile_2 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.5).dropna())
        quantile_3 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.75).dropna())
        quantile_max = pd.DataFrame(grouped_quartile_data1.quantile(q=1.00).dropna())         
        iqr = quantile_3-quantile_1
        upper = quantile_3 + 1.5 * iqr
        lower = quantile_1 - 5.5 * iqr       
        upper.Value = [min([x,y]) for (x,y) in zip(list(quantile_max.loc[:,'Value']),upper.Value)]
        lower.Value = [max([x,y]) for (x,y) in zip(list(quantile_min.loc[:,'Value']),lower.Value)] 
        time_period_list1 = box_plot_dataset['Time Period'].dropna().tolist()      
        box_plots = figure(tools="", background_fill_color="#efefef", x_range=time_period_list, toolbar_location=None)        
        box_plots.segment(time_period_list1, upper.Value, time_period_list1, quantile_3.Value, line_color="black")
        box_plots.segment(time_period_list1, lower.Value, time_period_list1, quantile_1.Value, line_color="black")       
        box_plots.vbar(time_period_list1, 0.7, quantile_2.Value, quantile_3.Value, fill_color="#E08E79", line_color="black")
        box_plots.vbar(time_period_list1, 0.7, quantile_1.Value, quantile_2.Value, fill_color="#3B8686", line_color="black")       
        box_plots.rect(time_period_list1, lower.Value, 0.2, 0.01, line_color="black")
        box_plots.rect(time_period_list1, upper.Value, 0.2, 0.01, line_color="black")                                 
        box_plots.xgrid.grid_line_color = None
        box_plots.ygrid.grid_line_color = "white"
        box_plots.grid.grid_line_width = 2
        box_plots.xaxis.major_label_text_font_size="12pt"
        Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in box_plot_dataset1.columns] # bokeh columns
        box_plot_data_table.columns = Columns
        box_plot_data_table.source = ColumnDataSource(box_plot_dataset1)
        box_plot_data_table.update()

def box_plots_areas_in_region_on_change(attr, old, new):
    print("inside box_plots_areas_in_region_on_change....")
    print(box_plots_area_type_select.value)
    print(box_plots_areas_in_region_select.value)
    print(box_plots_indicator_select.value)
    grouped_quartile_data1 = get_boxplot_indicator_data(box_plots_area_type_select.value,box_plots_areas_in_region_select.value,box_plots_indicator_select.value)
    box_plot_dataset1 = get_boxplot_data_table(grouped_quantile_data)
    print(box_plot_dataset1['Minimum'])
    quantile_min = pd.DataFrame(grouped_quartile_data1.quantile(q=0.00).dropna())
    quantile_1 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.25).dropna())
    quantile_2 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.5).dropna())
    quantile_3 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.75).dropna())
    quantile_max = pd.DataFrame(grouped_quartile_data1.quantile(q=1.00).dropna())     
    iqr = quantile_3-quantile_1
    upper = quantile_3 + 1.5 * iqr
    lower = quantile_1 - 5.5 * iqr    
    upper.Value = [min([x,y]) for (x,y) in zip(list(quantile_max.loc[:,'Value']),upper.Value)]
    lower.Value = [max([x,y]) for (x,y) in zip(list(quantile_min.loc[:,'Value']),lower.Value)]   
    time_period_list = box_plot_dataset['Time Period'].dropna().tolist()
    box_plots = figure(tools="", background_fill_color="#efefef", x_range=time_period_list, toolbar_location=None)    
    box_plots.segment(time_period_list, upper.Value, time_period_list, quantile_3.Value, line_color="black")
    box_plots.segment(time_period_list, lower.Value, time_period_list, quantile_1.Value, line_color="black")    
    box_plots.vbar(time_period_list, 0.7, quantile_2.Value, quantile_3.Value, fill_color="#E08E79", line_color="black")
    box_plots.vbar(time_period_list, 0.7, quantile_1.Value, quantile_2.Value, fill_color="#3B8686", line_color="black")   
    box_plots.rect(time_period_list, lower.Value, 0.2, 0.01, line_color="black")
    box_plots.rect(time_period_list, upper.Value, 0.2, 0.01, line_color="black")                            
    box_plots.xgrid.grid_line_color = None
    box_plots.ygrid.grid_line_color = "white"
    box_plots.grid.grid_line_width = 2
    box_plots.xaxis.major_label_text_font_size="12pt"
    Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in box_plot_dataset1.columns] # bokeh columns
    box_plot_data_table.columns = Columns
    box_plot_data_table.source = ColumnDataSource(box_plot_dataset1)
    box_plot_data_table.update()
    
def box_plots_indicator_on_change(attr, old, new):
    print("inside box_plots_indicator_on_change....")
    print(box_plots_area_type_select.value)
    print(box_plots_areas_in_region_select.value)
    print(box_plots_indicator_select.value)
    grouped_quartile_data1 = get_boxplot_indicator_data(box_plots_area_type_select.value,box_plots_areas_in_region_select.value,box_plots_indicator_select.value)
    box_plot_dataset1 = get_boxplot_data_table(grouped_quartile_data1)
    print(box_plot_dataset1['Minimum'])
    quantile_min = pd.DataFrame(grouped_quartile_data1.quantile(q=0.00).dropna())
    quantile_1 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.25).dropna())
    quantile_2 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.5).dropna())
    quantile_3 = pd.DataFrame(grouped_quartile_data1.quantile(q=0.75).dropna())
    quantile_max = pd.DataFrame(grouped_quartile_data1.quantile(q=1.00).dropna())     
    iqr = quantile_3-quantile_1
    upper = quantile_3 + 1.5 * iqr
    lower = quantile_1 - 5.5 * iqr    
    upper.Value = [min([x,y]) for (x,y) in zip(list(quantile_max.loc[:,'Value']),upper.Value)]
    lower.Value = [max([x,y]) for (x,y) in zip(list(quantile_min.loc[:,'Value']),lower.Value)]    
    time_period_list1 = box_plot_dataset['Time Period'].dropna().tolist()   
    box_plots = figure(tools="", background_fill_color="#efefef", x_range=time_period_list, toolbar_location=None)    
    box_plots.segment(time_period_list1, upper.Value, time_period_list1, quantile_3.Value, line_color="black")
    box_plots.segment(time_period_list1, lower.Value, time_period_list1, quantile_1.Value, line_color="black")    
    box_plots.vbar(time_period_list1, 0.7, quantile_2.Value, quantile_3.Value, fill_color="#E08E79", line_color="black")
    box_plots.vbar(time_period_list1, 0.7, quantile_1.Value, quantile_2.Value, fill_color="#3B8686", line_color="black")    
    box_plots.rect(time_period_list1, lower.Value, 0.2, 0.01, line_color="black")
    box_plots.rect(time_period_list1, upper.Value, 0.2, 0.01, line_color="black")                              
    box_plots.xgrid.grid_line_color = None
    box_plots.ygrid.grid_line_color = "white"
    box_plots.grid.grid_line_width = 2
    box_plots.xaxis.major_label_text_font_size="12pt"
    Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in box_plot_dataset1.columns] # bokeh columns
    box_plot_data_table.columns = Columns
    box_plot_data_table.source = ColumnDataSource(box_plot_dataset1)
    box_plot_data_table.update()  
         
def outliers(group):
    cat = group.name
    return group[(group.Value > upper.loc[cat]['Value']) | (group.Value < lower.loc[cat]['Value'])]['Value']

###########OVERVIEW#################################  
# Select options for Area type list
overview_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
overview_area_type_select.on_change('value', overview_area_type_on_change)

# Select options for Area grouped by list
overview_area_grouped_by_select = Select(title="Area grouped by", value="Region", options=["Region"])
#area_grouped_by_select.on_change('value', areas_grouped_by_on_change)
region_areas = get_entire_dataset(overview_area_type_select.value)
areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

# Select options for Areas in region
overview_areas_in_region_select = Select(title="Region", value=areas_list[0], options=areas_list)
overview_areas_in_region_select.on_change('value', overview_areas_in_region_on_change)

temp_dataset = get_new_data_populated(overview_area_type_select.value, overview_areas_in_region_select.value,'2015 - 17')
Columns = [TableColumn(field=Ci, title=Ci, width=50, formatter=HTMLTemplateFormatter(template=template)) for Ci in temp_dataset.columns] # bokeh columns
overview_data_table = DataTable(columns=Columns, scroll_to_selection=True,selectable=True,
                       source=ColumnDataSource(temp_dataset),align ="center",
                       fit_columns=True,index_position = None,header_row = True,width_policy = "auto",index_header= "#",
                      width=3000, height=300) 

overview_data_table.update()

#################COMPARE INDICATORS########################
# Select options for list of all indicators
compare_indicators_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
compare_indicators_area_type_select.on_change('value', compare_indicators_area_type_on_change)

# Select options for Area grouped by list
compare_indicators_area_grouped_by_select = Select(title="Area grouped by", value="Region", options=["Region"])
#area_grouped_by_select.on_change('value', areas_grouped_by_on_change)
region_areas = get_entire_dataset(compare_indicators_area_type_select.value)
areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

# Select options for Areas in region
compare_indicators_areas_in_region_select = Select(title="Region", value=areas_list[0], options=areas_list)
compare_indicators_areas_in_region_select.on_change('value',  compare_indicators_areas_in_region_on_change)

indicators_list = get_overview_indicators_list(compare_indicators_area_type_select.value, compare_indicators_areas_in_region_select.value,'2015 - 17')
compare_x_indicator_select = Select(title='Indicator', value=indicators_list[0], options=indicators_list)
compare_x_indicator_select.on_change('value', compare_x_indicator_on_change)

all_indicators_list = get_entire_indicators_list(compare_indicators_area_type_select.value,'2015 - 17')
compare_y_indicator_select = Select(title='Indicator on Y axis', value=all_indicators_list[0], options=all_indicators_list)
compare_y_indicator_select.on_change('value', compare_y_indicator_on_change)

compare_all_indicators_button_group = CheckboxButtonGroup(labels=["All in "+compare_indicators_areas_in_region_select.value, "All in England"], active=[0, 1])

result_dataset = get_compare_indicators_data(compare_indicators_area_type_select.value, 
                                compare_indicators_areas_in_region_select.value, 
                                compare_x_indicator_select.value,
                                compare_y_indicator_select.value,
                                '2015 - 17')
# Create linear regression object
regressor = LinearRegression()
regressor.fit([result_dataset['X']], [result_dataset['Y']])
y_predict = regressor.predict([result_dataset['X']])

regression_plot = figure(plot_width=1200, plot_height=400, tools=tools,title="Compare Indicators" )
print("result set....")
print(y_predict.flatten())
# add a circle renderer with a size, color, and alpha
regression_plot.circle(result_dataset['X'], result_dataset['Y'], size=10, color="navy", alpha=0.5)
regression_plot.line(result_dataset['X'],y_predict.flatten(), color='red')


#################COMPARE AREAS########################
# Select options for list of all indicators
compare_areas_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
compare_areas_area_type_select.on_change('value', compare_areas_area_type_on_change)

# Select options for Area grouped by list
compare_areas_area_grouped_by_select = Select(title="Area grouped by", value="Region", options=["Region"])
#area_grouped_by_select.on_change('value', areas_grouped_by_on_change)
region_areas = get_entire_dataset(compare_areas_area_type_select.value)
compare_areas_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

# Select options for Areas in region
compare_areas_areas_in_region_select = Select(title="Region", value=compare_areas_list[0], options=compare_areas_list)
compare_areas_areas_in_region_select.on_change('value',  compare_areas_areas_in_region_on_change)

compare_areas_indicators_list = get_overview_indicators_list(compare_areas_area_type_select.value, compare_areas_areas_in_region_select.value,'2015 - 17')
compare_areas_indicator_select = Select(title='Indicator', value=compare_areas_indicators_list[0], options=compare_areas_indicators_list)
compare_areas_indicator_select.on_change('value', compare_areas_indicator_on_change)
#
compare_areas_indicators_button_group = CheckboxButtonGroup(labels=["All in "+compare_areas_areas_in_region_select.value, "All in England"], active=[0, 1])
#
compare_area_result_dataset = get_compare_areas_data(compare_areas_area_type_select.value, 
                                compare_areas_areas_in_region_select.value, 
                                compare_areas_indicator_select.value,
                                '2015 - 17')

Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in compare_area_result_dataset.columns] # bokeh columns
compare_areas_data_table = DataTable(columns=Columns, scroll_to_selection=True,selectable=True,
                       source=ColumnDataSource(compare_area_result_dataset),align ="center",
                       fit_columns=True,index_position = None,header_row = True,row_height=35, width_policy = "auto",index_header= "#",
                      width=1000, height=300) 

compare_areas_data_table.update()

##############################AREA PROFILES######################################
area_profiles_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
area_profiles_area_type_select.on_change('value', area_profiles_area_type_on_change)

# Select options for Area grouped by list
area_profiles_area_grouped_by_select = Select(title="Area grouped by", value="Region", options=["Region"])
#area_grouped_by_select.on_change('value', areas_grouped_by_on_change)
region_areas = get_entire_dataset(area_profiles_area_type_select.value)
area_profiles_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

# Select options for Areas in region
area_profiles_areas_in_region_select = Select(title="Area", value=compare_areas_list[0], options=compare_areas_list)
compare_areas_areas_in_region_select.on_change('value',  area_profiles_areas_in_region_on_change)

areas_list = get_areas_for_region(area_profiles_area_type_select.value,area_profiles_areas_in_region_select.value,'2015 - 17')
# Select options for Areas in region
area_profiles_areas_of_region_select = Select(title="Region", value=areas_list[0], options=areas_list)
area_profiles_areas_of_region_select.on_change('value',  area_profiles_areas_of_region_on_change)

area_profiles_dataset = get_area_profiles_data(area_profiles_area_type_select.value,area_profiles_areas_of_region_select.value,'2015 - 17')

area_profiles_data_table = DataTable(columns=Columns, scroll_to_selection=True,selectable=True,
                       source=ColumnDataSource(area_profiles_dataset),align ="center",
                       fit_columns=True,index_position = None,header_row = True,row_height=35, width_policy = "auto",index_header= "#",
                      width=1000, height=300) 
area_profiles_data_table.update()
#########################ENGLAND######################################
england_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
temp_dataset = get_new_data_populated(england_area_type_select.value,'England','2015 - 17').iloc[:,[0,10]]
Columns = [TableColumn(field=Ci, title=Ci, width=50, formatter=HTMLTemplateFormatter(template=template)) for Ci in temp_dataset.columns] # bokeh columns
england_data_table = DataTable(columns=Columns, scroll_to_selection=True,selectable=True,
                       source=ColumnDataSource(temp_dataset),
                       fit_columns=True,index_position = None,header_row = True,
                      width=500, height=300) 
england_area_type_select.on_change('value', england_area_type_on_change)
###################################BOX PLOTS#########################################################
box_plots_area_type_select = Select(title="Area Type", value="CountyUA", options=["CountyUA", "DistrictUA", "Region"])
box_plots_area_type_select.on_change('value', box_plots_area_type_on_change)

# Select options for Area grouped by list
box_plots_area_grouped_by_select = Select(title="Area grouped by", value="Region", options=["Region"])
#area_grouped_by_select.on_change('value', areas_grouped_by_on_change)
region_areas = get_entire_dataset(area_profiles_area_type_select.value)
box_plots_regions_list = region_areas.loc[region_areas['Parent Name']!='England']['Parent Name'].dropna().unique().tolist()

# Select options for Areas in region
box_plots_areas_in_region_select = Select(title="Region", value=box_plots_regions_list[0], options=box_plots_regions_list)
box_plots_areas_in_region_select.on_change('value',  box_plots_areas_in_region_on_change)

box_plots_areas_list = get_areas_for_region(box_plots_area_type_select.value,box_plots_areas_in_region_select.value,'2015 - 17')
# Select options for Areas in region
box_plots_areas_of_region_select = Select(title="Area", value=box_plots_areas_list[0], options=box_plots_areas_list)
#box_plots_areas_of_region_select.on_change('value',  box_plots_areas_of_region_on_change)

box_plots_indicators_list = get_overview_indicators_list(box_plots_area_type_select.value, box_plots_areas_in_region_select.value,'2015 - 17')

box_plots_indicator_select = Select(title='Indicator', value=box_plots_indicators_list[0], options=box_plots_indicators_list)
box_plots_indicator_select.on_change('value', box_plots_indicator_on_change)

grouped_quantile_data = get_boxplot_indicator_data(box_plots_area_type_select.value,box_plots_areas_in_region_select.value,box_plots_indicator_select.value)

box_plot_dataset = get_boxplot_data_table(grouped_quantile_data)

quantile_05 = pd.DataFrame(grouped_quantile_data.quantile(q=0.05).dropna())
quantile_1 = pd.DataFrame(grouped_quantile_data.quantile(q=0.25).dropna())
quantile_2 = pd.DataFrame(grouped_quantile_data.quantile(q=0.5).dropna())
quantile_3 = pd.DataFrame(grouped_quantile_data.quantile(q=0.75).dropna())
quantile_95 = pd.DataFrame(grouped_quantile_data.quantile(q=0.95).dropna())
 
iqr = quantile_3-quantile_1
upper = quantile_3 + 1.5 * iqr
lower = quantile_1 - 5.5 * iqr

upper.Value = [min([x,y]) for (x,y) in zip(list(quantile_95.loc[:,'Value']),upper.Value)]
lower.Value = [max([x,y]) for (x,y) in zip(list(quantile_05.loc[:,'Value']),lower.Value)]

time_period_list = box_plot_dataset['Time Period'].dropna().tolist()

box_plots = figure(tools="", background_fill_color="#efefef", x_range=time_period_list, toolbar_location=None, height=500,width=1500)
# stems
box_plots.segment(time_period_list, upper.Value, time_period_list, quantile_3.Value, line_color="black")
box_plots.segment(time_period_list, lower.Value, time_period_list, quantile_1.Value, line_color="black")
# boxes
box_plots.vbar(time_period_list, 0.7, quantile_2.Value, quantile_3.Value, fill_color="#E08E79", line_color="black")
box_plots.vbar(time_period_list, 0.7, quantile_1.Value, quantile_2.Value, fill_color="#3B8686", line_color="black")

# whiskers (almost-0 height rects simpler than segments)
box_plots.rect(time_period_list, lower.Value, 0.2, 0.01, line_color="black")
box_plots.rect(time_period_list, upper.Value, 0.2, 0.01, line_color="black")

## outliers
#if not box_plot_outliers.empty:
#    box_plots.circle(box_plot_outlier_x, box_plot_outlier_y, size=6, color="#F38630", fill_alpha=0.6)
                     
box_plots.xgrid.grid_line_color = None
box_plots.ygrid.grid_line_color = "white"
box_plots.grid.grid_line_width = 2
box_plots.xaxis.major_label_text_font_size="12pt"
#
Columns = [TableColumn(field=Ci, title=Ci, width=50) for Ci in box_plot_dataset.columns] # bokeh columns
box_plot_data_table = DataTable(columns=Columns, scroll_to_selection=True,selectable=True,
                       source=ColumnDataSource(box_plot_dataset),align ="center",
                       fit_columns=True,index_position = None,header_row = True,row_height=35, width_policy = "auto",index_header= "#",
                      width=1500, height=300) 
box_plot_data_table.update()
#####################CREATING PANELS##################################
overview = Panel(child=layout([overview_area_type_select,overview_area_grouped_by_select],[overview_areas_in_region_select],[overview_data_table],width=400), title="Overview")
compare_indicators = Panel(child=layout([compare_indicators_area_type_select,compare_indicators_area_grouped_by_select],
                                        [compare_indicators_areas_in_region_select],[compare_x_indicator_select],[compare_y_indicator_select],
                                        [compare_all_indicators_button_group],[regression_plot], 
                                        width=400),title="Compare Indicators")

maps = Panel(child=layout([]),title="Map")
trends = Panel(child=layout([]),title="Trends")
compare_areas = Panel(child=layout([compare_areas_area_type_select,compare_areas_area_grouped_by_select], 
                                   [compare_areas_areas_in_region_select],
                                   [compare_areas_indicator_select],
                                   [compare_areas_indicators_button_group],
                                   [compare_areas_data_table],
                                   width=400),title="Compare Areas")
area_profiles = Panel(child=layout([area_profiles_area_type_select,area_profiles_area_grouped_by_select],
                                   [area_profiles_areas_of_region_select,area_profiles_areas_in_region_select],
                                   [area_profiles_data_table]),title="Area profiles")
inequalities = Panel(child=layout([]),title="Inequalities")
england = Panel(child=layout([england_area_type_select],[england_data_table]),title="England")
population = Panel(child=layout([]),title="Population")
box_plots_panel = Panel(child=layout([box_plots_area_type_select,box_plots_area_grouped_by_select,
                                      box_plots_areas_in_region_select,box_plots_areas_of_region_select,
                                      box_plots_indicator_select],[box_plots],[box_plot_data_table]),title="Box plots")
definitions = Panel(child=layout([]),title="Definitions")
downloads = Panel(child=layout([]),title="Downloads")
life_exp = Tabs(tabs=[overview,compare_indicators,
                      maps,trends,compare_areas,area_profiles,
                      inequalities,england,population,box_plots_panel,
                      definitions,downloads])

life_exp_panel = Panel(child=life_exp, title="Life expectancy and causes of death")

local_authority_tabs = Tabs(tabs=[ life_exp_panel])
# Determine where the visualization will be rendered
#output_file('output_file_test.html', title='Public Health Profiles')
curdoc().add_root(local_authority_tabs)

#bokeh serve --show public-health.py