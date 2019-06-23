drop table if exists pinterest_img;
create table pinterest_img
(
  id          int auto_increment primary key,
  search_text varchar(100),
  img_src     varchar(1000) unique key,
  is_crawled  int default 0
);