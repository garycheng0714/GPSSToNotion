from argparse import ArgumentParser
from notionPatent import NotionPatent
import pandas as pd

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
        notion_patent.create_patent_range()
        notion_patent.create_patent_detail()
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


if __name__ == '__main__':
    main()
