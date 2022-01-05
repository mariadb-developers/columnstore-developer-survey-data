# Analyzing Stack Overflow Annual Developer Survey Data with MariaDB

This repository provides data and information that will enable you to transform, import and analyze the [raw Stack Overflow Annual Developer Survey data](https://insights.stackoverflow.com/survey) with [MariaDB](https://mariadb.com) [ColumnStore](https://mariadb.com/docs/features/mariadb-columnstore/). 

Starting at [Step 2, Parse and transform the data,](#parse-transform) this repository will walk you through the process of preparing, importing and, ultimately, being able to analyze the [raw Stack Overflow Annual Developer Survey data for 2020](https://drive.google.com/file/d/1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB/view) (which is included in the [developer_survey_2020](developer_survey_2020) folder). 

**Note:** This repository will be updated to include the raw 2021 data once it becomes available [here](https://insights.stackoverflow.com/survey).

# Table of Contents
1. [Requirements](#requirements)
2. [Parse and transform the data](#parse-transform)
3. [Prepare the database](#prepare-db)
    1. [Docker Container](#docker)
    2. [MariaDB SkySQL](#skysql)
4. [Create the schema](#schema)
5. [Import the data](#import)
6. [Analyze the data](#analyze)
    1. [SQL](#docker)
    2. [MariaDB SkySQL](#skysql)
7. [Support and contribution](#support-contribution)
8. [License](#license)

## Requirements <a name="requirements"></a>

* [MariaDB Client](https://mariadb.com/products/skysql/docs/clients/), used to connect to MariaDB database instances.
* [Python v. 3+](https://www.python.org/downloads/)

## Parsing and transforming the data <a name="parse-transform"></a>

In this sample you will use the Python script file, [parse_and_transform.py](parse_and_transform.py), to parse and transform the [Stack Overflow Annual Survey data for 2020](/developer_survey_2020).

Executing [parse_and_transform.py](parse_and_transform.py) will parse through the [survey results data] and split each row, which contains all the responses from an single survey respondent, into multiple rows, one per response. The result of turns ~66k rows of data into ~5 million rows. 

To execute the [parse_and_transform.py](parse_and_transform.py) you need to perform the following steps.

1. Open a new terminal window at this location.

2. Create a new Python virtual environment.

```bash
$ python3 -m venv venv
```

3. Activate the virtual environment.

```bash 
$ . venv/bin/activate
```

4. Install the pandas Python package, which will be use for data manipulation within [parse_and_transform.py](parse_and_transform.py).

```bash
$ pip install pandas
```

5. And, finally, execute the [parse_and_transform.py](parse_and_transform.py) script!

```bash
$ python3 parse_and_transform.py
```

## Preparing the database <a name="import"></a>

To be able to store and analyze the survey data you're going to need a place to put it. MariaDB to the rescue! Below includes instructions on setting up a local database, using the [official MariaDB Docker image](https://hub.docker.com/_/mariadb), or [MariaDB SkySQL](https://mariadb.com/products/skysql/), the ultimate MariaDB database in the cloud. 

### Docker Container <a name="docker"></a>

Running a single instance (container) of MariaDB ColumnStore is incredibly simple using the MariaDB Community Server ColumnStore image. 

Check out the instructions [here](https://hub.docker.com/r/mariadb/columnstore).

### MariaDB SkySQL <a name="skysql"></a>

[SkySQL](https://mariadb.com/products/skysql/) is the first and only database-as-a-service (DBaaS) to bring the full power of MariaDB Platform to the cloud, including its support for transactional, analytical and hybrid workloads. Built on Kubernetes, and optimized for cloud infrastructure and services, SkySQL combines ease of use and self-service with enterprise reliability and world-class support – everything needed to safely run mission-critical databases in the cloud, and with enterprise governance.

[Get started with SkySQL!](https://mariadb.com/products/skysql/#get-started)

<p align="center" spacing="10">
    <kbd>
        <img src="media/skysql.png" />
    </kbd>
</p>

**IMPORTANT:** Once you've registered for MariaDB SkySQL you will need to create a new analytics service so that you can take advantage of the MariaDB columnar storage engine, [ColumnStore](https://mariadb.com/docs/features/mariadb-columnstore/). For more information on how to do this check out [this walk-through](https://mariadb.com/resources/blog/getting-started-with-mariadb-skysql-for-analytics/), or check out this short video on [launching a new SkySQL service](https://www.youtube.com/watch?v=jr9oPHALmr4) - don't worry it only takes a couple of minutes! 

## Create the schema <a name="schema"></a>

The survey result data contained in newly created **answers.csv** file will need to be imported to MariaDB. To accomodate that you will need to create a new database, `survey_data`, that contains a single table, `answers`.

To create the new database and table you can either copy and execute the following code within a database client of your choice.

```sql
DROP DATABASE IF EXISTS survey_data;
CREATE DATABASE survey_data;

CREATE TABLE answers (
    respondent_id INT unsigned NOT NULL, 
    question_id VARCHAR(25) NOT NULL,
    answer VARCHAR(65) NOT NULL
) ENGINE=ColumnStore DEFAULT CHARSET=utf8;
```

or use the MariaDB Client to execute the [schema.sql](schema.sql) script contained within this repository.

For example: 

_Locally_
```bash
$ mariadb --host 127.0.0.1 --user root -pPassword123! < schema.sql
```

_SkySQL_
```bash
mariadb --host analytics-1.mdb0001265.db.skysql.net --port 5001 --user DB00004537 -p --ssl-ca ~/Downloads/skysql_chain.pem < schema.sql
```

**Note:** Remember to update the command above with your database location, user and SSL information accordingly!

## Import the data <a name="import"></a>

After you've created the new schema, you can import the answers.csv data using the MariaDB Client. 

For example:

_Locally_
```bash
mariadb --host 127.0.0.1 --port 3306 --user root -pPassword123! -e "LOAD DATA LOCAL INFILE 'answers.csv' INTO TABLE answers FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'" survey_data
```

_SkySQL_
```bash
mariadb --host analytics-1.mdb0001265.db.skysql.net --port 5001 --user DB00004537 -p --ssl-ca ~/Downloads/skysql_chain.pem -e "LOAD DATA LOCAL INFILE 'answers.csv' INTO TABLE answers FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n'" survey_data
```

**Note:** Remember to update the command above with your database location, user and SSL information accordingly!

## Analyze the data <a name="analyze"></a>

Once the data has been successfully imported into MariaDB there are many ways that you can use the data!

### SQL <a name="skysql"></a>

You can use a database client to execute SQL queries directly on the results data contained in the `answers` table. 

For exmple, using the MariaDB Client:

1. Start by connecting to your MariaDB database instance. 

```bash
$ mariadb --host 127.0.0.1 --user root -pPassword123!
```

2. Execute the following query to `SELECT` the top 10 programming langauges that have been used by respondents that have also used MariaDB.

```sql
SELECT
	answer, COUNT(answer) AS respondent_count
FROM
	survey_data.answers
WHERE 
	question_id = "LanguageWorkedWith" AND 
	respondent_id IN (SELECT respondent_id FROM answers WHERE question_id = "DatabaseWorkedWith" AND answer = "MariaDB")
GROUP BY
	answer
ORDER BY
	COUNT(answer) DESC
LIMIT 10;
```

```
+-----------------------+------------------+
| answer                | respondent_count |
+-----------------------+------------------+
| JavaScript            |             6878 |
| HTML/CSS              |             6597 |
| SQL                   |             6239 |
| PHP                   |             5149 |
| Python                |             4204 |
| Java                  |             4028 |
| Bash/Shell/PowerShell |             3746 |
| TypeScript            |             2558 |
| C#                    |             2396 |
| C++                   |             2277 |
+-----------------------+------------------+
```

### Python & Jupyter Lab <a name="skysql"></a>

You can also use modern data analysis and visualization tools like [Jupyter Lab](https://jupyter.org/), in combination with [MariaDB Connector/Python](https://mariadb.com/docs/clients/mariadb-connectors/connector-python/) and [Python](https://www.python.org/) libraries like [Plotly](https://plotly.com/) and [Pandas](https://pandas.pydata.org/). 

For more information on how you can do this please check out the following resources:

* [Using Data Analysis and Visualization with MariaDB Connector/Python](https://github.com/mariadb-corporation/dev-example-connector-python/blob/master/samples/analysis/README.md) (GitHub Repository)

* [Deep dive: Taking advantage of MariaDB Connector for Python](https://go.mariadb.com/21Q4-WBN-GLBL-OSSG-Python-Connector-2021-08-26_Registration-LP.html?_ga=2.247064967.2067136692.1629673971-817046405.1628296957&_gac=1.61026014.1629298886.CjwKCAjw3_KIBhA2EiwAaAAlitUQQTxd3HGd6jjzQw3h2pLtya8fOTTptfZol-3Fh96QbVwm4Ek9VxoC-McQAvD_BwE) (Webinar) 

## Support and Contribution <a name="support-contribution"></a>

Please feel free to submit PR's, issues or requests to this project project directly.

If you have any other questions, comments, or looking for more information on MariaDB please check out:

* [MariaDB Developer Hub](https://mariadb.com/developers)
* [MariaDB Community Slack](https://r.mariadb.com/join-community-slack)

Or reach out to us diretly via:

* [developers@mariadb.com](mailto:developers@mariadb.com)
* [MariaDB Twitter](https://twitter.com/mariadb)

## License <a name="license"></a>
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=plastic)](https://opensource.org/licenses/MIT)
