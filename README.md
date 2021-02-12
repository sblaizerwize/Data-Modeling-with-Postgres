# **README**

## **Introduction**

Sparkify is a digital music application that enables users to listen to music online. Currently, the application aims to offer new content to users based on their song preferences. However, the information collected from users, including songs and user logs (metadata), is stored in JSON files, which avoids querying data and therefore running analytics on it. 

JSON file containing song's information. 


```
{
    "num_songs": 1,
    "artist_id": "ARD7TVE1187B99BFB1",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "California - LA",
    "artist_name": "Casual",
    "song_id": "SOMZWCG12A8C13C480",
    "title": "I Didn't Mean To",
    "duration": 218.93179,
    "year": 0
}
```


JSON file containing user logs information. 


```
{
    "artist": null,
    "auth": "Logged In",
    "firstName": "Walter",
    "gender": "M",
    "itemInSession": 0,
    "lastName": "Frye",
    "length": null,
    "level": "free",
    "location": "San Francisco-Oakland-Hayward, CA",
    "method": "GET",
    "page": "Home",
    "registration": 1540919166796.0,
    "sessionId": 38,
    "song": null,
    "status": 200,
    "ts": 1541105830796,
    "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
    "userId": "39"
}
```
---

## **Proposed solution**

The proposed solution in this repository consists of migrating source data in JSON format to a PostgreSQL database named Sparkify following a star schema design and implementing an ETL pipeline. 

The star schema that the Sparkify database follows is described in Figure 1. It consists of a FACT table surrounded by DIMENSION tables that contain data attributes. A star schema is simple to implement because data located in fact tables is not normalized. Also, this schema fosters data fetching by performing direct join operations among the dimension tables and the fact table. 

![sparkify schema](/images/sparkify_schema.png)
**Figure 1** Sparkify star schema design.
<br />

The ETL pipeline for migrating source data into the Sparkify database includes the following tasks after creating the database and required tables. 

1. Connect to the Sparkify database and get a cursor.
2. Process song_data files. 
    1. Append paths of JSON files.
    2. Get the total number of files to be processed.
    3. Process every single JSON file. 
        1. Read JSON file.
        2. Drop records that contain any ***NULL*** fields.
        3. Extract fields for ***artist table.***
        4. Insert records into ***artist table.***
        5. Extract fields for ***song table.***
        6. Insert records into ***song table.***
3. Process log_data files. 
    1. Append paths of JSON files.
    2. Get the total number of files to be processed.
    3. Process every single JSON file. 
        1. Read JSON file.
        2. Drop records that contain any _NUL_L fields.
        3. Extract ***timestamp field*** filtered by ***NextSong***.
        4. Transform ***timestamp fields*** into datetime format.
        5. Insert datetime records into ***time table***.
        6. Extract fields for ***user table***.
        7. Insert records into ***user table***.
        8. Extract records for ***songplays table*** including ***songid*** and ***artistid*** fields.
        9. Transform the ***timestamp*** and ***userid*** fields.
        10. Insert records into ***songplays table***. 
4. Close connection

---
## **Explanation of the files in this repository**

The following table describes the content of this repository. 

<table>
  <tr>
   <td><strong>File</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td>create_tables.py
   </td>
   <td>Python script that drops any existing database and tables, and creates the required Sparkify database and tables.
   </td>
  </tr>
  <tr>
   <td>etl.ipynb
   </td>
   <td>Jupyter notebook that performs a step-by-step extraction, transformation, and loading of single records into the Sparkify database. 
   </td>
  </tr>
  <tr>
   <td>etl.py
   </td>
   <td>Python script that performs the extraction, transformation, and loading of all records into the Sparkify database. 
   </td>
  </tr>
  <tr>
   <td>README.md
   </td>
   <td>File that contains the main information and instructions of how to use this repository. 
   </td>
  </tr>
  <tr>
   <td>sample_queries.ipynb
   </td>
   <td>Jupyter notebook that includes queries examples for analyzing data from the Sparkify database. 
   </td>
  </tr>
  <tr>
   <td>sql_queries.py
   </td>
   <td>Python script that contains queries for dropping, creating, and inserting data into Sparkify tables.
   </td>
  </tr>
  <tr>
   <td>test.ipynb
   </td>
   <td>Jupyter notebook that helps validate the data model by querying loaded data from the Sparkify database. 
   </td>
  </tr>
  <tr>
   <td>data/log_data
   </td>
   <td>Source file that contains information about user logs in JSON format. 
   </td>
  </tr>
  <tr>
   <td>data/song_data
   </td>
   <td>Source file that contains information about songs in JSON format. 
   </td>
  </tr>
</table>

---
## **Prerequisites**

Before using this repository, you must comply with the following:

*   Install Postgresql on your local machine  \
For iOS, follow this tutorial to [install PostgreSQL](https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb).  
*   Install [Psycopg](https://towardsdatascience.com/python-and-postgresql-how-to-access-a-postgresql-database-like-a-data-scientist-b5a9c5a0ea43), a PostgreSQL adapter for the Python programming language.
*   Clone this repository.

---
## **How to run the Python scripts**

After you clone this repository:

1. Go to the root folder of this repository. 
2. Run on your terminal the following command to create the Sparkify database and required tables: 

    ```python create_tables.py```

3. Open and run the commands in the `test.ipyn`b notebook to validate that the required tables were created. 
4. Restart the kernel of the `test.ipynb` notebook to close the psycopg connection.
5. Run on your terminal the following command to perform the extraction, transformation, and loading of records from the source files to the Sparkify database:

    ```python etl.py```

    This is an excerpt of the result you get. 

```
71 files found in data/song_data
    1/71 files processed.
    2/71 files processed.
    3/71 files processed.
    4/71 files processed.
    5/71 files processed.
    …

    30 files found in data/log_data
    1/30 files processed.
    2/30 files processed.
    3/30 files processed.
    4/30 files processed.
    5/30 files processed.
    …
```


6. Follows steps 2 and 3 to validate that your data is correctly loaded into the Sparkify database.  

---
## **Sample queries and for data analysis**

The following are sample queries to run some analytics on the Sparkify database. Consult the `sample_queries.ipynb` file for more details. 


### **Identifying the top 5 users with the most records**

```
%%sql SELECT user_id, 
COUNT(user_id) AS total_user
FROM songplays
GROUP BY user_id
ORDER BY total_user DESC
LIMIT 5;
```

Results
<table>
  <tr>
   <td><strong>user_id</strong>
   </td>
   <td><strong>total_user</strong>
   </td>
  </tr>
  <tr>
   <td>80
   </td>
   <td>74
   </td>
  </tr>
  <tr>
   <td>44
   </td>
   <td>61
   </td>
  </tr>
  <tr>
   <td>49
   </td>
   <td>57
   </td>
  </tr>
  <tr>
   <td>29
   </td>
   <td>39
   </td>
  </tr>
  <tr>
   <td>88
   </td>
   <td>36
   </td>
  </tr>
</table> 

<br />

### **Identifying the top 5 user locations**

```
%%sql SELECT location,
COUNT(location) AS total_number
FROM songplays  
GROUP BY location 
ORDER BY total_number DESC
LIMIT 5;
```
Results
<table>
  <tr>
   <td><strong>location</strong>
   </td>
   <td><strong>total_number</strong>
   </td>
  </tr>
  <tr>
   <td>Portland-South Portland, ME
   </td>
   <td>74
   </td>
  </tr>
  <tr>
   <td>Waterloo-Cedar Falls, IA
   </td>
   <td>61
   </td>
  </tr>
  <tr>
   <td>San Francisco-Oakland-Hayward, CA
   </td>
   <td>57
   </td>
  </tr>
  <tr>
   <td>San Jose-Sunnyvale-Santa Clara, CA
   </td>
   <td>41
   </td>
  </tr>
  <tr>
   <td>Atlanta-Sandy Springs-Roswell, GA
   </td>
   <td>39
   </td>
  </tr>
</table>
<br />

### **Identifying the top 5 web browsers**

```
%%sql SELECT user_agent,
COUNT(user_agent) AS total_agent
FROM songplays  
GROUP BY user_agent 
ORDER BY total_agent DESC
LIMIT 5;
```

Results
<table>
  <tr>
   <td><strong>user_agent</strong>
   </td>
   <td><strong>total_agent</strong>
   </td>
  </tr>
  <tr>
   <td>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
   </td>
   <td>111
   </td>
  </tr>
  <tr>
   <td>Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0
   </td>
   <td>70
   </td>
  </tr>
  <tr>
   <td>Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0
   </td>
   <td>57
   </td>
  </tr>
  <tr>
   <td>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"
   </td>
   <td>52
   </td>
  </tr>
  <tr>
   <td>"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
   </td>
   <td>36
   </td>
  </tr>
</table>
<br />

### **Identifying top 5 users with paid and free subscriptions**
```
%%sql SELECT level,
COUNT(level) AS total_level
FROM songplays  
GROUP BY level 
ORDER BY total_level DESC;
```

Results
<table>
  <tr>
   <td><strong>level</strong>
   </td>
   <td><strong>total_level</strong>
   </td>
  </tr>
  <tr>
   <td>paid
   </td>
   <td>410
   </td>
  </tr>
  <tr>
   <td>free
   </td>
   <td>122
   </td>
  </tr>
</table>
<br />

### **Identifying the gender of users**
```
%%sql SELECT 
users.gender,
COUNT(users.gender) AS total
FROM songplays  
INNER JOIN users
ON songplays.user_id = users.user_id
GROUP BY users.gender
ORDER BY total DESC;
```
Results

<table>
  <tr>
   <td><strong>gender</strong>
   </td>
   <td><strong>total</strong>
   </td>
  </tr>
  <tr>
   <td>F
   </td>
   <td>390
   </td>
  </tr>
  <tr>
   <td>M
   </td>
   <td>142
   </td>
  </tr>
</table>