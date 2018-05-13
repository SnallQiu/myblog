CREATE TABLE IF NOT EXISTS `todolist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `title` varchar(1024) NOT NULL,
  `status` int(2) NOT NULL COMMENT '是否完成',
  `create_time` TIMESTAMP(4) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;

insert into todolist(id, user_id, title, status, create_time) values(1, 1, '习近平五谈稳中求进织密扎牢民生保障网', '0', 1482214350), (2, 1, '特朗普获超270张选举人票将入主白 宫', '1', 1482214350);


CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) DEFAULT NULL,
  `password_hash` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

insert into user values(1, 'admin', 'admin');
 CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` TEXT(65355) DEFAULT NULL,
  `timestamp` TIMESTAMP(4) NOT NULL,
  `author_id` INT(30) NOT NULL ,
  `title` VARCHAR (30) NOT NULL ,
  `link` VARCHAR (60) NOT NULL ,
  `vote` int(10) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
insert into posts values(1, '这是一篇测试博客，里面啥也没写', '2018-05-05 21:49:00',6,'TEST','www.baidu.com');
