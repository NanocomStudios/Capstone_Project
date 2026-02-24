-- Adminer 5.4.2 PostgreSQL 16.12 dump

DROP TABLE IF EXISTS "deliveries";
CREATE TABLE "public"."deliveries" (
    "id" character varying NOT NULL,
    "order_id" character varying NOT NULL,
    "driver_id" character varying NOT NULL,
    "package_id" character varying NOT NULL,
    "delivery_address" character varying NOT NULL,
    "status" character varying NOT NULL,
    "created_at" timestamp,
    "updated_at" timestamp,
    CONSTRAINT "deliveries_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX ix_deliveries_order_id ON public.deliveries USING btree (order_id);

CREATE INDEX ix_deliveries_driver_id ON public.deliveries USING btree (driver_id);

CREATE INDEX ix_deliveries_id ON public.deliveries USING btree (id);

INSERT INTO "deliveries" ("id", "order_id", "driver_id", "package_id", "delivery_address", "status", "created_at", "updated_at") VALUES
('481da799-0ce6-45ef-b029-88632c7455b6',	'1order',	'1driver',	'1package',	'Tomy home on this day',	'assigned',	'2026-02-21 13:25:38.78491',	'2026-02-21 13:25:38.784949'),
('8572cca6-5349-477e-91bf-797d49cb976c',	'ORD-1001',	'DRV-7',	'PKG-55',	'Colombo',	'delivered',	'2026-02-22 10:08:30.846205',	'2026-02-22 10:08:35.189487'),
('e9f6b912-c343-4b3a-b75d-cbf96491df63',	'ORD-1001',	'DRV-7',	'PKG-55',	'Colombo',	'assigned',	'2026-02-22 10:08:55.005339',	'2026-02-22 10:08:55.005347'),
('6357afb6-f892-41e7-bf90-bb4737a86653',	'2',	'1',	'1',	'dfjldfjldjfldkjfkldf',	'assigned',	'2026-02-22 13:04:04.906643',	'2026-02-22 13:04:04.906681'),
('5c26109d-ceb3-42d4-9ed9-e70ab32abc8d',	'1',	'1',	'1',	'1',	'delivered',	'2026-02-21 13:30:27.766024',	'2026-02-22 13:12:37.503175');

DROP TABLE IF EXISTS "delivery_feedback";
CREATE TABLE "public"."delivery_feedback" (
    "id" character varying NOT NULL,
    "delivery_id" character varying NOT NULL,
    "status" character varying NOT NULL,
    "reason" character varying,
    "signature_data" character varying,
    "photo_url" character varying,
    "timestamp" timestamp,
    CONSTRAINT "delivery_feedback_pkey" PRIMARY KEY ("id")
)
WITH (oids = false);

CREATE INDEX ix_delivery_feedback_delivery_id ON public.delivery_feedback USING btree (delivery_id);

CREATE INDEX ix_delivery_feedback_id ON public.delivery_feedback USING btree (id);

INSERT INTO "delivery_feedback" ("id", "delivery_id", "status", "reason", "signature_data", "photo_url", "timestamp") VALUES
('12125cdb-84f0-4719-a7d9-322cd81804eb',	'8572cca6-5349-477e-91bf-797d49cb976c',	'delivered',	NULL,	'c2lnbmF0dXJl',	'https://example.com/pod.jpg',	'2026-02-22 10:08:35.189628'),
('25ce8738-2d8a-4df5-8a30-0bcaaf622cbe',	'5c26109d-ceb3-42d4-9ed9-e70ab32abc8d',	'delivered',	'handover',	'today',	'none',	'2026-02-22 13:12:37.504242');

-- 2026-02-22 13:45:21 UTC
