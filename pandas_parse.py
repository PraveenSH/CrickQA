import pandas as pd

tables = pd.read_html("http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;home_or_away=2;orderby=batting_average;team=6;template=results;type=batting")
table = tables[2]

result = table[['Player', 'Ave']][table['Mat']>=10]
print(result[:4])
