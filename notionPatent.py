from notion.client import NotionClient
from patent import Patent
from table_schema import PATENT_INFO_SCHEMA
from notion.block import CollectionViewBlock, HeaderBlock, CalloutBlock, ToggleBlock, ImageBlock, TextBlock
from os import listdir
import os


class NotionPatent:
    def __init__(self, number):
        self.patent = Patent(number)

        # Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
        self.client = NotionClient(
            token_v2=""
        )
        self.page = None
        self.__create_patent_page()

    def __create_patent_page(self):
        # Replace this URL with the URL of the page you want to edit
        cv = self.client.get_collection_view("")

        self.page = cv.collection.add_row()
        self.page.title = self.patent.number
        self.page.url = self.patent.url
        self.page.tag = 'A'
        self.page.name = self.patent.name
        self.page.summary = self.patent.summary

    def create_image(self):
        self.patent.download_all_image()
        folder_path = os.getcwd() + '/image'
        image_file_list = listdir(folder_path)
        image_file_list.sort()

        if len(image_file_list) == 0:
            print('No patent image')

        for image_file in image_file_list:
            image_block = self.page.children.add_new(ImageBlock)
            image_block.upload_file(folder_path + '/' + image_file)

    def create_summary_block(self):
        # How to use string literal to create emoji
        # https://stackoverflow.com/a/52953582
        summary = self.patent.summary
        if summary:
            self.page.children.add_new(HeaderBlock, title="摘要")
            self.page.children.add_new(CalloutBlock, title=summary, icon='\N{pushpin}')
        else:
            print("No summary")

    def create_patent_detail(self):
        patent_detail_text = self.patent.get_patent_detail_text()

        if patent_detail_text:
            patent_detail_section = self.page.children.add_new(ToggleBlock, title="詳細說明")
            patent_detail_section.children.add_new(TextBlock, title=patent_detail_text)
        else:
            print("No patent detail")

    def create_patent_range(self):
        patent_range_text = self.patent.get_patent_range_text()

        if patent_range_text:
            patent_range = self.page.children.add_new(ToggleBlock, title="專利範圍")
            patent_range.children.add_new(TextBlock, title=patent_range_text)
        else:
            print("No patent range")

    def create_patent_info(self):
        cvb = self.page.children.add_new(CollectionViewBlock)

        cvb.collection = self.client.get_collection(
            self.client.create_record("collection", parent=cvb, schema=PATENT_INFO_SCHEMA)
        )

        cvb.title = '書目資料'
        cvb.views.add_new(view_type="table")

        patent_info_df = self.patent.get_data()

        for i in range(patent_info_df.shape[0]):
            info_row = cvb.collection.add_row()
            info_row.name = patent_info_df.iloc[i].values[0]
            info_row.property = patent_info_df.iloc[i].values[1]