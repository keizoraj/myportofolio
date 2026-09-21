Nama: Keizora Jelita Wohingati

NPM: 2506597510

Kelas: PBP A

### Tugas 1

1. Saya menggunakan section untuk memisahkan bagian profile dan bagian experience. Saya juga menggunakan article untuk tiap experience yang saya lampirkan karena tiap experience adalah topik yang berdiri sendiri, jadi saya pisahkan juga agar enak dilihat.

2. Tantangan yang saya temui adalah untuk mempertahankan agar informasi yang tertera tetap mudah dan enak dibaca ketika ukuran layar menjadi kecil seperti pada mobile. Misal, pada tampilan desktop bagian experience menggunakan 3 kolom menyamping, kalau layout seperti itu diterapkan pada mobile maka tiap kolom akan menyempit dan tulisan jadi sulit terbaca. Maka, saya menggunakan media query (yang max width 600px) dan mengubah grid template columns menjadi 1 fr, jadi tiap experience ditampilkannya dalam 1 kolom kebawah, tidak menyamping. Saya juga memperkecil ukuran heading experience dari 2.5rem menjadi 2rem. Buat menentukan bagian yang perlu diubah atau diperbaiki, saya mengecek tampilan website pada HP saya.

3. Karena saat ini website saya masih berupa static web, informasi seperti experience harus ditulis secara langsung dalam HTML. Kalau nanti experience saya bertambah banyak seiring waktu atau skill saya dan projek saya bertambah maka hal ini akan menjadi kurang efisien kalau harus mengedit kode secara manual. Pada iterasi berikutnya, mungkin saya ingin menambahkan database untuk menyimpan data portfolio seperti pengalaman organisasi, skills, dan projects. Saya juga ingin membuat fungsionalitas untuk menampilkan data tersebut secara otomatis dari database sehingga informasi portfolio dapat dikelola dan diperbarui dengan lebih mudah tanpa harus mengubah HTML secara langsung.

AI DECLARATION:
Pada tugas ini saya menggunakan chatgpt untuk menjelaskan kepada saya bagaimana caranya untuk bisa memecah tiap experience saya ke beberapa section jadi terlihat enak dilihat. Saya juga menanyakan bagaimana caranya menambahkan/menghubungkan url page experience yang sedang saya buat.


### Tugas 2

1. Saat pengguna membuka halaman Projects melalui navbar, request akan diarahkan terlebih dahulu ke urls.py pada project, lalu diteruskan ke urls.py pada aplikasi main. Dari sana, URL untuk Projects akan menjalankan show_projects yang ada di views.py. View tersebut mengambil data project yang sudah disimpan di model Project, kemudian mengirimkannya ke projects.html. Setelah itu, template menampilkan data project yang diterima menggunakan perulangan. Jadi, data yang ada di database dapat ditampilkan ke browser tanpa perlu menuliskannya satu per satu di HTML.

2. Menurut saya menyimpan data project di model akan lebih memudahkan ketika data portfolio semakin bertambah banyak. Kalau misal semua informasi project ditulis langsung di template, tiap kali kita ingin menambah atau mengubah project saya harus mengubah kode HTML secara manual. Dengan menggunakan model, saya cukup mengubah data yang disimpan tanpa perlu mengubah struktur halaman. Hal ini juga membuat bagian data dan tampilan jadi lebih terpisah sehingga website akan lebih mudah dirawat dan dikembangkan kedepannya.

3. makemigrations digunakan untuk membuat file yang mencatat perubahan pada model yang saya buat, sedangkan migrate digunakan untuk menerapkan perubahan tersebut ke database. Contohnya, pada tugas ini saya menambahkan model Project dengan field seperti title, description, category, dan year. Setelah menambahkan model tersebut, saya menjalankan python manage.py makemigrations untuk membuat migration baru, kemudian menjalankan python manage.py migrate agar model Project tersebut benar-benar dibuat di database.

AI DECLARATION:
Pada tugas 2 ini saya menggunakan chatgpt untuk membantu saya dalam ide pembuatan test case, saya juga menggunakannya untuk membantu ketika ada problem saat ingin saya commit dan malah terjadi error.


### Tugas 3

1. GET request digunakan untuk mengambil atau menampilkan data dari server, sedangkan POST request digunakan untuk mengirim data ke server. Pada proyek ini, GET digunakan untuk menampilkan halaman dan mengambil data, sedangkan POST digunakan ketika user mengisi form untuk menambah atau mengubah data.

2. Kedua fungsi tersebut memiliki tugas yang berbeda. Fungsi untuk menampilkan form digunakan ketika user membuka halaman form, sedangkan fungsi untuk memproses submission digunakan untuk menerima data yang dikirim melalui POST, melakukan validasi, dan menyimpan data jika data yang diberikan valid. Dengan memisahkan proses tersebut, alur penggunaan form menjadi lebih jelas.

3. ModelForm mempermudah pembuatan form karena form dapat dibuat berdasarkan model yang sudah ada. Field dan validasi dasar juga dapat dibuat oleh Django secara otomatis. Selain itu, data yang sudah valid dapat langsung disimpan ke database menggunakan form.save(), sehingga kode yang dibutuhkan lebih sedikit dibandingkan membuat form secara manual.

AI DECLARATION:
Pada tugas ini, saya menggunakan chatgpt untuk membantu saya dalam pembuatan testcase dan menanyakan apakah testcase saya sudah mengcover keseluruhan program saya.