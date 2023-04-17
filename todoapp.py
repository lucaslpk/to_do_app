import psycopg2 
import datetime

def opt1(cursor) : 
    opt = 0
    while True :
        options = '''
        Show tasks:
        1) Completed.
        2) Not completed.
        3) All.
        4) Overdue.
        5) Return to main menu.
        ---------------------------
        Choose option (1 to 4): '''
        opt = int(input(options))
        if opt == 1 :
            sql = "SELECT * FROM todo_list WHERE completed = 'YES'"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 2 :
            sql = "SELECT * FROM todo_list WHERE completed = 'NO'"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 3 :
            sql = "SELECT * FROM todo_list"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 4 :
            sql = "SELECT * FROM todo_list WHERE due_date < NOW() AND completed = 'NO'"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 5 :
            return
        else :
            print(opt, "is not a valid option. Try again.")

def opt2(cursor) : 
    opt = 0
    while True :
        options = '''
        Sort tasks by:
        1) Priority.
        2) Due date (earliest first).
        3) Due date (latest first)
        4) Date created
        5) ID Number
        6) Return to main menu.
        ---------------------------
        Choose option (1 to 6): '''
        opt = int(input(options))
        if opt == 1 :
            sql = "SELECT * FROM todo_list ORDER BY priority"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 2 :
            sql = "SELECT * FROM todo_list ORDER BY due_date"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 3 :
            sql = "SELECT * FROM todo_list ORDER BY due_date DESC"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 4 :
            sql = "SELECT * FROM todo_list ORDER BY created_at"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 5 :
            sql = "SELECT * FROM todo_list ORDER BY id"
            runQueryAndPrintTable(cursor, sql)
        elif opt == 6 :
            return
        else :
            print("--------------------------------------")
            print(opt, "is not a valid option. Try again.")

def opt3(cursor, conn) : 
    opt = 0
    while True :
        options = '''
        Add/Edit/Remove a task.:
        1) Add
        2) Edit
        3) Remove
        4) Return to main menu.
        ---------------------------
        Choose option (1 to 4): '''
        opt = int(input(options))
        if opt == 1 :
            job_name = input("Type in a task description (max.26 characters): ")
            if len(job_name) > 26 :
                print("------------------------------------------------------")
                print("Max lenght of description is 26 characters. Try again.")
            else :
                try :
                    priority = int(input("Assign priority from 1 to 5: "))
                    if priority not in range(1, 6) :
                        print("----------------------------------------------")
                        print("Priority has to be between 1 and 5. Try again.")
                    else :
                        due_date = input("Type in a Due Date AND Time (i.e 2020-01-01 12:00:00) or press Enter if no Due Date: ")
                        if due_date != '' :
                            try :
                                d = datetime.datetime(2000,1,1)   #creating a dummy object of datetime class to run a strptime METHOD instead of strptime function from time module, which seems to be nonexistent!
                                d = d.strptime(due_date, '%Y-%m-%d %H:%M:%S') # object used to check if user input is convertible to a datetime object
                            except ValueError :
                                print("--------------------------------------------")
                                print("Date and/or Time format incorrect. Try again")
                                continue

                            sql = "INSERT INTO todo_list(job_name, priority, created_at, due_date, completed) VALUES ('"+job_name+"', '"+str(priority)+"', NOW(), '"+str(due_date)+"', 'NO');"
                        else: 
                            sql = "INSERT INTO todo_list(job_name, priority, created_at, due_date, completed) VALUES ('"+job_name+"', '"+str(priority)+"', NOW(), NULL, 'NO');"
                            print(sql)
                        try :
                            cursor.execute(sql)
                            conn.commit()
                            sql = "SELECT * FROM todo_list WHERE job_name = '"+str(job_name)+"';" 
                            print("--------------")
                            print("Created task: ")
                            runQueryAndPrintTable(cursor, sql)

                        except psycopg2.errors.UniqueViolation :
                            print("--------------")
                            print("Task with name '{}' already exist. Try different name.".format(job_name))

                except ValueError :
                    print("-------------------------")
                    print("Try a number this time...")
        elif opt == 2 :      
            print("--------------------------------------------")
            id_to_edit = int(input("Type in the id number of task to be edited: ")) # there is a potential ValueError here which won't be dealt with but will be passed 'up the stack' to be dealt with by main()
            sql = 'SELECT id FROM todo_list'    
            cursor.execute(sql)
            tempList = cursor.fetchall()  # returns [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)] so a list where every element is a 1-element tuple. Strange...
            for i in range(len(tempList)) :             # enhanced 'for item in List' doesn't do the trick - it takes items from the list but the result of any operations on it is not saved back to List
                tempList[i] = tempList[i][0]
            if id_to_edit not in tempList :
                print("----------------------------------------------")
                print("There is no task with a given ID No. Try again.")
            else :
                sql = "SELECT * FROM todo_list WHERE id = "+str(id_to_edit)+";"
                runQueryAndPrintTable(cursor, sql)
                try :
                    options = '''
        Choose what you want to edit:
        1) Job description (max 26 characters).
        2) Priority (1-5).
        3) Due Date (or remove Due Date).
        4) Completion status (Y/N).
        5) Return to main menu.
        ---------------------------
        Choose option (1 to 4): '''
                    opt = int(input(options))
                    if opt not in range(1,6) :
                        print("--------------------------------------")
                        print(opt, "is not a valid option. Try again.")
                    elif opt == 5 :
                        continue
                    else :
                        sql = "SELECT * FROM todo_list WHERE id = "+str(id_to_edit)+";" 
                        cursor.execute(sql)
                        row = cursor.fetchall() 
                        print(row)   
                        print(type(row[0][4]))         
                        job_name = row[0][1]     # row is a 1-element list containing a tuple, and tuple is immutable, easier and clearer to break it in to 6 variables and later put a query back together
                        priority = row[0][2]
                        due_date = row[0][4] 
                        if due_date is None :    # you cant use == operator here because None != None just like null != null in JS
                            due_date = ''
                        completed = row[0][5]
                        if opt == 1 :
                            job_name = input("Type in a task description (max.26 characters): ")
                            if len(job_name) > 26 :
                                print("------------------------------------------------------")
                                print("Max lenght of description is 26 characters. Try again.")
                                continue
                        elif opt == 2 :
                            try :
                                priority = int(input("Assign priority from 1 to 5: "))
                                if priority not in range(1, 6) :
                                    print("----------------------------------------------")
                                    print("Priority has to be between 1 and 5. Try again.")
                                    continue
                            except ValueError :
                                print("-------------------------")
                                print("Try a number this time...")
                                continue
                        elif opt == 3 :
                            due_date = input("Type in a Due Date AND Time (i.e 2020-01-01 12:00:00) or press Enter if no Due Date: ")
                            if due_date != '' :
                                try :
                                    d = datetime.datetime(2000,1,1)   #creating a dummy object of datetime class to run a strptime METHOD instead of strptime function from time module, which seems to be nonexistent!
                                    d = d.strptime(due_date, '%Y-%m-%d %H:%M:%S') # using dummy object to check if user input is convertible to a datetime object, if STDIN string (due_date) incorrect => ValueError
                                except ValueError :
                                    print("--------------------------------------------")
                                    print("Date and/or Time format incorrect. Try again")
                                    continue
                        elif opt == 4 :
                            completed = input("Enter completion status (Y/N): ").upper() 
                            if completed not in ('Y', 'N', 'YES', 'NO') :
                                print("-------------------------")
                                print("Choose from Yes or No options ONLY.")
                                continue
                            if completed == 'Y' :
                                completed = 'YES'
                            if completed == 'N' :
                                completed = 'NO'

                        if due_date != '' :
                            sql = '''UPDATE todo_list SET
                                    job_name = '{}',
                                    priority =  {},
                                    due_date = '{}',
                                    completed ='{}'
                                    WHERE id =  {};'''.format(job_name,priority,due_date,completed,id_to_edit)    
                        else: 
                            sql = '''UPDATE todo_list SET
                                    job_name = '{}',
                                    priority =  {},
                                    due_date = NULL,
                                    completed ='{}'
                                    WHERE id =  {};'''.format(job_name,priority,completed,id_to_edit)
                        
                        cursor.execute(sql)
                        conn.commit()
                        sql = "SELECT * FROM todo_list WHERE id = "+str(id_to_edit)+";" 
                        print("--------------")
                        print("Updated task: ")
                        runQueryAndPrintTable(cursor, sql)

                except ValueError :
                    print("Try a number this time...")

        elif opt == 3 :
            try :
                id_to_del = int(input("Type in the id number of task to be removed: "))
                sql = 'SELECT id FROM todo_list'    
                cursor.execute(sql)
                tempList = cursor.fetchall()  # returns [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)] so a list where every element is a 1-element tuple. Strange...
                for i in range(len(tempList)) :
                    tempList[i] = tempList[i][0]
                if id_to_del not in tempList :
                    print("----------------------------------------------")
                    print("There is no task with a given ID No. Try again.")
                else :
                    sql = "SELECT * FROM todo_list WHERE id = "+str(id_to_del)+";"
                    runQueryAndPrintTable(cursor, sql)
                    opt = input("Are you sure you want to remove the above tasks?(Y/N): ").upper() 
                    if opt in ('Y', 'YES') :
                        sql = "DELETE FROM todo_list WHERE id = "+str(id_to_del)+";"
                        cursor.execute(sql)
                        conn.commit()
                        sql = "SELECT COUNT (*) FROM todo_list WHERE id = {};".format(id_to_del)
                        cursor.execute(sql)
                        if cursor.fetchall()[0][0] == 0 :
                            print("------------------------------------------")
                            print("Task No", id_to_del, "succesfully removed.")
                        else :
                            print("----------------------------------------------------------------")
                            print("Something went wrong. Go to: Main Menu --> Show tasks to verify.")
                    elif opt in ('N', 'NO') :
                        continue
                    else :
                        print("------------------------------")
                        print("Choose from Yes or No options.")
            except ValueError :
                print("-------------------------")
                print("Try a number this time...")
        elif opt == 4 :
            return
        else :
            print("--------------------------------------")
            print(opt, "is not a valid option. Try again.")

def opt4(cursor, conn) :
    #while True:
        sql = "SELECT * FROM todo_list WHERE completed = 'NO'"
        runQueryAndPrintTable(cursor, sql)
        print("------------------------------------------------------------------------")
        try :
            userTasksList = [int(x) for x in input("Enter a space separated list of task numbers to be marked as completed or 'Q' to quit: ").split()]
            
            sql = "SELECT id FROM todo_list WHERE completed = 'NO'"
            cursor.execute(sql)
            incompList = cursor.fetchall()
            for i in range(len(incompList)) :   # conversion from a list of tuples to a normal list
                incompList[i] = incompList[i][0]
            toMarkList = [0]                      # '0' is inserted as a dummy element otherwise in case of only 1 task to be marked, list would be converted to 1 element tuple and trigger an SQL error
            nonExList = []
            for item in userTasksList :         # you cannot pop item from the list while you iterate it or you will loose data. 
                if item in incompList :
                    toMarkList.append(item)     # splitting the list in 2: valid and invalid data - both sets need to be used later, hence 2 additional lists.
                else :
                    nonExList.append(item)      # 4 different lists are used in here!!! Does the job but looks messy. There has to be a more elegant solution

            if len(nonExList) > 0 :        
                print("----------------------------------------------")
                print("The following tasks IDs don't exist {}.".format(tuple(nonExList)))

            sql = "SELECT * FROM todo_list WHERE id IN {}".format(tuple(toMarkList)) # the sql IN operator takes arguments in (round) brackets - in Python that is a tuple, hence conversion - list would be pasted in the query with [square] brackets
            runQueryAndPrintTable(cursor, sql)
            opt = input("Are you sure you want to mark the above task(s) as completed?(Y/N): ").upper() 
            if opt in ('Y', 'YES') :
                sql = "UPDATE todo_list SET completed = 'YES' WHERE id IN {}".format(tuple(toMarkList));
                cursor.execute(sql)
                conn.commit()
                print("--------------------------------------------------------------------")
                print("List succesfully updated. The following tasks are stil not completed") 
                sql = "SELECT * FROM todo_list WHERE completed = 'NO'"
                runQueryAndPrintTable(cursor, sql)
                return
            elif opt in ('N', 'NO') :
                return
            else :
                print("-----------------------------------")
                print("Choose from Yes or No options ONLY.") 
                  
        except ValueError :
            print("-------------------------------------")
            print("Enter space separated numbers only...")

def opt5(cursor, conn) :
    while True :
        sql = "SELECT * FROM todo_list WHERE completed = 'YES'"
        runQueryAndPrintTable(cursor, sql)
        sql = "SELECT COUNT (*) FROM todo_list WHERE completed = 'YES';"
        cursor.execute(sql)
        count = cursor.fetchall()
        count = count[0][0]
        opt = input("Are you sure you want to remove {} completed task(s)?(Y/N): ".format(count)).upper() 
        if opt in ('Y', 'YES') :
            sql = "DELETE FROM todo_list WHERE COMPLETED = 'YES'"
            cursor.execute(sql)
            conn.commit()
            sql = "SELECT COUNT (*) FROM todo_list WHERE completed = 'YES';"
            cursor.execute(sql)
            if cursor.fetchall()[0][0] == 0 :
                print("------------------------------------------")
                print(count, "completed tasks succesfully removed")
            else :
                print("----------------------------------------------------------------")
                print("Something went wrong. Go to: Main Menu --> Show tasks to verify.")
            return   
        elif opt in ('N', 'NO') :
            return
        else :
            print("------------------------------")
            print("Choose from Yes or No options ONLY.")

def runQueryAndPrintTable(cursor, sql) :
    cursor.execute(sql)
    table = cursor.fetchall()
    print("-----+------------------------------+----------+----------------------------+----------------------------+------------")
    print("| id |           job_name           | priority |         created_at         |          due_date          | completed |")
    print("-----+------------------------------+----------+----------------------------+----------------------------+------------")
    for row in table:
        row = list(row)
        tempRow = []
        for item in row :
            item = str(item)            # have to convert datetime object to string
            tempRow.append(item)
        print('| {:2} | {:<28} | {:^8} | {:<26} | {:<26} | {:^9} |'.format(*tempRow))
    print("-----+------------------------------+----------+----------------------------+----------------------------+------------")

def main() :
    conn = psycopg2.connect(       
    database='exercises',
    user='lucaslpk',
    password='password',
    host='localhost',
    port='5432')
    cursor = conn.cursor() 
    opt = 0
    while True :
        try :
            options = '''
        Available options:
        1) Show tasks.
        2) Sort tasks.
        3) Add/Edit/Remove a task.
        4) Mark as completed.
        5) Remove completed tasks.
        6) Quit app.
        ---------------------------
        Choose option (1 to 6): '''
            opt = int(input(options))
            if opt == 1 :
                opt1(cursor)
            elif opt == 2 :
                opt2(cursor)
            elif opt == 3 :
                opt3(cursor, conn)
            elif opt == 4 :
                opt4(cursor, conn)
            elif opt == 5 :
                opt5(cursor, conn)
            elif opt == 6 :
                conn.close()
                quit()
            else :
                print(opt, "is not a valid option. Try again.")
        except ValueError :
            print("-----------------------------------------------------")
            print("Options have to be numbers and not letters. Try again")
        except psycopg2.errors.InFailedSqlTransaction :
            print("----------------------------------------------------------------------------")
            print("SQL Transaction Failed. Something went wrong but IDK what exactly. Try again")

def exampleToDoList () :
    conn = psycopg2.connect(       
    database='exercises',
    user='lucaslpk',
    password='password',
    host='localhost',
    port='5432')
    cursor = conn.cursor()  

    sql = '''
    CREATE TABLE IF NOT EXISTS todo_list(
        id SERIAL PRIMARY KEY,
        job_name VARCHAR(28) UNIQUE NOT NULL,
        priority INT NOT NULL CHECK (priority BETWEEN 1 AND 5),
        created_at TIMESTAMP NOT NULL,
        due_date TIMESTAMP,
        completed VARCHAR(3) CHECK (completed IN ('YES', 'NO'))        
    );'''

    cursor.execute(sql)

    sql = '''
    INSERT INTO todo_list(job_name, priority, created_at, due_date, completed) 
    VALUES  ('paint nails', 2, NOW(), '2023-04-24 10:10:53.163', 'NO'),
            ('buy groceries', 5, NOW(), NULL, 'NO'),
            ('wash dishes', 3, NOW(), '2023-04-14 10:00:00', 'NO'),
            ('take out trash', 1, '2023-03-19', NOW() + INTERVAL '1 day', 'YES'),
            ('cook dinner', 4, '2023-04-15 12:00:00', '2023-04-15 21:00:00', 'NO'),
            ('call Howard', 1, '2023-04-15', '2023-04-20', 'YES'),
            ('do homework', 5, NOW(), '2023-04-17 10:00:00', 'NO'),
            ('take the dog for a walk', 3, NOW(), CURRENT_DATE + INTERVAL '21 hour', 'NO'), 
            ('order snacks for next Sunday', 2, '2023-04-12', '2023-04-21', 'NO')
    ON CONFLICT (job_name) DO NOTHING;'''

    cursor.execute(sql)

    print("Sample todo List inserted successfully...")

    conn.commit()
    conn.close()

exampleToDoList()
main()