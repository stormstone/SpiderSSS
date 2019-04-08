drop table if exists music163_follow_href;
create table music163_follow_href
(
  id          int primary key auto_increment,
  follow_href varchar(200) unique key,
  is_used     int default 0
);

drop table if exists music163_user_id;
create table music163_user_id
(
  id      int primary key auto_increment,
  user_id varchar(200) unique key,
  is_used int default 0
);

drop table if exists music163_user_info;
create table music163_user_info
(
  id           int primary key auto_increment,
  user_id      varchar(20) unique key,
  user_name    varchar(200),
  user_djp     varchar(200),
  user_lev     int,
  event_count  int,
  follow_count int,
  fan_count    int,
  user_intr    varchar(200),
  user_base    varchar(100),
  user_age     varchar(10)
);

drop table if exists music163_user_song;
create table music163_user_song
(
  id          int primary key auto_increment,
  user_id     int,
  song_index  int,
  song_title  varchar(200),
  song_author varchar(200),
  song_href   varchar(200),
  song_hot    int,
  unique_key  varchar(100) unique key
);
