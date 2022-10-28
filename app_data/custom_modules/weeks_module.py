import re


# Example string:
# Элективная дисциплина по физической культуре и спорту: прикладная физическая культура, доц. Ю.И.Капля (п.з.), а. 108 , 2-14, 18 нед 
def parse_weeks(string):
    weeks = []
    weeks_string = string.split(",", maxsplit=3)
    #print(weeks_string)

    #! Workaround for cabinets
    try:
        weeks_string = weeks_string[3].strip()
    except:
        weeks_string = weeks_string[2].strip()

    weeks_string = weeks_string.split("нед")[0]

    found_weeks = re.findall(r"[0-9]{1,2}\s*-\s*[0-9]{1,2}|[0-9]{1,2}", weeks_string)
    for i in found_weeks:
        if re.search(r"[0-9]{1,2}\s*-\s*[0-9]{1,2}", i):
            #print(f"{i} range")
            range_ = list(map(int, i.split("-")))
            for j in range(range_[0], range_[1]+1):
                weeks.append(j)
        else:
            #print(f"{i} single")
            weeks.append(int(i))
    
    return weeks

#print(parse_weeks("Элективная дисциплина по физической культуре и спорту: прикладная физическая культура, доц. Ю.И.Капля (п.з.), а. 108 , 2-14, 18 нед "))