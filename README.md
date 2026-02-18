# Py_justiceadmin
[![Publish](https://github.com/Geminy3/py_justiceadmin/actions/workflows/publish.yml/badge.svg)](https://github.com/Geminy3/py_justiceadmin/actions/workflows/publish.yml/badge.svg)
![Pypi](https://img.shields.io/pypi/v/py-justiceadmin.svg)
![PythonPypi](https://img.shields.io/pypi/pyversions/py-justiceadmin.svg)

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

Pour communiquer avec le serveur, nous avons implémenté une méthode simple d'utilisation. Il suffit d'instancier un objet `JA_requester`:
```python
from py_justiceadmin import JA_requester

# Par défaut, l'url de l'API est déjà renseigné, mais vous pouvez la changer avec l'argument `base_url`
client = JA_requester()
```

Une fois le client créé, vous pouvez ensuite faire une requête en utilisant la fonction `get_query()` et en précisant les arguments nécessaires:

```python

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
Par défaut, l'ensemble des arguments sont fixés sur `None`, et le nombre de décision renvoyé est de 10.000, ce qui est la limite maximale proposée par le moteur de recherche. 

### Informations sur l'argument `keywords`
L'argument `keywords` peut contenir des requêtes sous forme de texte : 
- On peut utiliser l'argument `et` dans le texte : *trouble et anormal*. On garantie que deux termes sont présents dans un texte
- On peut utiliser l'argument `ou` qui garantie que l'un ou l'autre des termes sont présents. 
- Si l'on veut utiliser une expression exacte, nous avons ajouter un argument `exact_sentece` qui permet d'envoyer une chaîne de caractère entouré de double guillement, qui garantie que l'expression se trouve dans le texte d'une décision

Pour les argument `et` et `ou`, on peut les remplace par les opérateurs `+` et `-` (respectivement).

### Information sur l'argument `type`
L'argument type permet de spécifier si l'on souhaite n'obtenir que les `"ordonnance"`, ou les `"decision"`. 

### Information sur les arguments `juridiction` et `ville`
Ces deux arguments permettent de cibler si l'on souhaite travailler sur un niveau de juridiction particulier : 
- `ta` : pour tribunal administratif, c'est-à-dire la juridiction du fond
- `ca` : pour cour d'appel administrative
- `ce` : pour le Conseil d'État
Et si l'on souhaite travailler sur une ville particulier, parmi la liste des villes disponible, disponible avec la fonction `get_parameters()`. 

```python
client.get_parameters()
```

La gestion des juridictions et des villes se fait automatiquement, mais si vous sélectionnez une ville qui n'a pas de cour d'appel, la requête ne pourra pas aboutir. 

## Exemple d'usages

Si l'on cherche à récupérer des décisions en fonction d'une recherche :

```python
from py-justiceadmin import JA_requester()

client = JA_requester(
    base_url = 'https://opendata.justice-administrative.fr/recherche/api/',
    # Cette URL est fournie par défaut
    query_verbose = False
    # Ce paramètre permet d'afficher les éléments de la requête dans le terminal, ainsi que l'URL ainsi créée
)

reponse = client.get_query(
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
print(reponse)
print(client.data)
```
> # Length reponse : 2

À partir d'identifiant de décision, on peut chercher le texte de celle-ci :

```python
client.get_decision(response = client.data['hits'][1])
print(client.dec)

#res = client.get_decision(response = client.data['hits'][1])
print(res)
```
> {'total': {'value': 1}, 'hits': [{'_id': 'ORTA_2202099_20221129.xml_TA33', '_source': {'Identification': 'ORTA_2202099_20221129.xml', 'Code_Juridiction': 'TA33', 'Nom_Juridiction': 'Tribunal Administratif de Bordeaux', 'Numero_ECLI': 'undefined', 'Code_Publication': 'D', 'Formation_Jugement': '', 'Numero_Dossier': '2202099', 'Type_Decision': 'Ordonnance', 'Date_Lecture': '2022-11-29', 'paragraph': 'Vu la procédure suivante :$$$Par une requête enregistrée le 12 avril 2022, M. B A demande au tribunal  d\'annuler l\'arrêté du 13 décembre 2021 par lequel le maire de la commune de Bordeaux s\'est opposé à sa déclaration préalable en vue de la création d\'une piscine enterrée, de modifications des murs de clôture, de remise en peinture et de pose d\'une terrasse sur un terrain situé 1 rue Longchamp, parcelle cadastrée 63 VD 17 ;$$$Il soutient que : $$$- l\'élévation du mur entre les parcelles du voisinage ne relève pas$$$du règlement du plan local d\'urbanisme et n\'entraîne pas de trouble anormal de voisinage ; $$$- le choix de la peinture choisie s\'intègre à l\'environnement et ne crée pas d\'îlot de chaleur compte tenu de son orientation.$$$Par un mémoire enregistré le 24 novembre 2022, M. B A déclare se désister de sa requête.$$$Vu les pièces du dossier.$$$Vu le code de justice administrative.$$$Considérant ce qui suit :$$$1. Aux termes de l\'article R. 222-1 du code de justice administrative : " Les présidents de tribunal administratif  () et les présidents de formation de jugement des tribunaux () peuvent, par ordonnance : / 1\' donner acte des désistements ; ()".$$$2. M. B A déclare se désister de sa requête. Ce désistement est pur et simple et rien ne s\'oppose à ce qu\'il en soit donné acte.$$$O R D O N N E :$$$Article 1er : Il est donné acte du désistement d\'instance de  M. A.$$$Article 2 : La présente ordonnance sera notifiée à M. B A et à la commune de Bordeaux.$$$Fait à Bordeaux, le 29 novembre 2022.$$$Le président de la 2ème chambre,$$$L. POUGET$$$La République mande et ordonne à la préfète de la Gironde en ce qui la concerne ou à tous commissaires de justice à ce requis en ce qui concerne les voies de droit commun contre les parties privées, de pourvoir à l\'exécution de la présente décision.$$$Pour expédition conforme,$$$Le greffier,$$$', 'lastModified': '2025-03-21'}, 'highlight': None}]}

On peut également récupérer toutes les décisions dans un dictionnaire
```python
client.get_all_decisions()#verbose = True
print(client.all_dec)

#res = client.get_all_decisions()#verbose = True
#print(res)
```

## TODO
- [X] Trouver une meilleure implémentation pour URL_BUILDER
- [X] Simplifier le requêtage de l'api via des arguments d'une fonction (nota pour les keywords, ajouter un argument `exact_text`)
- [X] Créer une fonction de récupération auto de l'ensemble des décisions d'une requête
- [ ] Rédiger les fonctions de tests
