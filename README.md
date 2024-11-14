# Web Uygulamalarına Yönelik Siber Saldırıların Log Analizi ile Tespiti (Grup No:114)

Bu proje, makine öğrenmesi ve sınıflandırma algoritmaları kullanarak web uygulamalarına yönelik siber saldırıları tespit etmeyi amaçlamaktadır. Proje kapsamında, popüler saldırı simülasyon araçları (Acunetix, Netsparker, OWASP ZAP gibi) kullanılarak oluşturulan saldırı logları ile normal kullanıcı logları karşılaştırılmıştır ve makine öğrenmesi projesinde kullanılmak üzere hazırlanmıştır. Ayrıca isterlerden en önemlisi ve makine öğrenmesinde büyük bir öneme sahip olan "Web Scraping" içlemi için bir DEMO uygulaması yapılmıştır. Bu uygulamada bir e-Ticaret sisteminden çeşitli ürünlerin marka-model-çeşitli özellikler gibi bilgileri Web Scraping içlemi ile çekilmiştir.

## Proje Amacı

Web uygulamalarına yönelik siber saldırılar, çoğunlukla sistem loglarında anormal davranışlar bırakır. Bu proje, HTTP loglarının analizine dayalı olarak siber saldırı tespiti yapmak için makine öğrenmesi modellerini kullanmaktadır. Normal ve saldırı logları oluşturulmuş ve sınıflandırma algoritmaları ile analiz edilmiştir.

## Kullanılan Teknolojiler

- **Python-Flask-MySQL:** Zafiyetli bir web uygulaması geliştirmek için kullanıldı.
- **Saldırı Simülasyon Araçları:** Acunetix, Netsparker, OWASP ZAP.
- **Makine Öğrenmesi Kütüphaneleri:** Saldırı tespiti için sınıflandırma algoritmaları (örneğin, scikit-learn).
- **Web Kazıma Araçları:** E-ticaret sitesi üzerinden veri çekmek için Selenium ve BeautifulSoup.
- **Diğer:** JSON, Proxy, Middleware.

## Özellikler

1. **HTTP Log Analizi:** Normal kullanıcı davranışları ve saldırı içeren loglar arasındaki farklılıkları analiz etme.
2. **Makine Öğrenmesi ile Saldırı Tespiti:** Sınıflandırma algoritmaları ile saldırı tespiti yapılması.
3. **Demo Uygulama:** Web kazıma teknikleri kullanılarak e-ticaret sitesinden ürün bilgileri çekme.

## Web Scraping Demo

Bu projeyi çalıştırmak için aşağıdaki adımları izleyin:
**Gereklilikler:** Gerekli Python kütüphanelerini kurmak için aşağıdaki komutu kullanın:
   ```pip install -r "Web Scraping/requirements.txt"``` ardından ```python3 "Web Scraping/main.py"``` ile ilgili python dosyasını çalışıtırın.

## E-Ticaret Uygulamasının Ayağa Kaldırılması ve Logların görüntülenmesi
1. DBMS Üzerinde "ring" isminde bir Veri Tabanı Oluşturun.
2. ring.sql dosyası içerisinde yer alan SQL komutlarını "ring" Veri Tabanı içerinde çalıştırın. İlgili tabloların ve ilişkilerin oluşturulmasını sağlayın.
3. İlgili Python kütüphanelerini sisteminize kurun (`flask,flask_cors,uuid,pymysql,hashlib,jwt,numpy,ast,requests,datetime`). Bunun için `python pip `aracını kullanabilirsini.
4. app.py dosyasında yer alan veri tabanı bağlantı bilgilerinin doğru olduğundan emin olun.
5. `python3.exe app.py` komutunu çalıştırarak uygulamayı ayağa kaldırın
6. Yazılan Raporda anlatılan zafiyetli web uygulaması ve log üretme aşamasında ortaya çıkan sonuçlar `"E-Commerce App & Logs/ring.local/logs"` dizini altında yer almaktadır.
   

