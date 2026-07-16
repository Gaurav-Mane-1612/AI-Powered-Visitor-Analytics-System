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