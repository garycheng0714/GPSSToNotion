from notion.client import NotionClient
from global_patent import Patent
from notion.block import CollectionViewBlock
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-n", "--number", help="The number of patent")
args = parser.parse_args()

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
client = NotionClient(token_v2="")

# Replace this URL with the URL of the page you want to edit
cv = client.get_collection_view("")


# https://github.com/jamalex/notion-py/blob/56b7a904474619cf60c4768db435c921ca18f44f/notion/smoke_test.py#L177
def get_collection_schema():
    return {
        "dV$q": {"name": "Property", "type": "text"},
        "title": {"name": "Name", "type": "title"},
    }


patent = Patent(args.number)

# create property
row = cv.collection.add_row()
row.title = patent.number
row.url = patent.url
row.tag = 'A'
row.name = patent.get_name()
row.summary = patent.get_summary()

# create database (table)
cvb = row.children.add_new(CollectionViewBlock)

cvb.collection = client.get_collection(
    client.create_record("collection", parent=cvb, schema=get_collection_schema())
)

cvb.title = 'Information'
cvb.views.add_new(view_type="table")

patent_info_df = patent.get_data()

for i in range(patent_info_df.shape[0]):
    info_row = cvb.collection.add_row()
    info_row.name = patent_info_df.iloc[i].values[0]
    info_row.property = patent_info_df.iloc[i].values[1]


# if __name__ == '__main__':
#     main()
