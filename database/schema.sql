-- ==========================================
-- AI-Powered Visitor Analytics System
-- Database Schema
-- Version : 1.0
-- Team : Krishna & Himanshu
-- ==========================================

DROP DATABASE IF EXISTS visitor_analytics_db;

CREATE DATABASE visitor_analytics_db;

USE visitor_analytics_db;

-- ==========================================
-- Users Table
-- ==========================================

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin','Receptionist') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--===========================================
-- Visitors Table
--===========================================

CREATE TABLE visitors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    organization VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--============================================
-- Visits Table
--============================================

CREATE TABLE visits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visitor_id INT NOT NULL,
    host_name VARCHAR(100) NOT NULL,
    purpose VARCHAR(255) NOT NULL,
    check_in DATETIME NOT NULL,
    check_out DATETIME,
    status ENUM('Checked-In','Checked-Out') DEFAULT 'Checked-In',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visitor_id)
    REFERENCES visitors(id)
);

--============================================
-- Feedback Table
--============================================

CREATE TABLE feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    visit_id INT NOT NULL,
    rating TINYINT NOT NULL,
    feedback TEXT,
    sentiment ENUM('Positive','Neutral','Negative'),
    ai_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (visit_id)
    REFERENCES visits(id)
);