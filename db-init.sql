-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Step 1: Create the businesses table with nullable fields
CREATE TABLE IF NOT EXISTS businesses (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    description TEXT NULL,
    registration_number VARCHAR(100) UNIQUE NULL,
    website VARCHAR(255) NULL,
    email VARCHAR(255) NULL,
    phone VARCHAR(50) NULL,
    established_year INT NULL,
    revenue DECIMAL(15,2) NULL,
    company_size VARCHAR(50) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Step 2: Create a function to update "updated_at" automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Create a trigger to call the function before updates
CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON businesses
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Step 4: Create business_meta table with nullable meta_value
CREATE TABLE IF NOT EXISTS business_meta (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    meta_key VARCHAR(255) NOT NULL,
    meta_value TEXT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Step 5: Create business_tags table
CREATE TABLE IF NOT EXISTS business_tags (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    tag VARCHAR(255) NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Step 6: Create business_owners table (contact details are optional)
CREATE TABLE IF NOT EXISTS business_owners (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    owner_name VARCHAR(255) NOT NULL,
    contact_number VARCHAR(50) NULL,
    email VARCHAR(255) NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Step 7: Create business_locations table (allowing NULL for location fields)
CREATE TABLE IF NOT EXISTS business_locations (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(100) NULL,
    country VARCHAR(100) NULL,
    latitude DECIMAL(10,8) NULL,
    longitude DECIMAL(11,8) NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Step 8: Create business_embeddings table for AI-powered search
CREATE TABLE IF NOT EXISTS business_embeddings (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    business_id BIGINT NOT NULL,
    embedding_vector JSON NOT NULL,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);
