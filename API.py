import untangle
import requests
import mysql.connector
import sys
import pandas
pandas.set_option('display.height', 1000)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
import numpy
from mysql.connector import Error


class API(object):
    def __init__(self,):
        self.purchaseUrl = 'http://www.directtextbook.com/xml_buyback.php?'
        self.sellUrl = 'http://www.directtextbook.com/xml.php?'
        self.key = '09b44e468dc53813a073c66dd1c4aea8'
        self.booksInfo = []

    def run(self, isbnList):

        for isbn in isbnList:
            bookInfo = BookInfo(isbn)
            buyBackResponse = requests.get(self.purchaseUrl+'key='+self.key+'&ean='+isbn)
            cleanDecodedContent = self.clean_response(buyBackResponse.content)
            purchaseObject = self.untangle(cleanDecodedContent)
            self.package(bookInfo, purchaseObject, 'Purchase')

            sellResponse = requests.get(self.sellUrl+'key='+self.key+'&ean='+bookInfo.isbn)
            cleanDecodedContent = self.clean_response(sellResponse.content)
            sellObject = self.untangle(cleanDecodedContent)
            self.package(bookInfo, sellObject, 'Sell')

            self.booksInfo.append(bookInfo)

    def package(self, bookInfo, resultsObject, type):
        rows = []

        try:
            bookInfo.title = resultsObject.book.title.cdata
        except:
            bookInfo.title = None

        try:
            bookInfo.author = resultsObject.book.author.cdata
        except:
            bookInfo.author = None

        try:
            bookInfo.edition = resultsObject.book.edition.cdata
        except:
            bookInfo.edition = None

        try:
            for item in resultsObject.book.items.item:

                try:
                    vendor = item.vendor.cdata
                except:
                    vendor = None
                try:
                    price = item.price.cdata
                except:
                    price = None
                try:
                    condition = item.condition.cdata
                except:
                    condition = None

                rows.append(Row(vendor, price, condition, type))

            if type == 'Purchase':
                bookInfo.purchaseInfo = Info(rows)
            else:
                bookInfo.sellInfo = Info(rows)

        except:
            if type == 'Purchase':
                bookInfo.purchaseInfo = None
            else:
                bookInfo.sellInfo = None

    def clean_response(self, response):
        decodedResponse = response.decode('utf-8')
        cleanDecodedResponse = decodedResponse.replace(' <', '<')
        return cleanDecodedResponse

    def untangle(self, cleanDecodedResponse):
        o = untangle.parse(cleanDecodedResponse)
        return o

    def show(self):
        for bookInfo in self.booksInfo:
            try:
                for purchaseRow in bookInfo.purchaseInfo.rows:
                    print('{} {} {} {} {} {} {} {}'.format(bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, purchaseRow.vendor, purchaseRow.price, purchaseRow.condition, purchaseRow.type))
            except:
                print('There are no purchase prices for this book')

            try:
                for sellRow in bookInfo.sellInfo.rows:
                    print('{} {} {} {} {} {} {} {}'.format(bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, sellRow.vendor, sellRow.price, sellRow.condition, sellRow.type))
            except:
                print('There are no selling prices for this book')
        self.translate_to_data_frame()

    def show_statistics(self):
        pass


    def translate_to_data_frame(self):
        for bookInfo in self.booksInfo:
            try:
                purchaseData = []
                for purchaseRow in bookInfo.purchaseInfo.rows:
                    purchaseData.append([bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, purchaseRow.vendor, purchaseRow.price, purchaseRow.condition, purchaseRow.type])

                df = pandas.DataFrame(purchaseData, columns=['Title', 'Author', 'ISBN', 'Edition', 'Vendor', 'Price', 'Condition', 'Type'])
                print(df)
            except:
                print('There are no purchase prices for this book')

            try:
                sellData = []
                for sellRow in bookInfo.sellInfo.rows:
                    sellData.append([bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, sellRow.vendor, sellRow.price, sellRow.condition, sellRow.type])
                df = pandas.DataFrame(sellData, columns=['Title', 'Author', 'ISBN', 'Edition', 'Vendor', 'Price', 'Condition', 'Type'])
                print(df)
            except:
                print('There are no selling prices for this book')





class Row(object):
    def __init__(self, vendor, price, condition, type):
        self.vendor = vendor
        self.price = price
        self.condition = condition
        self.type = type

class BookInfo(object):
    def __init__(self, isbn):
        self.isbn = isbn
        self.title = None
        self.author = None
        self.edition = None
        self.purchaseInfo = None
        self.sellInfo = None

class Info(object):
    def __init__(self, rows):
        self.rows = rows

class DataBaseDelegate(object):
    def __init__(self, ip, database, user, password):
        self.connect(ip, database, user, password)
        self.cursor = self.connection.cursor()

    def connect(self, ip, database, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=ip,
                database=database,
                user=user,
                password=password
            )
            if self.connection.is_connected():
                print('Successfully connected to {}'.format(database))
        except Error as e:
            print('Unable to connect to {}'.format(database))
            print(e)

    def get_book_ids(self):
        isbns = []
        self.cursor.callproc('show_book_ISBNs')
        results = self.cursor.stored_results()
        unpackedResults = self.unpack(results)

        for x in unpackedResults:
            isbns.append(x[0])

        return isbns

    def insert_book(self, bookInfo):
        self.cursor.callproc('insert_book', [bookInfo.title, bookInfo.author, bookInfo.edition, bookInfo.isbn, ''])
        self.connection.commit()

    def unpack(self, results):
        """Unpacks the results of fetchall() into a local list"""
        temp = []
        list = []
        for result in results:
            temp.append(result.fetchall())
        for x in temp:
            for y in x:
                list.append(y)
        return list

    def close(self):
        self.cursor.close()
        self.connection.close()

class WarehouseDelegate(object):
    def __init__(self, ip , database, user, password):
        self.connect(ip, database, user, password)
        self.cursor = self.connection.cursor()

    def connect(self, ip, database, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=ip,
                database=database,
                user=user,
                password=password
            )
            if self.connection.is_connected():
                print('Successfully connected to {}'.format(database))
        except Error as e:
            print('Unable to connect to {}'.format(database))
            print(e)

    def insert_book_info(self, booksInfo):

        for bookInfo in booksInfo:
            try:
                for row in bookInfo.sellInfo.rows:
                    self.cursor.callproc('insert_api_data', [bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, row.vendor, row.price, row.condition, row.type])
                    self.connection.commit()
            except:
                pass

            try:
                for row in bookInfo.purchaseInfo.rows:
                    self.cursor.callproc('insert_api_data',[bookInfo.title, bookInfo.author, bookInfo.isbn, bookInfo.edition, row.vendor, row.price, row.condition, row.type])
                    self.connection.commit()
            except:
                pass

    def close(self):
        self.cursor.close()
        self.connection.close()

class Controller(object):
    def __init__(self):
        self.databaseDelegate = DataBaseDelegate('35.197.44.156', 'alexandriabooks', 'Justin Needham', 'DeoJuvante')
        self.warehouseDelegate = WarehouseDelegate('35.197.44.156', 'alexandria_data_warehouse', 'Justin Needham', 'DeoJuvante')
        self.api = API()

    def run(self):
        self.api.run(self.databaseDelegate.get_book_ids())
        self.databaseDelegate.close()

        self.warehouseDelegate.insert_book_info(self.api.booksInfo)
        self.warehouseDelegate.close()

    def search(self, isbnList):
        self.api.run(isbnList)
        self.warehouseDelegate.insert_book_info(self.api.booksInfo)
        self.check_isbns_against_database(isbnList)
        self.api.show()

    def check_isbns_against_database(self, isbnList):
        """Checks the search isbns against the existing isbns in the database, if they don't exist, call api and update"""
        existingIsbns = self.databaseDelegate.get_book_ids()

        for isbn in isbnList:
            if isbn not in existingIsbns:
                for bookInfo in self.api.booksInfo:
                    if bookInfo.isbn == isbn:
                        self.databaseDelegate.insert_book(bookInfo)
                        print('Successfully added book {} to database'.format(bookInfo.isbn))

    def read_args(self, args):
        try:
            if args[1].lower().strip() == 'search':
                isbns = []
                for x in args[2:]:
                    isbns.append(x.replace(",", ''))

                self.search(isbns)

            elif args[1].lower().strip() == 'run':
                self.run()

            else:
                print('Not a valid command')

        except IndexError:
            print('Please provide a command after script name')
            print("Example: 'python API.py run")

controller = Controller()
controller.read_args(sys.argv)


















