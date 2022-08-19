#create  DB
1) console->python
2) >>> from mainApp import db
3) >>> db.create_all()


pip freeze -l > requirements.txt
pip install -r requirements.txt


-- SQLite
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('1', '00', 'Produkcja - 00 - Produkcja', 'Prod');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('2', '11', 'Awaria - 11 - Czujniki', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('3', '12', 'Awaria - 12 - Siłowniki pneumatyczne', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('4', '13', 'Awaria - 13 - Kompresor', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('5', '14', 'Awaria - 14 - Hamulce', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('6', '15', 'Awaria - 15 - Przewody elektryczne', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('7', '16', 'Awaria - 16 - Przewody pneumatyczne', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('8', '17', 'Awaria - 17 - Inne', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('9', '21', 'Przezbrojenie - 21 - Modelu', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('10', '22', 'Przezbrojenie - 22 - Wymiaru', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('11', '31', 'Zasilenie maszyny - 31 - Rury', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('12', '32', 'Zasilenie maszyny - 32 - Wzmocnienia', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('13', '33', 'Zasilenie maszyny - 33 - Kolektory', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('14', '40', 'Braki materiału - 40', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('15', '50', 'Przerwa - 50', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('16', '61', 'Regulacje parametrów -61 - Moc zgrzewania', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('17', '62', 'Regulacje parametrów -62 - Ciśnienie', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('18', '63', 'Regulacje parametrów -63 - Czas zgrzewania', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('19', '70', 'Zmiana siatki na elektrodach -70', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('20', '80', 'Zmiana palety - 80', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('21', '90', 'Kontrola szczelności - 90', 'Error');
INSERT INTO "status" ("id", "statusCode", "statusName", "production") VALUES ('22', '100', 'Sprzątanie stanowiska - 100', 'Error');