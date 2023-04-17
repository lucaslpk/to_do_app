# to_do_app
An app for creating and managing a 'To Do' list of tasks, written in Python and using PostgreSQL as permanent storage.


About the app

When I started writing this script the main purpose I had in mind was to demonstrate my ability to communicate with a database and to programmatically run SQL queries from a Python program level. There probably was an easier way to achieve this goal, but I wouldn’t be happy with anything less than a ‘functional’ app – and this is what it is. Yes, without a GUI the app is awkward to use, due to inherent flaws of Python IDE’s STDIN and STDOUT when used as a user interface, but it is nevertheless a fully functioning program that provides the user with the following functionalities:

    - show tasks and filter by: completed, not completed, overdue
    - sort tasks by: priority, date created, due date, id number
    - add/edit/remove a single task
    - batch mark tasks as completed
    - batch remove all completed tasks

About the code

A list of tasks to do, along with information like: description, priority, due date, completion status etc. is a fairly simple set of data – there is really only one table and no complex ‘many-to-many’ relationships and foreign keys are needed. All queries are relatively simple and easy to create with standard string methods. When ready, a query is stored in a string type variable and passed as an argument to methods imported from ‘psycopg2’ module – a Python driver for PostgreSQL.

As a QA measure, every time an SQL query – that is expected to make changes in the database (INSERT, UPDATE, REMOVE) – is run, there is a follow up SELECT query. Only if the second query confirms that changes to the database were made, a ‘Success’ message is printed on screen (STDOUT).

The code demonstrates handling of a fairly complex (for my current level) flow control, including handling exceptions. Some of the errors caught in the ‘try-except’ statements are standard Python errors and some are defined in the ‘psycopg2’ package. The single most time consuming task while writing this app was manual testing. Making sure that every path of execution is passed multiple times and with different data types/data sets required some imagination. I had to put myself in a user’s position and try every possibility for user error, like: inputting letters where a number is required, or multiple numbers where only 1 is needed; typing anything else than ‘Y’ or ‘N’ where user is given only ‘Yes/No’ option; typing in data in an incorrect format (most notably a datetime object) etc.

The code also features some data cleaning and type casting where needed, as well as some ‘workarounds’, like creating a dummy object in order to be able to use its class’s methods, that would otherwise not be accessible as module functions.
Github repository

You will find the source code oin my Github repository. Should you want to run the code and test the app yourself, you will need access to a PostgreSQL database and the ‘psycopg2’ package installed in your IDE environment. You will need to create a database/user/password on your localhost to match those in the source code or edit the code to match the database/user/password that you do have access to.

There is an ‘exampleToDoList()’ function that will insert some rows for testing. I included different statements for defining Due Date, like: NOW() + INTERVAL ’12 hour’ or  CURRENT_DATE + INTERVAL ’10 day’ – as a test. Those could be useful in the future if the app were to have “set due date X days from today” or “set due date Y hours from now” functionalities.

The ‘exampleToDoList()’ function should be run at least once if you want to insert test data and can be ‘#commented out’ later. If not commented out, the function will not insert duplicates, but…  there will be some unwanted behaviour.

Unlike some other SQL DBMSystems (i.e. MySQL) PostgreSQL does not support the ‘AUTO_INCREMENT’ property. Instead it uses data types: smallserial, serial and bigserial. These are not true types, but merely a notational convenience for creating unique identifier columns. The above mentioned unwanted behaviour is that every time the safeguard against duplicate entries is triggered ( ON CONFLICT (..) DO NOTHING), SERIAL passes to the next integer anyway, even if no INSERT action took place. That effectively makes it skip the id numbers.
