### Сущности: пользователь, товар, предложение

### Модель NoSQL
```
offers:
{
	_id: ObjectId,
	product: {
		weight: string,
		size: string,
		category: string,
		state: string,
		photo: string,
		description: string
	},
	create_date: date,
	edit_date: date,
	status: string,
	city: string,
	delivery_city: string,
	price: int,
	views: int, 
	likes: int,
	owner_id: ObjectId
	purchaser_id: ObjectId
}

users:
{
	email: string,
	password: string,
	full_name: string
}
```
### Объем:
V = Vo + Vu

Учитывая, что размер ObjectId = 12 байт, int = 4 байт, date - 8 байт, string = средняя длина поля*4 байт
Примерный расчет средней длины строковых полей коллекций:
```
offers.product.size - 5
offers.product.category - 8
offers.product.state - 8
offers.product.photo - 30 (url)
offers.product.description - 150

offers.status - 8
offers.city - 12
offers.delivery_city - 12

users.email - 14
users.password - 10
users.full_name - 30

Vo = (4 + 5 + 8 + 8 + 30 + 150 + 8 + 12 + 12)*4 + 3*4 + 3*12 + 2*8 = 1012 байт
Vu = (14 + 10 + 30)*4 = 216
```

Предположим, что каждый пользователь делает 0.2 предложения. Тогда, если количество пользователей n будет 5000, то объем данных будет

```V = n*Vu + 0.2*n*Vo = 2031,25кбайт```

Коллекция избыточна засчет дублирования product. Если заменить это поле на id, то размер каждого документа коллекции offers будет 811
Коллекция users не избыточна

Тогда 
```
Vclean = n*Vu + 0.2*n*833 = 1858,3984375
V/Vclean = 1,099316868
```

### Запросы:
Аутентификация пользователя:
Предположим, что был введен email test@gmail.com и пароль pass123
```
db.users.find({email: "test@gmail.com", password: "pass123"})
```

Создание предложения об обмене:
Пусть его создает пользователь с id 1
```
db.offers.insertOne({
	{
		product: {
			weight: "3 кг",
			size: "2 м",
			category: "Одежда",
			state: "Новое",
			photo: "https://swapdomain.com/photos/product1.png",
			description: "Отдается новая кофта, почти не ношенная. Не подошла по размеру"
		},
		create_date: 06.06.2022,
		edit_date: 06.06.2022,
		status: "Опубликован",
		city: "Москва",
		delivery_city: "Санкт-Петербург",
		price: 300,
		views: 10, 
		likes: 2,
		owner_id: 1
		purchaser_id: null
	}
})
```
Посмотреть предложения с товарами, категория, которых - одежда
```
db.offers.find({"product.category": "Одежда"})
```

Осуществить покупку какого-то товара через предложение:
Пусть id предложения - 50, id - пользователя, совершающего покупку - 2
```
db.offers.updateOne({_id: 50}, {$set: {purchaser_id: 2}})
```
Так как при просмотре каждого товара, который еще не купили (purchaser_id = null) необходимо делать запрос так же к коллекции users, то количество запросов будет n*2, где n - количество совершенных предложений. Условно n = 1000, тогда количество запросов = 2000

### Реляционная модель:
![sql](https://user-images.githubusercontent.com/54910797/203839980-bc8524cd-a4da-465a-b719-9437b4446cb3.png)

### Объем
V = Vp + Vo + Vu
Пусть каждое строковое поле будет varchar(m), где m - средняя длина поля * 2, а каждое поле id - serial
```
Vp = 4 + (4 + 5 + 8 + 8 + 30 + 150)*2 = 414
Vo = 3*4 + 2*4 + (8 + 12 + 12)*2 + 3 * 4 = 96
Vu = (14 + 10 + 30)*2 = 108
```
Пусть также количество пользователей 5000 и каждый пользователь сделал 0.2 предложения
```
V = (Vp + Vo)*1000 + 5000*Vu = 1050000 байт
```
Чистый объем можно посчитать, убрав связывающие ключи из таблиц
```
Vp = (4 + 5 + 8 + 8 + 30 + 150)*2 = 410
Vo = 2*4 + (8 + 12 + 12)*2 + 3 * 4 = 84
Vu = (14 + 10 + 30)*2 = 108
V = (Vp + Vo)*1000 + 5000*Vu = 1034000 байт = 1009,76562 кбайт
V/Vclean = 1,015473888
```

### Запросы:

Аутентификация
```
SELECT * FROM users WHERE
email = "test@gmail.com" AND
password = "pass123"
````

Создание предложения об обмене
```
INSERT INTO product
VALUES ("3 кг","2 м","Одежда","Новое","https://swapdomain.com/photos/product1.png", "Отдается новая кофта, почти не ношенная. Не подошла по размеру");
INSERT INTO offer
VALUES  (1, 1, NULL, 06.06.2022, 06.06.2022, "Опубликован","Москва","Санкт-Петербург", 300, 10, 2);
```

Как видно для создания одного предложения об обмене необходимо 2 запроса к БД, в то время как в неряляционной модели можно было ограничиться 1м запросом.

Посмотреть предложения с товарами, категория, которых - одежда
```
SELECT * FROM offer JOIN product ON offer.product_id = product.id
WHERE category = "Одежда"
```
Осуществить покупку какого-то товара через предложение:
Пусть id предложения - 50, id - пользователя, совершающего покупку - 2
```
UPDATE offer
SET purchaser_id = 2
WHERE id = 50
```

### Выводы
Модель NoSQL занимает больше памяти чем модель в SQL. Некоторые запросы в NoSQL более быстрые, чем в SQL, однако некоторые нет 


