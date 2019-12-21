CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(180) NOT NULL,
  `email` varchar(180) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `age` int(11) unsigned DEFAULT NULL,
  `ts_last_login` int(11) unsigned DEFAULT NULL,
  `ts_registration` int(11) unsigned NOT NULL,
  `last_login_ip` varchar(255) DEFAULT NULL,
  `registration_ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_email` (`email`),
  UNIQUE KEY `unq_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

