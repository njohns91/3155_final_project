CREATE TABLE user (
    user_id uuid DEFAULT uuid_generate_v4 (),
    first_name    VARCHAR(255) NOT NULL,
    last_name    VARCHAR(255) NOT NULL,,
	email    VARCHAR(255) NOT NULL,
	profile_image    VARCHAR(255) NOT NULL,
    pass   VARCHAR(255) NOT NULL,
	bio  VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);


CREATE TABLE listing (
    listing_id uuid DEFAULT uuid_generate_v4 (),
    date_posted    VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
	title    VARCHAR(255) NOT NULL,
	category    VARCHAR(255) NOT NULL,
	listing_image    VARCHAR(255) NOT NULL,
    price   INT NOT      NULL,
	user_id  VARCHAR(255) NOT NULL,
    PRIMARY KEY (listing_id)
);


CREATE TABLE post (
    post_id uuid DEFAULT uuid_generate_v4 (),
    user_id    VARCHAR(255) NOT NULL,
    listing_id VARCHAR(255) NOT NULL,
	date_posted    VARCHAR(255) NOT NULL,
	contents    VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id)
);





