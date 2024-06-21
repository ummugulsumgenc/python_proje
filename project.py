import sqlite3
import random
import csv

class Baslangic:
    def __init__(self):
        self.current_user = None
        self.conn = sqlite3.connect('movie.sqlite')  # Veritabanına bağlanıyoruz
        self.cursor = self.conn.cursor()  # cursor oluşturuyoruz
        self.kullanici()     

    def kullanici(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS kullanici_bilgileri
                               (kullanici_adi TEXT PRIMARY KEY, sifre TEXT)''') # kullanici_bilgileri tablosu oluşturuyoruz
        self.conn.commit()                                                 

    def basla(self):
        print("IMDB Takip Programına Hoş geldiniz!")  # başlangic yazısı yazarak kullanıcıya programın işlevini aktarıyoruz
        print("IMDB Takip Programında türlere göre ayrılmış filmleri, her filmin özelliklerini ve izlenme sayılarını görüntüleyebilirsiniz.")
        self.giris_ekrani()  # giriş ekranına yönlendiriyoruz

    def giris_ekrani(self): 
        print("1. Giriş Yap")
        print("2. Yeni Kullanıcı Oluştur")
        sec = input("Seçiminiz: ")
        if sec == '1':
            self.giris()  # giriş yapıyoruz
        elif sec == '2':
            self.kullanici_olustur() # kullanıcı olusturuyoruz
        else:
            print("Geçersiz seçim, tekrar deneyin.")
            self.giris_ekrani()  

    def giris(self):
        kullanici_adi = input("Kullanıcı adı: ")  # kullanıcı adını ve şifreleri alıyoruz
        sifre = input("Şifre: ")  
        self.cursor.execute('SELECT * FROM kullanici_bilgileri WHERE kullanici_adi=? AND sifre=?', (kullanici_adi, sifre)) 
        kisi = self.cursor.fetchone()   # kullanıcı bilgilerini select ile çekip kontrol ediyoruz 
        if kisi:
            kisi_adi = kisi[0]
            if kisi_adi == 'admin':  #  admin kullanıcı adıyla giriş yapan kişiyi admin sınıfına değilse standart kişi sınıfına atıyoruz
                self.current_user = Yonetici(kullanici_adi, sifre, self)  
            else:
                self.current_user = StandartKullanici(kullanici_adi, sifre, self)  
            self.current_user.main_menu()
        else:
            print("Hatalı kullanıcı adı veya şifre.")
            self.giris_ekrani()  

    def kullanici_olustur(self):   
        kullanici_adi = input("Yeni kullanıcı adı: ")  
        sifre = input("Şifre: ")  
        try:
            self.cursor.execute('INSERT INTO kullanici_bilgileri (kullanici_adi, sifre) VALUES (?, ?)',
                                (kullanici_adi, sifre))  #  aldıgımız kullanıcı bilgilerini tablomuza ekliyoruz. 
            self.conn.commit()
            print(f"{kullanici_adi} kullanıcısı oluşturuldu.")
        except sqlite3.IntegrityError:  #  hata yakalarsa giriş ekranına yonlendirir
            print("Bu kullanıcı adı zaten mevcut.")
        self.giris_ekrani()


class Yonetici():
    def __init__(self, kullanici_adi, sifre, baslangic):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.baslangic = baslangic
        self.cursor = baslangic.cursor
        self.conn = baslangic.conn

    def main_menu(self):
        print("1. Film Ekleme")
        print("2. Film Türü Ekleme")
        print("3. Film Izlenme Verisi Ekleme")
        print("4. Çıkış Yap")
        sec = input("Lütfen birini seçin: ")
        if sec == '1':      # admin için işlemler 
            self.film_ekle()
        elif sec == '2':
            self.film_turu_ekle()
        elif sec == '3':
            self.izlenme_ekle()
        elif sec == '4':
            self.baslangic.basla()
        else:
            print("Geçersiz seçim, tekrar deneyin.")
            self.main_menu()

    def film_ekle(self):     # film eklemek için filmin bilgilerini alıyoruz
        movie_id = input("film numarası: ")  
        title = input("film adı: ")  
                
        random_number = random.uniform(1, 10)  
        rounded_number = round(random_number, 1)  # Ondalık kısmını bir karakterle sınırlandırıyoruz
        rating = rounded_number  # 1 ile 10 arasında rastgele bir float değer oluşturuyoruz
        try:
            self.cursor.execute('INSERT INTO IMDB (Movie_id, Title, Rating) VALUES (?, ?, ?)',
                                (movie_id, title, rating))  #  3 sutun insert ediyoruz. arttırılabilir.
            self.conn.commit()
            print(f"{title} filmi eklendi.")
        except sqlite3.IntegrityError:  #  hata yakalarsa menuye yonlendiriyoruz
            print("Bu film zaten mevcut.")
        self.main_menu()
        
    
    def film_turu_ekle(self):     # film turu eklemek için bilgileri alıyoruz
        movie_id = input("film numarası: ")  
        genre = input("film Türü: ")  
        try:
            self.cursor.execute('INSERT INTO genre (Movie_id, genre) VALUES (?, ?)',
                                (movie_id, genre))  #   insert ediyoruz.
            self.conn.commit()
            print(f"{movie_id} numaralı filmin türü eklendi.")
        except sqlite3.IntegrityError:  #  hata yakalarsa menuye yonlendiriyoruz
            print("Bu film zaten mevcut.")
        self.main_menu()

    def izlenme_ekle(self):     # film turu eklemek için bilgileri alıyoruz
        movie_id = input("film numarası: ")  
        domestic = input("Yerel izlenme sayısı: ")
        worldwide = input("Dünya izlenme sayısı: ")  
        try:
            self.cursor.execute('INSERT INTO earning (Movie_id, Domestic, Worldwide) VALUES (?, ?, ?)',
                                (movie_id, domestic, worldwide))  #   insert ediyoruz.
            self.conn.commit()
            print(f"{movie_id} numaralı filmin izlenme verileri eklendi.")
        except sqlite3.IntegrityError:  #  hata yakalarsa menuye yonlendiriyoruz
            print("Bu film zaten mevcut.")
        self.main_menu()

class StandartKullanici():
    def __init__(self, kullanici_adi, sifre, baslangic):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.baslangic = baslangic
        self.cursor = baslangic.cursor
        self.conn = baslangic.conn

    def main_menu(self):
        print("1. Film Listesi")
        print("2. Film Türü Listesi")
        print("3. Film Izlenme Oranları Listesi")
        print("4. Çıkış Yap")
        sec = input("Lütfen birini seçin: ")
        if sec == '1':      # standart kullanıcı için işlemler 
            try:
                query = 'SELECT * FROM IMDB'   #  tablodaki verileri çekiyoruz
                self.baslangic.cursor.execute(query)
                rows = self.baslangic.cursor.fetchall()
                with open('IMDB.csv', 'w', newline='', encoding='utf-8') as file:  #  csv dosyasına yazıyoruz
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in self.baslangic.cursor.description])  # Sütun başlıkları
                    writer.writerows(rows)
                print("IMDB.csv dosyası oluşturuldu.")
                self.main_menu()
            except sqlite3.IntegrityError:   # hata yakalama
                print("IMDB.csv oluşturulamadı.")
        elif sec == '2':
            try:
                query = 'SELECT * FROM genre'   #  tablodaki verileri çekiyoruz
                self.baslangic.cursor.execute(query)
                rows = self.baslangic.cursor.fetchall()
                with open('genre.csv', 'w', newline='', encoding='utf-8') as file:  #  csv dosyasına yazıyoruz
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in self.baslangic.cursor.description])  # Sütun başlıkları
                    writer.writerows(rows)
                print("genre.csv dosyası oluşturuldu.")
                self.main_menu()
            except sqlite3.IntegrityError:   # hata yakalama
                print("genre.csv oluşturulamadı.")
        elif sec == '3':
            try:
                query = 'SELECT * FROM earning'   #  tablodaki verileri çekiyoruz
                self.baslangic.cursor.execute(query)
                rows = self.baslangic.cursor.fetchall()
                with open('earning.csv', 'w', newline='', encoding='utf-8') as file:  #  csv dosyasına yazıyoruz
                    writer = csv.writer(file)
                    writer.writerow([i[0] for i in self.baslangic.cursor.description])  # Sütun başlıkları
                    writer.writerows(rows)
                print("earning.csv dosyası oluşturuldu.")
                self.main_menu()
            except sqlite3.IntegrityError:   # hata yakalama
                print("earning.csv oluşturulamadı.")
        elif sec == '4':
            self.baslangic.basla()
        else:
            print("Geçersiz seçim, tekrar deneyin.")
            self.main_menu()

   


if __name__ == "__main__":
    Baslangic = Baslangic()
    Baslangic.basla()
