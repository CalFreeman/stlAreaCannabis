CREATE TABLE json_normalized (
  id UUID PRIMARY KEY,
  dispensary_id BIGINT,
  json_raw_id BIGINT,
  brand VARCHAR(255),
  gram VARCHAR(255),
  image VARCHAR(255),
  name VARCHAR(255),
  price SMALLINT,
  qty SMALLINT,
  status VARCHAR(255),
  strain VARCHAR(255),
  type VARCHAR(255)
);