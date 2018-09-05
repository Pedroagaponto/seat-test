#!/usr/bin/env python2
import requests


def get_emissao(ticket):
    return int(ticket["emissao"])


def get_prioridade(ticket):
    priorityList = {"atendido": -1, "preferencial": 0, "geral": 1}
    priority = priorityList[ticket["prioridade"]]
    if 'chamada' in ticket:
        priority = priorityList["atendido"]

    return int(priority)


def fill_stats(tickets):
    position = 0
    waitTime = avg_service_time(tickets)

    for t in tickets:
        if 'chamada' in t:
            continue

        t["naFrente"] = position
        t["espera"] = (position + 1) * waitTime
        position += 1


def print_tickets(tickets):
    for t in tickets:
        print t["senha"],
        print t["emissao"],
        print t["prioridade"]


def avg_service_time(tickets):
    serviceTime = list([])
    for t in tickets:
        if 'fim' in t:
            serviceTime.append(t["fim"]-t["chamada"])

    return sum(serviceTime)/len(serviceTime)


def get_unique(tickets):
    uniq = list([])

    for t in tickets:
        if t in uniq:
            continue
        else:
            uniq.append(t)
        print t["senha"]
    return uniq


def print_hist(tickets):
    waitTimes = []
    for t in tickets:
        if "chamada" in t:
            waitTimes.append((t["chamada"] - t["emissao"])/int(3e5))

    hist = []
    for i in range(3):
        hist.append(waitTimes.count(i))
    hist.append(len(waitTimes) - sum(hist))

    text = ["< 05min: {}{}{}", "< 10min: {}{}{}",
            "< 15min: {}{}{}", "> 15min: {}{}{}"]
    for i in range(4):
        print text[i].format("#"*hist[i], ' ' if hist[i] > 0 else '', hist[i])


def main():
    name = "Pedro Henrique"
    url = "http://seat.ind.br/processo-seletivo/2018/02/desafio.php"
    payload = {"nome": name}

    rGet = requests.get(url, payload)
    data = rGet.json()

    tickets = data["input"]
    uniq = get_unique(tickets)

    uniq.sort(key=get_emissao)
    uniq.sort(key=get_prioridade)
    fill_stats(uniq)
    print_hist(uniq)

    result = {"nome": name, "chave": data["chave"], "resultado": uniq}
    rPost = requests.post(data["postTo"]["url"], data=result)

    with open("output.html", "w") as f:
        f.write(rPost.content)


if __name__ == "__main__":
    main()
