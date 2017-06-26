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

def full_record(circ_filename, mrk_filename, outname=None):
    if outname:
        output = open(outname, "w")
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

    if output:
        output.close()

    return scifi

if __name__ == "__main__":
    #filename = "data/example.mrk"
    circ_filename = "data/scifi_circ.txt"
    mrk_filename = "data/scifi_data.mrk"
    outname = "life_sorted.txt"
    scifi = full_record(circ_filename, mrk_filename, outname)
    outname = open(outname, "w")
    scifi.Sort("life")
    scifi.print_books(outname)

    
    '''
    series_books = scifi.Series()
    count = 1
    for key in series_books:
        print "-------------count: ", count, "---------------"
        print key, ":"
        tmp = []
        for elem in series_books[key]:
            tmp.append(elem[0])
        tmp.sort()
        for elem in tmp:
            print elem
        print "----------------------------"
        count += 1

    '''
