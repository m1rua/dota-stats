CREATE TABLE cache (
    account_id BIGINT PRIMARY KEY,
    data JSONB,
    cached_at TIMESTAMP DEFAULT NOW()
);
