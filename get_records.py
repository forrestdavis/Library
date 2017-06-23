from library import *

circ_data = open("data/scifi_circ.txt", 'r')
output = open("output.txt",'w')

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
        #Remove leading "
        if x == 0:
            line[x] = line[x][1:]

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

    #Add book to collection
    scifi.add_book(book)

#scifi.print_books(output)
scifi.print_books()

circ_data.close()
output.close()
