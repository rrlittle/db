-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: jamesli_db
-- ------------------------------------------------------
-- Server version	5.7.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add group',4,'add_group'),(11,'Can change group',4,'change_group'),(12,'Can delete group',4,'delete_group'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add choice',7,'add_choice'),(20,'Can change choice',7,'change_choice'),(21,'Can delete choice',7,'delete_choice'),(22,'Can add survey',8,'add_survey'),(23,'Can change survey',8,'change_survey'),(24,'Can delete survey',8,'delete_survey'),(25,'Can add question',9,'add_question'),(26,'Can change question',9,'change_question'),(27,'Can delete question',9,'delete_question'),(31,'Can add answer',11,'add_answer'),(32,'Can change answer',11,'change_answer'),(33,'Can delete answer',11,'delete_answer'),(34,'Can add person',12,'add_person'),(35,'Can change person',12,'change_person'),(36,'Can delete person',12,'delete_person'),(40,'Can add measure',14,'add_measure'),(41,'Can change measure',14,'change_measure'),(42,'Can delete measure',14,'delete_measure'),(43,'Can add relation',15,'add_relation'),(44,'Can change relation',15,'change_relation'),(45,'Can delete relation',15,'delete_relation'),(46,'Can add source choice',16,'add_sourcechoice'),(47,'Can change source choice',16,'change_sourcechoice'),(48,'Can delete source choice',16,'delete_sourcechoice'),(49,'Can add survey question',17,'add_surveyquestion'),(50,'Can change survey question',17,'change_surveyquestion'),(51,'Can delete survey question',17,'delete_surveyquestion'),(52,'Can add choice group',18,'add_choicegroup'),(53,'Can change choice group',18,'change_choicegroup'),(54,'Can delete choice group',18,'delete_choicegroup'),(55,'Can add source scheme',19,'add_sourcescheme'),(56,'Can change source scheme',19,'change_sourcescheme'),(57,'Can delete source scheme',19,'delete_sourcescheme'),(58,'Can add kwargs',20,'add_kwargs'),(59,'Can change kwargs',20,'change_kwargs'),(60,'Can delete kwargs',20,'delete_kwargs'),(61,'Can add source column',21,'add_sourcecolumn'),(62,'Can change source column',21,'change_sourcecolumn'),(63,'Can delete source column',21,'delete_sourcecolumn'),(64,'Can add source question',22,'add_sourcequestion'),(65,'Can change source question',22,'change_sourcequestion'),(66,'Can delete source question',22,'delete_sourcequestion');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$30000$YKsHhCLuEo21$9wCB9Yu/5JE7OK4uDqy72JLuDb/6dJOM2zwFh2kfGy0=','2016-11-29 18:27:57',1,'russell','','','rrlittle2@gmail.com',1,1,'2016-09-16 19:10:06');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_answer`
--

DROP TABLE IF EXISTS `db_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_answer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_of_response` date NOT NULL,
  `int_response` int(11) DEFAULT NULL,
  `float_response` double DEFAULT NULL,
  `date_response` date DEFAULT NULL,
  `boolean_response` tinyint(1) DEFAULT NULL,
  `text_response` varchar(60) DEFAULT NULL,
  `answer_id` int(11) NOT NULL,
  `respondent_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `surveyQuestion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_answer_fb12e902` (`answer_id`),
  KEY `db_answer_86c98acb` (`respondent_id`),
  KEY `db_answer_ffaba1d1` (`subject_id`),
  KEY `db_answer_42b588d6` (`surveyQuestion_id`),
  CONSTRAINT `db_answer_answer_id_b17abf37_fk_db_choice_id` FOREIGN KEY (`answer_id`) REFERENCES `db_choice` (`id`),
  CONSTRAINT `db_answer_respondent_id_a1cb26b6_fk_db_person_id` FOREIGN KEY (`respondent_id`) REFERENCES `db_person` (`id`),
  CONSTRAINT `db_answer_subject_id_ba0690c9_fk_db_person_id` FOREIGN KEY (`subject_id`) REFERENCES `db_person` (`id`),
  CONSTRAINT `db_answer_surveyQuestion_id_d8db970c_fk_db_surveyquestion_id` FOREIGN KEY (`surveyQuestion_id`) REFERENCES `db_surveyquestion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_answer`
--

LOCK TABLES `db_answer` WRITE;
/*!40000 ALTER TABLE `db_answer` DISABLE KEYS */;
INSERT INTO `db_answer` VALUES (1,'2016-11-15',1,NULL,NULL,NULL,NULL,1,1,1,1);
/*!40000 ALTER TABLE `db_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_choice`
--

DROP TABLE IF EXISTS `db_choice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `order` int(11) DEFAULT NULL,
  `show_name` tinyint(1) NOT NULL,
  `allow_custom_responses` tinyint(1) NOT NULL,
  `default_boolean_resp` tinyint(1) DEFAULT NULL,
  `default_date_resp` date DEFAULT NULL,
  `default_text_resp` varchar(60) DEFAULT NULL,
  `default_int_resp` int(11) DEFAULT NULL,
  `default_float_resp` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_choice`
--

LOCK TABLES `db_choice` WRITE;
/*!40000 ALTER TABLE `db_choice` DISABLE KEYS */;
INSERT INTO `db_choice` VALUES (1,'good',1,1,0,NULL,NULL,'',1,NULL),(2,'not good',2,1,0,NULL,NULL,'',-1,NULL);
/*!40000 ALTER TABLE `db_choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_choicegroup`
--

DROP TABLE IF EXISTS `db_choicegroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_choicegroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `ui` varchar(20) NOT NULL,
  `datatype` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_choicegroup`
--

LOCK TABLES `db_choicegroup` WRITE;
/*!40000 ALTER TABLE `db_choicegroup` DISABLE KEYS */;
INSERT INTO `db_choicegroup` VALUES (1,'good/not','check','int');
/*!40000 ALTER TABLE `db_choicegroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_choicegroup_choices`
--

DROP TABLE IF EXISTS `db_choicegroup_choices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_choicegroup_choices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choicegroup_id` int(11) NOT NULL,
  `choice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_choicegroup_choices_choicegroup_id_dd608d3a_uniq` (`choicegroup_id`,`choice_id`),
  KEY `db_choicegroup_choices_choice_id_594f9137_fk_db_choice_id` (`choice_id`),
  CONSTRAINT `db_choicegroup_choi_choicegroup_id_d84d4ba8_fk_db_choicegroup_id` FOREIGN KEY (`choicegroup_id`) REFERENCES `db_choicegroup` (`id`),
  CONSTRAINT `db_choicegroup_choices_choice_id_594f9137_fk_db_choice_id` FOREIGN KEY (`choice_id`) REFERENCES `db_choice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_choicegroup_choices`
--

LOCK TABLES `db_choicegroup_choices` WRITE;
/*!40000 ALTER TABLE `db_choicegroup_choices` DISABLE KEYS */;
INSERT INTO `db_choicegroup_choices` VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `db_choicegroup_choices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_kwargs`
--

DROP TABLE IF EXISTS `db_kwargs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_kwargs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `value` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_kwargs`
--

LOCK TABLES `db_kwargs` WRITE;
/*!40000 ALTER TABLE `db_kwargs` DISABLE KEYS */;
/*!40000 ALTER TABLE `db_kwargs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_measure`
--

DROP TABLE IF EXISTS `db_measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_measure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_measure`
--

LOCK TABLES `db_measure` WRITE;
/*!40000 ALTER TABLE `db_measure` DISABLE KEYS */;
/*!40000 ALTER TABLE `db_measure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_person`
--

DROP TABLE IF EXISTS `db_person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(60) NOT NULL,
  `lastName` varchar(60) NOT NULL,
  `birthdate` date NOT NULL,
  `studyid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `studyid` (`studyid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_person`
--

LOCK TABLES `db_person` WRITE;
/*!40000 ALTER TABLE `db_person` DISABLE KEYS */;
INSERT INTO `db_person` VALUES (1,'rus','L','2016-11-15',3),(2,'kjsdlafjd','asfjlasdkfj','2016-11-29',1),(3,'assafsdfsadfs','sadfasfsafas','2016-11-29',2),(4,'asfsfasfsdf','asdfsdfsf','2016-11-29',4);
/*!40000 ALTER TABLE `db_person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_question`
--

DROP TABLE IF EXISTS `db_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(60) NOT NULL,
  `prompt` varchar(200) NOT NULL,
  `allow_multiple_responses` tinyint(1) NOT NULL,
  `missing_value_int` int(11) DEFAULT NULL,
  `missing_value_float` double DEFAULT NULL,
  `missing_value_boolean` tinyint(1) DEFAULT NULL,
  `missing_value_date` date DEFAULT NULL,
  `missing_value_text` varchar(60) DEFAULT NULL,
  `choiceGroup_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_question_choiceGroup_id_9dcd4195_fk_db_choicegroup_id` (`choiceGroup_id`),
  CONSTRAINT `db_question_choiceGroup_id_9dcd4195_fk_db_choicegroup_id` FOREIGN KEY (`choiceGroup_id`) REFERENCES `db_choicegroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_question`
--

LOCK TABLES `db_question` WRITE;
/*!40000 ALTER TABLE `db_question` DISABLE KEYS */;
INSERT INTO `db_question` VALUES (1,'day','How is Your day?',0,999,NULL,NULL,NULL,'',1);
/*!40000 ALTER TABLE `db_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_relation`
--

DROP TABLE IF EXISTS `db_relation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_relation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `relation` varchar(20) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `to_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_relation_subject_id_717e0481_fk_db_person_id` (`subject_id`),
  KEY `db_relation_to_id_974914cd_fk_db_person_id` (`to_id`),
  CONSTRAINT `db_relation_subject_id_717e0481_fk_db_person_id` FOREIGN KEY (`subject_id`) REFERENCES `db_person` (`id`),
  CONSTRAINT `db_relation_to_id_974914cd_fk_db_person_id` FOREIGN KEY (`to_id`) REFERENCES `db_person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_relation`
--

LOCK TABLES `db_relation` WRITE;
/*!40000 ALTER TABLE `db_relation` DISABLE KEYS */;
/*!40000 ALTER TABLE `db_relation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcechoice`
--

DROP TABLE IF EXISTS `db_sourcechoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcechoice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(60) NOT NULL,
  `equivalent_choice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_sourcechoice_equivalent_choice_id_b72393a0_fk_db_choice_id` (`equivalent_choice_id`),
  CONSTRAINT `db_sourcechoice_equivalent_choice_id_b72393a0_fk_db_choice_id` FOREIGN KEY (`equivalent_choice_id`) REFERENCES `db_choice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcechoice`
--

LOCK TABLES `db_sourcechoice` WRITE;
/*!40000 ALTER TABLE `db_sourcechoice` DISABLE KEYS */;
INSERT INTO `db_sourcechoice` VALUES (1,'well',1),(2,'0',2);
/*!40000 ALTER TABLE `db_sourcechoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcecolumn`
--

DROP TABLE IF EXISTS `db_sourcecolumn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcecolumn` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `column_header` varchar(200) NOT NULL,
  `missing_value` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcecolumn`
--

LOCK TABLES `db_sourcecolumn` WRITE;
/*!40000 ALTER TABLE `db_sourcecolumn` DISABLE KEYS */;
INSERT INTO `db_sourcecolumn` VALUES (1,'q1','999');
/*!40000 ALTER TABLE `db_sourcecolumn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcecolumn_valid_values`
--

DROP TABLE IF EXISTS `db_sourcecolumn_valid_values`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcecolumn_valid_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sourcecolumn_id` int(11) NOT NULL,
  `sourcechoice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_sourcecolumn_valid_values_sourcecolumn_id_2f961b4e_uniq` (`sourcecolumn_id`,`sourcechoice_id`),
  KEY `db_sourcecolumn_v_sourcechoice_id_5243d2a3_fk_db_sourcechoice_id` (`sourcechoice_id`),
  CONSTRAINT `db_sourcecolumn_v_sourcechoice_id_5243d2a3_fk_db_sourcechoice_id` FOREIGN KEY (`sourcechoice_id`) REFERENCES `db_sourcechoice` (`id`),
  CONSTRAINT `db_sourcecolumn_v_sourcecolumn_id_e7edeb7d_fk_db_sourcecolumn_id` FOREIGN KEY (`sourcecolumn_id`) REFERENCES `db_sourcecolumn` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcecolumn_valid_values`
--

LOCK TABLES `db_sourcecolumn_valid_values` WRITE;
/*!40000 ALTER TABLE `db_sourcecolumn_valid_values` DISABLE KEYS */;
INSERT INTO `db_sourcecolumn_valid_values` VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `db_sourcecolumn_valid_values` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcequestion`
--

DROP TABLE IF EXISTS `db_sourcequestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcequestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `analysis_func` varchar(80) DEFAULT NULL,
  `question_equivalent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_sourcequestion_8bdabf0d` (`question_equivalent_id`),
  CONSTRAINT `db_sourcequest_question_equivalent_id_fc2878ca_fk_db_question_id` FOREIGN KEY (`question_equivalent_id`) REFERENCES `db_question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcequestion`
--

LOCK TABLES `db_sourcequestion` WRITE;
/*!40000 ALTER TABLE `db_sourcequestion` DISABLE KEYS */;
INSERT INTO `db_sourcequestion` VALUES (1,'',1);
/*!40000 ALTER TABLE `db_sourcequestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcequestion_args`
--

DROP TABLE IF EXISTS `db_sourcequestion_args`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcequestion_args` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sourcequestion_id` int(11) NOT NULL,
  `kwargs_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_sourcequestion_args_sourcequestion_id_bbb82481_uniq` (`sourcequestion_id`,`kwargs_id`),
  KEY `db_sourcequestion_args_kwargs_id_ce520efa_fk_db_kwargs_id` (`kwargs_id`),
  CONSTRAINT `db_sourceques_sourcequestion_id_8a305a99_fk_db_sourcequestion_id` FOREIGN KEY (`sourcequestion_id`) REFERENCES `db_sourcequestion` (`id`),
  CONSTRAINT `db_sourcequestion_args_kwargs_id_ce520efa_fk_db_kwargs_id` FOREIGN KEY (`kwargs_id`) REFERENCES `db_kwargs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcequestion_args`
--

LOCK TABLES `db_sourcequestion_args` WRITE;
/*!40000 ALTER TABLE `db_sourcequestion_args` DISABLE KEYS */;
/*!40000 ALTER TABLE `db_sourcequestion_args` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcequestion_source_columns`
--

DROP TABLE IF EXISTS `db_sourcequestion_source_columns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcequestion_source_columns` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sourcequestion_id` int(11) NOT NULL,
  `sourcecolumn_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_sourcequestion_source_columns_sourcequestion_id_f432ce6f_uniq` (`sourcequestion_id`,`sourcecolumn_id`),
  KEY `db_sourcequestion_sourcecolumn_id_4a0c61ce_fk_db_sourcecolumn_id` (`sourcecolumn_id`),
  CONSTRAINT `db_sourceques_sourcequestion_id_9f2ae72a_fk_db_sourcequestion_id` FOREIGN KEY (`sourcequestion_id`) REFERENCES `db_sourcequestion` (`id`),
  CONSTRAINT `db_sourcequestion_sourcecolumn_id_4a0c61ce_fk_db_sourcecolumn_id` FOREIGN KEY (`sourcecolumn_id`) REFERENCES `db_sourcecolumn` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcequestion_source_columns`
--

LOCK TABLES `db_sourcequestion_source_columns` WRITE;
/*!40000 ALTER TABLE `db_sourcequestion_source_columns` DISABLE KEYS */;
INSERT INTO `db_sourcequestion_source_columns` VALUES (1,1,1);
/*!40000 ALTER TABLE `db_sourcequestion_source_columns` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcescheme`
--

DROP TABLE IF EXISTS `db_sourcescheme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcescheme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `survey_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `db_sourcescheme_00b3bd7e` (`survey_id`),
  CONSTRAINT `db_sourcescheme_survey_id_d1dbe231_fk_db_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `db_survey` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcescheme`
--

LOCK TABLES `db_sourcescheme` WRITE;
/*!40000 ALTER TABLE `db_sourcescheme` DISABLE KEYS */;
INSERT INTO `db_sourcescheme` VALUES (1,1,'testimport.csv');
/*!40000 ALTER TABLE `db_sourcescheme` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_sourcescheme_sourcequestions`
--

DROP TABLE IF EXISTS `db_sourcescheme_sourcequestions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_sourcescheme_sourcequestions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sourcescheme_id` int(11) NOT NULL,
  `sourcequestion_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_sourcescheme_sourceQuestions_sourcescheme_id_5f5a1ab6_uniq` (`sourcescheme_id`,`sourcequestion_id`),
  KEY `db_sourcesche_sourcequestion_id_733d1e59_fk_db_sourcequestion_id` (`sourcequestion_id`),
  CONSTRAINT `db_sourcesche_sourcequestion_id_733d1e59_fk_db_sourcequestion_id` FOREIGN KEY (`sourcequestion_id`) REFERENCES `db_sourcequestion` (`id`),
  CONSTRAINT `db_sourcescheme_s_sourcescheme_id_25e4ab99_fk_db_sourcescheme_id` FOREIGN KEY (`sourcescheme_id`) REFERENCES `db_sourcescheme` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_sourcescheme_sourcequestions`
--

LOCK TABLES `db_sourcescheme_sourcequestions` WRITE;
/*!40000 ALTER TABLE `db_sourcescheme_sourcequestions` DISABLE KEYS */;
INSERT INTO `db_sourcescheme_sourcequestions` VALUES (1,1,1);
/*!40000 ALTER TABLE `db_sourcescheme_sourcequestions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_survey`
--

DROP TABLE IF EXISTS `db_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_survey` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) NOT NULL,
  `surveytype` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_survey`
--

LOCK TABLES `db_survey` WRITE;
/*!40000 ALTER TABLE `db_survey` DISABLE KEYS */;
INSERT INTO `db_survey` VALUES (1,'test','self report');
/*!40000 ALTER TABLE `db_survey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db_surveyquestion`
--

DROP TABLE IF EXISTS `db_surveyquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db_surveyquestion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_order` int(10) unsigned NOT NULL,
  `question_id` int(11) NOT NULL,
  `survey_id` int(11) NOT NULL,
  `unit_of_measure_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `db_surveyquestion_survey_id_86ea78c1_uniq` (`survey_id`,`question_order`),
  KEY `db_surveyquestion_question_id_cf8b2ce1_fk_db_question_id` (`question_id`),
  KEY `db_surveyquestion_unit_of_measure_id_2e8afe79_fk_db_measure_id` (`unit_of_measure_id`),
  CONSTRAINT `db_surveyquestion_question_id_cf8b2ce1_fk_db_question_id` FOREIGN KEY (`question_id`) REFERENCES `db_question` (`id`),
  CONSTRAINT `db_surveyquestion_survey_id_fdce4312_fk_db_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `db_survey` (`id`),
  CONSTRAINT `db_surveyquestion_unit_of_measure_id_2e8afe79_fk_db_measure_id` FOREIGN KEY (`unit_of_measure_id`) REFERENCES `db_measure` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db_surveyquestion`
--

LOCK TABLES `db_surveyquestion` WRITE;
/*!40000 ALTER TABLE `db_surveyquestion` DISABLE KEYS */;
INSERT INTO `db_surveyquestion` VALUES (1,0,1,1,NULL);
/*!40000 ALTER TABLE `db_surveyquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-09-16 19:29:31','1','APQ',1,'[{\"added\": {}}]',8,1),(2,'2016-09-16 19:30:15','1','nev, almo nev, som, oft, alw',1,'[{\"added\": {}}]',NULL,1),(3,'2016-09-16 19:30:18','1','you have a friendly chat',1,'[{\"added\": {}}]',9,1),(4,'2016-09-16 19:30:42','1','APQ[1]=>you have a friendly chat',1,'[{\"added\": {}}]',NULL,1),(5,'2016-09-16 19:31:15','2','you let your child know when they are doing a good job',1,'[{\"added\": {}}]',9,1),(6,'2016-09-16 19:31:19','2','APQ[2]=>you let your child know when they are doing a good job',1,'[{\"added\": {}}]',NULL,1),(7,'2016-09-16 19:31:37','1','never',1,'[{\"added\": {}}]',7,1),(8,'2016-09-16 19:31:49','2','almost never',1,'[{\"added\": {}}]',7,1),(9,'2016-09-16 19:32:06','3','sometimes',1,'[{\"added\": {}}]',7,1),(10,'2016-09-16 19:32:16','4','often',1,'[{\"added\": {}}]',7,1),(11,'2016-09-16 19:32:33','5','always',1,'[{\"added\": {}}]',7,1),(12,'2016-09-16 20:31:00','2','favorite foods',1,'[{\"added\": {}}]',NULL,1),(13,'2016-09-16 20:31:45','6','turkey',1,'[{\"added\": {}}]',7,1),(14,'2016-09-16 20:31:54','7','ice cream',1,'[{\"added\": {}}]',7,1),(15,'2016-09-16 20:32:05','8','beer',1,'[{\"added\": {}}]',7,1),(16,'2016-09-16 20:32:32','3','what is your favorite food?',1,'[{\"added\": {}}]',9,1),(17,'2016-09-16 20:32:35','3','APQ[3]=>what is your favorite food?',1,'[{\"added\": {}}]',NULL,1),(18,'2016-09-16 20:32:58','1','russ lil',1,'[{\"added\": {}}]',12,1),(19,'2016-09-16 20:33:12','2','john hopkins',1,'[{\"added\": {}}]',12,1),(20,'2016-09-16 20:33:34','1','foods',1,'[{\"added\": {}}]',14,1),(21,'2016-09-16 20:33:39','1','russ lil [APQ[3]=>what is your favorite food?=turkey]',1,'[{\"added\": {}}]',11,1),(22,'2016-09-16 20:33:51','2','russ lil [APQ[3]=>what is your favorite food?=ice cream]',1,'[{\"added\": {}}]',11,1),(23,'2016-09-20 18:28:42','4','often',2,'[{\"changed\": {\"fields\": [\"order\"]}}]',7,1),(24,'2016-09-20 18:29:01','3','sometimes',2,'[{\"changed\": {\"fields\": [\"order\"]}}]',7,1),(25,'2016-09-20 18:29:56','8','beer',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',7,1),(26,'2016-09-20 18:30:03','7','ice cream',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',7,1),(27,'2016-09-20 18:30:11','6','turkey',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',7,1),(28,'2016-09-20 23:35:13','4','APQ[4]=>you have a friendly chat',1,'[{\"added\": {}}]',NULL,1),(29,'2016-09-20 23:35:18','5','APQ[5]=>you have a friendly chat',1,'[{\"added\": {}}]',NULL,1),(30,'2016-09-20 23:35:24','6','APQ[6]=>what is your favorite food?',1,'[{\"added\": {}}]',NULL,1),(31,'2016-09-20 23:35:29','7','APQ[7]=>what is your favorite food?',1,'[{\"added\": {}}]',NULL,1),(32,'2016-09-20 23:35:34','8','APQ[8]=>you let your child know when they are doing a good job',1,'[{\"added\": {}}]',NULL,1),(33,'2016-09-20 23:35:41','9','APQ[9]=>you have a friendly chat',1,'[{\"added\": {}}]',NULL,1),(34,'2016-09-21 01:03:27','3','freeform',1,'[{\"added\": {}}]',NULL,1),(35,'2016-09-21 01:03:29','4','how is your day going?',1,'[{\"added\": {}}]',9,1),(36,'2016-09-21 01:03:36','10','APQ[0]=>how is your day going?',1,'[{\"added\": {}}]',NULL,1),(37,'2016-09-21 01:04:50','9','freeform',1,'[{\"added\": {}}]',7,1),(38,'2016-09-21 03:15:32','1','test',1,'[{\"added\": {}}]',8,1),(39,'2016-09-21 03:16:07','1','radiogroup',1,'[{\"added\": {}}]',NULL,1),(40,'2016-09-21 03:16:10','1','select one of these',1,'[{\"added\": {}}]',9,1),(41,'2016-09-21 03:16:23','1','stuff',1,'[{\"added\": {}}]',14,1),(42,'2016-09-21 03:16:28','1','test[0]=>select one of these',1,'[{\"added\": {}}]',NULL,1),(43,'2016-09-21 03:16:37','1','test[0]=>select one of these',2,'[]',NULL,1),(44,'2016-09-21 03:17:01','2','checkgroup',1,'[{\"added\": {}}]',NULL,1),(45,'2016-09-21 03:17:04','2','select some of these',1,'[{\"added\": {}}]',9,1),(46,'2016-09-21 03:17:18','2','test[1]=>select some of these',1,'[{\"added\": {}}]',NULL,1),(47,'2016-09-21 03:18:08','3','freeform',1,'[{\"added\": {}}]',NULL,1),(48,'2016-09-21 03:18:10','3','write something',1,'[{\"added\": {}}]',9,1),(49,'2016-09-21 03:18:19','3','test[3]=>write something',1,'[{\"added\": {}}]',NULL,1),(50,'2016-09-21 03:18:26','4','test[4]=>select one of these',1,'[{\"added\": {}}]',NULL,1),(51,'2016-09-21 03:18:35','5','test[5]=>select one of these',1,'[{\"added\": {}}]',NULL,1),(52,'2016-09-21 03:19:32','1','something',1,'[{\"added\": {}}]',7,1),(53,'2016-09-21 03:20:05','2','somethign else',1,'[{\"added\": {}}]',7,1),(54,'2016-09-21 03:20:39','3','blablbalsbd',1,'[{\"added\": {}}]',7,1),(55,'2016-09-21 03:21:16','1','rs l',1,'[{\"added\": {}}]',12,1),(56,'2016-09-21 03:37:29','4','hhhhhhhh',1,'[{\"added\": {}}]',7,1),(57,'2016-09-21 03:37:47','5','yyyyyy',1,'[{\"added\": {}}]',7,1),(58,'2016-09-21 03:38:19','6','ooooo',1,'[{\"added\": {}}]',7,1),(59,'2016-09-21 03:39:57','7','freeform',1,'[{\"added\": {}}]',7,1),(60,'2016-09-21 04:19:03','1','rs l [test[1]=>select some of these=ooooo]',3,'',11,1),(61,'2016-09-21 04:19:50','2','rs l [test[1]=>select some of these=ooooo]',3,'',11,1),(62,'2016-09-21 04:23:08','13','rs l [test[1]=>select some of these=ooooo]',3,'',11,1),(63,'2016-09-21 04:23:08','12','rs l [test[1]=>select some of these=somethign else]',3,'',11,1),(64,'2016-09-21 04:23:08','11','rs l [test[1]=>select some of these=blablbalsbd]',3,'',11,1),(65,'2016-09-21 04:23:08','10','rs l [test[1]=>select some of these=something]',3,'',11,1),(66,'2016-09-21 04:23:08','9','rs l [test[4]=>select one of these=hhhhhhhh]',3,'',11,1),(67,'2016-09-21 04:23:08','8','rs l [test[4]=>select one of these=yyyyyy]',3,'',11,1),(68,'2016-09-21 04:23:08','7','rs l [test[5]=>select one of these=yyyyyy]',3,'',11,1),(69,'2016-09-21 04:23:08','6','rs l [test[5]=>select one of these=hhhhhhhh]',3,'',11,1),(70,'2016-09-21 04:23:08','5','rs l [test[3]=>write something=freeform]',3,'',11,1),(71,'2016-09-21 04:23:08','4','rs l [test[0]=>select one of these=yyyyyy]',3,'',11,1),(72,'2016-09-21 04:23:08','3','rs l [test[0]=>select one of these=hhhhhhhh]',3,'',11,1),(73,'2016-09-21 04:23:33','24','rs l [test[1]=>select some of these=ooooo]',3,'',11,1),(74,'2016-09-21 04:23:33','23','rs l [test[1]=>select some of these=somethign else]',3,'',11,1),(75,'2016-09-21 04:23:33','22','rs l [test[1]=>select some of these=blablbalsbd]',3,'',11,1),(76,'2016-09-21 04:23:33','21','rs l [test[1]=>select some of these=something]',3,'',11,1),(77,'2016-09-21 04:23:33','20','rs l [test[4]=>select one of these=hhhhhhhh]',3,'',11,1),(78,'2016-09-21 04:23:33','19','rs l [test[4]=>select one of these=yyyyyy]',3,'',11,1),(79,'2016-09-21 04:23:33','18','rs l [test[5]=>select one of these=yyyyyy]',3,'',11,1),(80,'2016-09-21 04:23:33','17','rs l [test[5]=>select one of these=hhhhhhhh]',3,'',11,1),(81,'2016-09-21 04:23:33','16','rs l [test[3]=>write something=freeform]',3,'',11,1),(82,'2016-09-21 04:23:33','15','rs l [test[0]=>select one of these=yyyyyy]',3,'',11,1),(83,'2016-09-21 04:23:33','14','rs l [test[0]=>select one of these=hhhhhhhh]',3,'',11,1),(84,'2016-09-21 04:33:43','7','freeform',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',7,1),(85,'2016-10-25 17:39:05','1','test',1,'[{\"added\": {}}]',8,1),(86,'2016-10-25 17:40:00','1','freeform text',1,'[{\"added\": {}}]',NULL,1),(87,'2016-10-25 17:40:22','1','what did you last dream about?',1,'[{\"added\": {}}]',9,1),(88,'2016-10-25 17:56:06','1','test[1]=>what did you last dream about?',1,'[{\"added\": {}}]',NULL,1),(89,'2016-10-25 17:56:43','2','wellornot',1,'[{\"added\": {}}]',NULL,1),(90,'2016-10-25 17:56:51','2','how is your day',1,'[{\"added\": {}}]',9,1),(91,'2016-10-25 17:58:09','2','test[2]=>how is your day',1,'[{\"added\": {}}]',NULL,1),(92,'2016-10-25 17:58:41','3','favorite foods',1,'[{\"added\": {}}]',NULL,1),(93,'2016-10-25 17:58:55','3','favourite foods',1,'[{\"added\": {}}]',9,1),(94,'2016-10-25 17:59:09','3','test[3]=>favourite foods',1,'[{\"added\": {}}]',NULL,1),(95,'2016-10-25 19:08:06','1','russell little',1,'[{\"added\": {}}]',12,1),(96,'2016-10-25 19:56:49','4','big freeformtext',1,'[{\"added\": {}}]',NULL,1),(97,'2016-10-25 20:04:15','4','big freeformtext',2,'[]',NULL,1),(98,'2016-10-25 20:04:22','3','favorite foods',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',NULL,1),(99,'2016-10-25 20:04:31','2','wellornot',2,'[]',NULL,1),(100,'2016-10-25 20:05:15','4','describe your day',1,'[{\"added\": {}}]',9,1),(101,'2016-10-25 20:05:19','4','test[4]=>describe your day',1,'[{\"added\": {}}]',NULL,1),(102,'2016-10-25 20:05:33','3','test[3]=>favourite foods',2,'[]',NULL,1),(103,'2016-10-25 20:09:10','1','freeform text',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',NULL,1),(104,'2016-10-25 20:09:12','1','what did you last dream about?',2,'[]',9,1),(105,'2016-10-25 20:11:00','1','well',1,'[{\"added\": {}}]',7,1),(106,'2016-10-25 20:11:13','2','not well',1,'[{\"added\": {}}]',7,1),(107,'2016-10-25 20:11:40','3','freeform text',1,'[{\"added\": {}}]',7,1),(108,'2016-10-25 20:12:04','4','big text',1,'[{\"added\": {}}]',7,1),(109,'2016-10-25 20:12:21','5','fruit',1,'[{\"added\": {}}]',7,1),(110,'2016-10-25 20:12:35','6','boogers',1,'[{\"added\": {}}]',7,1),(111,'2016-10-25 20:56:25','3','favorite foods',2,'[]',NULL,1),(112,'2016-10-25 20:56:31','4','big freeformtext',2,'[]',NULL,1),(113,'2016-10-25 20:56:40','2','wellornot',2,'[]',NULL,1),(114,'2016-10-25 20:56:49','1','freeform text',2,'[]',NULL,1),(115,'2016-10-26 06:05:02','2','wellornot',2,'[]',NULL,1),(116,'2016-10-28 06:55:43','6','boogers',2,'[]',7,1),(117,'2016-10-28 06:58:45','4','big text',2,'[{\"changed\": {\"fields\": [\"show_name\"]}}]',7,1),(118,'2016-10-28 06:58:56','3','freeform text',2,'[{\"changed\": {\"fields\": [\"show_name\"]}}]',7,1),(119,'2016-10-28 06:59:18','6','boogers',2,'[{\"changed\": {\"fields\": [\"show_name\"]}}]',7,1),(120,'2016-10-28 06:59:23','5','fruit',2,'[{\"changed\": {\"fields\": [\"show_name\"]}}]',7,1),(121,'2016-10-28 18:55:16','1','what did you last dream about?',2,'[]',9,1),(122,'2016-10-28 18:56:19','1','freeform text',2,'[]',NULL,1),(123,'2016-10-28 18:56:21','1','what did you last dream about?',2,'[]',9,1),(124,'2016-10-28 18:56:57','1','what did you last dream about?',2,'[{\"changed\": {\"fields\": [\"title\"]}}]',9,1),(125,'2016-10-28 18:59:06','4','1 [test[1]=>what did you last dream about?=freeform text]',3,'',11,1),(126,'2016-10-28 18:59:06','3','1 [test[3]=>favourite foods=fruit]',3,'',11,1),(127,'2016-10-28 18:59:06','2','1 [test[4]=>describe your day=big text]',3,'',11,1),(128,'2016-10-28 18:59:07','1','1 [test[3]=>favourite foods=boogers]',3,'',11,1),(129,'2016-10-28 19:04:49','2','how hungry am I',1,'[{\"added\": {}}]',8,1),(130,'2016-10-28 19:05:08','5','how hungry am I[2]=>favourite foods',1,'[{\"added\": {}}]',NULL,1),(131,'2016-10-28 19:05:45','7','yes',1,'[{\"added\": {}}]',7,1),(132,'2016-10-28 19:05:54','8','no',1,'[{\"added\": {}}]',7,1),(133,'2016-10-28 19:05:56','5','yesno',1,'[{\"added\": {}}]',NULL,1),(134,'2016-10-28 19:06:05','5','are you hungry',1,'[{\"added\": {}}]',9,1),(135,'2016-10-28 19:06:10','6','how hungry am I[1]=>are you hungry',1,'[{\"added\": {}}]',NULL,1),(136,'2016-10-28 19:09:19','10','1 [how hungry am I[1]=>are you hungry=yes]',3,'',11,1),(137,'2016-10-28 19:09:19','9','1 [how hungry am I[2]=>favourite foods=boogers]',3,'',11,1),(138,'2016-10-28 19:09:19','8','1 [test[1]=>what did you last dream about?=freeform text]',3,'',11,1),(139,'2016-10-28 19:09:19','7','1 [test[3]=>favourite foods=fruit]',3,'',11,1),(140,'2016-10-28 19:09:19','6','1 [test[4]=>describe your day=big text]',3,'',11,1),(141,'2016-10-28 19:09:19','5','1 [test[2]=>how is your day=well]',3,'',11,1),(142,'2016-11-01 20:37:39','1','1 [test[2]=>how is your day=well]',1,'[{\"added\": {}}]',11,1),(143,'2016-11-02 03:19:57','1','freeform text',2,'[]',NULL,1),(144,'2016-11-02 03:49:11','1','None',3,'',11,1),(145,'2016-11-02 04:01:03','2','2',1,'[{\"added\": {}}]',12,1),(146,'2016-11-02 04:03:22','3','freeform text',2,'[{\"changed\": {\"fields\": [\"allow_custom_responses\"]}}]',7,1),(147,'2016-11-02 04:03:32','4','big text',2,'[{\"changed\": {\"fields\": [\"allow_custom_responses\"]}}]',7,1),(148,'2016-11-02 04:04:04','14','2',3,'',11,1),(149,'2016-11-02 04:04:04','13','blah',3,'',11,1),(150,'2016-11-02 04:04:04','12','blaaaaaaaaaahhhhhh',3,'',11,1),(151,'2016-11-02 04:04:04','11','booges',3,'',11,1),(152,'2016-11-02 04:04:04','10','2',3,'',11,1),(153,'2016-11-02 04:04:04','9','blah',3,'',11,1),(154,'2016-11-02 04:04:04','8','blaaaaaaaaaahhhhhh',3,'',11,1),(155,'2016-11-02 04:04:04','7','booges',3,'',11,1),(156,'2016-11-02 04:04:04','6','blah',3,'',11,1),(157,'2016-11-02 04:04:04','5','froot',3,'',11,1),(158,'2016-11-02 04:04:04','4','blaaaaaaaaaahhhhhh',3,'',11,1),(159,'2016-11-02 04:04:04','3','booges',3,'',11,1),(160,'2016-11-02 04:04:04','2','1',3,'',11,1),(161,'2016-11-02 04:05:24','3','favourite foods',2,'[{\"changed\": {\"fields\": [\"missing_value_text\"]}}]',9,1),(162,'2016-11-15 19:38:21','1','test',1,'[{\"added\": {}}]',8,1),(163,'2016-11-15 19:38:59','1','good',1,'[{\"added\": {}}]',7,1),(164,'2016-11-15 19:39:14','2','not good',1,'[{\"added\": {}}]',7,1),(165,'2016-11-15 19:39:16','1','good/not',1,'[{\"added\": {}}]',18,1),(166,'2016-11-15 19:39:24','1','How is Your day?',1,'[{\"added\": {}}]',9,1),(167,'2016-11-15 19:39:33','1','test[0]=>How is Your day?',1,'[{\"added\": {}}]',17,1),(168,'2016-11-15 19:41:39','1','3',1,'[{\"added\": {}}]',12,1),(169,'2016-11-15 19:43:08','1','good/not',2,'[]',18,1),(170,'2016-11-15 19:43:11','1','How is Your day?',2,'[]',9,1),(171,'2016-11-15 19:45:25','1','good/not',2,'[{\"changed\": {\"fields\": [\"ui\"]}}]',18,1),(172,'2016-11-15 19:56:14','1','sourceChoice object',1,'[{\"added\": {}}]',16,1),(173,'2016-11-15 19:56:26','2','sourceChoice object',1,'[{\"added\": {}}]',16,1),(174,'2016-11-15 19:56:34','1','sourceColumn object',1,'[{\"added\": {}}]',21,1),(175,'2016-11-15 20:01:33','1','src to test[0]=>How is Your day?',1,'[{\"added\": {}}]',22,1),(176,'2016-11-15 20:01:51','1','SourceScheme object',1,'[{\"added\": {}}]',19,1),(177,'2016-11-29 19:34:36','2','1',1,'[{\"added\": {}}]',12,1),(178,'2016-11-29 19:34:44','3','2',1,'[{\"added\": {}}]',12,1),(179,'2016-11-29 19:34:54','4','4',1,'[{\"added\": {}}]',12,1),(180,'2016-11-29 19:34:58','4','4',2,'[]',12,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(4,'auth','group'),(2,'auth','permission'),(3,'auth','user'),(5,'contenttypes','contenttype'),(11,'db','answer'),(7,'db','choice'),(18,'db','choicegroup'),(20,'db','kwargs'),(14,'db','measure'),(12,'db','person'),(9,'db','question'),(15,'db','relation'),(16,'db','sourcechoice'),(21,'db','sourcecolumn'),(22,'db','sourcequestion'),(19,'db','sourcescheme'),(8,'db','survey'),(17,'db','surveyquestion'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-09-16 19:08:22'),(2,'auth','0001_initial','2016-09-16 19:08:23'),(3,'admin','0001_initial','2016-09-16 19:08:23'),(4,'admin','0002_logentry_remove_auto_add','2016-09-16 19:08:23'),(5,'contenttypes','0002_remove_content_type_name','2016-09-16 19:08:23'),(6,'auth','0002_alter_permission_name_max_length','2016-09-16 19:08:23'),(7,'auth','0003_alter_user_email_max_length','2016-09-16 19:08:23'),(8,'auth','0004_alter_user_username_opts','2016-09-16 19:08:23'),(9,'auth','0005_alter_user_last_login_null','2016-09-16 19:08:23'),(10,'auth','0006_require_contenttypes_0002','2016-09-16 19:08:23'),(11,'auth','0007_alter_validators_add_error_messages','2016-09-16 19:08:23'),(12,'auth','0008_alter_user_username_max_length','2016-09-16 19:08:23'),(13,'sessions','0001_initial','2016-09-16 19:08:23'),(25,'db','0001_initial','2016-11-15 19:37:15'),(26,'db','0002_auto_20161115_1421','2016-11-15 20:21:10');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('aypnbozez73mwn2cf87eghk4l2om00o0','YTYxZjkxNmE0MGM0ZGE4ZjFkMDdhYmE2ZDhlZDdjNjk0OTgzMzFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjA4YjYxZWIxMTkwZDRjODAyZDFlMmEzNzAzYWZmYTM1ZWZiY2RhZDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-09-30 19:10:30'),('dmiiq36ca4090dj1cqyfebmpmn46fnr2','YTYxZjkxNmE0MGM0ZGE4ZjFkMDdhYmE2ZDhlZDdjNjk0OTgzMzFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjA4YjYxZWIxMTkwZDRjODAyZDFlMmEzNzAzYWZmYTM1ZWZiY2RhZDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-21 23:58:24'),('i3xeo71ny9epinuwur1lwmsxlnp8pqn9','YTYxZjkxNmE0MGM0ZGE4ZjFkMDdhYmE2ZDhlZDdjNjk0OTgzMzFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjA4YjYxZWIxMTkwZDRjODAyZDFlMmEzNzAzYWZmYTM1ZWZiY2RhZDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-08 18:06:11'),('nuxeg2tgzao7dcven7441nzv5w0qjjs9','YTYxZjkxNmE0MGM0ZGE4ZjFkMDdhYmE2ZDhlZDdjNjk0OTgzMzFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjA4YjYxZWIxMTkwZDRjODAyZDFlMmEzNzAzYWZmYTM1ZWZiY2RhZDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-11 08:43:31'),('uovewdhf917ht4e9aqjnd25ct47m0jll','YTYxZjkxNmE0MGM0ZGE4ZjFkMDdhYmE2ZDhlZDdjNjk0OTgzMzFjZTp7Il9hdXRoX3VzZXJfaGFzaCI6IjA4YjYxZWIxMTkwZDRjODAyZDFlMmEzNzAzYWZmYTM1ZWZiY2RhZDAiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-12-13 18:27:57');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-30 14:58:14
