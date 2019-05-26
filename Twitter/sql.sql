drop table if exists twitter_img;
create table twitter_img
(
  id         int auto_increment primary key,
  username   varchar(100),
  img_src    varchar(1000) unique key,
  is_crawled int default 0
);