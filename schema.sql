DROP DATABASE IF EXISTS survey_data;
CREATE DATABASE survey_data;

CREATE TABLE answers (
    respondent_id INT unsigned NOT NULL, 
    question_id VARCHAR(25) NOT NULL,
    answer VARCHAR(65) NOT NULL
) ENGINE=ColumnStore DEFAULT CHARSET=utf8;
