-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Queue table
CREATE TABLE queue (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    media_type VARCHAR(10) CHECK (media_type IN ('video', 'image')),
    generation_parameters JSONB,
    status VARCHAR(20) CHECK (status IN ('pending', 'in_progress', 'completed', 'error')),
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    time_taken INTERVAL,
    result_file VARCHAR(255),
    error_message TEXT
);

-- Create index on status and priority for efficient querying
CREATE INDEX idx_queue_status_priority ON queue (status, priority);

-- Create Privileges table
CREATE TABLE privileges (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    privilege VARCHAR(50) NOT NULL,
    UNIQUE (user_id, privilege)
);

-- Create users
INSERT INTO users (username, email) VALUES 
    ('user.local', 'user@local'),
    ('admin.local', 'admin@local');

-- Assign privileges
INSERT INTO privileges (user_id, privilege) VALUES
    ((SELECT id FROM users WHERE username = 'user.local'), 'submit_job'),
    ((SELECT id FROM users WHERE username = 'user.local'), 'view_own_jobs'),
    ((SELECT id FROM users WHERE username = 'admin.local'), 'submit_job'),
    ((SELECT id FROM users WHERE username = 'admin.local'), 'view_all_jobs'),
    ((SELECT id FROM users WHERE username = 'admin.local'), 'manage_users'),
    ((SELECT id FROM users WHERE username = 'admin.local'), 'manage_queue');

-- Sample queue items (commented out)
/*
INSERT INTO queue (user_id, media_type, generation_parameters, status, priority)
VALUES
    (1, 'video', '{"duration": 60, "resolution": "1080p", "theme": "nature"}', 'pending', 3),
    (1, 'image', '{"width": 1920, "height": 1080, "style": "abstract"}', 'pending', 2),
    (1, 'video', '{"duration": 30, "resolution": "720p", "theme": "urban"}', 'pending', 4);
*/
