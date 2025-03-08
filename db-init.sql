CREATE TABLE IF NOT EXISTS businesses (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    registration_number VARCHAR(100) UNIQUE,
    website VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    established_year INT,
    revenue DECIMAL(15,2),
    company_size VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS business_meta (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    meta_key VARCHAR(255) NOT NULL,
    meta_value TEXT NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS business_tags (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS business_owners (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    owner_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(50),
    email VARCHAR(255),
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS business_locations (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS business_embeddings (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    embedding_vector JSON NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);
