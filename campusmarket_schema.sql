CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE person (
    person_id       uuid DEFAULT uuid_generate_v4 () NOT NULL,
    first_name      VARCHAR(255) NOT NULL,
    last_name       VARCHAR(255) NOT NULL,
	email           VARCHAR(255) NOT NULL UNIQUE,
	profile_image   VARCHAR(255),
    person_pass     VARCHAR(255) NOT NULL,
	bio             VARCHAR(255),
    PRIMARY KEY (person_id)
);


CREATE TABLE listing (
    listing_id          uuid DEFAULT uuid_generate_v4 () NOT NULL,
    date_posted         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    listing_description TEXT NOT NULL,
	title               VARCHAR(255) NOT NULL,
	category            VARCHAR(255) NOT NULL,
	listing_image       VARCHAR(255) NOT NULL,
    price               FLOAT NOT NULL,
	person_id           uuid NOT NULL,
    PRIMARY KEY (listing_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id)
);


CREATE TABLE comment (
    comment_id          uuid DEFAULT uuid_generate_v4 () NOT NULL,
    listing_id          uuid  NOT NULL,
    person_id           uuid  NOT NULL,
	date_posted         TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	content             VARCHAR(255) NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (listing_id) REFERENCES listing(listing_id)
);