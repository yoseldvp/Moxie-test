CREATE TYPE appointmentstate AS ENUM ('SCHEDULED', 'COMPLETED', 'CANCELED');

CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name character varying NOT NULL,
  UNIQUE (name)
);

CREATE TABLE service (
  id SERIAL PRIMARY KEY,
  name character varying NOT NULL,
  description character varying,
  category_id integer,
  UNIQUE (name),
  FOREIGN KEY (category_id) REFERENCES category (id)
);

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  name character varying NOT NULL,
  markup numeric NOT NULL,
  supplier character varying,
  service_id integer,
  FOREIGN KEY (service_id) REFERENCES service (id)
);

CREATE TABLE customer (
  id SERIAL PRIMARY KEY,
  name character varying NOT NULL,
  email character varying NOT NULL,
  UNIQUE (email)
);

CREATE TABLE medspa (
  id SERIAL PRIMARY KEY,
  name character varying NOT NULL,
  address character varying,
  phone character varying,
  email_address character varying,
  UNIQUE (name)
);

CREATE TABLE medspaservice (
  id SERIAL PRIMARY KEY,
  medspa_id integer,
  service_id integer,
  created_at timestamp without time zone NOT NULL,
  price numeric NOT NULL,
  duration integer NOT NULL,
  FOREIGN KEY (medspa_id) REFERENCES medspa (id),
  FOREIGN KEY (service_id) REFERENCES service (id)
);

CREATE TABLE appointment (
  id SERIAL PRIMARY KEY,
  start_time timestamp without time zone NOT NULL,
  medspa_id integer,
  customer_id integer,
  FOREIGN KEY (customer_id) REFERENCES customer (id),
  FOREIGN KEY (medspa_id) REFERENCES medspa (id)
);

CREATE TABLE appointmenthistory (
  id SERIAL PRIMARY KEY,
  state appointmentstate NOT NULL,
  created_at timestamp without time zone NOT NULL,
  appointment_id integer,
  notes character varying,
  FOREIGN KEY (appointment_id) REFERENCES appointment (id)
);

CREATE TABLE procedure (
  id SERIAL PRIMARY KEY,
  appointment_id integer,
  medspaservice_id integer,
  FOREIGN KEY (appointment_id) REFERENCES appointment (id),
  FOREIGN KEY (medspaservice_id) REFERENCES medspaservice (id)
);
