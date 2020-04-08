--                                                                                          [161/267]
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-0+deb10u1)
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: climate; Type: TABLE; Schema: public; Owner: wetter
--

CREATE TABLE public.climate (
    id bigint NOT NULL,
    station bigint NOT NULL,
    date date NOT NULL,
    qn_3 integer,
    fx real,
    fm real,
    qn_4 integer,
    rsk real,
    rskf integer,
    sdk real,
    shk_tag real,
    nm real,
    vpm real,
    pm real,
    tmk real,
    upm real,
    txk real,
    tnk real,
    tgk real,
    dwd_last_update timestamp without time zone
);


ALTER TABLE public.climate OWNER TO wetter;

--
-- Name: climate_id_seq; Type: SEQUENCE; Schema: public; Owner: wetter
--

CREATE SEQUENCE public.climate_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.climate_id_seq OWNER TO wetter;

--
-- Name: climate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wetter
--

ALTER SEQUENCE public.climate_id_seq OWNED BY public.climate.id;


--
-- Name: stations; Type: TABLE; Schema: public; Owner: wetter
--

CREATE TABLE public.stations (
    id bigint NOT NULL,
    name character varying(200) NOT NULL,
    lat numeric(10,8) NOT NULL,
    lon numeric(11,8) NOT NULL,
    dwd_id character varying(5),
    dwd_last_update timestamp without time zone,
    state character varying(200),
    sea_level integer
);


ALTER TABLE public.stations OWNER TO wetter;

--
-- Name: stations_id_seq; Type: SEQUENCE; Schema: public; Owner: wetter
--

CREATE SEQUENCE public.stations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stations_id_seq OWNER TO wetter;

--
-- Name: stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: wetter
--

ALTER SEQUENCE public.stations_id_seq OWNED BY public.stations.id;


--
-- Name: climate id; Type: DEFAULT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.climate ALTER COLUMN id SET DEFAULT nextval('public.climate_id_seq'::regclass
);


--
-- Name: climate station; Type: DEFAULT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.climate ALTER COLUMN station SET DEFAULT nextval('public.climate_station_seq'
::regclass);


--
-- Name: stations id; Type: DEFAULT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.stations ALTER COLUMN id SET DEFAULT nextval('public.stations_id_seq'::regcla
ss);


--
-- Name: climate climate_pkey; Type: CONSTRAINT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.climate
    ADD CONSTRAINT climate_pkey PRIMARY KEY (id);


--
-- Name: stations stations_pkey; Type: CONSTRAINT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.stations
    ADD CONSTRAINT stations_pkey PRIMARY KEY (id);


--
-- Name: climate climate_station_fkey; Type: FK CONSTRAINT; Schema: public; Owner: wetter
--

ALTER TABLE ONLY public.climate
    ADD CONSTRAINT climate_station_fkey FOREIGN KEY (station) REFERENCES public.stations(id);


--
-- PostgreSQL database dump complete
--
