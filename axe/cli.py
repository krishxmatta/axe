import click
import re
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.argument("question")
def search(question):
    parameters = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": question,
        "prop": "categories",
        "cllimit": "max",
    }

    response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)

    search_list = [(x["index"], x["title"]) for x in filter(lambda y: not any([z["title"] == "Category:All disambiguation pages" for z in y["categories"]]), response.json()["query"]["pages"].values())]
    list.sort(search_list)

    if(len(search_list) == 1):
        return search_list[0][1]

    for index, value in enumerate(search_list):
        click.echo(f"{index + 1}) {value[1]}")
    input_value = click.prompt("Please enter the corresponding number of the article you want to choose", type=int)

    click.echo(query(search_list[input_value - 1][1]))


def query(title):
    parameters = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "redirects": 1,
        "titles": title,
    }

    response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)
    ret = list(response.json()["query"]["pages"].values())[0]["extract"].split("\n")[0]
    ret = re.sub(' +', ' ', ret)
    return ret


@cli.command()
def random():
    parameters = {
        "action": "query",
        "format": "json",
        "generator": "random",
        "prop": "extracts",
        "exintro": 1,
        "explaintext": 1,
        "redirects": 1,
        "grnnamespace": 0,
    }

    response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)
    page = list(response.json()["query"]["pages"].values())[0]
    click.echo(f"Page Title: {page['title']}")
    click.echo(page["extract"])
