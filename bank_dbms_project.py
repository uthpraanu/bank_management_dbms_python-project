import mysql.connector

myconn = mysql.connector.connect(host="localhost", user="root", password="129", database="bank")
mycursor = myconn.cursor()


def create_account():
    import random
    import datetime

    r = str(random.randint(100, 500))
    t = datetime.datetime.today()
    sy = str(t.year)
    sm = str(t.month)
    sd = str(t.day)
    t1 = str(t.second)

    accno = (r + sy + sm + sd + t1)
    name = input("enter name:")
    add = input("Enter address:")
    mob = int(input("Enter moble no:"))
    email = input("Enter your email id: ")

    tyacc = input("Enter type of account:")
    intam = int(input("Enter the initial amount: "))

    d1 = datetime.datetime.now()
    t11 = str(d1.hour)
    t22 = str(d1.minute)
    t33 = str(d1.second)
    time = str(t11 + ':' + t22 + ':' + t33)
    date = str(sy + '-' + sm + '-' + sd)

    d1 = [name, accno, add, mob, email]

    sql = "INSERT INTO CUSTOMER(NAME,ACCOUNT_NUMBER,address,mobile_no,email_id) VALUES(%s,%s,%s,%s,%s)"
    d = [name, accno, add, mob, email]
    mycursor.execute(sql, d)
    myconn.commit()

    query = 'insert into ACCOUNT_DETAILS values(%s,%s,%s)'
    val = (accno, tyacc, intam)
    mycursor.execute(query, val)
    myconn.commit()

    print("Account created successfully!!")

    sql1 = "INSERT INTO TRANSACTION(ACCOUNT_NUMBER,AMOUNT_DEPOSITED,DATE_OF_DEPOSITION,TIME_OF_DEPOSITION,AMOUNT_WITHDRAWAL) VALUES (%s,%s,%s,%s,%s)"
    d1 = (accno, intam, date, time,0)
    mycursor.execute(sql1, d1)

    myconn.commit()
    print("Your account number is:", accno)


def deposit_money():
    import datetime
    d = datetime.date.today()
    sy = str(d.year)
    sm = str(d.month)
    sd = str(d.day)
    date = str(sy + '-' + sm + '-' + sd)

    acn = input("Enter your account number: ")
    q1 = "select account_number from customer "
    mycursor.execute(q1)
    l = mycursor.fetchall()
    s=[]
    for i in range(0,len(l)):
        s.append(l[i][0])

    if acn in s :
        t = "SELECT AMOUNT FROM ACCOUNT_DETAILS WHERE ACCNO = %s"
        mycursor.execute(t,([acn]))
        lili=mycursor.fetchall()
        for i in mycursor:
            for x in i:
                t = int(x)
        print("Balance left in your account: ", lili[0][0])
        print("\n")

        d4 = datetime.datetime.now()
        t1 = str(d4.hour)
        t2 = str(d4.minute)
        t3 = str(d4.second)
        t4 = str(t1 + ':' + t2 + ':' + t3)

        d1 = int(input("Enter the amount to be deposited: "))
        new = lili[0][0]+d1

        s1 = "UPDATE ACCOUNT_DETAILS SET AMOUNT=%s WHERE ACCNO=%s"
        val = (new, acn)
        mycursor.execute(s1, val)
        myconn.commit()

        s4 = "INSERT INTO TRANSACTION (ACCOUNT_NUMBER,AMOUNT_DEPOSITED,DATE_OF_DEPOSITION,TIME_OF_DEPOSITION,AMOUNT_WITHDRAWAL) VALUES (%s,%s,%s,%s,%s)"
        val3 = (acn, d1,date, t4,0)
        mycursor.execute(s4, val3)
        myconn.commit()
        print("Your amount has been deposited successfully!!")
    else :
        print("\nWrong account number !!\n ")

def withdraw_money():
    import datetime
    d = datetime.date.today()
    sy = str(d.year)
    sm = str(d.month)
    sd = str(d.day)
    date = str(sy + '-' + sm + '-' + sd)
    acn = input("Enter your account number: ")

    q1 = "select account_number from customer "
    mycursor.execute(q1)
    l = mycursor.fetchall()
    s = []
    for i in range(0, len(l)):
        s.append(l[i][0])

    if acn in s:
        s = "SELECT amount FROM ACCOUNT_DETAILS WHERE ACCNO=%s"
        mycursor.execute(s, ([acn]))
        lili=mycursor.fetchall()
        for i in mycursor:
            for x in i:
                t = int(x)
        print("Balance left in your account: ", lili[0][0])
        print("\n")

        d4 = datetime.datetime.now()
        t1 = str(d4.hour)
        t2 = str(d4.minute)
        t3 = str(d4.second)
        t4 = str(t1 + ':' + t2 + ':' + t3)

        d1 = int(input("Enter the amount to be withdrawn: "))
        new = lili[0][0]-d1
        if new < 0 :
            print("You don't have enough balance")
            return;
        else :
            s1 = "UPDATE ACCOUNT_DETAILS SET amount=%s WHERE accno=%s"
            val = (new, acn)
            mycursor.execute(s1, val)
            myconn.commit()

            s4 = "INSERT INTO TRANSACTION (ACCOUNT_NUMBER,AMOUNT_DEPOSITED,DATE_OF_DEPOSITION,TIME_OF_DEPOSITION,AMOUNT_WITHDRAWAL) VALUES (%s,%s,%s,%s,%s)"
            val3 = (acn, 0, date, t4,d1)
            mycursor.execute(s4, val3)
            myconn.commit()
            print("Your amount has been withdrawn successfully!!")
    else :
        print("\nWrong account number !!\n ")


def transfer_money():
    sender = input("Enter Your Account Number : ")
    receiver = input("Enter Account Number, to whom you wish to transfer : ")

    q="select account_number from customer "
    mycursor.execute(q)
    lk=mycursor.fetchall()
    acc = []
    for r in lk:
        acc.append(r[0])

    if sender not in acc:
        print("Sender account not found")
        return;
    elif receiver not in acc:
        print("Receiver account not found")
        return;
    else :
        mon = int(input("Enter the amount : "))
        q1 = "select amount from account_details where accno = %s"
        mycursor.execute(q1,([sender]))
        l=mycursor.fetchall()
        m = l[0][0]
        m =  m - mon

        if m < 0:
            print("You dont have enough money  ")
            return;

        q1 = "update account_details set amount = %s where accno = %s"
        val = [m, sender]
        mycursor.execute(q1, val)

        q1 = "select amount from account_details where accno = %s"
        mycursor.execute(q1,([receiver]))
        l = mycursor.fetchall()
        m=l[0][0]

        m= m + mon

        q1 = "update account_details set amount = %s where accno = %s"
        val = (m, receiver)
        mycursor.execute(q1, val)
        myconn.commit()
        print("Transacton sucessfull")



def balance_enquiry():
    acn = input("Enter your account number: ")
    s = "SELECT amount FROM ACCOUNT_details WHERE ACCNO=%s"
    mycursor.execute(s, ([acn]))
    for i in mycursor:
        for x in i:
            t = int(x)
    print("You have Rs.", t, "left in your account")


def Account_holder():
    sql = "SELECT c.name,d.accno,d.type_of_account,d.amount from account_details as d,customer as c where c.account_number = d.accno"
    mycursor.execute(sql)
    for x in mycursor:
        print(x)


def close_account():
    acn = input("Enter your account number: ")
    sql1 = "DELETE FROM account_details WHERE accno=%s"
    mycursor.execute(sql1, ([acn]))
    myconn.commit()
    sql2 = "DELETE FROM customer WHERE account_number=%s"
    mycursor.execute(sql2, ([acn]))
    myconn.commit()
    print("Your account has been deleted")


def modify_account():
    print("Which information you want to modify?")
    print("1.Name")
    print("2.Address")
    print("3.Mobile no.")
    print("4.Email id")
    print("5.Type of account")
    print("\n")
    c = int(input("Enter your choice:"))
    print("\n")
    if c == 1:
        acn = input("Enter account no: ")
        sql = "SELECT * from CUSTOMER where ACCOUNT_NUMBER=%s"
        N = input("Enter new name: ")
        qry = "UPDATE customer set Name=%s WHERE ACCOUNT_NUMBER=%s"
        d = (N, acn)
        mycursor.execute(qry, d)
        print("Record updated")
        myconn.commit()
    elif c == 2:
        acn = int(input("Enter account no: "))
        sql = "SELECT * from CUSTOMER where ACCOUNT_NUMBER=%s"
        a = input("Enter new address:")
        qry = "UPDATE customer set address=%s WHERE Account_number=%s"
        d = (a, acn)
        mycursor.execute(qry, d)
        print("Record updated")
        myconn.commit()
    elif c == 3:
        acn = int(input("Enter account no: "))
        sql = "SELECT * from CUSTOMER where ACCOUNT_NUMBER=%s"
        m = int(input("Enter new mobile no: "))
        qry = "UPDATE customer set mobile_no=%s WHERE Account_number=%s"
        d = (m, acn)
        mycursor.execute(qry, d)
        print("Record updated")
        myconn.commit()
    elif c == 4:
        acn = int(input("Enter account no: "))
        sql = "SELECT * from CUSTOMER where ACCOUNT_NUMBER=%s"
        e = input("Enter new email_id:")
        qry = "UPDATE customer set email_id=%s WHERE Account_number=%s"
        d = (e, acn)
        mycursor.execute(qry, d)
        print("Record updated")
        myconn.commit()
    elif c == 5:
        acn = int(input("Enter account no: "))
        sql = "SELECT * from CUSTOMER where ACCOUNT_NUMBER=%s"
        a = input("Enter new type of account:")
        qry1 = "UPDATE Account_details set type_of_account=%s WHERE Account_number=%s"
        d = (a, acn)
        mycursor.execute(qry1, d)
        print("Record updated")
        myconn.commit()
    else:
        print("Invaild input")


def loop():
    while True:
        print("\n")
        print("TASKS TO BE PERFORMED....!!\n")

        print("1. To create a new account")
        print("2. To Deposit Amount")
        print("3. To Withdraw Amount")
        print("4. Transfer to an another account")
        print("5. To Balance Enquiry")
        print("6. All account Holder list")
        print("7. Close an account")
        print("8. Modify an account")
        print("9. To Exit")
        print("\n")
        ch = int(input("Enter your choice:"))
        print("\n")
        if ch == 1:
            create_account()
            print("\n")
        elif ch == 2:
            deposit_money()
            print("\n")
        elif ch == 3:
            withdraw_money()
            print("\n")
        elif ch==4:
            transfer_money()
            print("\n")
        elif ch == 5:
            balance_enquiry()
            print("\n")
        elif ch == 6:
            Account_holder()
            print("\n")
        elif ch == 7:
            close_account()
            print("\n")
        elif ch == 8:
            modify_account()
            print("\n")
        elif ch == 9:
            print("Exiting!!")
            break
        else:
            print("....Please enter a valid choice")


print("\n")
print("*........WELCOME........*")
print("\n")
while(True):
    inp = input(("\nAre you registered with our online service? \n Enter 'y' to yes and 'n' to no; e to exit: "))
    if inp.lower()=="y":
        print("\n")
        user_name = input('Enter your username :- ')
        password1 = input('Enter your password :- ')
        value = (user_name, password1)
        query = "select * from login_details where username=%s and password=%s "
        mycursor.execute(query, value)
        if mycursor.fetchone() is None:
            print("....Login Unsuccessful")
            print("Incorrect username or password!!")
        else:
            print("\n\n....Login Successful!!\n\n")
            loop()
    elif inp.lower()=="n":
        print("\n")
        us = input('Create your username :- ')
        p = input('Create your password :- ')

        query = 'insert into login_details values(%s,%s)'
        val = (us, p)
        mycursor.execute(query, val)
        myconn.commit()
        print("Your account is registered in online mode")
        loop()
    elif inp.lower()=="e":
        break;
    else:
        print("\nPlease enter a valid input \n")



