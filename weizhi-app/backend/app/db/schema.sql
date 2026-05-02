create table if not exists cities (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name_zh text not null,
  name_en text,
  country_region text not null,
  is_supported boolean not null default false,
  content_depth text not null check (content_depth in ('core', 'expansion', 'unsupported')),
  tone_summary text,
  hero_image_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists works (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  original_title text,
  work_type text not null check (work_type in ('book', 'film', 'series')),
  creator text,
  year text,
  synopsis text not null,
  cover_image_url text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists places (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  city_id uuid not null references cities(id) on delete cascade,
  name text not null,
  intro text not null,
  image_url text,
  address text,
  latitude numeric,
  longitude numeric,
  map_query text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists work_city_relations (
  id uuid primary key default gen_random_uuid(),
  work_id uuid not null references works(id) on delete cascade,
  city_id uuid not null references cities(id) on delete cascade,
  relation_summary text not null,
  recommendation_note text not null,
  theme_tags text[] not null default '{}',
  source_url text,
  source_note text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  unique(work_id, city_id)
);

create table if not exists work_place_relations (
  id uuid primary key default gen_random_uuid(),
  work_id uuid not null references works(id) on delete cascade,
  place_id uuid not null references places(id) on delete cascade,
  meaning text not null,
  source_url text,
  source_note text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  unique(work_id, place_id)
);

create table if not exists collections (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  entity_type text not null check (entity_type in ('work', 'place')),
  entity_id uuid not null,
  city_id uuid not null references cities(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique(user_id, entity_type, entity_id)
);

create table if not exists recommendation_caches (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id) on delete cascade,
  content_type text not null default 'all',
  theme_tags text[] not null default '{}',
  cache_key text not null unique,
  result_json jsonb not null,
  generation_mode text not null check (generation_mode in ('pre_generated', 'realtime')),
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
