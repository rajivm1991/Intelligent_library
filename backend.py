import csv,os,time

#~ print(help('csv.DictReader'))
cwd             = os.getcwd()
data_dir        = os.path.join(cwd, 'Data')
book_fields     = ['book_no', 'book_name', 'book_author', 'book_publisher']
staff_fields    = ['staff_name', 'designation', 'staff_id']
status_fields   = ['book_no', 'in_out_status', 'date', 'staff_id', 'note']

def Is_book_found(book_no):
    if(os.path.exists( os.path.join(data_dir, 'Books.csv') )):
        for book, status in List_all_books():
            if(book['book_no'] == book_no):
                return status['in_out_status']
    return False

def get_book_info(book_no='nil', book_name='nil'):
    if(book_no != 'nil'):
        for book, status in List_all_books():
            if(book['book_no'] == book_no):
                return book
    elif(book_name != 'nil'):
        for book, status in List_all_books():
            if(book['book_name'] == book_name):
                return book
    return False

def Add_new_book( book, status='nil'):
    if(not Is_book_found(book['book_no'])):
        for key in book_fields:
            book[key] = book[key].replace(',',';')

        BookShelf   = open( os.path.join(data_dir, 'Books.csv'), 'a' )
        writer      = csv.DictWriter( f=BookShelf, fieldnames=book_fields )
        writer.writerow(book)
        BookShelf.close()
        #~ --------------------
        StatusRegister  = open( os.path.join(data_dir, 'Status.csv'), 'a' )
        writer          = csv.DictWriter( f=StatusRegister, fieldnames=status_fields )
        if(status == 'nil'):
            d = time.localtime()
            status =    {   'book_no'       : book['book_no'],
                            'in_out_status' : 'IN',
                            'date'          : '%d/%d/%d'%(d.tm_mday,d.tm_mon,d.tm_year),
                            'staff_id'      : '-',
                            'note'          : 'newly added'
                        }
        writer.writerow(status)
        StatusRegister.close()
        print('book', book['book_no'], 'inserted')
        return('book', book['book_no'], 'inserted')
    else:
        print('book', book['book_no'], 'already there')
        return('book', book['book_no'], 'already there')

def Delete_a_book(book_no):
    if( Is_book_found(book_no) ):
        old_BookShelf   = open( os.path.join(data_dir, 'Books.csv'), 'r')
        NewBookList     = [ book for book in csv.DictReader( f=old_BookShelf, fieldnames=book_fields ) if(book['book_no'] != book_no) ]
        old_BookShelf.close()

        new_BookShelf   = open( os.path.join(data_dir, 'Books.csv'), 'w')
        csv.DictWriter( f=new_BookShelf, fieldnames=book_fields ).writerows(NewBookList)
        new_BookShelf.close()

        # --------------------

        old_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'r')
        NewStatusList   = [ status for status in csv.DictReader( f=old_StatusReg, fieldnames=status_fields ) if(status['book_no'] != book_no) ]
        old_StatusReg.close()

        new_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'w')
        csv.DictWriter( f=new_StatusReg, fieldnames=status_fields ).writerows(NewStatusList)
        new_StatusReg.close()

        print('book',book_no,'has been deleted')
        return('book',book_no,'has been deleted')
    else:
        print('book',book_no,'not found')
        return('book',book_no,'not found')

def Modify_a_book(book_no, modified_book):
    if( Is_book_found(book_no) ):
        for key in book_fields:
            modified_book[key] = modified_book[key].replace(',',';')

        old_BookShelf   = open( os.path.join(data_dir, 'Books.csv'), 'r')
        NewBookList     = [ book if(book['book_no'] != book_no) else modified_book for book in csv.DictReader( f=old_BookShelf, fieldnames=book_fields ) ]
        old_BookShelf.close()

        new_BookShelf   = open( os.path.join(data_dir, 'Books.csv'), 'w')
        csv.DictWriter( f=new_BookShelf, fieldnames=book_fields ).writerows(NewBookList)
        new_BookShelf.close()

        # --------------------

        old_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'r')
        NewStatusList   = [ status if(status['book_no'] != book_no) else    {   'book_no'       :   modified_book['book_no'],
                                                                                'in_out_status' :   status['in_out_status'],
                                                                                'date'          :   status['date'],
                                                                                'staff_id'      :   status['staff_id'],
                                                                                'note'          :   status['note']
                                                                            } for status in csv.DictReader( f=old_StatusReg, fieldnames=status_fields ) ]
        old_StatusReg.close()

        new_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'w')
        csv.DictWriter( f=new_StatusReg, fieldnames=status_fields ).writerows(NewStatusList)
        new_StatusReg.close()

        print('book',book_no,'has been modified')
        return('book',book_no,'has been modified')
    else:
        print('book',book_no,'not found')
        return('book',book_no,'not found')

def Mk_book_transaction(book_no, in_out_status, date, staff_id, note=''):
    trans = {'book_no':book_no, 'in_out_status':in_out_status, 'date':date, 'staff_id':staff_id, 'note':note}

    book_status = Is_book_found(book_no)
    if  (book_status in ['IN', 'OUT']):
        if  (in_out_status != book_status):
            if  (Is_staff_found(staff_id)):
                old_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'r')
                NewStatusList   = [ status if(status['book_no'] != book_no) else trans for status in csv.DictReader( f=old_StatusReg, fieldnames=status_fields ) ]
                old_StatusReg.close()

                new_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'w')
                csv.DictWriter( f=new_StatusReg, fieldnames=status_fields ).writerows(NewStatusList)
                new_StatusReg.close()

                print('book',book_no,'is "',in_out_status,'" @', date,'by staff', staff_id)
            else:
                print('Wrong trasaction, staff "', staff_id, '" not found in staff Register')
        else:
            print('Wrong trasaction, book "',book_no,'" is already "',in_out_status,'"')
    else:
        print('Wrong trasaction, book "',book_no,'" is not in Library book list')

def List_all_books():
    Books   = csv.DictReader( f=open( os.path.join(data_dir, 'Books.csv' ), 'r'), fieldnames=book_fields    )
    Status  = csv.DictReader( f=open( os.path.join(data_dir, 'Status.csv'), 'r'), fieldnames=status_fields  )
    return zip(Books, Status)

def Search_books(key):
    Ret = ''
    for book, status in List_all_books():
        if(True in [key in book[x].lower() for x in book_fields]):
            Ret += '''no      :   %s
name    :   %s
author  :   %s
publish :   %s
status  :   %s

'''%(   book['book_no'],
        book['book_name'],
        book['book_author'],
        book['book_publisher'],
        'IN' if(status['in_out_status']=='IN') else 'OUT to '+Is_staff_found(staff_id=status['staff_id'])
    )
    return(Ret)

def List_all_staffs():
    Staffs   = csv.DictReader( f=open( os.path.join(data_dir, 'Staffs.csv' ), 'r'), fieldnames=staff_fields    )
    return Staffs

def Is_staff_found(staff_id='nil', staff_name='nil'):
    if(os.path.exists( os.path.join(data_dir, 'Staffs.csv') )):
        for staff in csv.DictReader( f=open( os.path.join(data_dir, 'Staffs.csv'), 'r'), fieldnames=staff_fields  ):
            if(staff_id != 'nil'):
                if(staff['staff_id'] == staff_id):
                    return staff['staff_name']
            else:
                if(staff['staff_name'] == staff_name):
                    return staff['staff_id']
    return False

def Delete_a_staff(staff_id):
    if( Is_staff_found(staff_id) != False ):
        old_StaffReg    = open( os.path.join(data_dir, 'Staffs.csv'), 'r')
        NewStaffList    = [ staff for staff in csv.DictReader( f=old_StaffReg, fieldnames=staff_fields ) if(staff['staff_id'] != staff_id) ]
        old_StaffReg.close()

        new_StaffReg    = open( os.path.join(data_dir, 'Staffs.csv'), 'w')
        csv.DictWriter( f=new_StaffReg, fieldnames=staff_fields ).writerows(NewStaffList)
        new_StaffReg.close()

        print('staff', staff_id, 'has been deleted')
        return('staff', staff_id, 'has been deleted')
    else:
        print('staff', staff_id, 'not found in register')
        return('staff', staff_id, 'not found in register')

def Add_new_staff( staff ):
    print(staff)
    if(Is_staff_found(staff['staff_id']) == False):
        StaffReg    = open( os.path.join(data_dir, 'Staffs.csv'), 'a' )
        writer      = csv.DictWriter( f=StaffReg, fieldnames=staff_fields )
        writer.writerow(staff)
        StaffReg.close()
        #~ --------------------
        print('staff', staff['staff_name'], 'added in Register')
        return('staff', staff['staff_name'], 'added in Register')
    else:
        print('staff', staff['staff_name'], 'already there')
        return('staff', staff['staff_name'], 'already there')

if(__name__ == '__main__'):
    ''
    #~ 'book_no', 'in_out_status', 'date', 'staff_id'
    x = input('Do u want to reset the library data (y/n)?\n')
    if(x.lower() == 'y'):
        Books   = csv.DictReader( f=open( os.path.join(data_dir, 'Books.csv' ), 'r'), fieldnames=book_fields    )
        new_StatusReg   = open( os.path.join(data_dir, 'Status.csv'), 'w')
        writer = csv.DictWriter( f=new_StatusReg, fieldnames=status_fields )

        for book in Books:
            writer.writerow(    {   'book_no'       :   book['book_no'],
                                    'in_out_status' :   'IN',
                                    'date'          :   '01/04/2012',
                                    'staff_id'      :   '~',
                                    'note'          :   '~'
                                }   )
        print('All books are set to status "IN"')
    else:
        print('Library data not affected')
    #~ new_StatusReg.close()

    #~ for i in range(10):
        #~ Add_new_book(   {   'book_no'       :'%d'%(i),
                            #~ 'book_name'     :'b_name_%d'%(i),
                            #~ 'book_author'   :'b_author_%d'%(i),
                            #~ 'book_publisher':'b_pub_%d'%(i)
                        #~ }   )

    #~ Delete_a_book('2')

    #~ Delete_a_staff('1')
    #~ Add_new_staff   (   {   'staff_id'  : '1',
                            #~ 'designation': 'staff',
                            #~ 'staff_name': 'staff_name_1'
                        #~ }   )
    #~ Delete_a_staff('2')

    #~ print( 'Found' if(Is_book_found('8')) else 'Not Found' )
    #~ print( 'Found' if(Is_book_found('2')) else 'Not Found' )

    #~ Mk_book_transaction(book_no='3', in_out_status='IN' , date='26/3/2012', staff_id='2')
    #~ Mk_book_transaction(book_no='3', in_out_status='IN' , date='26/3/2012', staff_id='30433002')
    #~ Mk_book_transaction(book_no='3', in_out_status='OUT', date='26/3/2012', staff_id='1')
    #~ Mk_book_transaction(book_no='3', in_out_status='OUT', date='26/3/2012', staff_id='1')
