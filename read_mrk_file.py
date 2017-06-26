

def read_mrk(filename):
    data = open(filename, "r")

    author = ''
    title = ''
    series_title = ''
    series_number = ''
    for line in data:
        line = line.strip()
        if "=100" in line:
            line = line.split("  ")
            for element in line:
                if "$a" in element:
                    author = element[4:]
        if "=245" in line:
            line = line.split("  ")
            for element in line:
                if "$a" in element:
                    element = element.split(" /")
                    title = element[0][4:]
        if "=490" in line:
            line = line.split("  ")
            line = line[1].split("$")
            for element in line:
                if element[0] == "a":
                    series_title = element[1:]
                    if series_title[len(series_title)-1] == ";":
                        series_title = series_title[:len(series_title)-1]
                    print series_title
                if element[0] == "v":
                    series_number = element[1:]
                    print series_number

    data.close()
    return author, title, series_title, series_number
