import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('main.db')
        self.cursor = self.con.cursor()

        
    def create_table(self):
        self.cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY AUTOINCREMENT,
        chat_id integer,
        lang varchar(3),
        contact varchar(20)
    )
    """)
        
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS location (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                address TEXT,
                UNIQUE(chat_id, address)  -- UNIQUE cheklovi bu yerda qo'llaniladi
            )
        """)

        self.cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS basket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product INTEGER NOT NULL,
        count INTEGER NOT NULL,
        total_price INTEGER,
        user integer,
        FOREIGN KEY (user) REFERENCES users(chat_id)
);
""")
        
        self.cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name VARCHAR(255) UNIQUE
    )
    """)
        
        self.cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT,
        category INTEGER,
        FOREIGN KEY (category) REFERENCES Categories(id)
    )
    """)
        
        self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT NOT NULL,
        count INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        user INTEGER NOT NULL,
        phone VARCHAR(255) NOT NULL,
        address TEXT NOT NULL,
        FOREIGN KEY (user) REFERENCES users(chat_id)
        FOREIGN KEY (phone) REFERENCES users(contact)
        FOREIGN KEY (address) REFERENCES location(address)
)
""")
        self.con.commit()
    



    def insert_user(self, chat_id, lang):
        self.cursor.execute(f"""
    insert into users(chat_id, lang) values (?, ?)
    """, (chat_id,lang,))
        self.con.commit()


    def get_contact(self, chat_id):    
        self.cursor.execute(f"""
    select contact from users where chat_id = ?
    """, (chat_id,))
        contact = self.cursor.fetchone()[0]
        return contact


    def all_chat_id(self):
        self.cursor.execute(f"""select chat_id from users""")
        chat_id = [i[0] for i in self.cursor.fetchall()]
        return chat_id


    def language(self, lang, chat_id):
        self.cursor.execute(f"""
    UPDATE users
    SET lang = ?
    WHERE chat_id = ?
    """, (lang, chat_id,))
        self.con.commit()
        
    def update_contact(self, contact, chat_id):
        # if cursor.fetchone() is not None:
        self.cursor.execute(f"""
    UPDATE users
    SET contact = ?
    WHERE chat_id = ?
    """, (contact, chat_id))
        self.con.commit()
        print(f"Контакт {contact} успешно обновлён для chat_id {chat_id}.")


    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        return rows


    def check_language(self, chat_id):
        self.cursor.execute("SELECT lang FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        # print(result)
        return result[0] if result else None
    

        
    def insert_location(self, chat_id, address):
        try:
            self.cursor.execute("""
                INSERT INTO location (chat_id, address) 
                VALUES (?, ?)
            """, (chat_id, address))
            self.con.commit()
            print("Manzil qo'shildi")
        except sqlite3.IntegrityError:
            print("Bu manzil allaqachon mavjud")

    def update_location(self, address, chat_id):
            self.cursor.execute("""
    UPDATE location SET address = ? WHERE chat_id = ?
    """, (address, chat_id,))
        
    def get_location_by_address(self, chat_id, address):
        self.cursor.execute("""
    SELECT address FROM location
    WHERE chat_id = ? AND address = ?
    """, (chat_id, address))
        return self.cursor.fetchone()
    
    def get_location(self, chat_id):
         self.cursor.execute("""
SELECT address FROM location WHERE chat_id = ?
""", (chat_id,))
         return self.cursor.fetchall()

    
    def delete_location(self):
          self.cursor.execute("DROP TABLE location")
          self.con.commit()
        


            
    def insert_category(self, category_name):
            self.cursor.execute("""
    INSERT INTO Categories (category_name)
    VALUES (?)
    """, (category_name,))
            self.con.commit()

    def get_all_categories(self):
            self.cursor.execute("SELECT * FROM Categories")
            rows = self.cursor.fetchall()
            return rows
        
    def get_category_id_by_name(self, name):
            self.cursor.execute("SELECT id FROM categories WHERE category_name = ?", (name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        
            

    

        
    def insert_product(self, name, description, price, image, category):
        self.cursor.execute("""
    INSERT INTO Products (name, description, price, image, category)
    VALUES (?, ?, ?, ?, ?)
    """, (name, description, price, image, category,))
        self.con.commit()

    def get_products_by_category_id(self, category_id):
            self.cursor.execute("SELECT * FROM Products WHERE category = ?", (category_id,))
            return self.cursor.fetchall()
    
    def get_product_name_by_category_id(self, category_id):
            self.cursor.execute("SELECT name FROM Products WHERE category = ?", (category_id,))
            return self.cursor.fetchone()
    
    def get_product_price_by_category_id(self, category_id):
            self.cursor.execute("SELECT price FROM Products WHERE category = ?", (category_id,))
            return self.cursor.fetchone()
    
    def get_products(self, product_name):
          self.cursor.execute("SELECT * FROM Products WHERE name = ?", (product_name,))
          return self.cursor.fetchall()
    
    
    def delete_product(self):
          self.cursor.execute("DELETE FROM Products")
          self.con.commit()

    

    def insert_product_to_basket(self, count, total_price, product, user_id):
    # Count o'zgaruvchisini to'g'ri turga o'zgartiring
        if isinstance(count, tuple):
            count = count[0]

        self.cursor.execute("""
        SELECT count, total_price FROM basket WHERE product=? AND user=?
        """, (product, user_id))
        existing_product = self.cursor.fetchone()

        if existing_product:
            # Agar mahsulot mavjud bo'lsa, sonini yangilash va umumiy narxni qo'shish
            new_count = existing_product[0] + count
            new_total_price = existing_product[1] + total_price
            self.cursor.execute("""
            UPDATE basket SET count=?, total_price=? WHERE product=? AND user=?
            """, (new_count, new_total_price, product, user_id))
        else:
            # Agar mahsulot mavjud bo'lmasa, yangi yozuv qo'shish
            self.cursor.execute("""
            INSERT INTO basket (product, count, total_price, user)
            VALUES (?, ?, ?, ?)
            """, (product, count, total_price, user_id))

        print("Savatga qo'shildi")
        self.con.commit()


    def get_product_price_by_name(self, name):
            self.cursor.execute("SELECT price FROM Products WHERE name =?", (name,))
            return self.cursor.fetchone()

    def get_basket(self, user_id):
        self.cursor.execute("""
        SELECT id, product, count, total_price FROM basket WHERE user=?
        """, (user_id,))
        items = self.cursor.fetchall()
        return items

    def calculate_total_price(self, user_id):
        self.cursor.execute("""
        SELECT SUM(product) FROM basket WHERE user=?
        """, (user_id,))
        total = self.cursor.fetchone()[0]
        return total if total else 0

        
    def delete_basket(self, user):
          self.cursor.execute("DELETE FROM basket WHERE user=?", (user,))
          self.con.commit()

    def remove_product_from_basket(self, chat_id, product_id):
          self.cursor.execute("DELETE FROM basket WHERE user=? AND id=?", (chat_id, product_id))
          self.con.commit()


    def drop_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS basket")
        self.con.commit()
        print("Tabellar o'chirildi")


    def insert_order(self, product, count, total_price, user_id, address, phone=None):
        if phone is None:
            self.cursor.execute("SELECT contact FROM users WHERE chat_id=?", (user_id,))
            phone_record = self.cursor.fetchone()
            if phone_record:
                phone = phone_record[0]
            else:
                return False, "Telefon raqami yo'q"

        self.cursor.execute("""
        INSERT INTO orders (product, count, total_price, user, phone, address)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (product, count, total_price, user_id, phone, address))
        
        self.con.commit()
        return True, "Buyurtma muvaffaqiyatli kiritildi"
    
    def get_my_orders(self, chat_id):
          self.cursor.execute("SELECT * FROM orders WHERE user=?", (chat_id,))
          orders = self.cursor.fetchall()
          return orders
    
    def delete_orders(self):
          self.cursor.execute("DELETE FROM orders")
          self.con.commit()




db = Database()



# if __name__ == "__main__":
#     print(get_contact(846986401))