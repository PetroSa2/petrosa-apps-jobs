-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: petrosa_b3.mysql.dbaas.com.br
-- Generation Time: Sep 07, 2023 at 01:01 PM
-- Server version: 5.7.32-35-log
-- PHP Version: 5.6.40-0+deb8u12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `petrosa_b3`
--

-- --------------------------------------------------------

--
-- Table structure for table `backtest_results_lists`
--

CREATE TABLE `backtest_results_lists` (
  `id` int(11) NOT NULL,
  `_id` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `period` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `strategy` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `symbol` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `insert_timestamp` datetime DEFAULT NULL,
  `n_trades` double DEFAULT NULL,
  `status` double DEFAULT NULL,
  `str_class` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `type` varchar(24) COLLATE latin1_general_ci DEFAULT NULL,
  `Size` double DEFAULT NULL,
  `EntryBar` double DEFAULT NULL,
  `ExitBar` double DEFAULT NULL,
  `EntryPrice` double DEFAULT NULL,
  `ExitPrice` double DEFAULT NULL,
  `PnL` double DEFAULT NULL,
  `ReturnPct` double DEFAULT NULL,
  `EntryTime` datetime DEFAULT NULL,
  `ExitTime` datetime DEFAULT NULL,
  `Duration` double DEFAULT NULL,
  `sql_insert_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `backtest_results_lists`
--
ALTER TABLE `backtest_results_lists`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `backtest_results_lists`
--
ALTER TABLE `backtest_results_lists`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
