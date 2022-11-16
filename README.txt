-- indeks detalu
sugerowany format modelCode: 0001/08/22/ZP/1

-- aktywne pole w HTML
autofocus="autofocus"

-- create  DB
1) console->python
2) >>> from mainApp import db
3) >>> db.create_all()

-- pip zapisanie listy
pip freeze -l > requirements.txt
-- pip instalacja
pip install -r requirements.txt

-- BABEL
in mainAPP: pybabel extract -F babel.cfg -o messages.pot .  
pybabel init -i messages.pot -d translations -l pl 
pybabel compile -d translations  


--SQL 

CREATE TABLE status (
	id INTEGER NOT NULL, 
	"statusCode" INTEGER, 
	"statusName" VARCHAR(20), 
	production VARCHAR(20), displayOrder INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE ("statusName")
)

CREATE TABLE event (
	id INTEGER NOT NULL, 
	"idProd" INTEGER, 
	"idStatus" INTEGER, 
	"startDate" INTEGER, 
	"endDate" INTEGER, 
	"okCounter" INTEGER, 
	"nokCounter" INTEGER, 
	"userID" INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY("idProd") REFERENCES product (id), 
	FOREIGN KEY("idStatus") REFERENCES status (id), 
	FOREIGN KEY("userID") REFERENCES user (id)
)

CREATE TABLE product (
	id INTEGER NOT NULL, 
	"modelCode" VARCHAR(20), 
	"modelName" VARCHAR(20), 
	"orderStatus" VARCHAR(20), 
	"startDate" INTEGER, 
	"executionDate" INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE ("modelCode")
)


CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(100), 
	password_hash VARCHAR, 
	email_address VARCHAR, 
	role INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (id), 
	UNIQUE (username)
)

INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('1', '0', 'Zamknij zlecenie', 'Finish', '1');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('2', '0', 'Produkcja - Produkcja', 'Prod', '2');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('3', '12', 'Awaria - Siłowniki pneumatyczne', 'Error', '20');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('4', '13', 'Awaria - Kompresor', 'Error', '30');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('5', '14', 'Awaria - Hamulce', 'Error', '40');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('6', '15', 'Awaria - Przewody elektryczne', 'Error', '50');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('7', '16', 'Awaria - Przewody pneumatyczne', 'Error', '60');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('8', '17', 'Awaria - Inne', 'Error', '70');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('9', '21', 'Przezbrojenie - Modelu', 'TPZ', '80');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('10', '22', 'Przezbrojenie - Wymiaru', 'TPZ', '90');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('11', '31', 'Zasilenie maszyny - Rury', 'TPZ', '100');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('12', '32', 'Zasilenie maszyny - Wzmocnienia', 'TPZ', '110');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('13', '33', 'Zasilenie maszyny - Kolektory', 'TPZ', '120');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('14', '40', 'Braki materiału', 'Error', '130');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('15', '50', 'Przerwa', 'Error', '140');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('16', '61', 'Regulacje parametrów - Moc zgrzewania', 'TPZ', '150');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('17', '62', 'Regulacje parametrów - Ciśnienie', 'TPZ', '160');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('18', '63', 'Regulacje parametrów - Czas zgrzewania', 'TPZ', '170');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('19', '70', 'Zmiana siatki na elektrodach', 'TPZ', '180');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('20', '80', 'Zmiana palety', 'TPZ', '190');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('21', '90', 'Kontrola szczelności', 'TPZ', '200');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('22', '100', 'Sprzątanie stanowiska', 'TPZ', '210');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('23', '110', 'Szkolenie', 'Error', '220');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('24', '120', 'Start maszyny', 'TPZ', '230');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('25', '130', 'Pakowanie', 'Finish', '0');
INSERT INTO "main"."status" ("id", "statusCode", "statusName", "production", "displayOrder") VALUES ('26', '140', 'Wiercenie', 'Prod', '0');


INSERT INTO "main"."user" ("id", "username", "password_hash", "email_address", "role") VALUES ('1', 'Administrator', 'pbkdf2:sha256:260000$cX9Coj8JfNHdVnUY$d02143023c01fbdb7bc521d2421eeddd9b30c70d646daa0807b7d3c0fcf22ecb', '666666@666666.pl', 'admin');
INSERT INTO "main"."user" ("id", "username", "password_hash", "email_address", "role") VALUES ('2', 'Operator Marek', 'pbkdf2:sha256:260000$9ldhGxm36cqpkYTR$6f49058f25748c11a16ce2c8a07e95108b0e31690c76e89c6fa910e3858de665', '7777777@7777777.pl', 'user');
INSERT INTO "main"."user" ("id", "username", "password_hash", "email_address", "role") VALUES ('3', 'Operator Darek', 'pbkdf2:sha256:260000$kz4L2YiPTc9dplmY$5e0ab76bbc17f6ef8300f7a0b9e5e505f683c2f68c45c7370c11e56bd972996c', '8888888@8888888.pl', 'user');
INSERT INTO "main"."user" ("id", "username", "password_hash", "email_address", "role") VALUES ('4', 'Magazynier Radek', 'pbkdf2:sha256:260000$JlwV7lLoi7ltOw26$2efa79da94476cf3ffd3c5c2f5c1aa221bf3028ced5988b5d118d18b5f15e090', 'admin@admin.pl', 'uset');
INSERT INTO "main"."user" ("id", "username", "password_hash", "email_address", "role") VALUES ('6', 'Magazynier Adam', 'pbkdf2:sha256:260000$GsxWEH5JLKggXyvv$cf2c3ddd181e67bf980b5d9b7debeba910b734e473af868fc6af43bbb22f639d', '88888888@88888888.pl', 'user');


0001/08/22/ZP/1


OEE - raport produkcyjny
trakowanie usera dzienny
trakowanie produkt
założone wydajności 