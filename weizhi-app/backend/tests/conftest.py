import os


os.environ["APP_ENV"] = "local"
os.environ["SUPABASE_URL"] = "https://example.supabase.co"
os.environ["SUPABASE_SERVICE_ROLE_KEY"] = "replace-with-service-role-key"
os.environ["SUPABASE_JWT_SECRET"] = "replace-with-supabase-jwt-secret-at-least-32-characters"
os.environ["MIMOAI_API_BASE_URL"] = "https://api.example.com"
os.environ["MIMOAI_API_KEY"] = "replace-with-mimoai-key"
