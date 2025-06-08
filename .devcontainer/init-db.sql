-- Create additional databases for development and testing
SELECT 'CREATE DATABASE nextcrm_test' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nextcrm_test')\gexec

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE nextcrm_dev TO nextcrm;
GRANT ALL PRIVILEGES ON DATABASE nextcrm_test TO nextcrm;