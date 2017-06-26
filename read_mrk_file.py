

def read_mrk(filename):
    data = open(filename, "r")

    authors = []
    titles = []
    series_titles = []
    series_numbers = []
    series_title = 'NA'
    series_number = 0
    for line in data:
        line = line.strip()
        if not line:
            series_numbers.append(int(series_number))
            series_titles.append(series_title)
            series_title = 'NA'
            series_number = 0
            
        if "=100" in line:
            line = line.split("  ")
            for element in line:
                if "$a" in element:
                    authors.append(element[4:])
        if "=245" in line:
            line = line.split("  ")
            for element in line:
                if "$a" in element:
                    element = element.split(" /")
                    titles.append(element[0][4:])
        if "=800" in line:
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

    data.close()
    return authors, titles, series_titles, series_numbers

if __name__ == "__main__":
    #filename = "data/example.mrk"
    filename = "data/scifi_data.mrk"
    authors, titles, series_titles, series_numbers = read_mrk(filename)
    '''
    print authors
    print titles
    print series_titles
    print series_numbers
    '''
