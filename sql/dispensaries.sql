CREATE TABLE dispensaries (
  id UUID PRIMARY KEY,
  company_id BIGINT,
  flower_url TEXT,
  pre_rolls_url TEXT,
  vaporizers_url TEXT,
  concentrates_url TEXT,
  edibles_url TEXT,
  tinctures_url TEXT,
  topicals_url TEXT,
  cbd_url TEXT,
  address VARCHAR
);