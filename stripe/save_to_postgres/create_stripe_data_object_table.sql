-- Table: public.stripe_data_object

-- DROP TABLE public.stripe_data_object;

CREATE TABLE public.stripe_data_object
(
    serial_id integer NOT NULL DEFAULT nextval('stripe_data_object_serial_id_seq'::regclass),
    id character varying(256) COLLATE pg_catalog."default",
    object character varying(256) COLLATE pg_catalog."default",
    created bigint,
    livemode character varying(256) COLLATE pg_catalog."default",
    paid character varying(256) COLLATE pg_catalog."default",
    amount integer,
    currency character varying(5) COLLATE pg_catalog."default",
    refunded character varying(256) COLLATE pg_catalog."default",
    source json,
    captured character varying(256) COLLATE pg_catalog."default",
    refunds json,
    balance_transaction character varying(256) COLLATE pg_catalog."default",
    failure_message character varying(256) COLLATE pg_catalog."default",
    failure_code character varying(256) COLLATE pg_catalog."default",
    amount_refunded integer,
    customer character varying(256) COLLATE pg_catalog."default",
    invoice character varying(256) COLLATE pg_catalog."default",
    description character varying(256) COLLATE pg_catalog."default",
    dispute character varying(256) COLLATE pg_catalog."default",
    metadata json,
    CONSTRAINT stripe_data_object_pkey PRIMARY KEY (serial_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.stripe_data_object
    OWNER to postgres;