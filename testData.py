from model import *
import random

firstNames = ['Justin', 'Laura', 'Josh', 'Jenna', 'Spencer', 'Emily', 'Nicola', 'Delaney', 'Holly']
lastNames = ['Nelson', 'Wolfley', 'Anderson', 'Needham', 'Musk', 'Bezos', 'Fitzpatrick']
titles = ['Atlas Shrugged', 'War and Peace', 'Zero to One', 'Candide', 'Ulysses ']
authors = ['Ayn Rand', 'Leo Tolstoy', 'Plato', 'Aristotle', 'Peter Thiel']
phoneNumbers = ['8016968074', '8015444220', '8017558112']
emails = ['crazyRiley@gmail.com', 'riseagainst9@msn.com', 'justneedham@gmail.com']
dates = ['10-12-12', '01-28-95', '02-14-20']
orderTypes = ['Sell Order', 'Buy Order']
transactionTypes = ['Paypal', 'Venmo', 'Square Cash']
prices = [10.51, 1.11, 15.32, 79.39, 65.69, 30.89, 100.32, 1.99]
tracking = ['382948573fjskfe', '5930gj39fkds8473', 'dkfj385ufncbsj4']
shipType = ['Buy Order Supplies', 'Buy Order', 'Sell Order']
numbers = [10, 20, 30, 40]
smallNumbers = [1,2,3,4,5,6,7,8,9]
shippingNumbers = [1,2,3]
ISBNs = ['24dk593049542', 'dkfjeir968594', 'fgjdnvl3i5jg94', 'dkfn439gjtu940']
conditions = ['Good', 'Acceptable', 'Like New', 'New']


class TestData():
    def __init__(self):
        self.orders = []
        for x in range(random.choice(numbers)):
            books = []
            for y in range(random.choice(smallNumbers)):
                orderItemData = {}
                orderItemData['Item Number'] = str(y)
                orderItemData['Title'] = random.choice(titles)
                orderItemData['Author'] = random.choice(authors)
                orderItemData['Edition'] = random.choice(smallNumbers)
                orderItemData['ISBN'] = random.choice(ISBNs)
                orderItemData['Condition'] = random.choice(conditions)
                orderItemData['Price'] = random.choice(prices)
                books.append(Order_Item(orderItemData))


            shipping = []
            for j in range(random.choice(smallNumbers)):

                shippingTypeArgs = {}
                shippingTypeArgs['Shipping Type ID'] = None
                shippingTypeArgs['Shipping Type Name'] = random.choice(shipType)

                shippingStatusArgs = {}
                shippingStatusArgs['Status ID'] = None
                shippingStatusArgs['Status Name'] = 'In-Transit'

                shippingArgs = {}
                shippingArgs['Connection'] = None
                shippingArgs['Shipping ID'] = None
                shippingArgs['Order ID'] = x
                shippingArgs['Shipping Cost'] = random.choice(prices)
                shippingArgs['Tracking'] = random.choice(tracking)
                shippingArgs['Shipping Date'] = random.choice(dates)
                shippingArgs['Expected Arrival'] = random.choice(dates)
                shippingArgs['Shipping Type'] = ShippingType(shippingTypeArgs)
                shippingArgs['Shipping Materials'] = None
                shippingArgs['Status'] = Status(shippingStatusArgs)
                shipping.append(Shipping_Order(shippingArgs))

            customerData = {}
            customerData['Customer ID'] = x
            customerData['First Name'] = random.choice(firstNames)
            customerData['Last Name'] = random.choice(lastNames)
            customerData['Phone Number'] = random.choice(phoneNumbers)
            customerData['Email'] = random.choice(emails)
            customerData['Date Joined'] = random.choice(dates)
            customerData['Referral Code'] = None
            customerData['Connection'] = None

            orderTypeArgs = {}
            orderTypeArgs['Order Type ID'] = None
            orderTypeArgs['Order Type Name'] = random.choice(orderTypes)

            transactionTypeArgs = {}
            transactionTypeArgs['Transaction Type ID'] = None
            transactionTypeArgs['Transaction Type Name'] = random.choice(transactionTypes)

            statusArgs = {}
            statusArgs['Status ID'] = None
            statusArgs['Status Name'] = 'Processing'

            orderData = {}
            orderData['Connection'] = None
            orderData['Order ID'] = x
            orderData['Customer'] = Customer(customerData)
            orderData['Order Type'] = OrderType(orderTypeArgs)
            orderData['Transaction'] = TransactionType(transactionTypeArgs)
            orderData['Amazon Order'] = None
            orderData['Order Date'] = random.choice(dates)
            orderData['Status'] = Status(statusArgs)
            orderData['Promotion Code'] = None
            orderData['Shipping'] = shipping
            orderData['Books'] = books

            self.orders.append(Order(orderData))

    def loadTestOrderView(self):
        rows = []
        for order in self.orders:
            rowArgs = {}
            rowArgs['Order ID'] = order.ID
            rowArgs['First Name'] = order.customer.firstName
            rowArgs['Last Name'] = order.customer.lastName
            rowArgs['Order Type'] = order.orderType.name
            rowArgs['Pay Method'] = order.transaction.name
            if order.amazonOrder == None:
                rowArgs['Amazon ID'] = 'None'
            else:
                rowArgs['Amazon ID'] = order.amazonOrder.ID
            rowArgs['Date'] = order.date
            rowArgs['Status'] = order.status.name
            rows.append(OrderRow(rowArgs))

        return rows

    def loadTestCustomerView(self):
        rows = []
        for order in self.orders:
            rowArgs = {}
            rowArgs['Customer ID'] = order.customer.ID
            rowArgs['First Name'] = order.customer.firstName
            rowArgs['Last Name'] = order.customer.lastName
            rowArgs['Email'] = order.customer.email
            rowArgs['Phone'] = order.customer.phone
            rowArgs['Date'] = order.customer.dateJoined
            rows.append(CustomerRow(rowArgs))

        return rows

    def loadOrders(self):
        return self.orders





