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

def update_record_series(collection, series):
    print books

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

def get_missing(collection):

    series_books = collection.Series()
    missing = open("missing.txt", "w")
    trash = open("trash.txt", "w")

    for series in series_books:
        poss = len(series_books[series])
        if series_books[series][0][1].total == "NA":
            series_books[series][0][1].total = 0
        act = int(series_books[series][0][1].total)

        if poss == act:
            books = []
            tmp = range(1, act+1)
            for book in series_books[series]:
                if book[1].number not in tmp:
                    print "error: "
                    print book[1].print_all()
                    value = raw_input("Change number, total, or series? ")
                    if value == "number":
                        num = raw_input("What is number? ")
                        book[1].number = int(num)
                    if value == "total":
                        num = raw_input("What is the total? ")
                        book[1].total = int(num)
                    if value == "series":
                        s = raw_input("What is the series title? ")
                        book[1].series = s
                        num = raw_input("What is the book number? ")
                        book[1].number = int(num)
                        num = raw_input("What is the total number? ")
                        book[1].total = int(num)
                    save_record(collection, "full_record.txt")
                else:
                    tmp.remove(int(book[1].number))
                    books.append(book[1])

            if tmp:
                print '------------------------'
                print series
                print '------------------------'
                author = books[0].author
                
                for book in books:
                    book.print_all()
                x = raw_input("Add to missing? or move all trash? ")
                if x == "missing":
                    title = raw_input("Title? ")
                    missing.write("-------------------------\n")
                    missing.write(series+"\n")
                    missing.write(author+'\n')
                    missing.write(title+'\n')
                    missing.write("-------------------------\n")
                if x == "trash":
                    for book in books:
                        books.print_all(trash)
        else:
            tmp = range(1, act+1)
            books = []
            miss_books = []
            print "------------------------------"
            print series
            print "------------------------------"
            for book in series_books[series]:
                if tmp[0] == book[0]:
                    book[1].print_all()
                    value = raw_input("Update record [y/n]? ")
                    if value == "y":
                        value = ''
                        while value != "done":
                            option = raw_input("Change what? ")
                            value = raw_input("Value: ")
                            if option == "number":
                                book[1].number = int(value)
                            if option == "total":
                                book[1].total = int(value)
                            if option == "series":
                                book[1].series = value
                            if option == "search":
                                x = collection.Search('title', value)
                                for i in x:
                                    i.print_all()

                        save_record(collection, "full_record.txt")
                    tmp.pop(0)
                while tmp[0] != book[0]:
                    print "Missing book number ", tmp.pop(0)
                    value = raw_input("What is the title? ")
                    look = collection.Search("title", value)
                    if look:
                        print "There are books in the collection with this title"
                        changed = 0
                        for b in look:
                            b.print_all()
                            value = raw_input("Is this book you are looking for? ")
                            if value == "y":
                                b.series = 


                    miss_books.append(value)
                books.append(book[1])
            value = raw_input("trash or mark missing? ")
            if value == "trash":
                for book in books:
                    books.print_all(trash)
            if value == "missing":
                author = books[0].author
                for title in miss_books:
                    missing.write("-------------------------\n")
                    missing.write(series+"\n")
                    missing.write(author+'\n')
                    missing.write(title+'\n')
                    missing.write("-------------------------\n")


    missing.close()
    trash.close()

if __name__ == "__main__":
    filename = "full_record.txt"
    scifi = load_record(filename)


    #job = raw_input("What do you want to do? ")
    
    #if job.lower() == "series":

    get_missing(scifi)

    
