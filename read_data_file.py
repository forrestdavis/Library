from pymarc import MARCReader

with open("SCIFI_UT8", 'rb') as data:
    reader = MARCReader(data, to_unicode=True, utf8_handling = 'replace')#, force_utf8=True)
    for record in reader:
        print(record['245'])
