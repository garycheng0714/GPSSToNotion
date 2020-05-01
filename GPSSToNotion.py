from notion.client import NotionClient
from global_patent import Patent
from notion.block import CollectionViewBlock, HeaderBlock, CalloutBlock, ToggleBlock, ImageBlock
from argparse import ArgumentParser
from os import listdir
import pandas as pd
import os

parser = ArgumentParser()
parser.add_argument("-n", "--number", help="The number of patent")
parser.add_argument("-f", "--file", help="Get all images of the patent in the excel file")
args = parser.parse_args()


def main():
    patent_numbers = get_patent_numbers_from_excel() if args.file else [args.number]

    for number in patent_numbers:
        print(f'Start to create {number}')
        notion_patent = NotionPatent(number)
        notion_patent.create_summary_block()
        notion_patent.create_patent_info()
        notion_patent.create_patent_detail()
        notion_patent.create_patent_range()
        notion_patent.create_case_status()
        notion_patent.create_right_change()
        notion_patent.create_image()
        print(f'Finish {number}')


def get_patent_numbers_from_excel():
    df = pd.read_excel(args.file)
    return df.iloc[:, 0]


"""
Change the cover
"""
# for page in cv.collection.get_rows():
#     if page.title == 'D203134':
#         print(page.get('format.page_cover'))
#         page.set('format.page_cover', '/Users/garycheng/PycharmProjects/Notion/test.png')
#         print(page.get('format.page_cover'))


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
        self.page.name = self.patent.get_name()
        self.page.summary = self.patent.get_summary()

    def create_image(self):
        self.patent.download_all_image()
        folder_path = os.getcwd() + '/image'
        image_file_list = listdir(folder_path)
        image_file_list.sort()

        for image_file in image_file_list:
            image_block = self.page.children.add_new(ImageBlock)
            image_block.upload_file(folder_path + '/' + image_file)

    def create_summary_block(self):
        # How to use string literal to create emoji
        # https://stackoverflow.com/a/52953582
        self.page.children.add_new(HeaderBlock, title="摘要")
        self.page.children.add_new(CalloutBlock, title=self.patent.get_summary(), icon='\N{pushpin}')

    def create_patent_detail(self):
        toggle = None
        patent_detail_list = self.patent.get_patent_detail()

        if patent_detail_list:
            detail = [line.strip(' \t\n\r') for line in patent_detail_list.split("\n") if line != '']

            for line in detail:
                if "【" in line:
                    toggle = self.page.children.add_new(ToggleBlock, title=line)
                else:
                    toggle.children.add_new(ToggleBlock, title=line)
        else:
            print("No patent detail")

    def create_patent_range(self):
        patent_range_list = self.patent.get_patent_range_detail()

        if patent_range_list:
            range_text = [line.strip(' \t\n\r') for line in patent_range_list.split("\n") if line]
            patent_range = self.page.children.add_new(ToggleBlock, title="專利範圍")

            for line in range_text:
                patent_range.children.add_new(ToggleBlock, title=line)
        else:
            print("No patent range")

    def create_patent_info(self):
        cvb = self.page.children.add_new(CollectionViewBlock)

        cvb.collection = self.client.get_collection(
            self.client.create_record("collection", parent=cvb, schema=self.__get_info_schema())
        )

        cvb.title = '書目資料'
        cvb.views.add_new(view_type="table")

        patent_info_df = self.patent.get_data()

        for i in range(patent_info_df.shape[0]):
            info_row = cvb.collection.add_row()
            info_row.name = patent_info_df.iloc[i].values[0]
            info_row.property = patent_info_df.iloc[i].values[1]

    @staticmethod
    def __get_info_schema():
        return {
            "dV$q": {"name": "Property", "type": "text"},
            "title": {"name": "Name", "type": "title"}
        }

    def create_case_status(self):
        patent_case_status_df = self.patent.get_case_status()

        if patent_case_status_df is not None:
            cvb = self.page.children.add_new(CollectionViewBlock)

            cvb.collection = self.client.get_collection(
                self.client.create_record("collection", parent=cvb, schema=self.__get_case_status_schema())
            )

            cvb.title = '案件狀態'
            cvb.views.add_new(view_type="table")

            for i in range(patent_case_status_df.shape[0]):
                status_row = cvb.collection.add_row()
                status_row.專利申請案號 = self.get_value(patent_case_status_df, i, 0)
                status_row.a狀態異動日期 = self.get_value(patent_case_status_df, i, 1)
                status_row.b案件申請日期 = self.get_value(patent_case_status_df, i, 2)
                status_row.c實體審查申請日 = self.get_value(patent_case_status_df, i, 3)
                status_row.d相關申請案號 = self.get_value(patent_case_status_df, i, 4)
                status_row.e公開號 = self.get_value(patent_case_status_df, i, 5)
                status_row.f公告號 = self.get_value(patent_case_status_df, i, 6)
                status_row.g證書號 = self.get_value(patent_case_status_df, i, 7)
                status_row.h專利類別 = self.get_value(patent_case_status_df, i, 8)
                status_row.i狀態異動資料 = self.get_value(patent_case_status_df, i, 9)
                status_row.j申請案狀態異動資料 = self.get_value(patent_case_status_df, i, 10)
        else:
            print("No case status")

    @staticmethod
    def get_value(df, index, column):
        value = str(df.iloc[index].values[column])
        return value if value != "nan" else ""

    @staticmethod
    def __get_case_status_schema():
        return {
            "title": {"name": "專利申請案號", "type": "text"},
            "1": {"name": "a狀態異動日期", "type": "text"},
            "2": {"name": "b案件申請日期", "type": "text"},
            "3": {"name": "c實體審查申請日", "type": "text"},
            "4": {"name": "d相關申請案號", "type": "text"},
            "5": {"name": "e公開號", "type": "text"},
            "6": {"name": "f公告號", "type": "text"},
            "7": {"name": "g證書號", "type": "text"},
            "8": {"name": "h專利類別", "type": "text"},
            "9": {"name": "i狀態異動資料", "type": "text"},
            "10": {"name": "j申請案狀態異動資料", "type": "text"}
        }

    def create_right_change(self):
        patent_right_change_df = self.patent.get_right_change()

        if patent_right_change_df is not None:
            cvb = self.page.children.add_new(CollectionViewBlock)

            cvb.collection = self.client.get_collection(
                self.client.create_record("collection", parent=cvb, schema=self.__get_right_change_schema())
            )

            cvb.title = '權利異動'
            cvb.views.add_new(view_type="table")

            for i in range(patent_right_change_df.shape[0]):
                status_row = cvb.collection.add_row()
                status_row.專利申請案號 = self.get_value(patent_right_change_df, i, 0)
                status_row.a授權註記 = self.get_value(patent_right_change_df, i, 1)
                status_row.b質權註記 = self.get_value(patent_right_change_df, i, 2)
                status_row.c讓與註記 = self.get_value(patent_right_change_df, i, 3)
                status_row.d繼承註記 = self.get_value(patent_right_change_df, i, 4)
                status_row.e信託註記 = self.get_value(patent_right_change_df, i, 5)
                status_row.f異議註記 = self.get_value(patent_right_change_df, i, 6)
                status_row.g舉發註記 = self.get_value(patent_right_change_df, i, 7)
                status_row.h消滅日期 = self.get_value(patent_right_change_df, i, 8)
                status_row.i撤銷日期 = self.get_value(patent_right_change_df, i, 9)
                status_row.j專利權始日 = self.get_value(patent_right_change_df, i, 10)
                status_row.k專利權止日 = self.get_value(patent_right_change_df, i, 11)
                status_row.l年費有效日期 = self.get_value(patent_right_change_df, i, 12)
                status_row.m年費有效年次 = self.get_value(patent_right_change_df, i, 13)
        else:
            print("No rights changed")

    @staticmethod
    def __get_right_change_schema():
        return {
            "title": {"name": "專利申請案號", "type": "text"},
            "1": {"name": "a授權註記", "type": "text"},
            "2": {"name": "b質權註記", "type": "text"},
            "3": {"name": "c讓與註記", "type": "text"},
            "4": {"name": "d繼承註記", "type": "text"},
            "5": {"name": "e信託註記", "type": "text"},
            "6": {"name": "f異議註記", "type": "text"},
            "7": {"name": "g舉發註記", "type": "text"},
            "8": {"name": "h消滅日期", "type": "text"},
            "9": {"name": "i撤銷日期", "type": "text"},
            "10": {"name": "j專利權始日", "type": "text"},
            "11": {"name": "k專利權止日", "type": "text"},
            "12": {"name": "l年費有效日期", "type": "text"},
            "13": {"name": "m年費有效年次", "type": "text"}
        }


if __name__ == '__main__':
    main()
