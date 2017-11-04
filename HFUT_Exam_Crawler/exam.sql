-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2016-06-18 17:30:56
-- 服务器版本: 5.5.47-0ubuntu0.14.04.1
-- PHP 版本: 5.5.9-1ubuntu4.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `exam`
--
CREATE DATABASE IF NOT EXISTS `exam` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `exam`;

-- --------------------------------------------------------

--
-- 表的结构 `marxism`
--

DROP TABLE IF EXISTS `marxism`;
CREATE TABLE IF NOT EXISTS `marxism` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `a` varchar(200) DEFAULT NULL,
  `b` varchar(200) DEFAULT NULL,
  `c` varchar(200) DEFAULT NULL,
  `d` varchar(200) DEFAULT NULL,
  `answer` varchar(200) NOT NULL,
  `chapter` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 插入之前先把表清空（truncate） `marxism`
--

TRUNCATE TABLE `marxism`;
-- --------------------------------------------------------

--
-- 表的结构 `mzdsxhzgteshzylltx`
--

DROP TABLE IF EXISTS `mzdsxhzgteshzylltx`;
CREATE TABLE IF NOT EXISTS `mzdsxhzgteshzylltx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `a` varchar(200) DEFAULT NULL,
  `b` varchar(200) DEFAULT NULL,
  `c` varchar(200) DEFAULT NULL,
  `d` varchar(200) DEFAULT NULL,
  `answer` varchar(200) NOT NULL,
  `chapter` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 插入之前先把表清空（truncate） `mzdsxhzgteshzylltx`
--

TRUNCATE TABLE `mzdsxhzgteshzylltx`;
-- --------------------------------------------------------

--
-- 表的结构 `sxddxyyfljc`
--

DROP TABLE IF EXISTS `sxddxyyfljc`;
CREATE TABLE IF NOT EXISTS `sxddxyyfljc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `a` varchar(200) DEFAULT NULL,
  `b` varchar(200) DEFAULT NULL,
  `c` varchar(200) DEFAULT NULL,
  `d` varchar(200) DEFAULT NULL,
  `answer` varchar(200) NOT NULL,
  `chapter` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 插入之前先把表清空（truncate） `sxddxyyfljc`
--

TRUNCATE TABLE `sxddxyyfljc`;
-- --------------------------------------------------------

--
-- 表的结构 `zgjdsgy`
--

DROP TABLE IF EXISTS `zgjdsgy`;
CREATE TABLE IF NOT EXISTS `zgjdsgy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `a` varchar(200) DEFAULT NULL,
  `b` varchar(200) DEFAULT NULL,
  `c` varchar(200) DEFAULT NULL,
  `d` varchar(200) DEFAULT NULL,
  `answer` varchar(200) NOT NULL,
  `chapter` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subject` (`subject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 插入之前先把表清空（truncate） `zgjdsgy`
--

TRUNCATE TABLE `zgjdsgy`;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
