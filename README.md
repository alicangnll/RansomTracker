# Flask Python MVC Örneği | Flask Python MVC Example

<p>
    Merhabalar, bu repoda Python'un Flask kütüphanesiyle MVC mimarisi yapısını kurdum. Umarım bu kaynak size çok yardımcı olmuştur.
<p>

## Kurulum
<pre>python3 -m pip install -r requirements.txt</pre>

## Database oluşturma
<p>Database oluşturmak için öncelikle proje klasörünün içerisinde <b>"python3 -m flask db init"</b> komutuyla migrate klasörlerini oluşturuyoruz. Ardından <b>"python3 -m flask db migrate"</b> ile DB dosyasını oluşturuyoruz. Tüm bu işlemlerden sonra ise <b>"python3 -m flask db upgrade"</b> ile DB içerisine tablolar insert edilir.</p>

## Dosya Yapısı
<pre>
proje/
|
├── templates/
|   └── index.html
|
├── migrations/ (Geçici dosya init komutuyla oluşturulacak)
|   └── ...
|
├── instance/
|   └── data.db (DB oluşturulduktan sonra gelecek)
|
├── routes/ (Yönlendiriciler. URL kısmını belirtenler. Örneğin alicangonullu.com/konu vb)
|   └── Route.py
|
├── models/ (Veritaban yapısını içeren alan)
|   └── DBModel.py
|
├── controllers/ (Tüm yapıyı UI ile bağlayan alan. Core alanı)
|   └── Controller.py
|
├── app.py (Uygulamanın başlatıcısı)
└── config.py (Uygulama ayarlayıcı)
</pre>

## Yapı Görsellemesi
![Yapı](https://github.com/user-attachments/assets/aec9ab12-c120-4554-ab13-683d8d73dfc0)

## Uygulama İçeriği
<pre>
main/
|
├── iexampleuser (Example userları insert eder)
└── listuser (Tablodaki kullanıcıları listeler)
</pre>


## PyCache dosyalarını silme kodu
<pre>
python -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
</pre>
