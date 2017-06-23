class Book:
    def __init__(self):
        self.barcode = 0
        self.author = ''
        self.title = ''
        self.year = ''
        self.type = ''
        self.series = ''
        self.subseries = ''
        self.number = 0
        self.total = 0
        self.checkout = ''
        self.ytd = -1
        self.prev = -1
        self.life = -1

    #Returns a list of attributes
    def help(self):
        print "The following is the list of attributes available for", 
        print "a book object:"
        print "barcode\nauthor\ntitle\nyear (published)\ntype ",
        print "(ebook, DVD, etc.)\nseries\nsubseries\nnumber ",
        print "(within (sub)series)\ntotal (books within (sub)series)\n",
        print "checkout (last checkout)\n",
        print "ytd (circulation)\nprev (circulation)\nlife (circulation)"

    #The following print functions can either print the formated
    #version of the given attribute or if a file object is given
    #will write to the file object
    def print_barcode(self, output=None):
        if self.barcode:
            if output:
                output.write("Barcode:\t"+self.barcode+"\n")
            else:
                print "Barcode:\t", self.barcode
        else:
            if output:
                output.write("Barcode:\tNA\n")
            else:
                print "Barcode:\tNO BARCODE"

    def print_author(self, output=None):
        if self.author:
            if output:
                output.write("Author:\t\t"+self.author+"\n")
            else:
                print "Author:\t\t", self.author
        else:
            if output:
                output.write("Author:\t\tNO AUTHOR\n")
            else:
                print "Author:\t\tNO AUTHOR"

    def print_title(self, output=None):
        if self.title:
            if output:
                output.write("Title:\t\t"+self.title+"\n")
            else:
                print "Title:\t\t", self.title
        else:
            if output:
                output.write("Title:\t\tNo TITLE\n")
            else:
                print "Title:\t\tNO TITLE"

    def print_year(self, output=None):
        if self.year:
            if output:
                output.write("Year:\t\t"+self.year+"\n")
            else:
                print "Year:\t\t", self.year
        else:
            if output:
                output.write("Year:\t\tNA\n")
            else:
                print "Year:\t\tNA"

    def print_type(self, output=None):
        if self.type:
            if output:
                output.write("Type:\t\t"+self.type+"\n")
            else:
                print "Type:\t\t", self.type
        else:
            if output:
                output.write("Type:\t\tNA\n")
            else:
                print "Type:\t\tNA"

    def print_series(self, output=None):
        if self.series:
            if output:
                output.write("Series:\t\t"+self.series+"\n")
            else:
                print "Series:\t\t", self.series
        else:
            if output:
                output.write("Series:\t\tNA\n")
            else:
                print "Series:\t\tNA"

    def print_subseries(self, output=None):
        if self.subseries:
            if output:
                output.write("Subseries:\t"+self.subseries+"\n")
            else:
                print "Subseries:\t", self.subseries
        else:
            if output:
                output.write("Subseries:\tNA\n")
            else:
                print "Subseries:\tNA"

    def print_number(self, output=None):
        if self.number > 0:
            if output:
                output.write("Number:\t\t"+str(self.number)+"\n")
            else:
                print "Number:\t\t", self.number
        else:
            if output:
                output.write("Number:\t\tNA\n")
            else:
                print "Number:\t\tNA"

    def print_total(self, output=None):
        if self.total > 0:
            if output:
                output.write("Total:\t\t"+str(self.total)+"\n")
            else:
                print "Total:\t\t", self.total
        else:
            if output:
                output.write("Total:\t\tNA\n")
            else:
                print "Total:\t\tNA"

    def print_checkout(self, output=None):
        if self.checkout:
            if output:
                output.write("Checkout:\t"+self.checkout+"\n")
            else:
                print "Checkout:\t", self.checkout
        else:
            if output:
                output.write("Checkout:\tNA\n")
            else:
                print "Checkout:\tNA"
                
    def print_ytd(self, output=None):
        if self.ytd >= 0:
            if output:
                output.write("ytd:\t\t"+str(self.ytd)+"\n")
            else:
                print "ytd:\t\t", self.ytd
        else:
            if output:
                output.write("ytd:\t\tNA\n")
            else:
                print "ytd:\t\tNA"

    def print_prev(self, output=None):
        if self.prev >= 0:
            if output:
                output.write("prev:\t\t"+str(self.prev)+"\n")
            else:
                print "prev:\t\t", self.prev
        else:
            if output:
                output.write("prev:\t\tNA\n")
            else:
                print "prev:\t\tNA"

    def print_life(self, output=None):
        if self.life >= 0:
            if output:
                output.write("life:\t\t"+str(self.life)+"\n")
            else:
                print "life:\t\t", self.life
        else:
            if output:
                output.write("life:\t\tNA\n")
            else:
                print "life:\t\tNA"

    def print_all(self, output=None):
        self.print_barcode(output)
        self.print_author(output)
        self.print_title(output)
        self.print_year(output)
        self.print_type(output)
        self.print_series(output)
        self.print_subseries(output)
        self.print_number(output)
        self.print_total(output)
        self.print_checkout(output)
        self.print_ytd(output)
        self.print_prev(output)
        self.print_life(output)


class Collection:
    def __init__(self):
        self.name = ''
        self.books = []
    
    def construct(self, books):
        self.books = books

    def add_book(self, Book):
        self.books.append(Book)

    def print_books(self, output=None):
        count = 1
        if output:
            output.write("Collection Title:\t"+self.name+"\n\n")
            for book in self.books:
                output.write("------------count: "+str(count)+"-----------\n")
                book.print_all(output)
                output.write("--------------------------------\n")
                count += 1
        else:
            print "Collection Title:\t", self.name, "\n"
            for book in self.books:
                print "----------------count: ",count,"----------------"
                book.print_all()
                print "------------------------------------------"
                count += 1

    def ytd_Sort(self, book1, book2):
        return book1.ytd - book2.ytd

    def prev_Sort(self, book1, book2):
        return book1.prev - book2.prev

    def life_Sort(self, book1, book2):
        return book1.life - book2.life
        
    def Sort(self, sort_basis):
        if sort_basis == "ytd":
            self.books = sorted(self.books, cmp=self.ytd_Sort)

        if sort_basis == "prev":
            self.books = sorted(self.books, cmp=self.prev_Sort)

        if sort_basis == "life":
            self.books = sorted(self.books, cmp=self.life_Sort)

    def Search(self, basis, value, compare=None):
        self.Sort(basis)
        return_books = []

        #Search by Author
        if basis == "author":
            for book in self.books:
                if value.lower() in book.author.lower():
                    return_books.append(book)

        #Search by Title
        if basis == "title":
            for book in self.books:
                if value.lower() in book.title.lower():
                    return_books.append(book)
                
        #Search by circulation history
        if basis == "ytd":
            for book in self.books:
                if compare == "greater":
                    if book.ytd > value:
                        return_books.append(book)
                if compare == "less":
                    if book.ytd < value:
                        return_books.append(book)
                if compare == "equals":
                    if book.ytd == value:
                        return_books.append(book)

        if basis == "prev":
            for book in self.books:
                if compare == "greater":
                    if book.prev > value:
                        return_books.append(book)
                if compare == "less":
                    if book.prev < value:
                        return_books.append(book)
                if compare == "equals":
                    if book.prev == value:
                        return_books.append(book)

        if basis == "life":
            for book in self.books:
                if compare == "greater":
                    if book.life > value:
                        return_books.append(book)
                if compare == "less":
                    if book.life < value:
                        return_books.append(book)
                if compare == "equals":
                    if book.life == value:
                        return_books.append(book)

        return return_books

    def getCount(self, basis, value=None):

        counts = {}
        if basis == "Author":
            for book in self.books:
                if book.author in counts:
                    counts[book.author] = counts[book.author]+1
                else:
                    counts[book.author] = 1
        return counts
