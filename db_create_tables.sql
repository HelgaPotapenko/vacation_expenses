-- enable foreign keys
PRAGMA foreign_keys = ON;

-- expense_categories definition
CREATE TABLE expense_categories (
id integer primary key autoincrement,
expense_category_name text not null
);

-- payers definition
CREATE TABLE payers (
id integer primary key autoincrement,
payer_name text not null
);

-- vacations definition
CREATE TABLE vacations (
id integer primary key autoincrement,
date_start date not null,
date_end date not null,
description text not null
);

-- expenses definition
CREATE TABLE expenses (
id integer primary key autoincrement,
expense_date date not null,
vacation_id integer,
expense_category_id integer,
description text not null,
payer_id integer,
constraint payer_id_fk foreign key(payer_id) references payers(id) ON UPDATE CASCADE ON DELETE SET NULL,
constraint expense_category_id_fk foreign key(expense_category_id) references expense_categories(id) ON UPDATE CASCADE ON DELETE SET NULL, 
constraint vacation_fk foreign key(vacation_id) references vacations(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE VIEW vw_expenses AS 
SELECT e.id, e.expense_date, e.description, v.description as vacation, ec.expense_category_name as expense_category, p.payer_name as payer
FROM expenses e
join expense_categories ec on ec.id = e.expense_category_id
join vacations v  on v.id  = e.vacation_id 
join payers p on p.id = e.payer_id;