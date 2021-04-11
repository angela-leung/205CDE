-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 11, 2021 at 05:20 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `205CDE`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_address`
--

DROP TABLE IF EXISTS `account_address`;
CREATE TABLE `account_address` (
  `id` int(11) NOT NULL,
  `country` varchar(120) NOT NULL,
  `city` varchar(120) NOT NULL,
  `street` varchar(120) NOT NULL,
  `postcode` varchar(120) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date_posted` datetime NOT NULL,
  `content` text NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `shopping_order`
--

DROP TABLE IF EXISTS `shopping_order`;
CREATE TABLE `shopping_order` (
  `id` int(11) NOT NULL,
  `violin_id` int(11) NOT NULL,
  `order_date` datetime NOT NULL,
  `user` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email_address` varchar(120) NOT NULL,
  `image_file` varchar(20) NOT NULL,
  `password` varchar(60) NOT NULL,
  `isaadminUser` tinyint(1) DEFAULT NULL
) ;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email_address`, `image_file`, `password`, `isaadminUser`) VALUES
(1, 'angela', 'angela@gmail.com', 'default.jpg', '$2b$12$RVmSxAleWXZOlF0C.3ajlOHWP6WE6QKCqr9oa7E7CZVYsfXZHBfUS', 1),
(3, 'angela1', 'violinfactoryhouse@gmail.com', 'default.jpg', '$2b$12$MBrC4.fGpUFzm4SZiG9f..4BGXcSJXR1N.yw0YUCbnf.ovpCp.DM6', 0);

-- --------------------------------------------------------

--
-- Table structure for table `violin`
--

DROP TABLE IF EXISTS `violin`;
CREATE TABLE `violin` (
  `id` int(11) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `product_images` varchar(20) NOT NULL,
  `product_date` datetime NOT NULL,
  `price` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `violin`
--

INSERT INTO `violin` (`id`, `product_name`, `product_images`, `product_date`, `price`) VALUES
(2, 'Violin', 'home1.jpeg', '2021-04-10 04:53:17', 30000);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_address`
--
ALTER TABLE `account_address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `shopping_order`
--
ALTER TABLE `shopping_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `violin_id` (`violin_id`),
  ADD KEY `user` (`user`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email_address` (`email_address`);

--
-- Indexes for table `violin`
--
ALTER TABLE `violin`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_address`
--
ALTER TABLE `account_address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `shopping_order`
--
ALTER TABLE `shopping_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `violin`
--
ALTER TABLE `violin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account_address`
--
ALTER TABLE `account_address`
  ADD CONSTRAINT `account_address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `shopping_order`
--
ALTER TABLE `shopping_order`
  ADD CONSTRAINT `shopping_order_ibfk_1` FOREIGN KEY (`violin_id`) REFERENCES `violin` (`id`),
  ADD CONSTRAINT `shopping_order_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
