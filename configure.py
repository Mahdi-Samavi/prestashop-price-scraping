import sqlite3
from tabulate import tabulate

class Configure():
    def __init__(self):
        self.con = sqlite3.connect('database')
        self.cur = self.con.cursor()

    def asking(self):
        ask = input('Add again? (Y/N)')
        if (ask == 'N'):
            self.repeat = False

    def addAdmin(self):
        self.cur.execute('''
            INSERT INTO admins (name, url, username, password) VALUES (?, ?, ?, ?)
        ''', [self.adminName, self.adminUrl, self.username, self.password])
        self.con.commit()

    def addProduct(self):
        self.cur.execute('''
            INSERT INTO products (admin_id, name, product_id, scrap_url, xpath) VALUES (?, ?, ?, ?, ?)
        ''', [self.adminId, self.productName, self.productId, self.scrapUrl, self.xPath])
        self.con.commit()

    def setAdmin(self):
        self.repeat = True
        while self.repeat:
            self.adminName = input('Enter your admin name: ')
            self.adminUrl = input('Enter your admin url page: ')
            self.username = input('Enter your username: ')
            self.password = input('Enter your password: ')
            self.addAdmin()
            self.asking()

    def setProduct(self):
        self.repeat = True
        while self.repeat:
            self.adminId = int(input('Admin id: '))
            self.productName = input('Product name: ')
            self.productId = int(input('editing product id: '))
            self.scrapUrl = input('Scrap url page for getting data: ')
            self.xPath = input('xPath of element: ')
            self.addProduct()
            self.asking()
    
    def getAdmins(self):
        admins = self.cur.execute('SELECT * FROM admins').fetchall()
        print(tabulate([('id', 'name', 'url', 'username', 'password')] + admins, headers='firstrow', tablefmt='grid'))
    
    def getProducts(self):
        products = self.cur.execute('SELECT * FROM products').fetchall()
        print(tabulate([('id', 'admin id', 'name', 'editing product id', 'scrap url', 'xPath')] + products, headers='firstrow', tablefmt='grid'))