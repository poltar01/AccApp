from datetime import datetime
from kivy.uix.screenmanager import Screen,SlideTransition
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDRaisedButton
from kivy.utils import get_color_from_hex
import mysql.connector
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.toast import toast
import pytz

# con = mysql.connector.connect(
#     user = "sql11500459",
#     password = "hbKelUx9dX",
#     host = "sql11.freemysqlhosting.net",
#     database = "sql11500459",
#     auth_plugin='mysql_native_password'
# )

con = mysql.connector.connect(
    user = "root",
    password = "",
    host = "localhost",
    database = "accounting_db",
    auth_plugin='mysql_native_password'
)

cursor = con.cursor()


timeZ_Tr = pytz.timezone('Europe/Istanbul')
current_total_table_name = f"araba_{datetime.now(timeZ_Tr).day}_{datetime.now(timeZ_Tr).month}_{datetime.now(timeZ_Tr).year}_total"
current_logs_db_name = f"araba_{datetime.now(timeZ_Tr).day}_{datetime.now(timeZ_Tr).month}_{datetime.now(timeZ_Tr).year}_logs" # İLERDE LAZIM OLACAK

cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {current_total_table_name} (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        customer VARCHAR(255) UNIQUE NOT NULL,

        sabah INT DEFAULT 0 NOT NULL,
        08_00 INT DEFAULT 0 NOT NULL,
        ogle INT DEFAULT 0 NOT NULL,
        aksam INT DEFAULT 0 NOT NULL,
        son INT DEFAULT 0 NOT NULL,
        f_giden INT DEFAULT 0 NOT NULL,
        iade INT DEFAULT 0 NOT NULL,
        bayat INT DEFAULT 0 NOT NULL,
        tahsilat FLOAT(24) DEFAULT 0 NOT NULL,
        devir FLOAT(24) DEFAULT 0 NOT NULL,
        FOREIGN KEY (customer) REFERENCES araba_customers(name) ON DELETE RESTRICT ON UPDATE CASCADE
        )""")

# cursor.execute(f"""
# ALTER TABLE {current_total_table_name}
# ADD FOREIGN KEY (customer) REFERENCES araba_customers(name) ON DELETE RESTRICT ON UPDATE CASCADE
# """)


cursor.execute(f"INSERT IGNORE INTO {current_total_table_name} (customer) SELECT name FROM araba_customers")
con.commit()
cursor.close()


class ArabaScreen(MDScreen):

    current_total_table_name = f"araba_{datetime.now(timeZ_Tr).day}_{datetime.now(timeZ_Tr).month}_{datetime.now(timeZ_Tr).year}_total"
    current_logs_db_name = f"araba_{datetime.now(timeZ_Tr).day}_{datetime.now(timeZ_Tr).month}_{datetime.now(timeZ_Tr).year}_logs" # İLERDE LAZIM OLACAK


    def on_pre_enter(self):
        print("araba ekranı girilidi")
        self.ids.araba_customers_grid.clear_widgets()
        cursor = con.cursor()
        cursor.execute("SELECT name FROM araba_customers ORDER BY name")
       
        for customer in cursor.fetchall():
            self.ids.araba_customers_grid.add_widget(
                MDRaisedButton(
                    text = f"{customer[0]}",
                    size_hint=(1,None),
                    # md_bg_color = get_color_from_hex("#f7f4e7"),
                    # text_color = get_color_from_hex("#4a4939"),
                    font_size = "20dp",
                    elevation = 5,
                    on_release= self.arabaCustomerClick
                )
            )
        cursor.close()

    def arabaCustomerClick(self,instance):
        self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(customerName = instance.text)
        # print(f"Müşteri '{instance.text}' Seçildi.")
        # self.manager.transition = SlideTransition(direction="left")
        # self.manager.current = "araba_islemler_screen"
        # self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text = instance.text

        # self.data_tables = MDDataTable(
        #     padding= (10,10,10,10),
        #     size_hint=(1, 0.5),
        #     background_color = get_color_from_hex("#f7f4e7"),
        #     # text_color = get_color_from_hex("#4a4939"),
        #     # use_pagination=True,
        #     # check=True,
        #     # name column, width column, sorting function column(optional)
        #     column_data=[
        #         ("[color=#4a4939]E[/color]", dp(9)),
        #         ("[color=#4a4939]İ[/color]", dp(9)),
        #         ("[color=#4a4939]B[/color]", dp(9)),
        #         ("[color=#4a4939]T[/color]", dp(9)),
        #         ("[color=#4a4939]D[/color]", dp(9))
        #         # ("Schedule", dp(30), lambda *args: print("Sorted using Schedule")),
        #     ],
        # )
       
        # self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.add_widget(self.data_tables,1)


   
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "login_screen"
        self.manager.get_screen('login_screen').resetForm()

class ArabaIslemlerScreen(MDScreen):

    def arabaIslemlerSetup(self,customerName):
        print(f"Müşteri '{customerName}' Seçildi.")
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "araba_islemler_screen"
        self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text = customerName
        # Araba İşlemler Ekranı Tablosu İçin Müşteri Verisi Çekme Bölümü
        cursor = con.cursor()
        cursor.execute(f"SELECT (sabah+08_00+ogle+aksam+son+f_giden),iade,bayat,tahsilat,devir FROM {current_total_table_name} WHERE customer = '{customerName}'")
        customer_data = cursor.fetchone()
        if customer_data != None:
            self.data_tables = MDDataTable(
                padding= (10,10,10,10),
                # size_hint=(1, 0.5),
                background_color = get_color_from_hex("#f7f4e7"),
                # text_color = get_color_from_hex("#4a4939"),
                # use_pagination=True,
                # check=True,
                # name column, width column, sorting function column(optional)
                column_data=[
                    ("Ekmek", dp(15)),
                    ("İade", dp(15)),
                    ("Bayat", dp(15)),
                    ("Tahsilat", dp(15)),
                    ("Devir", dp(15))
                    # ("Schedule", dp(30), lambda *args: print("Sorted using Schedule")),
                ],
                row_data=[(
                    customer_data[0],
                    customer_data[1],
                    customer_data[2],
                    customer_data[3],
                    customer_data[4]
                    )
                ]
            )
       
            self.ids.araba_islemler_datatable_boxlayout.add_widget(self.data_tables,1)

    def arabaIslemlerIleri(self,instance):
        self.manager.transition = SlideTransition(direction="left")
        if instance.text == "Ekmek":
            self.manager.current = "araba_durum_screen"
        elif instance.text == "İade":
            self.manager.current = "araba_iade_screen"
        elif instance.text == "Bayat":
            self.manager.current = "araba_bayat_screen"
        elif instance.text == "Tahsilat":
            self.manager.current = "araba_tahsilat_screen"
        

    def arabaIslemlerGeri(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "araba_screen"
        self.ids.araba_islemler_datatable_boxlayout.clear_widgets()

    def arabaIslemGeri(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "araba_islemler_screen"

    def on_pre_enter(self):
        self.ids.araba_islemler_gridlayout.clear_widgets()
        for button in ["Ekmek","İade","Bayat","Tahsilat"]:
            self.ids.araba_islemler_gridlayout.add_widget(
                MDRaisedButton(
                    text=button,
                    size_hint=(1,1),
                    font_size= "25dp",
                    on_release= self.arabaIslemlerIleri
                )
            )
        

class ArabaDurumScreen(MDScreen):
    def on_pre_enter(self):
        self.customerName = self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text
        self.ids.araba_durum_customer_label.text = self.customerName
        self.ids.araba_durum_datatable_boxlayout.clear_widgets()
        self.ids.araba_durum_gridlayout.clear_widgets()
        # Araba Durum Ekranı Tablosu İçin Müşteri Verisi Çekme Bölümü
        cursor = con.cursor()
        print("###########################################>>>>>>",current_total_table_name,self.customerName)
        cursor.execute(f"SELECT sabah,08_00,ogle,aksam,son,f_giden FROM {current_total_table_name} WHERE customer = '{self.customerName}'")
        customer_data = cursor.fetchone()
        if customer_data != None:
            self.data_tables = MDDataTable(
                padding= (10,10,10,10),
                # size_hint=(1, 0.5),
                # background_color = get_color_from_hex("#f7f4e7"),
                # text_color = get_color_from_hex("#4a4939"),
                # use_pagination=True,
                # check=True,
                # name column, width column, sorting function column(optional)
                column_data=[
                    ("Sabah", dp(12)),
                    ("8:00", dp(12)),
                    ("Öğle", dp(12)),
                    ("Akşam", dp(12)),
                    ("Son", dp(12)),
                    ("F.Giden", dp(12))
                    # ("Schedule", dp(30), lambda *args: print("Sorted using Schedule")),
                ],
                row_data=[(
                    customer_data[0],
                    customer_data[1],
                    customer_data[2],
                    customer_data[3],
                    customer_data[4],
                    customer_data[5]
                    )
                
                ]
            )  
            self.ids.araba_durum_datatable_boxlayout.add_widget(self.data_tables)
            
            for button in ["Sabah","08:00","Öğle","Akşam","Son","F. Giden"]:
                self.ids.araba_durum_gridlayout.add_widget(
                    MDRaisedButton(
                        text=button,
                        size_hint=(1,1),
                        font_size= "25dp",
                        on_release= self.arabaDurumIleri
                    )
                )

    def arabaDurumIleri(self,instance):
        self.manager.transition = SlideTransition(direction="left")
        if instance.text == "Sabah":
            self.durum = "sabah"
            self.manager.current = "araba_ekmek_screen"
        elif instance.text == "08:00":
            self.durum = "08_00"
            self.manager.current = "araba_ekmek_screen"
        elif instance.text == "Öğle":
            self.durum = "ogle"
            self.manager.current = "araba_ekmek_screen"
        elif instance.text == "Akşam":
            self.durum = "aksam"
            self.manager.current = "araba_ekmek_screen"
        elif instance.text == "Son":
            self.durum = "son"
            self.manager.current = "araba_ekmek_screen"
        elif instance.text == "F. Giden":
            self.durum = "f_giden"
            self.manager.current = "araba_ekmek_screen"
        
        
   
    def arabaDurumGeri(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "araba_islemler_screen"

class ArabaEkmekScreen(MDScreen):

    def on_pre_enter(self):
        self.customerName = self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text
        self.ids.araba_ekmek_customer_label.text = self.customerName
        self.durum = self.manager.get_screen("araba_durum_screen").durum
       
    def arabaEkmek(self):
        input_ekmek = int(self.ids.araba_ekmek_inputfield.text)
        self.ids.araba_ekmek_inputfield.text = ""
        if input_ekmek != "":
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "araba_islemler_screen"
            # Duruma Ekmek Girişi
            cursor = con.cursor()
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET {self.durum} = {self.durum} + {input_ekmek}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            # Müşterinin ekmek fiyatına göre borcun hesaplanıp devirin işlenmesi
            cursor.execute(f"SELECT ekmek_price FROM araba_customers WHERE name = '{self.customerName}'")
            customer_ekmek_price = cursor.fetchone()[0]
            input_devir = input_ekmek * customer_ekmek_price
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET devir = devir + {input_devir}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"İşlem Başarılı")
        else:
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"Geçersiz Değer")
       

    def on_leave(self):
        print("***Araba Ekmek Çıkış Yapıldı")
        self.ids.araba_ekmek_customer_label.text = "<Customer_Name>"

class ArabaIadeScreen(MDScreen):
    def on_pre_enter(self):
        self.customerName = self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text
        self.ids.araba_iade_customer_label.text = self.customerName

    def arabaIade(self):
        input_iade = int(self.ids.araba_iade_inputfield.text)
        self.ids.araba_iade_inputfield.text = ""
        if input_iade != "":
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "araba_islemler_screen"
            # Duruma Ekmek Girişi
            cursor = con.cursor()
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET iade = iade + {input_iade}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            # Müşterinin ekmek fiyatına göre borcun hesaplanıp devirin işlenmesi
            cursor.execute(f"SELECT ekmek_price FROM araba_customers WHERE name = '{self.customerName}'")
            customer_ekmek_price = cursor.fetchone()[0]
            input_devir = input_iade * -customer_ekmek_price
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET devir = devir + {input_devir}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"İşlem Başarılı")
        else:
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"Geçersiz Değer")

    def on_leave(self):
        print("***Araba İade Çıkış Yapıldı")
        self.ids.araba_iade_customer_label.text = "<Customer_Name>"

class ArabaBayatScreen(MDScreen):
    def on_pre_enter(self):
        self.customerName = self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text
        self.ids.araba_bayat_customer_label.text = self.customerName
       

    def arabaBayat(self):
        input_bayat = int(self.ids.araba_bayat_inputfield.text)
        self.ids.araba_bayat_inputfield.text = ""
        if input_bayat != "":
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "araba_islemler_screen"
            # Duruma Ekmek Girişi
            cursor = con.cursor()
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET bayat = bayat + {input_bayat}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            # Müşterinin ekmek fiyatına göre borcun hesaplanıp devirin işlenmesi
            cursor.execute(f"SELECT ekmek_price FROM araba_customers WHERE name = '{self.customerName}'")
            customer_ekmek_price = cursor.fetchone()[0]
            input_devir = (input_bayat * -customer_ekmek_price) / 2
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET devir = devir + {input_devir}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"İşlem Başarılı")
        else:
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"Geçersiz Değer")

    def on_leave(self):
        print("***Araba Bayat Çıkış Yapıldı")
        self.ids.araba_bayat_customer_label.text = "<Customer_Name>"

class ArabaTahsilatScreen(MDScreen):
    def on_pre_enter(self):
        self.customerName = self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_customer_label.text
        self.ids.araba_tahsilat_customer_label.text = self.customerName

    def arabaTahsilat(self):
        input_tahsilat = float(self.ids.araba_tahsilat_inputfield.text)
        self.ids.araba_tahsilat_inputfield.text = ""
        if input_tahsilat != "":
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = "araba_islemler_screen"
            # Duruma Ekmek Girişi
            cursor = con.cursor()
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET tahsilat = tahsilat + {input_tahsilat}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            # Müşterinin ekmek fiyatına göre borcun hesaplanıp devirin işlenmesi
            cursor.execute(f"""
                    UPDATE {current_total_table_name}
                    SET devir = devir - {input_tahsilat}
                    WHERE customer = '{self.customerName}'
            """)
            con.commit()
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"İşlem Başarılı")
        else:
            self.manager.get_screen("araba_islemler_screen").ids.araba_islemler_datatable_boxlayout.clear_widgets()
            self.manager.get_screen("araba_islemler_screen").arabaIslemlerSetup(self.customerName)
            toast(f"Geçersiz Değer")

    def on_leave(self):
        print("***Araba Tahsilat Çıkış Yapıldı")
        self.ids.araba_tahsilat_customer_label.text = "<Customer_Name>"