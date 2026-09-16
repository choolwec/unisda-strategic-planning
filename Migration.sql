
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: planning_db
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add designation',6,'add_designation'),(22,'Can change designation',6,'change_designation'),(23,'Can delete designation',6,'delete_designation'),(24,'Can view designation',6,'view_designation'),(25,'Can add role',7,'add_role'),(26,'Can change role',7,'change_role'),(27,'Can delete role',7,'delete_role'),(28,'Can view role',7,'view_role'),(29,'Can add user',8,'add_user'),(30,'Can change user',8,'change_user'),(31,'Can delete user',8,'delete_user'),(32,'Can view user',8,'view_user'),(33,'Can add kpi',9,'add_kpi'),(34,'Can change kpi',9,'change_kpi'),(35,'Can delete kpi',9,'delete_kpi'),(36,'Can view kpi',9,'view_kpi'),(37,'Can add main activity',10,'add_mainactivity'),(38,'Can change main activity',10,'change_mainactivity'),(39,'Can delete main activity',10,'delete_mainactivity'),(40,'Can view main activity',10,'view_mainactivity'),(41,'Can add activity',11,'add_activity'),(42,'Can change activity',11,'change_activity'),(43,'Can delete activity',11,'delete_activity'),(44,'Can view activity',11,'view_activity'),(45,'Can add report',12,'add_report'),(46,'Can change report',12,'change_report'),(47,'Can delete report',12,'delete_report'),(48,'Can view report',12,'view_report'),(49,'Can add strategic objective',13,'add_strategicobjective'),(50,'Can change strategic objective',13,'change_strategicobjective'),(51,'Can delete strategic objective',13,'delete_strategicobjective'),(52,'Can view strategic objective',13,'view_strategicobjective'),(53,'Can add strategic theme',14,'add_strategictheme'),(54,'Can change strategic theme',14,'change_strategictheme'),(55,'Can delete strategic theme',14,'delete_strategictheme'),(56,'Can view strategic theme',14,'view_strategictheme');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_strategic_planning_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_strategic_planning_user_id` FOREIGN KEY (`user_id`) REFERENCES `strategic_planning_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(11,'strategic_planning','activity'),(6,'strategic_planning','designation'),(9,'strategic_planning','kpi'),(10,'strategic_planning','mainactivity'),(12,'strategic_planning','report'),(7,'strategic_planning','role'),(13,'strategic_planning','strategicobjective'),(14,'strategic_planning','strategictheme'),(8,'strategic_planning','user');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-11-25 11:45:30.021074'),(2,'contenttypes','0002_remove_content_type_name','2024-11-25 11:45:30.105067'),(3,'auth','0001_initial','2024-11-25 11:45:30.589243'),(4,'auth','0002_alter_permission_name_max_length','2024-11-25 11:45:30.674288'),(5,'auth','0003_alter_user_email_max_length','2024-11-25 11:45:30.683817'),(6,'auth','0004_alter_user_username_opts','2024-11-25 11:45:30.695402'),(7,'auth','0005_alter_user_last_login_null','2024-11-25 11:45:30.706441'),(8,'auth','0006_require_contenttypes_0002','2024-11-25 11:45:30.712082'),(9,'auth','0007_alter_validators_add_error_messages','2024-11-25 11:45:30.722056'),(10,'auth','0008_alter_user_username_max_length','2024-11-25 11:45:30.732062'),(11,'auth','0009_alter_user_last_name_max_length','2024-11-25 11:45:30.741268'),(12,'auth','0010_alter_group_name_max_length','2024-11-25 11:45:30.769921'),(13,'auth','0011_update_proxy_permissions','2024-11-25 11:45:30.780921'),(14,'auth','0012_alter_user_first_name_max_length','2024-11-25 11:45:30.790979'),(15,'strategic_planning','0001_initial','2024-11-25 11:45:32.904240'),(16,'admin','0001_initial','2024-11-25 11:45:33.112754'),(17,'admin','0002_logentry_remove_auto_add','2024-11-25 11:45:33.131533'),(18,'admin','0003_logentry_add_action_flag_choices','2024-11-25 11:45:33.155720'),(19,'sessions','0001_initial','2024-11-25 11:45:33.206537'),(20,'strategic_planning','0002_auto_20241125_1410','2024-11-25 12:18:39.132084'),(21,'strategic_planning','0003_alter_report_actual_spent_alter_report_goal_score_and_more','2024-11-26 14:23:08.537467'),(22,'strategic_planning','0004_alter_report_goal_score','2024-11-26 14:43:12.684128'),(23,'strategic_planning','0005_remove_report_status_activity_status','2024-11-29 12:47:05.267881'),(24,'strategic_planning','0006_activity_designation','2024-12-01 06:52:33.208060'),(25,'strategic_planning','0007_remove_user_designation_user_designation','2024-12-06 08:28:31.549899'),(26,'strategic_planning','0002_initial_load_data','2024-12-08 11:59:50.185426'),(27,'strategic_planning','0003_remove_user_dob','2025-02-26 20:24:48.308712');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('14fi5ooxhqw97kv6la4gu258x2cplunk','.eJxVjE0OwiAYBe_C2hAEgeLSfc9Avh-QqoGktCvj3W2TLnT7Zua9RYR1KXHtaY4Ti6sw4vS7IdAz1R3wA-q9SWp1mSeUuyIP2uXYOL1uh_t3UKCXrSbtbAZGQ4za-mBSSCZovuRssqXgENlCcjhs1FNQw9loVsp6xYpQi88XBHE4NA:1tjMwu:ty-bIapo7GFxflCBYACe2jX9oJdxAMArR88dls5cSvc','2025-03-01 18:31:32.674418'),('1mcdev4wmh94rag77xvtok01dmkscs76','.eJxVjM0OwiAQhN-FsyH8bEE8evcZyMIuUjU0Ke3J-O62SQ86x_m-mbeIuC41rp3nOJK4CBCn3y5hfnLbAT2w3SeZp7bMY5K7Ig_a5W0ifl0P9--gYq_bGtlRNoNWeguYzBYsIYAzmkMBHoIvQStnAwY2njJBUUmdtbK-WG3F5wvLcjcA:1tnNQK:DbLhV_CFwvCKZoCPCuSLUInhVslgTcuWwWwTLfn8Cjw','2025-03-12 19:50:28.495142'),('7hv74losj9hz19gjnfnwk1sfjn2mrynj','.eJxVjMsOwiAQRf-FtSEMrwku3fsNZICpVA0kpV0Z_12bdKHbe865LxFpW2vcBi9xLuIsQJx-t0T5wW0H5U7t1mXubV3mJHdFHnTIay_8vBzu30GlUb-19in4AsRgs6WgNBqLKShHxvCkk0ZGqxgL-wm1K-A9ZgCHyMkjOPH-AM3ANxY:1tI8tU:IgB7NIKE6JFqEpkXVy99aUBX3yxb73HbtkZsZtW8HKY','2024-12-16 16:03:28.801371'),('aju5dsa2xt7lgnk2pwvah98lp6yr5jqx','.eJxVjEEOwiAQRe_C2pABSgGX7j0DgRlGqoYmpV0Z765NutDtf-_9l4hpW2vcelniROIsjDj9bjnho7Qd0D212yxxbusyZbkr8qBdXmcqz8vh_h3U1Ou3hoBsUWvLlDNYxY5QjaMPbAJYUko5XQZjBo8A2jBpnzEAofPIwSfx_gDaVzel:1tG1PV:wCyQ_J3ADB2Sjezgh3vadIWm68CJjf1-gQIzqBzVHGI','2024-12-10 19:39:45.157102'),('culb20ot1d2g1lq43k6wquhb8mkdxiv4','.eJxVjEEOwiAQRe_C2pABSgGX7j0DgRlGqoYmpV0Z765NutDtf-_9l4hpW2vcelniROIsjDj9bjnho7Qd0D212yxxbusyZbkr8qBdXmcqz8vh_h3U1Ou3hoBsUWvLlDNYxY5QjaMPbAJYUko5XQZjBo8A2jBpnzEAofPIwSfx_gDaVzel:1tHmNc:POABJYpJawnV4o94yfejLmoeJi9CZAunXkKbxaTo57I','2024-12-15 16:01:04.362344'),('hfa4uz6xsa2wxfs52e4c86jz9c0z3h6a','.eJxVjDsOwjAQBe_iGlkY_zaU9Jwh2vV6cQDZUpxUiLtDpBTQvpl5LzXiupRx7XkeJ1ZnZdThdyNMj1w3wHest6ZTq8s8kd4UvdOur43z87K7fwcFe_nW4QiQkAxANhjZOZYYbBy8JOtpQAGDwjFFQQwA1gkwebbmFInZgXp_APH5OIA:1tJTjX:D_z4XY6X3Y1rbctvG2Ib1d6-IQ2tFytIRdFXoiL2454','2024-12-20 08:30:43.652620'),('k33yz76iihvs2u4r337qs3wxa9ciha5v','.eJxVjDsOwyAQRO9CHSEDyy9lep8BwbIEJxGWjF1FuXtsyUXSjea9mTcLcVtr2DotYcrsygS7_HYp4pPaAfIjtvvMcW7rMiV-KPyknY9zptftdP8Oaux1X6s4GKEwgUJDxRgJxSuHvuQknUjWgAdCl6Uug9Xold4jgUoSwDtL7PMF1-U3Ww:1tKG4X:6lMp7hhWWa7-Eg1o697SDjUDmwZE3xwsDJf9GFhCQSI','2024-12-22 12:07:37.553983'),('k6qu3awnmcrxu3emart7kiswpfv2h6u6','.eJxVjDsOwyAQRO9CHSEDyy9lep8BwbIEJxGWjF1FuXtsyUXSjea9mTcLcVtr2DotYcrsygS7_HYp4pPaAfIjtvvMcW7rMiV-KPyknY9zptftdP8Oaux1X6s4GKEwgUJDxRgJxSuHvuQknUjWgAdCl6Uug9Xold4jgUoSwDtL7PMF1-U3Ww:1tnNBm:gHuC8Z6Ffr7qNGFxLHH1BJwMtmcnKTwluvuFqCrlnLs','2025-03-12 19:35:26.081771'),('lei1nlxooi0700ryeyg5qzkxt0rqp4ph','.eJxVjDsOwyAQRO9CHSEDyy9lep8BwbIEJxGWjF1FuXtsyUXSjea9mTcLcVtr2DotYcrsygS7_HYp4pPaAfIjtvvMcW7rMiV-KPyknY9zptftdP8Oaux1X6s4GKEwgUJDxRgJxSuHvuQknUjWgAdCl6Uug9Xold4jgUoSwDtL7PMF1-U3Ww:1tMrgm:61cdineT0JHEyb629yQ-MWAvkGYj8GF9nAs6IxlbkQc','2024-12-29 16:41:52.809766'),('resv21kw6yslfis6pgyn9ljmzefu8esf','.eJxVjE0OwiAYBe_C2hAEgeLSfc9Avh-QqoGktCvj3W2TLnT7Zua9RYR1KXHtaY4Ti6sw4vS7IdAz1R3wA-q9SWp1mSeUuyIP2uXYOL1uh_t3UKCXrSbtbAZGQ4za-mBSSCZovuRssqXgENlCcjhs1FNQw9loVsp6xYpQi88XBHE4NA:1tnNSe:xBPPSLJFQNa7tmVHuemoSVyMJc1H7Fu2ylR_An_4Ekk','2025-03-12 19:52:52.579428'),('sfxna5v98adzt85qjkan14vea2luczfq','.eJxVjE0OwiAYBe_C2hAECsWl-56BfD8gVQNJaVfGu2uTLnT7Zua9RIRtLXHraYkzi4vQ4vS7IdAj1R3wHeqtSWp1XWaUuyIP2uXUOD2vh_t3UKCXb-3Z8pAtaJeDzhAUk1FBOTLeodWAxhuvCZOxzlkf6BxGQpUD5YFwNOL9AeF-N98:1tIvhL:2XiiOiqlN44Pd1NDhE1YR_KSuR79IHU9e0HPM_krD5g','2024-12-18 20:10:11.832444'),('tvq81hndvn2ut1162gpm1r2ribhm3clp','.eJxVjE0OwiAYBe_C2hAEgeLSfc9Avh-QqoGktCvj3W2TLnT7Zua9RYR1KXHtaY4Ti6sw4vS7IdAz1R3wA-q9SWp1mSeUuyIP2uXYOL1uh_t3UKCXrSbtbAZGQ4za-mBSSCZovuRssqXgENlCcjhs1FNQw9loVsp6xYpQi88XBHE4NA:1tKdEl:h8CO_6I6Lr1XySkK7huqsNv8T4ndmcNMK7_-487B2PI','2024-12-23 12:51:43.404153'),('xuu8741s6o95872q8lm7tfv2hkz82hgh','.eJxVjM0OwiAQhN-FsyH8bEE8evcZyMIuUjU0Ke3J-O62SQ86x_m-mbeIuC41rp3nOJK4CBCn3y5hfnLbAT2w3SeZp7bMY5K7Ig_a5W0ifl0P9--gYq_bGtlRNoNWeguYzBYsIYAzmkMBHoIvQStnAwY2njJBUUmdtbK-WG3F5wvLcjcA:1tMrNG:OeYfYnjw93ZJme87SaJvq2OKC3yTNtbVFTHzDKmhr_w','2024-12-29 16:21:42.575632'),('yoacbud4ivlolzvta3xjoc9fu57ov1q5','.eJxVjDsOwjAQBe_iGlkY_zaU9Jwh2vV6cQDZUpxUiLtDpBTQvpl5LzXiupRx7XkeJ1ZnZdThdyNMj1w3wHest6ZTq8s8kd4UvdOur43z87K7fwcFe_nW4QiQkAxANhjZOZYYbBy8JOtpQAGDwjFFQQwA1gkwebbmFInZgXp_APH5OIA:1tJT0l:-EcnU5YxpI1O-ok3rz3IdJ2ckhbuxcnn1NwuwxcGzTg','2024-12-20 07:44:27.855551');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_activity`
--

DROP TABLE IF EXISTS `strategic_planning_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_activity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  `start_date` date DEFAULT NULL,
  `end_date` date NOT NULL,
  `estimated_amount` decimal(12,2) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `kpi_id` bigint NOT NULL,
  `main_activity_id` bigint DEFAULT NULL,
  `status` int NOT NULL,
  `designation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_a_created_by_id_fc60ddc3_fk_strategic` (`created_by_id`),
  KEY `strategic_planning_a_kpi_id_7f256405_fk_strategic` (`kpi_id`),
  KEY `strategic_planning_a_main_activity_id_452a8d94_fk_strategic` (`main_activity_id`),
  KEY `strategic_planning_a_designation_id_63cc876d_fk_strategic` (`designation_id`),
  CONSTRAINT `strategic_planning_a_created_by_id_fc60ddc3_fk_strategic` FOREIGN KEY (`created_by_id`) REFERENCES `strategic_planning_user` (`id`),
  CONSTRAINT `strategic_planning_a_designation_id_63cc876d_fk_strategic` FOREIGN KEY (`designation_id`) REFERENCES `strategic_planning_designation` (`id`),
  CONSTRAINT `strategic_planning_a_kpi_id_7f256405_fk_strategic` FOREIGN KEY (`kpi_id`) REFERENCES `strategic_planning_kpi` (`id`),
  CONSTRAINT `strategic_planning_a_main_activity_id_452a8d94_fk_strategic` FOREIGN KEY (`main_activity_id`) REFERENCES `strategic_planning_mainactivity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_activity`
--

LOCK TABLES `strategic_planning_activity` WRITE;
/*!40000 ALTER TABLE `strategic_planning_activity` DISABLE KEYS */;
INSERT INTO `strategic_planning_activity` VALUES (1,'2024-11-25 12:37:51.174121','football fundraising','test','2024-11-18','2024-11-27',22009.00,1,1,1,1,NULL),(2,'2024-11-25 12:38:47.331655','Concert','test','2024-11-13','2024-11-05',1124.00,1,1,1,0,NULL),(3,'2024-11-25 19:05:30.480417','sub 1','test','2024-11-20','2024-11-26',20000.00,1,1,2,0,NULL),(4,'2024-11-25 19:06:26.728184','sub-2','test-2','2024-11-13','2024-11-20',2.00,1,1,2,0,NULL),(5,'2024-11-26 14:20:48.310291','sub4','lolem ipsum','2024-11-14','2024-11-23',23334.00,1,4,3,0,NULL),(6,'2024-11-26 14:21:09.869167','sub5','test',NULL,'2024-11-14',2233.00,1,4,3,0,NULL),(7,'2024-11-27 06:37:31.998890','sub-kpi3-1','test','2024-11-28','2024-11-28',500.00,1,5,4,0,NULL),(8,'2024-11-27 06:38:04.516828','sub-kpi3-2','test',NULL,'2024-11-30',34.00,1,5,4,0,NULL),(9,'2024-11-28 18:30:17.611885','this is a sub activity','this is a sub activity','2024-11-21','2024-11-27',3300.00,3,3,5,0,NULL),(10,'2024-11-28 19:08:58.364732','this is a sub activity - 3','this is a sub activity - 3','2024-11-27','2024-11-27',4009.00,3,3,7,0,NULL),(11,'2024-12-01 06:59:43.223572','Invite gaither to visit main church','hello','2024-12-30','2025-01-01',20000.00,3,3,8,1,2),(12,'2024-12-01 20:42:29.808942','first activity','second activity','2024-12-28','2024-12-31',2023.00,3,3,9,0,2),(13,'2024-12-01 20:43:47.671746','Acquire more music instruments 2 (Music)','test','2025-01-11','2025-01-10',4030.00,3,3,9,0,2),(14,'2024-12-04 20:11:57.581161','Simbarashe sub activity','test activity','2024-12-12','2024-12-19',23003.00,2,3,10,0,5),(15,'2024-12-04 20:12:41.047584','Simbarashe sub activity 3','this activity is nice','2025-01-23','2025-02-05',3321.00,2,3,10,0,5),(16,'2025-02-26 20:02:12.746285','Sabbath School','qwertyuio','2025-02-27','2025-02-28',2000.00,4,3,13,0,3),(17,'2025-02-26 20:03:03.674470','Plan and Host Spiritual Retreats and Workshops 1','wertyuio','2025-02-27','2025-02-27',4500.00,4,3,13,0,3);
/*!40000 ALTER TABLE `strategic_planning_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_designation`
--

DROP TABLE IF EXISTS `strategic_planning_designation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_designation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_designation`
--

LOCK TABLES `strategic_planning_designation` WRITE;
/*!40000 ALTER TABLE `strategic_planning_designation` DISABLE KEYS */;
INSERT INTO `strategic_planning_designation` VALUES (1,'2024-11-25 12:18:38.105577','Pastor'),(2,'2024-11-25 15:54:54.095941','Technical'),(3,'2024-11-26 13:57:08.815439','Music'),(4,'2024-11-26 13:57:19.244958','SOP'),(5,'2024-11-26 13:57:34.446132','Sabbath School'),(6,'2024-12-08 11:59:48.160881','SPEMEC');
/*!40000 ALTER TABLE `strategic_planning_designation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_kpi`
--

DROP TABLE IF EXISTS `strategic_planning_kpi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_kpi` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `strategic_objective_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_k_strategic_objective__72139120_fk_strategic` (`strategic_objective_id`),
  KEY `strategic_planning_k_created_by_id_c68314a1_fk_strategic` (`created_by_id`),
  CONSTRAINT `strategic_planning_k_created_by_id_c68314a1_fk_strategic` FOREIGN KEY (`created_by_id`) REFERENCES `strategic_planning_user` (`id`),
  CONSTRAINT `strategic_planning_k_strategic_objective__72139120_fk_strategic` FOREIGN KEY (`strategic_objective_id`) REFERENCES `strategic_planning_strategicobjective` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_kpi`
--

LOCK TABLES `strategic_planning_kpi` WRITE;
/*!40000 ALTER TABLE `strategic_planning_kpi` DISABLE KEYS */;
INSERT INTO `strategic_planning_kpi` VALUES (1,'2024-11-25 12:36:05.123132','Acquire more music instruments (Music)',1,1),(2,'2024-11-25 18:59:33.729031','second kpi',1,1),(3,'2024-11-26 14:17:55.603956','kpi1',1,4),(4,'2024-11-26 14:18:13.277476','kpi2',1,5),(5,'2024-11-26 14:18:42.179448','kpi3',1,3),(6,'2024-11-26 14:19:09.682658','kpi5',1,3),(7,'2025-02-26 22:04:32.598982','100% up',1,1),(8,'2025-02-26 22:41:01.157127','Increase # by 20',1,3),(9,'2025-02-26 22:41:01.165310','Increase # by 40',1,3);
/*!40000 ALTER TABLE `strategic_planning_kpi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_mainactivity`
--

DROP TABLE IF EXISTS `strategic_planning_mainactivity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_mainactivity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  `created_by_id` bigint DEFAULT NULL,
  `kpi_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_m_created_by_id_cc0d4c0b_fk_strategic` (`created_by_id`),
  KEY `strategic_planning_m_kpi_id_2b9e7681_fk_strategic` (`kpi_id`),
  CONSTRAINT `strategic_planning_m_created_by_id_cc0d4c0b_fk_strategic` FOREIGN KEY (`created_by_id`) REFERENCES `strategic_planning_user` (`id`),
  CONSTRAINT `strategic_planning_m_kpi_id_2b9e7681_fk_strategic` FOREIGN KEY (`kpi_id`) REFERENCES `strategic_planning_kpi` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_mainactivity`
--

LOCK TABLES `strategic_planning_mainactivity` WRITE;
/*!40000 ALTER TABLE `strategic_planning_mainactivity` DISABLE KEYS */;
INSERT INTO `strategic_planning_mainactivity` VALUES (1,'2024-11-25 12:37:10.819217','Construction','test',1,1),(2,'2024-11-25 19:04:36.370690','main','main-d',1,1),(3,'2024-11-26 14:19:39.410657','main1','test',1,4),(4,'2024-11-27 06:30:35.727675','kpi3 main','try it out',1,5),(5,'2024-11-28 18:29:25.927122','this is a main activity','this is a main activity',3,3),(6,'2024-11-28 18:32:46.870596','this is a main activity 2','this is a main activity',3,3),(7,'2024-11-28 19:07:39.236013','this is a main activity 3','test',3,3),(8,'2024-12-01 06:58:07.445391','Music day','promotions',3,3),(9,'2024-12-01 20:41:45.250229','start again','lets do this',3,3),(10,'2024-12-04 20:11:24.808511','Simbarashe activity','okay',2,3),(11,'2024-12-04 20:44:33.124281','Simbarashe second main activity','',2,3),(12,'2024-12-09 12:51:58.765697','Construction','werw',3,3),(13,'2025-02-26 20:01:25.403824','Retreats and Workshops','qwertyuiop[',4,3);
/*!40000 ALTER TABLE `strategic_planning_mainactivity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_report`
--

DROP TABLE IF EXISTS `strategic_planning_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_date` date DEFAULT NULL,
  `goal_score` varchar(20) NOT NULL,
  `report_details` longtext NOT NULL,
  `actual_spent` decimal(12,2) NOT NULL,
  `activity_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_r_activity_id_2ae5c2c4_fk_strategic` (`activity_id`),
  KEY `strategic_planning_r_designation_id_b239278f_fk_strategic` (`designation_id`),
  KEY `strategic_planning_r_user_id_497bdc1b_fk_strategic` (`user_id`),
  CONSTRAINT `strategic_planning_r_activity_id_2ae5c2c4_fk_strategic` FOREIGN KEY (`activity_id`) REFERENCES `strategic_planning_activity` (`id`),
  CONSTRAINT `strategic_planning_r_designation_id_b239278f_fk_strategic` FOREIGN KEY (`designation_id`) REFERENCES `strategic_planning_designation` (`id`),
  CONSTRAINT `strategic_planning_r_user_id_497bdc1b_fk_strategic` FOREIGN KEY (`user_id`) REFERENCES `strategic_planning_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_report`
--

LOCK TABLES `strategic_planning_report` WRITE;
/*!40000 ALTER TABLE `strategic_planning_report` DISABLE KEYS */;
INSERT INTO `strategic_planning_report` VALUES (1,'2024-11-06','1-49','test',1223.00,1,1,1),(2,'2024-11-28','100','des',22220.00,2,1,1),(3,'2024-11-14','Progressing','this is a gazzel',2233.00,3,1,1),(4,'2024-11-30','No Activity','try again',2560.00,4,1,1),(5,'2024-11-29','orange','okay',220.00,5,1,1),(6,'2024-11-28','green','ss',20.00,6,1,1),(7,'2024-11-29','orange','test',798.00,7,1,1),(8,'2024-11-29','red','test',0.00,8,1,1),(9,'2024-11-27','green','this a descriptionof the',3000.00,9,2,3),(10,NULL,'','',0.00,10,2,3),(11,'2024-11-27','orange','test',100.00,1,2,3),(12,'2025-02-28','green','wertyu',5500.00,11,2,3);
/*!40000 ALTER TABLE `strategic_planning_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_role`
--

DROP TABLE IF EXISTS `strategic_planning_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_role`
--

LOCK TABLES `strategic_planning_role` WRITE;
/*!40000 ALTER TABLE `strategic_planning_role` DISABLE KEYS */;
INSERT INTO `strategic_planning_role` VALUES (1,'Admin'),(2,'HOD'),(3,'Elder');
/*!40000 ALTER TABLE `strategic_planning_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_strategicobjective`
--

DROP TABLE IF EXISTS `strategic_planning_strategicobjective`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_strategicobjective` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `objective_name` varchar(200) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `strategic_theme_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_s_strategic_theme_id_16804281_fk_strategic` (`strategic_theme_id`),
  KEY `strategic_planning_s_created_by_id_b3e619e7_fk_strategic` (`created_by_id`),
  CONSTRAINT `strategic_planning_s_created_by_id_b3e619e7_fk_strategic` FOREIGN KEY (`created_by_id`) REFERENCES `strategic_planning_user` (`id`),
  CONSTRAINT `strategic_planning_s_strategic_theme_id_16804281_fk_strategic` FOREIGN KEY (`strategic_theme_id`) REFERENCES `strategic_planning_strategictheme` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_strategicobjective`
--

LOCK TABLES `strategic_planning_strategicobjective` WRITE;
/*!40000 ALTER TABLE `strategic_planning_strategicobjective` DISABLE KEYS */;
INSERT INTO `strategic_planning_strategicobjective` VALUES (1,'2024-11-25 12:35:43.394089','Faithfulness in stewardship',1,1),(2,'2024-11-25 18:58:17.267357','Faithfulness in Family life',1,1),(3,'2024-11-25 19:01:11.230941','Build Church',1,1),(4,'2024-11-26 14:01:47.082599','objective 10',1,2),(5,'2024-11-26 14:02:31.750025','objective 11',1,2);
/*!40000 ALTER TABLE `strategic_planning_strategicobjective` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_strategicobjective_designation`
--

DROP TABLE IF EXISTS `strategic_planning_strategicobjective_designation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_strategicobjective_designation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `strategicobjective_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `strategic_planning_strat_strategicobjective_id_de_87c9febb_uniq` (`strategicobjective_id`,`designation_id`),
  KEY `strategic_planning_s_designation_id_a628b708_fk_strategic` (`designation_id`),
  CONSTRAINT `strategic_planning_s_designation_id_a628b708_fk_strategic` FOREIGN KEY (`designation_id`) REFERENCES `strategic_planning_designation` (`id`),
  CONSTRAINT `strategic_planning_s_strategicobjective_i_ba3d6df0_fk_strategic` FOREIGN KEY (`strategicobjective_id`) REFERENCES `strategic_planning_strategicobjective` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_strategicobjective_designation`
--

LOCK TABLES `strategic_planning_strategicobjective_designation` WRITE;
/*!40000 ALTER TABLE `strategic_planning_strategicobjective_designation` DISABLE KEYS */;
INSERT INTO `strategic_planning_strategicobjective_designation` VALUES (1,1,1),(2,2,2),(3,3,1),(4,4,2),(6,4,3),(5,4,5),(7,5,1),(8,5,3);
/*!40000 ALTER TABLE `strategic_planning_strategicobjective_designation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_strategictheme`
--

DROP TABLE IF EXISTS `strategic_planning_strategictheme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_strategictheme` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` datetime(6) NOT NULL,
  `theme_name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `strategic_planning_s_created_by_id_43993d4f_fk_strategic` (`created_by_id`),
  CONSTRAINT `strategic_planning_s_created_by_id_43993d4f_fk_strategic` FOREIGN KEY (`created_by_id`) REFERENCES `strategic_planning_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_strategictheme`
--

LOCK TABLES `strategic_planning_strategictheme` WRITE;
/*!40000 ALTER TABLE `strategic_planning_strategictheme` DISABLE KEYS */;
INSERT INTO `strategic_planning_strategictheme` VALUES (1,'2024-11-25 12:21:30.606510','Spiritual Growth','test',NULL),(2,'2024-11-25 18:56:37.909320','Mission','test',NULL),(3,'2024-11-27 14:01:51.161093','Theme3','explanation',NULL);
/*!40000 ALTER TABLE `strategic_planning_strategictheme` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_user`
--

DROP TABLE IF EXISTS `strategic_planning_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `password` varchar(128) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `physical_address` longtext NOT NULL,
  `last_logged_in` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `strategic_planning_u_role_id_69417c8c_fk_strategic` (`role_id`),
  CONSTRAINT `strategic_planning_u_role_id_69417c8c_fk_strategic` FOREIGN KEY (`role_id`) REFERENCES `strategic_planning_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_user`
--

LOCK TABLES `strategic_planning_user` WRITE;
/*!40000 ALTER TABLE `strategic_planning_user` DISABLE KEYS */;
INSERT INTO `strategic_planning_user` VALUES (1,'2025-02-26 19:35:26.072085',1,'Admin','User','pbkdf2_sha256$870000$TKmmEWAKGYyi6Ty8R26gKv$D0PeefwodnLWHSdpIHoYA7sUcgd/WrOXHh/GF1ToYmQ=','1234567890','admin@gmail.com','Admin Address',NULL,1,1,1),(2,'2024-12-04 20:10:11.828440',0,'Simbarashe','Kapundu','pbkdf2_sha256$720000$Zu7QDVx6kLUVmdj8OiHH0m$ldOj/xjJRUK5CkOS1fQ5qFvoGR0heYLuEJFzUku/Vnw=','0989987678','simbarashekapundu@gmail.com','Valley view 156\r\nwatch tower',NULL,1,0,2),(3,'2025-02-26 19:52:52.574040',0,'boy','zulu','pbkdf2_sha256$870000$L7Eom5p3ixcsIT9jF6HEqD$1d63IK1NpA44RWesjaZuOHTrZOParwHMC9fCEwpRKHo=','0989987678','zulu@gmail.com','Valley view 156\r\nwatch tower',NULL,1,0,2),(4,'2025-02-26 19:50:28.488440',0,'simba','simba','pbkdf2_sha256$870000$HzcSX2r8LAE0rEQP23SN5u$3CkP9AOXg7P/KsnJyShyK0jE5caAcQe6Y94Wgq+/C6o=','12132424','simba@gmail.com','12eweqe',NULL,1,0,2),(5,'2025-02-15 18:29:17.559561',0,'joseph','Chipate','pbkdf2_sha256$870000$DapHD0rwiFwXNPMnclGPeT$X2gCKXQsqrDQHc004dfAC4DHQUP3sn8cTl2OUnzzS6g=','0978877888','joseph@gmail.com','qwerty',NULL,1,0,3),(6,NULL,0,'Tumelo','Kapundu','pbkdf2_sha256$870000$BI4s4Ljfiq0nu2BdIfDd88$sMA9wlUO6qZUqh8LG7Aopfl0eXt29tdxzf0jlAd4rUI=','0989987678','melo@gmail.com','Valley view 156\r\nwatch tower',NULL,1,0,2);
/*!40000 ALTER TABLE `strategic_planning_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_user_designation`
--

DROP TABLE IF EXISTS `strategic_planning_user_designation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_user_designation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `designation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `strategic_planning_user__user_id_designation_id_7b657f7d_uniq` (`user_id`,`designation_id`),
  KEY `strategic_planning_u_designation_id_bdb4fb96_fk_strategic` (`designation_id`),
  CONSTRAINT `strategic_planning_u_designation_id_bdb4fb96_fk_strategic` FOREIGN KEY (`designation_id`) REFERENCES `strategic_planning_designation` (`id`),
  CONSTRAINT `strategic_planning_u_user_id_3930d6d6_fk_strategic` FOREIGN KEY (`user_id`) REFERENCES `strategic_planning_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_user_designation`
--

LOCK TABLES `strategic_planning_user_designation` WRITE;
/*!40000 ALTER TABLE `strategic_planning_user_designation` DISABLE KEYS */;
INSERT INTO `strategic_planning_user_designation` VALUES (1,1,1),(2,3,2),(3,4,3),(4,5,2),(5,5,3),(6,5,4),(7,6,4);
/*!40000 ALTER TABLE `strategic_planning_user_designation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_user_groups`
--

DROP TABLE IF EXISTS `strategic_planning_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `strategic_planning_user_groups_user_id_group_id_edf56815_uniq` (`user_id`,`group_id`),
  KEY `strategic_planning_u_group_id_b52bed95_fk_auth_grou` (`group_id`),
  CONSTRAINT `strategic_planning_u_group_id_b52bed95_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `strategic_planning_u_user_id_3ef2910e_fk_strategic` FOREIGN KEY (`user_id`) REFERENCES `strategic_planning_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_user_groups`
--

LOCK TABLES `strategic_planning_user_groups` WRITE;
/*!40000 ALTER TABLE `strategic_planning_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `strategic_planning_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strategic_planning_user_user_permissions`
--

DROP TABLE IF EXISTS `strategic_planning_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `strategic_planning_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `strategic_planning_user__user_id_permission_id_4731c9e1_uniq` (`user_id`,`permission_id`),
  KEY `strategic_planning_u_permission_id_e7c46d55_fk_auth_perm` (`permission_id`),
  CONSTRAINT `strategic_planning_u_permission_id_e7c46d55_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `strategic_planning_u_user_id_d27a21ef_fk_strategic` FOREIGN KEY (`user_id`) REFERENCES `strategic_planning_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strategic_planning_user_user_permissions`
--

LOCK TABLES `strategic_planning_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `strategic_planning_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `strategic_planning_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-03 13:34:18
