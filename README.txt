#create  DB
1) console->python
2) >>> from mainApp import db
3) >>> db.create_all()

0 - zablokowany
1 - aktywny
666 - admin


pip freeze -l > requirements.txt
pip install -r requirements.txt


gon	pbkdf2:sha256:260000$3gEkNrdOJMAdnKrJ$6c138f74f3242f394423e334ec0142e356f3d295e96fa10c3985eab4e309b0e5	666


-- SQLite
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('1', '11', 'Awaria - 11 - Czujniki');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('2', '12', 'Awaria - 12 - Siłowniki pneumatyczne');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('3', '13', 'Awaria - 13 - Kompresor');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('4', '14', 'Awaria - 14 - Hamulce');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('5', '15', 'Awaria - 15 - Przewody elektryczne');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('6', '16', 'Awaria - 16 - Przewody pneumatyczne');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('7', '17', 'Awaria - 17 - Inne');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('8', '21', 'Przezbrojenie - 21 - Modelu');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('9', '22', 'Przezbrojenie - 22 - Wymiaru');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('10', '31', 'Zasilenie maszyny - 31 - Rury');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('11', '32', 'Zasilenie maszyny - 32 - Wzmocnienia');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('12', '33', 'Zasilenie maszyny - 33 - Kolektory');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('13', '40', 'Braki materiału - 40');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('14', '50', 'Przerwa - 50');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('15', '61', 'Regulacje parametrów -61 - Moc zgrzewania');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('16', '62', 'Regulacje parametrów -62 - Ciśnienie');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('17', '63', 'Regulacje parametrów -63 - Czas zgrzewania');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('18', '70', 'Zmiana siatki na elektrodach -70');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('19', '80', 'Zmiana palety - 80');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('20', '90', 'Kontrola szczelności - 90');
INSERT INTO "main"."event_type" ("id", "idEvent", "eventName") VALUES ('21', '100', 'Sprzątanie stanowiska - 100');

INSERT INTO "main"."product" ("id", "belegNumber", "modelName", "lenght", "numberOfParts", "bracket", "singleOrDouble", "orderStatus", "executionDate") VALUES ('1', 'No', 'No', '', '', '1', '1', '1', '2030-01-01 00:00:00.000000');