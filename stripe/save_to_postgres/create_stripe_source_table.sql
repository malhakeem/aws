-- Table: public.stripe_source

-- DROP TABLE public.stripe_source;

CREATE TABLE public.stripe_source
(
    serial_id integer NOT NULL DEFAULT nextval('stripe_source_serial_id_seq'::regclass),
    data_serial_id integer,
    created bigint,
    livemode character varying(256) COLLATE pg_catalog."default",
    id character varying(256) COLLATE pg_catalog."default",
    object character varying(256) COLLATE pg_catalog."default",
    type character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT stripe_source_pkey PRIMARY KEY (serial_id),
    CONSTRAINT stripe_source_data_serial_id_fkey FOREIGN KEY (data_serial_id)
        REFERENCES public.stripe_data_object (serial_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.stripe_source
    OWNER to postgres;