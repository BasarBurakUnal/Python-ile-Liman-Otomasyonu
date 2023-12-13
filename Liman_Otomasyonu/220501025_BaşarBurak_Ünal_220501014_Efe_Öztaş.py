import csv

class IstifAlani: #İstif alanı sınıfını temsil eder
    kapasite = 750 #İstif alanının yük kapasitesi

    def __init__(self):
        self.yukler = [] #İstif alanındaki yüklerin listesi
        self.dolu = False  #İstif alanın başlangıçta boş olduğunu ve dolu olmadığını belirtir. Kısaca İstif alanının doluluk durumunu kontrol eder

    def yuk_ekle(self, yuk): #İstif alanına yük ekleme
        if not self.dolu: #İstif alanının dolu olup olmadığını kontrol eder
            self.yukler.append(yuk) #Yükü istif alanına ekler
            toplam_yuk_miktari = sum(yuk['yük_miktarı'] for yuk in self.yukler) #İstif alanındaki toplam yükü hesaplar

            #İstif alanının toplam yük miktarının, istif alanının kapasitesini aşıp aşmadığını kontrol eder
            if toplam_yuk_miktari >= IstifAlani.kapasite:
                self.dolu = True
                print("İstif alanı doldu!")
            return True
        else:
            print("İstif alanı zaten dolu!")
            return False

    def yuk_cikar(self): #İstif alanından yük çıkarma
        if self.yukler:
            self.yukler.pop()  #İstif alanındaki yüklerden en üstteki yükü çıkarır
            if not self.yukler:  #Eğer yük kalmadıysa kullanıcıya uyarı gider
                self.dolu = False
                print("İstif alanı boşaldı!")
        else:
            print("İstif alanı zaten boş!")

class Vinc:
    def __init__(self):
        self.istif_alanlari = [IstifAlani(), IstifAlani()]  #İki adet istif alanına sahiptir
        self.aktif_istif_alani = self.istif_alanlari[0] #İlk istif alanının aktif olduğunu gösterir
        self.toplam_vinc_islem = 0 #Toplamda kaç vinc işlemi yapıldığını görmek için kullanılır

    def yuk_indir(self, tir): #TIRdan yük indirir ve istif alanına ekler
        yuk = tir.yuk_bilgisi
        if not self.aktif_istif_alani.yuk_ekle(yuk): #istif alanına yük eklemenin geçerli olup olmadığını kontrol eder
            yeni_istif_alani = IstifAlani() #Yeni istif alanı oluşturulur,aktif istif alanına yük eklenemediğinde kullanılır
            yeni_istif_alani.yuk_ekle(yuk)
            self.istif_alanlari.append(yeni_istif_alani) #Yeni istif alanını istif_alanlari listesine ekler
            self.aktif_istif_alani = yeni_istif_alani

    def yuk_yukle(self, gemi): #İstif alanındaki yükleri gemiye yükler
        for istif_alani in self.istif_alanlari:
            tersten_yukler = reversed(istif_alani.yukler) #En üstteki yükten başlayarak gemiye yükleme işlemi gerçekleştirilir
            for yuk in tersten_yukler:
                gemi_bilgisi = {} #Bu sözlük, gemiye yüklenen her bir yükün bilgilerini içerir
                anahtarlar = ['ülke', 'ton_adet_20', 'ton_adet_30', 'yük_miktarı', 'maliyet']

                for key in anahtarlar:
                    gemi_bilgisi[key] = yuk[key]

                print("Vinçle yük gemiye yükleniyor:", gemi_bilgisi)

                gemi.yuk_miktarini_guncelle(yuk['yük_miktarı'])
                self.toplam_vinc_islem += 1
                if self.toplam_vinc_islem >= 20:
                    print("Vinç işlem limitine ulaşıldı. İşlem sonlandırılıyor.")
                    return

    #Bu metot, toplamda kaç vinc işlemi gerçekleştirildiğini döndürür.
    def gecen_vinc_islem_sayisi(self):
        return self.toplam_vinc_islem

class TIR: #Tır adında bir sınıf tanımlanır
    plaka_sirasi = 1 #Bu değişken, oluşturulan TIR örneklerine sıralı plaka numaraları atamak için kullanılır

    def __init__(self, gelis_zamani, ulke, ton_adet_20, ton_adet_30, yuk_miktari, maliyet):
        self.gelis_zamani = gelis_zamani
        self.ulke = ulke
        self.ton_adet_20 = ton_adet_20
        self.ton_adet_30 = ton_adet_30
        self.yuk_miktari = yuk_miktari
        self.maliyet = maliyet
        self.plaka_numarasi = f"41_kostu_{TIR.plaka_sirasi:03d}"  #Sıralı plaka numaraları üretilir ve her bir TIR örneği için bir artırılır
        TIR.plaka_sirasi += 1
        self.yuk_bilgisi = {
            'geliş_zamanı': self.gelis_zamani,
            'plaka_numarası': self.plaka_numarasi,
            'ülke': self.ulke,
            'ton_adet_20': int(self.ton_adet_20),
            'ton_adet_30': int(self.ton_adet_30),
            'yük_miktarı': float(self.yuk_miktari),
            'maliyet': float(self.maliyet)
        }

    #TIR örneğinin taşıdığı bilgiler ekrana yazdırılır
    def bilgileri_yazdir(self):
        print(f"Geliş Zamanı: {self.gelis_zamani}, Plaka Numarası: {self.plaka_numarasi}, Ülke: {self.ulke}, "
              f"20 Ton Adet: {self.ton_adet_20}, 30 Ton Adet: {self.ton_adet_30}, "
              f"Yük Miktarı: {self.yuk_miktari}, Maliyet: {self.maliyet}")

    def yuk_miktari(self): #TIR örneğinin taşıdığı yük miktarını döndürür
        return self.yuk_bilgisi['yük_miktarı']

    def toplu_bilgi(self): #TIR örneğinin taşıdığı tüm yük bilgilerini içeren sözlüğü döndürür
        return self.yuk_bilgisi

class Gemi: #Gemi adında bir sınıf tanımlanır
    gemi_sirasi = 1 #Bu değişken,oluşturulan gemi örneklerine sıralı gemi numaraları atamak için kullanılır

    def __init__(self, gelis_zamani, kapasite, gidecek_ulke):
        self.gelis_zamani = gelis_zamani
        self.kapasite = float(kapasite)
        self.gidecek_ulke = gidecek_ulke
        self.gemi_numarasi = f"{Gemi.gemi_sirasi:03d}" #Sıralı gemi numaraları üretilir ve her bir gemi örneği için bir artırılır
        Gemi.gemi_sirasi += 1
        self.yuk_bilgisi = {
            'gemi_numarasi': self.gemi_numarasi,
            'ülke': self.gidecek_ulke,
            'kapasite': int(self.kapasite),
            'yük_miktarı': 0  #Gemiye yüklenen miktarı takip etmek için başlangıçta 0 olarak ayarlanır.
        }

    #GEMİ örneğinin bilgileri ekrana yazdırılır
    def bilgileri_yazdir(self):
        print("Geliş Zamanı:", self.gelis_zamani, end=' ')
        print("Gemi Numarası:", self.gemi_numarasi, end=' ')
        print("Kapasite:", self.kapasite, end=' ')
        print("Gidecek Ülke:", self.gidecek_ulke)

    #GEMİ örneğine yük miktarı eklenerek güncellenir
    def yuk_miktarini_guncelle(self, yuk_miktari):
        self.yuk_bilgisi['yük_miktarı'] += float(yuk_miktari)

    #GEMİ örneğinin taşıdığı tüm yük bilgilerini içeren sözlüğü döndürür
    def toplu_bilgi(self):
        return self.yuk_bilgisi

    #Gemi limanı terk edip etmemeyi kontrol eder
    def limani_terk_et(self):
        doluluk_orani = self.yuk_bilgisi['yük_miktarı'] / self.kapasite #Doluluk oranı hesaplanır
        return doluluk_orani >= 0.95 #Geminin doluluk oranı %95 veya daha fazlaysa, True döndürür. Aksi takdirde,False döndürür

#CSV dosyasından verileri okuma
def csv_dosyasindan_veri_okuma(dosya_adi):
    with open(dosya_adi, 'r', newline='') as file:
        reader = csv.DictReader(file) #CSV dosyasındaki her satırı bir sözlük olarak okur
        return list(reader)

#CSV dosyasından okunan olaylar listesini kullanarak bir TIR listesi oluşturur
olaylar_listesi = csv_dosyasindan_veri_okuma('olaylar.csv')
tir_listesi = [TIR(gelis_zamani=olay['geliş_zamanı'],
                   ulke=olay['ülke'],
                   ton_adet_20=olay['20_ton_adet'],
                   ton_adet_30=olay['30_ton_adet'],
                   yuk_miktari=float(olay['yük_miktarı']),
                   maliyet=float(olay['maliyet'])) for olay in olaylar_listesi] #Her bir olay için bir tır örneği oluşturulmasını sağlar.


#TIRları plaka numarasına göre sıralar
tir_listesi.sort(key=lambda tir: tir.plaka_numarasi)


vinc = Vinc() #Gemilere yük taşıma işlemlerini yönetir
#TIRın geliş zamanı, plaka numarası, yük miktarı, ülke ve maliyet bilgileri ekrana yazdırılır.
for tir in tir_listesi:
    print(f"{tir.gelis_zamani} zamanında gelen {tir.plaka_numarasi} plakalı TIR'ın "
          f"{tir.yuk_bilgisi['yük_miktarı']} ton yükü, {tir.ulke} ülkesine yola çıkmıştır. "
          f"Maliyet: {tir.yuk_bilgisi['maliyet']}")

    #TIRların yükleri istif alanına eklenirken, istif alanının kapasitesi aşılırsa döngü sona erer
    if not vinc.aktif_istif_alani.yuk_ekle(tir.yuk_bilgisi):
        break

    #Bir istif alanının kapasitesinin dolup dolmadığını kontrol etmek için kullanılır
    if vinc.aktif_istif_alani.dolu:
        print("İstif Alanı Dolu!")
    else:
        print("İstif Alanı Boş!")

    #İndirilen yükler  1 numaralı istif alanına ve üst üste yerleştirilir
    vinc.aktif_istif_alani = vinc.istif_alanlari[0]

    #Vinç işlem sayısı kontrol edilir
    if vinc.gecen_vinc_islem_sayisi() >= 20:
        print("Vinç işlem limitine ulaşıldı. İşlem sonlandırılıyor.")
        break

#Gemiler CSV dosyasından verileri okuma
gemiler_listesi = csv_dosyasindan_veri_okuma('gemiler.csv')
gemi_listesi = [Gemi(gelis_zamani=gemi['geliş_zamanı'],
                     kapasite=gemi['kapasite'],
                     gidecek_ulke=gemi['gidecek_ülke']) for gemi in gemiler_listesi] #Her bir gemi için bir Gemi örneği oluşturulmasını sağlar

#Sadece belirtilen 4 farklı ülkeye yük taşıyan TIR'lar ve bu ülkelere gidecek gemiler için yazılan kod
tir_ulkeler = set(tir.ulke for tir in tir_listesi)
hedef_ulke_gemi_listesi = [gemi for gemi in gemi_listesi if gemi.gidecek_ulke in tir_ulkeler]

#Gemiler yüklenmeye başlanır
for gemi in hedef_ulke_gemi_listesi:
    print(f"{gemi.gemi_numarasi} gemisinin yükleri yükleniyor.")

    #Geminin yük bilgileri güncellenir
    gemi.yuk_miktarini_guncelle(sum(tir.yuk_miktari for tir in tir_listesi if tir.ulke == gemi.gidecek_ulke))

    #Geminin yük bilgileri ekrana yazdırılır
    print("Yük Bilgisi:", gemi.yuk_bilgisi)

    #Geminin belirli bir doluluk oranını aştığında limandan ayrılmasını ve ilgili bilgilerin ekrana yazdırılmasını sağlar
    if gemi.limani_terk_et():
        doluluk_orani_yuzde = min(gemi.yuk_bilgisi['yük_miktarı'] / gemi.kapasite, 0.95) * 100
        print(f"{gemi.gemi_numarasi} gemisi limanı terk ediyor. Doluluk Oranı: {doluluk_orani_yuzde:.2f}%")
        hedef_ulke_gemi_listesi.remove(gemi) #Geminin limandan ayrıldığını ve hedef ülkeye gittiğini gösterir

    #İstif alanındaki yükler gemiye yüklenir
    vinc.yuk_yukle(gemi)
    #İstif alanı boşaltılır
    vinc.aktif_istif_alani.yukler = []


print("Toplam VİNÇ işlem sayısı:" ,vinc.gecen_vinc_islem_sayisi()) #Vinç işlem sayısını ekrana yazılır
print("Toplam TIR sayısı:" ,len(tir_listesi)) #Toplam TIR sayısı ekrana yazılır
print("Toplam GEMİ sayısı:" , len(gemi_listesi)) #Toplam GEMİ sayısı ekrana yazılır
#Sözlük veri tipinde TIR ve GEMİ bilgileri tutulur
tir_bilgileri = {tir.plaka_numarasi: tir.toplu_bilgi() for tir in tir_listesi}
gemi_bilgileri = {gemi.gemi_numarasi: gemi.toplu_bilgi() for gemi in gemi_listesi}


#Sözlüklerin uzunluklarını kontrol edilir
tir_keys = list(tir_bilgileri.keys())
gemi_keys = list(gemi_bilgileri.keys())

#Örnek TIR ve Gemi indeksleri
tir_indeks = 0  #Bu değeri geçerli bir indeksle değiştiriniz maksimum 4026 minimum 0
gemi_indeks = 0  #Bu değeri geçerli bir indeksle değiştiriniz maksimum 449 minimum 0

#Örnek TIR ve Gemi bilgileri ekrana yazılır
print("\nÖrnek TIR Bilgisi:")
if tir_indeks < len(tir_keys):
    print(tir_bilgileri[tir_keys[tir_indeks]])
else:
    print("Geçersiz TIR indeksi")

print("\nÖrnek Gemi Bilgisi:")
if gemi_indeks < len(gemi_keys):
    print(gemi_bilgileri[gemi_keys[gemi_indeks]])
else:
    print("Geçersiz Gemi indeksi")

