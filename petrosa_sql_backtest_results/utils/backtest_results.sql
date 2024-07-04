-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: petrosa_b3.mysql.dbaas.com.br
-- Generation Time: Sep 07, 2023 at 12:58 PM
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
-- Table structure for table `backtest_results`
--

CREATE TABLE `backtest_results` (
  `id` bigint(20) NOT NULL,
  `_id` varchar(200) COLLATE latin1_general_ci DEFAULT NULL,
  `period` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `strategy` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `symbol` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `avg_drawdown_duration` double DEFAULT NULL,
  `avg_drawdown_pcent` double DEFAULT NULL,
  `avg_trade_duration` bigint(20) DEFAULT NULL,
  `avg_trade_pcent` double DEFAULT NULL,
  `best_trade_pcent` double DEFAULT NULL,
  `buy_and_hold_return_pcent` double DEFAULT NULL,
  `calmar_ratio` double DEFAULT NULL,
  `duration` bigint(20) DEFAULT NULL,
  `end` datetime DEFAULT NULL,
  `equity_final_` double DEFAULT NULL,
  `equity_peak_` double DEFAULT NULL,
  `expectancy_pcent` double DEFAULT NULL,
  `exposure_time_pcent` double DEFAULT NULL,
  `insert_timestamp` datetime DEFAULT NULL,
  `max_drawdown_duration` double DEFAULT NULL,
  `max_drawdown_pcent` double DEFAULT NULL,
  `max_trade_duration` bigint(20) DEFAULT NULL,
  `n_trades` bigint(20) DEFAULT NULL,
  `profit_factor` double DEFAULT NULL,
  `return_ann_pcent` double DEFAULT NULL,
  `return_pcent` double DEFAULT NULL,
  `sharpe_ratio` double DEFAULT NULL,
  `sortino_ratio` double DEFAULT NULL,
  `sqn` double DEFAULT NULL,
  `start` datetime DEFAULT NULL,
  `status` bigint(20) DEFAULT NULL,
  `str_class` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `test_type` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `type` varchar(1024) COLLATE latin1_general_ci DEFAULT NULL,
  `volatility_ann_pcent` double DEFAULT NULL,
  `win_rate_pcent` double DEFAULT NULL,
  `worst_trade_pcent` double DEFAULT NULL,
  `sql_insert_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `backtest_results`
--
ALTER TABLE `backtest_results`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `period` (`period`,`strategy`,`symbol`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `backtest_results`
--
ALTER TABLE `backtest_results`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
