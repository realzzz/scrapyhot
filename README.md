# scrapyhot

A web spider for hot contents using scrapy framework

# What does it do?
The spider crawl hot keywords from weibo, baidu and sogou, and store them in mysql db

# How to run it?
1. First initialize mysql table using [hots.sql](./hots.sql)
2. Set up DB information in [HotPipelineLocal](./pipelines.py)
3. run the python script [autorunhot.py](./autorunhot.py)


