# README #

### About ###
```python-listcurator``` is a web service for managing a list of keys.  The
package comes with both a client and a service. The lists can be created in a
single Sqlite file or independent files.  The lists contain a minimum amount
of information, namely key value, expiration time, and a comment field.  The
service provides for some authentication, but this has not been extensively
tested.  The code needs more testing before it can be considered
production ready.  Use at your own risk.


#### Why didn't you use **redis**  or some other in-memory keystore?####

This was a side project to relearn SqlAlchemy and developing web
service APIs.  

### How do I get set up? ###

```service.py``` provides a basic set-up for the web service portion of this
project.   For basic authentication needs, users can be added to the
```test_data/test1.config```.  Optionally, the service can be run without any
authentication using ```-no_auth_users```, which is dangerous.  The
```-working_dir``` is where the lists databases are created and saved.

Typical command line is:
```python service.py -config_file test_data/test1.config -working_dir /tmp/```

The command above starts a ListCurator service on **0.0.0.0:45000** and all
the databases supporting lists are saved in ```/tmp/```.  The data used to
authenticate users based on an authorization key is read in from this file.

To implement a client, the unittests under ```./listcurator/test/``` provide
some basic examples.  These demonstrate how to create lists, add keys, and
render the plain-text files.

### Contribution guidelines ###

* If you want to contribute, I would be grateful.

### Client API and Service URIs ###

* **Client API=```listlists```** and **Server uri=```/list/lists```**:lists the
list present in the service.  The service does not automatically pre-load lists
in the ```working_dir``` when the service starts.  Issuing a ```listcreate```
will load this list and the unexpired keys.  

* **Client API=```listcreate```** and **Server uri=```/list/create```**: create
a list  

* **Client API=```listexists```** and **Server uri=```/list/exist```**: checks
for list in the service.

* **Client API=```listaddkeys```** and **Server uri=```/list/addkeys```**: add
keys to a particular list.  The client method takes a list of keys and a list
name to add the keys too.

* **Client API=```listaddkeyscomments```** and **Server uri=```/list/addkeyscomments```**: add
keys and comments to a particular list.  The client method takes a list name and
a list of lists or tuples (e.g. ```[["key", "comments for the key"], ...]```).

* **Client API=```listremovekeyscomments```** and **Server uri=```/list/removekeys```**: remove the listing of the key from the list database.

* **Client API=```listkeysexist```** and **Server uri=```/list/keysexist```**:
check to see of a list of keys exist in a list.

* **Client API=```listkeysinfo```** and **Server uri=```/list/keysinfo```**:
return the information listed for the key (e.g. expired, date/time of expiration,
  and comments).  The client requires a list name and a list of keys.

* **Client API=```listexpirekeys```** and **Server uri=```/list/expirekeys```**:
expire keys so that they are not rendered when a GET request for the list name
is issued by a client (e.g. ```/list/basicfile/{list_name}``` or
  ```/list/filecomments/{list_name}```).  See below for more information.

* **Client API=```listunexpirekeys```** and **Server uri=```/list/unexpirekeys```**:
unexpire keys so that they are rendered when a GET request for the list name
is issued by a client (e.g. ```/list/basicfile/{list_name}``` or
  ```/list/filecomments/{list_name}```).  See below for more information.


* **Client API=```get_basic```** and **Server uri=```/list/basicfile/{list_name}```**:
renders all unexpired keys in a list in a plain-text file.  Each key is rendered
on a new-line.  

* **Client API=```get_full```** and **Server uri=```/list/filecomments/{list_name}```**:
renders all unexpired keys along with the expiration date and comments in a list
in a plain-text file.  Each key is rendered on a new-line.  
