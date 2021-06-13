# GPSSToNotion
Get patent info from GPSS then write date into Notion

# [How to get Notion v2 token](https://www.redgregory.com/notion/2020/6/15/9zuzav95gwzwewdu1dspweqbv481s5)

# How to run

1. Set token_v2 in notionPatent.py
2. Set the notion url that you want to edit in notionPatent.py line 22, like [this url]((https://www.notion.so/6356b712fd1d4ccfa9d1aee08a097805?v=3ff6f5fef40c411eaedb4fd4d8956ff1))

```python
$ python GPSSToNotion.py -n US20200120829A1

or

$ python GPSSToNotion.py -f list_of_patent_numbers.excel
```

# Python Package
* [pipenv](https://medium.com/@chihsuan/pipenv-%E6%9B%B4%E7%B0%A1%E5%96%AE-%E6%9B%B4%E5%BF%AB%E9%80%9F%E7%9A%84-python-%E5%A5%97%E4%BB%B6%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7-135a47e504f4)
* [notion](https://pypi.org/project/notion/)
* [notion collection example](https://github.com/jamalex/notion-py#example-working-with-databases-aka-collections-tables-boards-etc)
* [argparse](https://dboyliao.medium.com/python-%E8%B6%85%E5%A5%BD%E7%94%A8%E6%A8%99%E6%BA%96%E5%87%BD%E5%BC%8F%E5%BA%AB-argparse-4eab2e9dcc69)
* [Pandas](https://www.learncodewithmike.com/2020/12/read-excel-file-using-pandas.html)
* [Beautiful Soup](https://blog.gtwang.org/programming/python-beautiful-soup-module-scrape-web-pages-tutorial/)
* [Selenium](https://medium.com/marketingdatascience/selenium%E6%95%99%E5%AD%B8-%E4%B8%80-%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8webdriver-send-keys-988816ce9bed)
* [df.iloc](https://medium.com/@b89202027_37759/%E5%AF%A6%E7%94%A8%E4%BD%86%E5%B8%B8%E5%BF%98%E8%A8%98%E7%9A%84pandas-dataframe%E5%B8%B8%E7%94%A8%E6%8C%87%E4%BB%A4-1-976f48eb2bd5)

# Troubleshooting

* notion: [requests.exceptions.HTTPError: Invalid input.](https://stackoverflow.com/a/66546826)
* chromedriver can not use --headless, the GPSS website will block you

# Note

* [url for develop this tool](https://www.notion.so/6356b712fd1d4ccfa9d1aee08a097805?v=3ff6f5fef40c411eaedb4fd4d8956ff1)
* notion package collection structure

```
File Structure
|-- Get Started
		|-- hidden layer (collection view)
				|-- test (collection)
						|-- Page 1 (collection row block)
								|-- collection container (collection view block)
										|-- table (collection)
						|-- Page 2 (collection row block)
						|-- Page 3 (collection row block)
"""
cv = client.get_collection_view(hidden_layer_url_or_id)

collection = cv.collection # It's test

# print out "Page1", "Page2", "Page3"
for row in collection.get_rows():
		print(row.name)

"""
create Page 4 under test
"""

row_page_4 = collection.add_row()
row_page_4.title = "Page 4"

"""
create table under Page 1 (collection row block)
"""
page1 = collectin.get_rows()[0]

# create collection container(collection view block) to store collection (e.g. table)
cvb = page1.children.add_new(CollectionViewBlock)

# set collection property to collection container
cvb.collection = client.get_collection(
		client.create_record("collection", parent=cvb)
)

cvb.title = "Set collection container title"

# create table under collection container
cvb.views.add_new(view_type="table")

# add row to collection
row = cvb.collection.add_raw()

```