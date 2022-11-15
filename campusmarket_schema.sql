CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE person (
    person_id       uuid DEFAULT uuid_generate_v4 (),
    first_name      VARCHAR(255) NOT NULL,
    last_name       VARCHAR(255) NOT NULL,
	email           VARCHAR(255) NOT NULL UNIQUE,
	profile_image   VARCHAR(255),
    person_pass     VARCHAR(255) NOT NULL,
	bio             VARCHAR(255),
    PRIMARY KEY (person_id)
);


CREATE TABLE listing (
    listing_id          uuid DEFAULT uuid_generate_v4 (),
    date_posted         VARCHAR(255) NOT NULL,
    listing_description TEXT NOT NULL,
	title               VARCHAR(255) NOT NULL,
	category            VARCHAR(255) NOT NULL,
	listing_image       VARCHAR(255) NOT NULL,
    price               INT NOT NULL,
	owner_id            uuid NOT NULL,
    PRIMARY KEY (listing_id),
    FOREIGN KEY (owner_id) REFERENCES person(person_id)
);


CREATE TABLE comment (
    post_id             uuid DEFAULT uuid_generate_v4 (),
    comment_id          uuid  NULL,
    poster_id           uuid  NULL,
	date_posted         VARCHAR(255) NOT NULL,
	content             VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (poster_id) REFERENCES person(person_id),
    FOREIGN KEY (comment_id) REFERENCES listing(listing_id)
);