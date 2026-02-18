# Py_justiceadmin
[![Publish](https://github.com/Geminy3/py_justiceadmin/actions/workflows/publish.yml/badge.svg)](https://github.com/Geminy3/py_justiceadmin/actions/workflows/publish.yml/badge.svg)

## Description
Ce projet s'appuie sur le site de [l'opendata des décisions de la justice administration](https://opendata.justice-administrative.fr/) avec pour objectif de réimplémenter le comportement du moteur de recherche avec une interface en python.
Il est ainsi possible de récupérer les décisions de la justice administrative en open source avec quelques arguments.

## Installation

Vous pouvez installer le package py_justiceadmin depuis Pypi:
```{bash}
# Pour les utilisateurs de pip
pip install py_justiceadmin

# Pour les utilisateurs d'uv
uv add py_justiceadmin
```

## Utilisation

Pour communiquer avec le serveur, nous avons implémenter une méthode simple d'utilisation. Il suffit d'instancier' un objet `JA_requester`:
```{python}
from py_justiceadmin import JA_requester

# Par défaut, l'url de l'API est déjà renseigné, mais vous pouvez la changer avec l'argument `base_url`
client = JA_requester()
```

Une fois le client créé, vous pouvez ensuite faire une requête en utilisant la fonction `get_query()` et en précisant les arguments nécessaires:

```{python}

client.get_query(
    keywords = "trouble anormal de voisinage", 
    exact_sentence=True,
    date_start = '2021-01-20',
    date_end = '2026-01-01',
    type = "Ordonnance",
    juridiction = "ta",
    ville = ["bordeaux", "paris"], 
    OnLine = True,
    nb_recherche = 10000
)

```
## 

## Exemple d'usages

# TODO
- [X] Trouver une meilleure implémentation pour URL_BUILDER
- [ ] Simplifier le requêtage de l'api via des arguments d'une fonction (nota pour les keywords, ajouter un argument `exact_text`)
- [ ] Utiliser les logs
- [X] Créer une fonction de récupération auto de l'ensemble des décisions d'une requête
