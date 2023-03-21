"""
output:
[0]: //website
[1]: '-'
[2]: '-'
[3]: '[//data'
[4]: '-//code]'
[5]: '"GET'
[6]: //resource
[7]: 'HTTP/1.0"'
[8]: //code HTTP
[9]: //number of B
"""
#tuple functions:
def read_log():
    import datetime
    result = []

    def verify(data):
        if( len(data)!=10 or data[1]!="-" or data[2]!="-" or data[5]!='"GET' or data[7]!='HTTP/1.0"'):
            return False
        else:
            return True
        
    while True:
        try:
            line = input().split(" ")
            #print(line[3][1::])
            if(verify(line)):
                dataTime:datetime.datetime = datetime.datetime.strptime(line[3][1::], "%d/%b/%Y:%H:%M:%S")
                tup = line[0], line[1], line[2], dataTime, int(line[4][1:-1:]), line[5][1::], line[6], line[7][:-1:], int(line[8]), int(line[9])
                result.append(tup)
        except EOFError:
            break
        except Exception:
            continue
    return result


def sort_log(tuples, elemNr:int):
    try:
        from copy import deepcopy
        if(elemNr>=len(tuples[0]) or elemNr<0): raise IndexError
        temp = deepcopy(tuples)
        temp.sort(key=lambda a:a[elemNr])
        return temp
    except IndexError:
        print("INDEX ERROR")
        return tuples
    except Exception:
        print("ANY ERROR")
        return tuples


def get_entries_by_addr(tuples, domain:str):
    if domain[-4::].count(".")==0: return []
    results = []
    for i in tuples:
        if(i[0]==domain): results.append(i)
    return results

def get_entries_by_code(tuples, code:int):
    results = []
    for i in tuples:
        if(i[8]==code): results.append(i)
    return results


def get_failed_reads(tuples, concat:bool):
    fourhundreds = []
    fivehundreds = []
    for i in tuples:
        if(i[8]>=400 and i[8]<500): fourhundreds.append(i)
        elif(i[8]>=500 and i[8]<600): fivehundreds.append(i)
    if concat: return fourhundreds+fivehundreds
    else: return fourhundreds, fivehundreds

def get_entires_by_extension(tuples, extension:str):
    results = []
    for i in tuples:
        if(i[6][-len(extension)::]==extension): results.append(i)
    return results

def print_entries(tuples, *args):
    for i in tuples:
        print(i)
    if(args):
        for n in args:
            print(n)




#dictionary functions:
def entry_to_dict(tup):
    ip, user1, user2, date, code, method, source, protocol, HTTPcode, bytesN = tup
    result = {
        "ip":ip,
        "user1":user1, 
        "user2":user2, 
        "date":date, 
        "code":code, 
        "method":method, 
        "source":source, 
        "protocol":protocol, 
        "HTTPcode":HTTPcode, 
        "bytesN":bytesN
    }
    return result

def log_to_dict(tuples):
    result = {}
    for i in tuples:
        if result.get(i[0]): result[i[0]].append(entry_to_dict(i))
        else: result[i[0]] = [entry_to_dict(i)]
    return result

def get_addrs(dictionary:dict):
    return dictionary.keys()

def print_dict_entry_dates(dictionary:dict):
    def codes200(listD):
        count = 0
        all = 0
        for d in listD:
            all+=1
            if(d.get("HTTPcode")==200):count+=1
        return str(count)+"/"+str(all)

    for i in dictionary:
        print(i, len(dictionary.get(i)), dictionary.get(i)[0].get("date"), dictionary.get(i)[-1].get("date"), codes200(dictionary.get(i)), "\n")






def main():
    print("przykladowe uzycia:\n")
    lista = read_log()
    print("zad1 a:\n", lista, "\n")
    print("zad1 b:")
    print_entries(sort_log(lista, 0), "\n")
    print("zad1 c:")
    print_entries(get_entries_by_addr(lista, "199.120.110.21"), "\n")
    print("zad1 d:")
    print_entries(get_entries_by_code(lista, 200), "\n")
    print("zad1 e:")
    print_entries(get_failed_reads(lista, True), "\n")
    print("zad1 f:")
    print_entries(get_entires_by_extension(lista, ".html"), "\n")
    print("zad1 g:")
    print_entries(lista, "\n")

    print("zad2 a:")
    print(entry_to_dict(lista[0]), "\n\n")
    print("zad2 b:")
    print(log_to_dict(lista), "\n\n")
    print("zad2 c:")
    print(get_addrs(log_to_dict(lista)), "\n\n")
    print("zad2 d:")
    print_dict_entry_dates(log_to_dict(lista))

if __name__ == "__main__": 
    #print(read_log())
    main()