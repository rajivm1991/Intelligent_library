from tkinter.tix import *
from tkinter.ttk import Treeview
import backend as library
import time

global global_bucket
global_bucket = {}

class Library_Handler:
    def __init__(self, w):
        self.root = w

    def MainBook(self):
        top = self.root
        book = NoteBook(top, ipadx=5, ipady=5, options="""
        tagPadX 6
        tagPadY 4
        borderWidth 2
        """)
        book.add('home', label="Library Home Page",
            createcmd=lambda book=book, name='home': MakeHome(book, name))
        book.add('update', label="Update Library Datas",
            createcmd=lambda book=book, name='update': UpdateLibrary(book, name))
        return book

    def build(self):
        w = self.root

        w.wm_title("KLN College of Information Technology, Department of ECE - Library Handler Software")
        w.wm_protocol("WM_DELETE_WINDOW", lambda self=self: self.quitcmd())
        w.state('zoomed')

        book=self.MainBook()
        book.pack(side=TOP,fill=BOTH,expand=1)
        print('>>> Main Project Window builded')

    def quitcmd(self):
        print('>>> Bye')
        sys.exit()

    def run(self):
        print('>>> Project running')
        mainloop()

def update():
    global global_bucket

    # reset phase
    def reset(widjet):
        if  ( str(type(widjet)) == "<class 'tkinter.ttk.Treeview'>" ):
            for item in widjet.get_children(''):
                widjet.delete(item)
        elif( str(type(widjet)) == "<class 'tkinter.tix.ComboBox'>" ):
            widjet.slistbox.listbox.delete(0,END)
        elif( str(type(widjet)) == "<class 'tkinter.tix.LabelEntry'>" ):
            widjet.entry.delete(0,END)

    for key in ['book_shelf', 'status_register', 'lb_book_no', 'lb1_book_no', 'lb2_book_no', 'lb_book_name', 'lb_staff_id', 'lb_staff_name', 'date', 'note']:
        if(key in global_bucket):
            reset(global_bucket[key])

    # insert phase
    d = time.localtime()
    if('date' in global_bucket):
        global_bucket['date'].entry.insert(END,'%d/%d/%d'%(d.tm_mday,d.tm_mon,d.tm_year))
    book_fields = library.book_fields
    for book, status in library.List_all_books():
        #~ if(status['in_out_status'] == 'IN'):
        if('lb_book_no' in global_bucket):
            global_bucket['lb_book_no'].insert  (END, book['book_no']   )
            global_bucket['lb_book_name'].insert(END, book['book_name'] )

            item = [ book[key] for key in book_fields ] + [status['in_out_status']]
            global_bucket['book_shelf'].insert  ('', 'end', values=item)

        if('lb1_book_no' in global_bucket):
            global_bucket['lb1_book_no'].insert  (END, book['book_no']   )
            global_bucket['lb2_book_no'].insert  (END, book['book_no']   )

        if('status_register' in global_bucket):
            if(status['in_out_status'] == 'OUT'):
                item = [ book['book_no'], book['book_name'], status['date'], status['staff_id'], library.Is_staff_found(status['staff_id']), status['note']]
                global_bucket['status_register'].insert  ('', 'end', values=item)
    if('lb_staff_id' in global_bucket):
        for staff in library.List_all_staffs():
            global_bucket['lb_staff_id'].insert     (END, staff['staff_id']     )
            global_bucket['lb_staff_name'].insert   (END, staff['staff_name']   )

    global_bucket['summary'].config (   text='''+-----------------------------------+
|    KLNCIT - ECE Dept., Library    |
+-----------------------------------+
|     Total no of Books : %4d      |
|     No of books IN    : %4d      |
|     No of books OUT   : %4d      |
+-----------------------------------+'''%   (   len(list(library.List_all_books())),
                                                len(['Mere Baba' for book,status in library.List_all_books() if(status['in_out_status'] == 'IN' ) ]),
                                                len(['Mere Baba' for book,status in library.List_all_books() if(status['in_out_status'] == 'OUT') ]),
                                            )
                                    )
    #~ Staffs      =   library.List_all_staffs()


def Mk_Book_display(book, name):
    w = book.page(name)
    disp = Frame(w)

    tree_columns = ('book_no', 'book_name', 'book_author', 'book_publisher', 'in_out_status')
    Entries=Treeview(   disp,
                        columns=tree_columns,
                        show="headings"
                    )


    global_bucket['book_shelf'] = Entries

    vsb = Scrollbar (   disp,
                        orient="vertical",
                        command=Entries.yview)
    Entries.configure(yscrollcommand=vsb.set)
    for col,width in zip(tree_columns,(4,20,10,5,6)):
        Entries.heading(col, text=col.title(), anchor='w')
        Entries.column(col, width=1)

    vsb.pack(side=RIGHT,fill=Y)
    Entries.pack(fill=BOTH, expand=1)
    disp.pack(fill=BOTH, expand=1)

    update()

def Mk_Status_display(book, name):
    w = book.page(name)
    disp = Frame(w)

    tree_columns = ('book_no', 'book_name', 'date', 'staff_id', 'staff_name', 'note')
    Entries=Treeview(   disp,
                        columns=tree_columns,
                        show="headings",
                    )

    global_bucket['status_register'] = Entries

    vsb = Scrollbar (   disp,
                        orient="vertical",
                        command=Entries.yview)
    Entries.configure(yscrollcommand=vsb.set)
    for col in tree_columns:
        Entries.heading(col, text=col.title(), anchor='w')
        Entries.column(col, width=0)
    vsb.pack(side=RIGHT,fill=Y)
    Entries.pack(fill=BOTH, expand=1)
    disp.pack(fill=BOTH, expand=1)

    update()

def Mk_Book_shelf(w):
    book = NoteBook(w, ipadx=5, ipady=5, options="""
                    tagPadX 6
                    tagPadY 4
                    borderWidth 2
                    """)
    book.add('bdisp', label="Library Books",
        createcmd=lambda book=book, name='bdisp': Mk_Book_display(book, name))
    book.add('sdisp', label="Outgone Books",
        createcmd=lambda book=book, name='sdisp': Mk_Status_display(book, name))

    book.pack(fill = BOTH, expand=1)

def Mk_Lending_control(w):
    options = 'label.anchor w'

    con_win = Frame(w)
    con_win.pack(fill=BOTH, expand=1, anchor='s')

    bucket = {}
    for key in ['date','note']:
        bucket[key] = LabelEntry(con_win, label = key.title(), options=options)

    for key in ['book_no', 'book_name', 'staff_id', 'staff_name']:
        bucket[key] = ComboBox(con_win, label=key.title(), options=options, editable=1)

    def set_book_name(book_no):
        bucket['book_name'  ].entry.delete(0, END)
        bucket['book_name'  ].entry.insert(END, library.get_book_info(book_no=book_no)['book_name'])
    def set_book_no(book_name):
        bucket['book_no'    ].entry.delete(0, END)
        bucket['book_no'    ].entry.insert(END, library.get_book_info(book_name=book_name)['book_no'])
    def set_staff_id(staff_name):
        bucket['staff_id'    ].entry.delete(0, END)
        bucket['staff_id'    ].entry.insert(END, library.Is_staff_found(staff_name=staff_name))
    def set_staff_name(staff_id):
        bucket['staff_name'    ].entry.delete(0, END)
        bucket['staff_name'    ].entry.insert(END, library.Is_staff_found(staff_id=staff_id))


    bucket['book_no'    ].config(command=set_book_name  )
    bucket['book_name'  ].config(command=set_book_no    )
    bucket['staff_id'   ].config(command=set_staff_name )
    bucket['staff_name' ].config(command=set_staff_id   )

    bucket['staff_id'   ].slistbox.listbox['height'] = 10
    bucket['staff_name' ].slistbox.listbox['height'] = 10
    #~ bucket['in_out_status'].slistbox.listbox['height'] = 2

    #~ global global_bucket
    global_bucket['lb_staff_id']    = bucket['staff_id']
    global_bucket['lb_staff_name']  = bucket['staff_name']
    global_bucket['lb_book_name']   = bucket['book_name']
    global_bucket['lb_book_no']     = bucket['book_no']
    global_bucket['date']           = bucket['date']
    global_bucket['note']           = bucket['note']

    #~ for value in ['IN', 'OUT']:
        #~ bucket['in_out_status'].insert(END, str(value))

    def Transaction(in_out_status):
        library.Mk_book_transaction (   book_no         = bucket['book_no'].entry.get() ,
                                        in_out_status   = in_out_status                 ,
                                        date            = bucket['date'].entry.get()    ,
                                        staff_id        = bucket['staff_id'].entry.get(),
                                        note            = bucket['note'].entry.get()
                                    )
        update()

    L = ButtonBox(con_win, orientation=HORIZONTAL)
    L.add('lend'    , text='Lend'   , underline=0, width=7, height=2, command=lambda in_out_status='OUT'    : Transaction(in_out_status) )
    L.add('receive' , text='Receive', underline=0, width=7, height=2, command=lambda in_out_status='IN'     : Transaction(in_out_status) )

    bucket['book_no'].form      ( left=0,                       top=0,                      right='%26' )
    bucket['staff_id'].form     ( left=bucket['book_no'],       top=0,                      right='%52' )
    bucket['date'].form         ( left=bucket['staff_id'],      top=0,                      right='%80' )

    bucket['book_name'].form    ( left=0,                       top=bucket['book_no'],      right='%40' )
    bucket['staff_name'].form   ( left=bucket['book_name'],     top=bucket['staff_id'],     right='%80' )
    bucket['note'].form         ( left=0,                       top=bucket['book_name'],    right='%80' )

    L.form                      ( left=bucket['date'],          top=0,                      right='%100', bottom='%100')

    #~ L.pack(fill=X)

def Mk_Search_control(w):
    def search(catch):
        WORD = ( b_search.entry.get()[ 0 : len( b_search.entry.get() ) - (catch.keycode == 8) ] + (catch.keycode != 8) * catch.char ).lower()
        books.text.delete('0.0',END)
        if(len(WORD) > 2):
            books.text.insert(END,library.Search_books(WORD))

    b_search = LabelEntry(w, label = 'Search Book', options = 'label.width 10 label.anchor w')
    b_search.form(left=0, top=0, right='%100')
    b_search.entry.bind('<KeyPress>',search)

    books = ScrolledText(w, scrollbar='auto')
    books.text['wrap'] = 'none'
    books.form(left=0, right='%100', top=b_search, bottom='%100')

def Mk_Library_Summary(w):
    w.config(bg='violet')
    global_bucket['summary'] = Label(w, font='courier 10', fg='red')

    global_bucket['summary'].form(left=0, top=0,                        right='%100', bottom='%100' )
    #~ add.form(                     left=0, top=global_bucket['summary'], right='%100', bottom='%100')
    #~ global_bucket['summary'].pack(  fill=X, pady=1, anchor='n', expand=0)
    #~ add.pack(                       fill=X, anchor='s', expand=0)

def MakeHome(book, name):
    w = book.page(name)

    Display = LabelFrame(w, label = 'Book Shelf')
    Lending = LabelFrame(w, label = 'Lending control')
    Search  = LabelFrame(w, label = 'Search for a Book in Library')
    Summary = LabelFrame(w, label = 'Library summary')

    Mk_Book_shelf(Display.frame)
    Mk_Lending_control(Lending.frame)
    Mk_Search_control(Search.frame)
    Mk_Library_Summary(Summary.frame)

    Display.form( left=0,       right='%70',    top=0,          bottom='%80'    )
    Search.form ( left=Display, right='%100',   top=0,          bottom='%70'    )
    Lending.form( left=0,       right='%70',    top=Display,    bottom='%100'   )
    Summary.form( left=Lending, right='%100',   top=Search,     bottom='%100'   )

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def Mk_books_insert(w):
    e = Frame(w)
    bucket = {}
    for key in ['book_no', 'book_name', 'book_author', 'book_publisher']:
        bucket[key] = LabelEntry(e, label = key.title(), options = 'label.width 14 label.anchor w')
        bucket[key].pack(fill=X, expand=1)
    status = Label(w, text='All fields are mandatry', bg='violet', fg='white')
    status.pack(side=BOTTOM, fill=X)
    e.pack(fill=X, side='left', expand=1, anchor='n')
    def insert():
        msg = library.Add_new_book  (   {   'book_no'       : bucket['book_no'].entry.get(),
                                            'book_name'     : bucket['book_name'].entry.get(),
                                            'book_author'   : bucket['book_author'].entry.get(),
                                            'book_publisher': bucket['book_publisher'].entry.get()
                                        }
                                    )
        status.config(text=msg)
        update()
    Insert = Button(w, text='Insert', width=15, command=insert)
    Insert.pack(side='right', anchor = 'center', fill=Y)

def Mk_books_edit(w):
    f = Frame(w)
    bucket = {}

    #~ book_name       = Label(f, text='|  / |    |   | +--- --+-- --+--      +--- +--- +---', font='courier 8', anchor='w')
    #~ book_author     = Label(f, text='|-   |    | \ | |      |     |   ===  |--  |    |-- ', font='courier 8', anchor='w')
    #~ book_publisher  = Label(f, text='|  \ +--- |   | +--- --+--   |        +--- +--- +---', font='courier 8', anchor='w')
    book_name       = Label(f, text='|   +++ +=\               +--- +--- +---', font='courier 8')
    book_author     = Label(f, text='|    |  |=<     <=*=>     |--  |    |-- ', font='courier 8')
    book_publisher  = Label(f, text='+-- +++ +=/               +--- +--- +---', font='courier 8')
    def show_book_detail(book_no):
        book_info   = library.get_book_info(book_no=book_no)
        if(book_info != False):
            book_name.config(       text = 'Book Name      :'+book_info['book_name']       , anchor='w')
            book_author.config(     text = 'Book Author    :'+book_info['book_author']     , anchor='w')
            book_publisher.config(  text = 'Book Publisher :'+book_info['book_publisher']  , anchor='w')

            for key in ['modified_book_no', 'modified_book_name', 'modified_book_author', 'modified_book_publisher']:
                bucket[key].entry.delete(0, END)
                bucket[key].entry.insert(END, book_info[ key[9:] ])

    book_no = ComboBox(f, label='Select a book_no', command=show_book_detail)
    global_bucket['lb1_book_no']     = book_no

    book_no.pack(fill=X)

    book_name.pack(fill=X, anchor='w', expand=1)
    book_author.pack(fill=X, anchor='w', expand=1)
    book_publisher.pack(fill=X, anchor='w', expand=1)

    e = Frame(w)
    for key in ['modified_book_no', 'modified_book_name', 'modified_book_author', 'modified_book_publisher']:
        bucket[key] = LabelEntry(e, label = key.title(), options = 'label.width 20 label.anchor w')
        bucket[key].pack(fill=X)
    status = Label(w, text='All fields are mandatry', bg='violet', fg='white')
    def modify():
        msg = library.Modify_a_book (   book_no         =   book_no.entry.get(),
                                        modified_book   =   {   'book_no'       :bucket['modified_book_no'].entry.get(),
                                                                'book_name'     :bucket['modified_book_name'].entry.get(),
                                                                'book_author'   :bucket['modified_book_author'].entry.get(),
                                                                'book_publisher':bucket['modified_book_publisher'].entry.get()
                                                            }
                                    )
        status.config(text=msg)
        update()
    Modify = Button(w, text='Modify', width=15, command=modify)

    f.form(left=0, top=0, right='%45')
    e.form(left=f, top=0, right='%90')
    Modify.form(left=e, top=0, right='%100', bottom='&'+str(e))
    status.form(left=0, top=e, right='%100', bottom='%100')
    update()

def Mk_books_delete(w):
    n = ComboBox(w, label='Select a book_no')
    global_bucket['lb2_book_no'] = n
    def delete():
        book_no = n.entry.get()
        msg = library.Delete_a_book(book_no)
        status.config(text=msg)
        update()
    Delete = Button(w, text='Delete', width=15, command=delete)
    status = Label(w, text='All fields are mandatry', bg='violet', fg='white')

    status.pack(side=BOTTOM, fill=X)
    n.pack(fill=X, side='left', expand=1, anchor='n')
    Delete.pack(side='right', anchor = 'center', fill=Y)

def Mk_add_staff(w):
    e = Frame(w)
    bucket = {}
    for key in ['staff_id', 'staff_name', 'designation']:
        bucket[key] = LabelEntry(e, label = key.title(), options = 'label.width 14 label.anchor w')
        bucket[key].pack(fill=X, expand=1)
    status = Label(w, text='All fields are mandatry', bg='violet', fg='white')
    status.pack(side=BOTTOM, fill=X)
    e.pack(fill=X, side='left', expand=1, anchor='n')

    def insert():
        msg = library.Add_new_staff (   staff = {   'staff_name' : bucket['staff_name'].entry.get(),
                                                    'designation': bucket['designation'].entry.get(),
                                                    'staff_id'   : bucket['staff_id'].entry.get()
                                                }
                                    )
        status.config( text=msg )
        update()
    Insert = Button(w, text='Add', width=15, command=insert)
    Insert.pack(side='right', anchor = 'center', fill=Y)

def Mk_delete_staff(w):
    n = LabelEntry(w, label='staff_id', options = 'label.width 14 label.anchor e')
    status = Label(w, text='All fields are mandatry', bg='violet', fg='white')
    def delete():
        msg = library.Delete_a_staff(n.entry.get())
        status.config( text=msg )
        update()
    Delete = Button(w, text='Remove', width=15, command=delete)

    status.pack(side=BOTTOM, fill=X)

    n.pack(fill=X, side='left', expand=1, anchor='n')
    Delete.pack(side='right', anchor = 'center', fill=Y)

def UpdateLibrary(book, name):
    w = book.page(name)

    B = LabelFrame(w, label='Books Update')
    B.form(top=0, left=0, right='%100', )

    S = LabelFrame(w, label='Staffs Update')
    S.form(top=B, left=0, right='%100', )

    InsF = LabelFrame(B.frame, label='Add New Book to Library')
    DelF = LabelFrame(B.frame, label='Delete a Book from library')
    EdiF = LabelFrame(B.frame, label="Modify a Book's detail found in library")
    StaffInsF = LabelFrame(S.frame, label='Add new staff name')
    StaffDelF = LabelFrame(S.frame, label='Delete a staff name')

    add = Label(w, text = '''
#      *       +-------GOD-Is-My-True-Friend-------+       *      #
#     *|*        Developer : M.RAJIV SUBRAMANIAN          *|*     #
#    *-*-*       mail me @ : rajiv.m1991@gmail.com       *-*-*    #
#     *|*        contact   : +91 9952113011               *|*     #
#      *       +-----------------------------------+       *      #''', font='courier 10', fg='purple')

    Mk_books_insert(InsF.frame)
    Mk_books_delete(DelF.frame)
    Mk_books_edit(EdiF.frame)

    Mk_add_staff(StaffInsF.frame)
    Mk_delete_staff(StaffDelF.frame)

    InsF.form(top=0,    left=0,     right='%50' )
    DelF.form(top=0,    left=InsF,  right='%100',   bottom='&'+str(InsF))
    EdiF.form(top=InsF, left=0,     right='%100')

    StaffInsF.form(top=0, left=0, right='%50', )
    StaffDelF.form(top=0, left=StaffInsF, right='%100', bottom='%100')

    add.form(left=0, top=S, right='%100', bottom='%100')


if(__name__ == '__main__'):
    w   = Tk()
    obj = Library_Handler(w)
    obj.build()
    obj.run()