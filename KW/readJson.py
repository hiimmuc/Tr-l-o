import json


def readjson(file):
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def check_text(text):
    kw = ''
    type_text = ''

    command = False
    greeting = False
    text = text.lower()
    data = readjson("qcclassifi.json")

    qc_list = data['command'].split(",")
    for qc in qc_list:
        if qc in text:
            type_text = 'command'
            command = True

    greeting_list = data['greeting'].split(",")
    for qc in greeting_list:
        if qc in text:
            type_text = 'greeting'
            greeting = True

    if command == False and greeting == False:
        type_text = 'question'

    if greeting:
        data = readjson('greeting.json')
        for key, value in data.items():
            for keyword in value.split(","):
                if keyword in text:
                    kw = key

    elif command:
        data = readjson('command.json')

    text = text.lower()
    data = readjson("qcclassifi.json")
    qc_list = data['question'].split(",")
    question = False
    for qc in qc_list:
        if qc in text:
            type_text = 'question'
            question = True

    if not question:
        if text.split(" ")[-1] in data['lastword'].split(","):
            question = True
            type_text = 'question'
        else:
            type_text = 'command'

    if question:
        data = readjson('quetion.json')

        for key, value in data.items():
            for keyword in value.split(","):
                if keyword in text:
                    kw = key


    else:
        data = readjson('quetion.json')

    else:
        data = readjson('command.json')

        for key, value in data.items():
            for keyword in value.split(","):
                if keyword in text:
                    kw = key

    data = readjson("keyword.json")

    print(f"Type: {type_text.upper()}")
    print(f"Tag: {kw}")
    print(f"Answer: {data[kw]}")
    print("*" * 50)
    return data[kw], kw


# def answer(text, data=None):
#     ans, kw = check_text(text)
#     if "%s" in ans:
#         data = tuple(data)
#         print(f"{ans}"%data)
#     else:
#         print(f"{ans}")
#     print("Tag: ",kw)
#     print("*"*50)

####test
question = ["Hôm nay là thứ mấy", "Bây giờ đang là tháng mấy", "Xin chào Friday",
            "Ngoài trời có đang mưa không", "Tìm kiếm con mèo trên wiki", "Hôm nay có nóng không", "bật điều hòa lên", ]
# ans = [["thứ 6"], [4], ["quạt"], ["có"],["con mèo trên wiki"]]
for i, q in enumerate(question):
    check_text(q)

    # print(f"Type: {type_text.upper()}")
    # print(f"Tag: {kw}")
    # print(f"Answer: {data[kw]}")

    # classification, tag, answer
    return type_text, kw, data[kw]


def answer(text, data=None):
    ans, kw = check_text(text)
    answer = str()
    if "%s" in ans:
        data = tuple(data)
        print(f"{ans}" % data)
        answer = f"{ans}" % data
    else:
        print(f"{ans}")
        answer = "{ans}"
    print("Tag: ", kw)
    # print("*" * 50)
    return answer


# # test
# question = [
#     "Hôm nay là thứ mấy", "Bây giờ đang là tháng mấy",
#     "Bật điều hòa lên", "Ngoài trời có đang mưa không",
#     "Tìm kiếm con mèo trên wiki"
# ]
# ans = [["thứ 6"], [4], ["quạt"], ["có"], ["con mèo trên wiki"]]
# for i, q in enumerate(question):
#     print(q)
#     answer(q, ans[i])

