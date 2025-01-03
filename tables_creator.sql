CREATE TABLE users (
    id UUID PRIMARY KEY,
    identifier TEXT NOT NULL UNIQUE,
    metadata JSONB NOT NULL,
    createdAt TIMESTAMPTZ
);

CREATE TABLE threads (
    id UUID PRIMARY KEY,
    createdAt TIMESTAMPTZ,
    name TEXT,
    userId UUID,
    userIdentifier TEXT,
    tags TEXT[],
    metadata JSONB,
    FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
);
