from library import *

def read_circ(filename):
    circ_data = open(filename, 'r')

    #Get layout and format for ease of use
    info = circ_data.readline()
    info = info.split(",")

    for x in range(len(info)):
        tmp = info[x]
        if "Barcode" in tmp:
            info[x] = "barcode"
        elif "Author" in tmp:
            info[x] = "author"
        elif "Title" in tmp:
            info[x] = "title"
        elif "YTD" in tmp:
            info[x] = "ytd"
        elif "Prev" in tmp:
            info[x] = "prev"
        elif "Life" in tmp:
            info[x] = "life"
        elif "CheckOut" in tmp:
            info[x] = "checkout"
        else:
            print info[x]

    scifi = Collection()
    scifi.name = "Adult Fiction - Science Fiction"

    for line in circ_data:
        book = Book()
        line = line.strip().split('"')
        #Unfortunate preprocessing of line split due to error in data
        tmp = [] 
        for i in range(len(line)):
            if line[i] and line[i]!=',':
                tmp.append(line[i])
        line = tmp
        for x in range(len(line)):

            #Fix blanks
            if line[x] == ',,':
                if info[x]=="ytd"or info[x]=="prev"or info[x]=="life":
                    line[x] = 0
                else:
                    line[x] ="NA"

            #Scrap data
            if info[x] == "barcode":
                book.barcode = line[x]
            if info[x] == "author":
                #Fix error with data
                if "author" in line[x]:
                    tmp = line[x].split(",")
                    if len(tmp) > 3:
                        print "We have a error", tmp
                    else:
                        line[x] = tmp[0]+","+tmp[1]

                book.author = line[x]
            if info[x] == "title":
                book.title = line[x]
            if info[x] == "ytd":
                book.ytd = int(line[x])
            if info[x] == "prev":
                book.prev = int(line[x])
            if info[x] == "life":
                book.life = int(line[x])
            if info[x] == "checkout":
                book.checkout = line[x]

            book.collection = scifi.name

        #Add book to collection
        scifi.add_book(book)

    circ_data.close()
    return scifi

def read_mrk(filename):
    data = open(filename, "r")

    authors = []
    titles = []
    series_titles = []
    series_numbers = []
    series_title = 'NA'
    series_number = 0
    author = 'NA'

    has800 = 0
    has490 = 0
    stored = ''
    for line in data:
        line = line.strip()

        #Adds author, series title and series number at end of 
        #record to account for missing sections
        if not line:
            if not has800 and has490:
                if "$v" in stored:
                    stored = stored.split("  ")[1].split('$')
                    for element in stored:
                        if element[0] == "a":
                            element = element[:len(element)-2]
                            series_title = element[1:]
                        if element[0] == "v":
                            series_number = ''.join(filter(str.isdigit, element))
                            if "one" in element:
                                series_number = 1
                            if "III" in element:
                                series_number = 3
                            elif "II" in element:
                                series_number = 2
                            elif "I" in element:
                                series_number = 1               

            has800 = 0
            has490 = 0
            authors.append(author)
            series_numbers.append(int(series_number))
            series_titles.append(series_title)
            author = 'NA'
            series_title = 'NA'
            series_number = 0
            
        if "=100" in line:
            line = line.split("  ")
            line = line[1].split("$")
            for element in line:
                if element[0] == "a":
                    element = element[:len(element)-1]
                    author = element[1:]
        if "=245" in line:
            line = line.split("  ")
            line = line[1].split("$")
            for element in line:
                if element[0] == "a":
                    if element[len(element)-1] == "/":
                        element = element[:len(element)-2]
                    elif element[len(element)-1] == "." and len(line) == 4:
                        extra = line[2][1:]
                        if extra[len(extra)-1] == "/":
                            extra = extra[:len(extra)-2]
                        element = element + " " + extra
                    elif(element[len(element)-1] == ":"
                            or element[len(element)-1] == ";"):
                        extra = line[2][1:]
                        if extra[len(extra)-1] == "/":
                            extra = extra[:len(extra)-2]
                        element = element + " " + extra
                    titles.append(element[1:])
        if "=800" in line:
            has800 = 1
            line = line.split("  ")
            line = line[1].split("$")
            for element in line:
                if element[0] == "t":
                    series_title = element[1:]
                    if series_title[len(series_title)-1] == ";":
                        series_title = series_title[:len(series_title)-1]
                if element[0] == "v":
                    series_number = ''.join(filter(str.isdigit, element))
                    if "one" in element:
                        series_number = 1
                    if "III" in element:
                        series_number = 3
                    elif "II" in element:
                        series_number = 2
                    elif "I" in element:
                        series_number = 1

        if "=490" in line:
            stored = line
            has490 = 1

    data.close()
    return authors, titles, series_titles, series_numbers

def create_record(circ_filename, mrk_filename, outname=None):

    if outname:
        output = open(outname, 'w')

    else:
        output = outname

    scifi = read_circ(circ_filename)

    authors, titles, series_titles, series_numbers = read_mrk(mrk_filename)

    for x in range(len(authors)):
        title = titles[x]
        author = authors[x]
        books = scifi.Search("book", [author, title])
        for book in books:
            book.series = series_titles[x]
            book.number = series_numbers[x]

    scifi.print_books(output)

    if output:
        output.close()

    return scifi

def load_record(filename):
    
    data = open(filename, "r")

    scifi = Collection()
    count = 0
    new = 0
    for line in data:
        line = line.strip()
        if "--count:" in line:
            count = 0
            new = 1
            book = Book()
        elif "------" in line:
            scifi.add_book(book)
            new = 0
        elif new:
            line = line.split("\t")
            line = line[len(line)-1]
            if count == 1:
                book.collection = line
            if count == 2:
                book.barcode = line
            if count == 3:
                book.author = line
            if count == 4:
                book.title = line
            if count == 5:
                book.year = line
            if count == 6:
                book.type = line
            if count == 7:
                book.series = line
            if count == 8:
                if line == "NA":
                    book.number = 0
                else:
                    book.number = int(line)
            if count == 9:
                book.total = line
            if count == 10:
                book.checkout = line
            if count == 11:
                book.ytd = int(line)
            if count == 12:
                book.prev = int(line)
            if count == 13:
                book.life = int(line)
        count += 1

    data.close()
    
    return scifi

def save_record(collection, filename):
    
    output = open(filename, "w")

    collection.print_books(output)

    output.close()

def validate_series(collection, outname=None):
    series_books = collection.Series()

    for series in series_books:
        total = -1
        print "--------------------------------"
        print series
        print "--------------------------------"
        if series_books[series][0][1].total != "NA":
            continue
        for pair in series_books[series]:
            print "\t", pair[0]
            pair[1].print_all()
            if pair[1].total == "NA":
                if pair[1].number == "NA" or pair[1].number == 0:
                    fix = raw_input("What is this book's series number? ")
                    pair[1].number = int(fix)
                if total != -1:
                    pair[1].total = total
                else:
                    tmp = raw_input("How many books in this series? ")
                    if tmp == "stop":
                        save_record(scifi, filename)
                        break
                    else:
                        total = int(tmp)
                        pair[1].total = total
    
    if outname:
        save_record(scifi, outname)
    else:
        collection.print_books()

def check_missing(miss, title):
    in_missing = 0
    for line in miss:
        if "title" in line:
            in_missing = 1

    return in_missing


def check_trash(trash, book):
    in_trash = 0
    for line in trash:
        if book.title in line:
            in_trash = 1

    return in_trash

def weed(collection):

    missing_file = open("missing.txt", "a")
    trash_file = open("trash.txt", "a")

    series_books = collection.Series()

    w_checkout = 2016
    w_life = 10
    
    count = 1
    for book in collection.books:
        b_checkout = book.checkout.split()[0].split("/")
        if b_checkout[0] == "NA":
            b_checkout = 0
        else:
            b_checkout = int(b_checkout[2])
        b_life = book.life

        if b_checkout < w_checkout and b_life < w_life:
            if book.series != "NA":
                check_pairs = series_books[book.series]
                check_series(collection, check_pairs, trash_file, missing_file)
                count += 1
            else:
                print "----------------------------"
                book.print_all()
                print '----------------------------'
                value = raw_input("Trash book [y/n]? ")
                if value == "y":
                    trash_file.write('---------------------------')
                    book.print_all(trash_file)
                    trash_file.write('---------------------------')

    trash_file.close()
    missing_file.close()

def update_series(collection, check_pairs, trash_file, missing_file, total_num=None):
    
    value = ''
    while value != "done":
        value = raw_input("What would you like to do with series? ")
        if value == "h" or value == "help":
            print "Options: "
            print "\tlist:\tlist current books in series"
            print "\tsearch:\tsearch for title"
            print "\tupdate:\tchange values of record"
            print "\ttrash:\tmark record as trash"
            print '\tmissing:\tmark missing books'
        if value == "list":
            for pair in check_pairs:
                print "---------------------------"
                print pair[1].print_all()
                print "---------------------------"

        if value == "search":
            title = raw_input("What is the search title? ")
            return_books = collection.Search('title', title)
            print "Return Values: "
            for book in return_books:
                print '-------------------------------'
                book.print_all()
                print '-------------------------------'
                y_n = raw_input("Is this the book? ")
                if "y" in y_n:
                    y_n = raw_input("Would you like to change this record? ")
                    if y_n == "y":
                        inner_value = ''
                        while inner_value != 'done':
                            inner_value = raw_input("What would you like to update? ")
                            change_value = raw_input("Value: ")

                            if inner_value == "series":
                                book.series = change_value
                            if inner_value == "number":
                                book.number = int(change_value)
                            if inner_value == "total":
                                book.total = int(change_value)
                        save_record(collection, "full_record.txt")
                        collection = load_record("full_record.txt")
                        update_series = collection.Series()
                        check_pairs = update_series[check_pairs[0][1].series]
                        

        if value == "update":
            for pair in check_pairs:
                print '---------------------------------'
                pair[1].print_all()
                print '---------------------------------'

                y_n = raw_input("Would you like to change this record? ")
                if y_n == "y":
                    inner_value = ''
                    while inner_value != 'done':
                        inner_value = raw_input("What would you like to update? ")
                        change_value = raw_input("Value: ")

                        if inner_value == "series":
                            pair[1].series = change_value
                        if inner_value == "number":
                            pair[1].number = int(change_value)
                        if inner_value == "total":
                            pair[1].total = int(change_value)

            save_record(collection, "full_record.txt")
            collection = load_record("full_record.txt")
            update_series = collection.Series()
            check_pairs = update_series[check_pairs[0][1].series]
       
        if value == "trash":
            for pair in check_pairs:
                trash_file.write("-----------------------------")
                pair[1].print_all(trash_file)
                trash_file.write("-----------------------------")
        
        if value == "missing":
            while total_num:
                if check_pairs:
                    if total_num[0] == check_pairs[0][0]:
                        total_num.pop(0)
                        pair = check_pairs.pop(0)
                        missing_file.write('----------------------------')
                        pair[1].print_all(missing_file)
                        missing_file.write('----------------------------')
                    elif total_num[0] != check_pairs[0][0]:
                        missing_num = total_num.pop(0)
                        print "Missing book number: ", missing_num
                        inner_value = raw_input("What is the title? ")
                        missing_file.write('----------------------------\n')
                        missing_file.write("MISSING BOOK: "+inner_value+'\n')
                        missing_file.write('----------------------------\n')
                else:
                    missing_num = total_num.pop(0)
                    print "Missing book number: ", missing_num
                    inner_value = raw_input("What is the title? ")
                    missing_file.write('----------------------------\n')
                    missing_file.write("MISSING BOOK: "+inner_value)
                    missing_file.write('----------------------------\n')


def check_series(collection, check_pairs, trash_file, missing_file):

    total_num = range(1, int(check_pairs[0][1].total)+1)

    if len(check_pairs) == len(total_num):
        print "The following series is complete but infrequent: "
        print "--------------------------------------"
        check_pairs[0][1].print_series()
        print "--------------------------------------"
        update_series(collection, check_pairs, trash_file, missing_file)

    if len(check_pairs) != len(total_num):
        print "The following series is incomplete"
        print "--------------------------------------"
        check_pairs[0][1].print_series()
        print "--------------------------------------"
        update_series(collection, check_pairs, trash_file, missing_file, total_num)


if __name__ == "__main__":
    filename = "full_record.txt"
    scifi = load_record(filename)

    weed(scifi)
