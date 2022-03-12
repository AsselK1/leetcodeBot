--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Ubuntu 14.1-1.pgdg21.10+1)
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-1.pgdg21.10+1)

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

SET default_table_access_method = heap;

--
-- Name: record; Type: TABLE; Schema: public; Owner: arsen
--

CREATE TABLE public.record (
    chat_id bigint NOT NULL,
    user_id bigint NOT NULL,
    easies integer,
    mediums integer,
    hards integer,
    username character varying(100)
);

ALTER TABLE public.record OWNER TO assel;

--
-- Data for Name: record; Type: TABLE DATA; Schema: public; Owner: arsen
--

COPY public.record (chat_id, user_id, easies, mediums, hards, username) FROM stdin;
\.


--
-- Name: record user_of_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: arsen
--

ALTER TABLE ONLY public.record
    ADD CONSTRAINT user_of_chat_pkey PRIMARY KEY (chat_id, user_id);


--
-- PostgreSQL database dump complete
--

