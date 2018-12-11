# Details for Oracle, Netezza and DSV {#data_movement_details}

This section reviews the details of each type of data movement for various types of source data:  [Oracle](#oracle_details), [Netezza](#netezza_details) and [Delimiter Separated Values (DSV) files](#dsv_details). For each source type, we review:
{:.list}

* Support for object and data types
* File structure for DSV (DSV only) 
* Constraints for movement into MPP SQL 
* Table and column names 


If you move data into the cloud using the Cazena Console, you will have the opportunity to review datatypes, table and column names, and constraints for each table that you move.  See the section on [moving data from the console](#move_data) for more details.

There is a limit of 1 table move at a time per [data store](#data_stores). You may start multiple table moves on a single data store, but they will be queued up and performed serially. 


## Oracle {#oracle_details}

### Objects
You may move Oracle __tables__ into your Cazena datacloud. Other Oracle object types are not supported.

### Datatypes
The following Oracle datatypes are supported. Some datatypes are supported with qualifications for various target service types. These qualifications are described below.

#### Numeric

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
number(p,s)	|	Possible loss in precision	|	Possible loss in precision	
float(p)	|	Possible loss in precision	|	Possible loss in precision	
binary_float	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
binary_double	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>

#### Character

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
char(n)	|	Converts to varchar for large values of n	|	Converts to varchar for large values of n	
varchar2(n)	|	Possible truncation for large values of n 	|	Possible truncation for large values of n
nvarchar(n)	|	Possible truncation for large values of n 	|	Possible truncation for large values of n
nchar(n)	|	Converts to varchar for large values of n 	|	Converts to varchar for large values of n 
nvarchar2(n)	|	Possible truncation for large values of n 	|	Possible truncation for large values of n

#### Temporal

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
date	|	Not supported as a temporal datatype; converts to varchar.	|	<span class="icon-checkmark"></span>
timestamp	|	Possible data loss	|	<span class="icon-checkmark"></span>	
timestamp with time zone	|	Not supported as a temporal datatype; defaults to varchar	|	Not supported as a temporal datatype; defaults to varchar
timestamp with local time zone	|	Not supported as a temporal datatype; defaults to varchar	|	Not supported as a temporal datatype; defaults to varchar
interval year to month	|	Not supported as a temporal datatype; defaults to varchar	|	Not supported as a temporal datatype; defaults to varchar
interval day to second	|	Not supported as a temporal datatype; defaults to varchar	|	Not supported as a temporal datatype; defaults to varchar

#### Other

Datatype  |Hive Metastore  |MPP SQL (Redshift)
:---------|:---------|:---------------------
rowid	|	Does not support intended meaning, defaults to varchar	|	Does not support intended meaning, defaults to varchar
urowid	|	Does not support intended meaning, defaults to varchar	|	Does not support intended meaning, defaults to varchar
mlslabel	|	Does not support intended meaning, defaults to varchar	|	Does not support intended meaning, defaults to varchar



### Constraint Support
The following types of Oracle construct clauses are supported by your Cazena datacloud:
{:.list}

* Primary key
* Foreign key
* Unique key
* Not null (column attribute)


### Table and Column Names
When moving data, the source and target services may have different rules for valid table and column names. As a result, table or column names may be changed in any of the following ways:

* The name may be truncated, quoted or changed to make it unique.
* Invalid/unsupported characters may be substituted. For example, Amazon Redshift requires ASCII only characters.
* Reserved words may be removed from names.

If you [move data using the Cazena console](#import_enterprise), these changes will be displayed during the review process. At that time, you can override the choices. 

### Data Store
See [Creating an Oracle data store](#oracle_data_store) for information on creating a data store that is able to access the data on the server. 


##Netezza {#netezza_details}

### Objects
You may move Netezza __tables__ and __external tables__ into your Cazena datacloud. Other Netezza object types are not supported.

### Datatypes
Cazena supports the following Netezza datatypes. Some datatypes are supported with qualifications for various target service types. These qualifications are described below.

#### Numeric

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
byteint (alias int1)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>	
smallint (alias int2)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>	
integer (alias int or int4)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
bigint (alias int8)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
numeric (p, s)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
numeric(p)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
numeric	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
decimal (alias for numeric)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
float(p)	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
real (same as float(6))	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>
double precision (same as float(15))	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>

#### Character

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
char (n)	|	Converts to varchar for large values of n	|	Converts to varchar for large values of n
varchar(n)	|	Possible truncation for large values of n	|	Possible truncation for large values of n
nchar(n)	|	Converts to nvarchar for large values of n	|	Converts to nvarchar for large values of n
nvarchar(n)	|	Possible truncation for large values of n	|	Possible truncation for large values of n

#### Temporal

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
date	|	Not supported as a temporal datatype in Cloudera Hadoop, converts to varchar.	|	<span class="icon-checkmark"></span>
time	|	Not supported as a temporal datatype; converts to varchar	|	Not supported as a temporal datatype; converts to varchar
time with time zone (alias timetz)	|	Not supported as a temporal datatype; converts to varchar	|	Not supported as a temporal datatype; converts to varchar	
timestamp	|	Possible data loss	|	<span class="icon-checkmark"></span>	
timestamp with time zone	|	Not supported as a temporal datatype; converts to varchar	|	Not supported as a temporal datatype; converts to varchar	
interval	|	Not supported as a temporal datatype; converts to varchar	|	Not supported as a temporal datatype; converts to varchar	

#### Other

Datatype  |Hive Metastore  |MPP SQL (Redshift)  
:---------|:---------|:---------------------
boolean	|	<span class="icon-checkmark"></span>	|	<span class="icon-checkmark"></span>


### Constraint Support
The following types of Netezza construct clauses may be moved into your Cazena datacloud:
{:.list}

* Primary key
* Foreign key
* Unique key
* distkey
* diststyle (e.g., HASH, RANDOM)
* not null (column attribute)

Although Netezza does not enforce keys, some Netezza tables may still include them for SQL compatibility. Note that when a Netezza table is imported to a service type that supports keys (e.g., MPP SQL), these constructs will be used in the creation of the target table if they are encountered.


### Table and Column Names
When moving data, the source and target services may have different rules for valid table and column names. As a result, table or column names may be changed in any of the following ways:

* The name may be truncated, quoted or changed to make it unique.
* Invalid/unsupported characters may be substituted. For example, Amazon Redshift requires ASCII only characters.
* Reserved words may be removed from names.

If you [move data using the Cazena console](#import_enterprise), these changes will be displayed during the review process. At that time, you can override the choices. 

### Data Store {#dsv_details}
See [Creating a Netezza data store](#netezza_data_store) for information on creating a data store that is able to access the data on the server. 


## Delimiter Separated Values (DSV) Files {#dmg_dsv_files}  

### File format

Delimiter Separated Values (DSV) files may be moved into the cloud from any type of source. They are most commonly moved from either the local file system or FTP/SFTP servers. 

This section describes how DSV files must be constructed so that they can be successfully loaded into your Cazena datacloud.

#### Lines

* Lines are delimited using LF (default) or CRLF
* Each row of the file must have exactly the same number of fields.
* Blank lines are invalid.
* The end of file is determined by either the termination of the last line (EOL/EOF character sequence) or at the beginning of a blank line at the end of the file.

This screenshot illustrates the default options for reading DSV files. These values can be changed when moving data using the Cazena Console.

![ DSV Options ](assets/documentation/data_movement_details/column_delimiter.png "Get Cazena Gateway IP Address")
{:.width-75}


#### Column Delimiter
By default, a comma is used as a column delimiter. The delimiter can be any printable ASCII character or tab character. Other non-printing or UTF-8 characters are not supported.

#### Header Row
* The file can optionally have one header row that contains column names.
* The rules for reading the header row are the same as for any row, using the same quoting, field delimiting, line delimiting and escaping.

#### Escape Character
* A backslash (\\) can be used as an escape key. 
  * __Example:__ `\n\t\f \075` results in `ntf 075`
* The backslash can escape itself. Doubling the backslash will include the escape character in the resulting field. 
    * __Example__: A double backslash in `abc\\def` results in `abc\def` 
* Backslashes cannot escape control characters or be used to include unicode, hexadecimal, or octal characters.

#### Text Quoting
Text delimiters can be used to include either line delimiters or column delimiters within a string. If you choose the option to use a text delimiter, then any string whose first non-space character is a quote will be interpreted as a quoted string. Nonquoted strings will be parsed verbatim.
{:.list}
* You can use either single quotes (‘) or double quotes (“) as a text delimiter. 
* Backslashes can escape the line delimiter, the field delimiter, or any text quote character. 
  * __Example:__ Including a newline (LF) in quotes in `"abc[LF]def"` results in `abc[LF]def`. LF is not treated as a line delimiter.
  * __Example:__ Including a comma in quotes in `"abc,def"` results in `abc,def`. The comma is not treated as a field delimiter.
* If you have selected the option to use backslash as an escape character, then backslashes will be applied within quoted strings. To include a backslash in the resulting field, use a double backslash. 
  * __Example:__ Escaping the quote in `"abc\"\"def"` results in `abc""def`           
* To include the text delimiter character within a string, double the character.  
  * __Example:__ Using double quotes in `"abc""""def"` results in `abc""def`              
* In general, leading and trailing spaces are ignored between the field delimiters. If leading and trailing spaces are significant, then text quoting needs to be used.
  * __Example:__ Quoting spaces in `"trailingSpaces            "` results in `trailingSpaces            `{:.show-whitespace} .


### Datatypes

In addition to strings as described in the previous sections, the following datatypes are recognized in DSV files.

Datatype		| Format		| Example
:----------------------------  |:--------------------- |:------------------------------------- 
date |	YYYY-MM-DD	|	5/17/15
time |	HH:MI:SS	|	25:51.2
timestamp |	YYYY-MM-DD HH:MI:SS	|	25:51.2
time with time zone |	HH:MI:SSTZ	|	14:25:51.246-06:00
timestamp with time zone |	YYYY-MM-DD HH:MI:SSTZ	|	2015-05-17 14:25:51.246-06:00
Integer	|	<sign><digits> Sign is optional	|	+1 -231 15 
Decimal / Floating point	|	\<sign\>\<digits\>.\<digits\><br>Sign is optional <br>Fractional component is optional Is a leading 0 required?	|	-123.45 2 3.00000
Null	|	\N	|	When `\N` is the only character in a field, it indicates the null value. Null-ness may not be preserved in all workload engines.


### Table and Column Names
When moving data, the source and target services may have different rules for valid table and column names. As a result, table or column names may be changed in any of the following ways:

* The name may be truncated, quoted or changed to make it unique.
* Invalid/unsupported characters may be substituted. For example, Amazon Redshift requires ASCII only characters.
* Reserved words may be removed from names.

If you [move data using the Cazena console](#import_ftp), these changes will be displayed during the review process. At that time, you can override the choices. 

### Data Store
See [Creating an Enterprise FTP/SFTP data store](#ent_ftp_data_store) or [Creating an Internet FTP/SFTP data store](#int_ftp_data_store) for information on creating data stores that are able to access the data on the server. 



