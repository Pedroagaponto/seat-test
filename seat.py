#!/usr/bin/env python2
import requests


def get_emissao(ticket):
    return int(ticket["emissao"])


def fill_stats(tickets):
    position = 0

    for t in tickets:
        if 'chamada' in t:
            continue

        t["naFrente"] = position
        position += 1


def print_tickets(tickets):
    for t in tickets:
        print t["senha"],
        print t["emissao"],
        print t["prioridade"]


def get_unique(tickets):
    uniq = list([])

    for t in tickets:
        if t in uniq:
            continue
        else:
            uniq.append(t)
        print t["senha"]
    return uniq


def main():
    name = "Pedro Henrique"
    url = "http://seat.ind.br/processo-seletivo/2018/02/desafio.php"
    payload = {"nome": name}

    rGet = requests.get(url, payload)
    data = rGet.json()

    tickets = data["input"]
    uniq = get_unique(tickets)

    uniq.sort(key=get_emissao)
    fill_stats(uniq)

    result = {"nome": name, "chave": data["chave"], "resultado": uniq}
    rPost = requests.post(data["postTo"]["url"], data=result)

    with open("output.html", "w") as f:
        f.write(rPost.content)


if __name__ == "__main__":
    main()
