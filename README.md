# Microblog
## Exemple d'usage de SqlAlchemy pour la recherche sur une relation m2m

L'objectif de ce projet compact mais complet est de montrer comment rechercher
avec SqlAlchemy des articles qui contienne des tags recherchés et de les classer
par ordre de pertinance (on veut d'abord les articles le plus de tags correspondants).

Cet exemple utilise la base de données Sqlite3, mais vous pouvez très facilement
le tester avec Mysql ou Postgres en définissant une variable d'environnement
DATABASE_URL spécifiant les informations de connexion selon le format spécifier
dans [cette documentation](https://docs.sqlalchemy.org/en/14/core/engines.html).
Pour utiliser mysql ou postgresql, il vous faudra en plus installer le driver
que vous désirez utiliser (voir section suivante).

### Installation des dépendances

Pour installer les dépendances de ce programme, vous aurez besoin de pipenv. Si
vous n'avez pas déjà installé cet outil, référez-vous à la [documentation officielle](https://packaging.python.org/tutorials/managing-dependencies/#installing-pipenv) pour la gestion des dépendances applicatives.

Voici les étapes pour tester cet exemple:

1. Cloner ce dépôt de code sur votre machine à l'aide de git.
2. Ouvrez un terminal à la racine du projet.
3. Lancez la commande `pipenv install`

Si vous utilisez Sqlite3, vous n'avez rien d'autre à toucher et le programme
d'exemple est prêt à l'utilisation (voir section suivante). Si vous souhaitez
expérimenter avec une autre base de données, continuer ci-dessous.

Si vous désirez utiliser une base de données comme Mysql ou Postgresql, il vous
suffit de créer un fichier .env à la racine de ce projet et d'y définir la
variable DATABASE_URL avec vos données de connexion:
```
DATABASE_URL = 'mysql+mysqlconnector://<votre-utilisateur>:<votre-mot-de-passe>@localhost/<nom-de-votre-db>'
DATABASE_URL = 'postgres+psycopg2://<votre-utilisateur>:<votre-mot-de-passe>@localhost/<nom-de-votre-db>'
```

Selon la base de données que vous aurez décidé d'installer, il vous faudra également installer mysql-connector-python (mysql) ou psycopg2-binary (postgresql)
à l'aide de pipenv. 

### Utilisation du programme d'exemple

Pour exécuter ce programme d'exemple, il faut dans un premier temps initialiser
la base de données à l'aide de la commande `$ pipenv run python -m microblog initdb`.

Une fois que la base est initialisée, vous pouvez afficher les articles à l'aide
de la commande `$ pipenv run python -m microblog show`.

Pour filter l'affichage des articles en fonction des tags qu'ils contiennent, vous
pouvez exécuter cette commande avec une liste de tags: `$ pipenv run python microblog -m show tag1 tag2 ...`

Pour créer une nouvel article ou pour taguer un article existant, utilisez la 
commande `pipenv run python -m microblog article "titre de mon article" tag1 tag2 ...`
