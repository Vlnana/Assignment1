import pandas as pd
import plotly.express as px

# 加载数据集
file_path = 'Macau_weather_dataset.xlsx'
df = pd.read_excel(file_path)

# 将 'Total rainfall' 列中的 'VST' 值替换为 0.1
df['Total rainfall'] = df['Total rainfall'].replace('VST', 0.1).astype(float)

# 将 'Date' 列转换为日期格式
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# 提取年份和月份
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

# 定义季节
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df['Season'] = df['Month'].apply(get_season)

# 选择数值列进行平均计算
numeric_columns = ['Mean maximum', 'Mean', 'Mean minimum', 'Mean relative humidity', 'Insolation duration', 'Total rainfall']

# 按年份和季节分组并计算数值列的平均值
seasonal_data = df.groupby(['Year', 'Season'])[numeric_columns].mean().reset_index()

# 定义季节颜色和顺序
season_colors = {
    'Spring': 'green',
    'Summer': 'red',
    'Autumn': 'orange',
    'Winter': 'blue'
}
season_order = ['Spring', 'Summer', 'Autumn', 'Winter']

# 创建交互式图表
fig_temp = px.line(seasonal_data, x='Year', y='Mean', color='Season',
                   category_orders={'Season': season_order},
                   color_discrete_map=season_colors,
                   title='Mean Temperature Comparison by Year and Season',
                   labels={'Mean': 'Mean Temperature (°C)'})

fig_rainfall = px.line(seasonal_data, x='Year', y='Total rainfall', color='Season',
                       category_orders={'Season': season_order},
                       color_discrete_map=season_colors,
                       title='Total Rainfall Comparison by Year and Season',
                       labels={'Total rainfall': 'Total Rainfall (mm)'})
fig_insolation = px.line(seasonal_data, x='Year', y='Insolation duration', color='Season',
                       category_orders={'Season': season_order},
                       color_discrete_map=season_colors,
                       title='Insolation duration Comparison by Year and Season',
                       labels={'Insolation duration': 'Insolation duration (h)'})
# 显示图表
fig_temp.show()
fig_rainfall.show()
fig_insolation.show()
