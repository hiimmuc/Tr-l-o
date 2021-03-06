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

# test
question = ["H??m nay la?? th???? m????y", "B??y gi???? ??ang la?? tha??ng m????y", "Xin ch??o Friday",
            "Ngoa??i tr????i co?? ??ang m??a kh??ng", "Ti??m ki????m con me??o tr??n wiki", "H??m nay c?? n??ng kh??ng", "b???t ??i????u ho??a l??n", ]
# ans = [["th???? 6"], [4], ["qua??t"], ["co??"],["con me??o tr??n wiki"]]
# for i, q in enumerate(question):
#     check_text(q)

#     # print(f"Type: {type_text.upper()}")
#     # print(f"Tag: {kw}")
#     # print(f"Answer: {data[kw]}")

#     # classification, tag, answer
#     print(type_text, kw)
#     return type_text, kw, data[kw]


def make_answer(text, data=None):
    _, kw, ans = check_text(text)
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
#     "H??m nay la?? th???? m????y", "B??y gi???? ??ang la?? tha??ng m????y",
#     "B????t ??i????u ho??a l??n", "Ngoa??i tr????i co?? ??ang m??a kh??ng",
#     "Ti??m ki????m con me??o tr??n wiki"
# ]
# ans = [["th???? 6"], [4], ["qua??t"], ["co??"], ["con me??o tr??n wiki"]]
# for i, q in enumerate(question):
#     print(q)

print(check_text("cho t??i bi???t th???i ti???t h??m nay"))
