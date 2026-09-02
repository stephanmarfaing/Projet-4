# Gestionnaire de Tournoi d'Échecs

Application en ligne de commande permettant de gérer des tournois d'échecs selon le système suisse : création de tournois, inscription de joueurs, génération des tours, saisie des résultats, classement et rapports.

## Fonctionnalités

- Gestion des tournois : création, listing, suivi de l'avancement (tour en cours / nombre total de tours)
- Gestion des joueurs : inscription via identifiant national d'échecs (détection automatique si le joueur existe déjà), création si nouveau joueur
- Génération des tours : appariement selon le système suisse
  - 1er tour : appariement aléatoire
  - tours suivants : appariement par proximité de classement, en évitant autant que possible les matchs déjà joués
- Saisie des résultats : victoire joueur 1 / victoire joueur 2 / match nul, avec sauvegarde après chaque match
- Classement : calcul des scores cumulés, consultable à tout moment (même en cours de tournoi), annonce automatique du vainqueur à la fin du tournoi
- Rapports :
  - Liste de tous les joueurs (ordre alphabétique)
  - Liste de tous les tournois
  - Nom et dates d'un tournoi donné
  - Liste des joueurs d'un tournoi (ordre alphabétique)
  - Liste des tours et matchs d'un tournoi
- Persistance des données : sauvegarde automatique au format JSON (data/tournaments.json, data/players.json)
- Validation des saisies : contrôle systématique des entrées utilisateur (dates, identifiants, champs obligatoires) avec redemande en cas d'erreur

## Architecture

Le projet suit une architecture MVC (Modèle-Vue-Contrôleur) :

```
.
├── main.py                        Point d'entree, menu principal
├── db.py                          Persistance JSON (lecture/ecriture)
├── validators.py                  Fonctions de validation des saisies
├── models/
│   ├── tournament.py              Modele Tournament (+ calcul des scores)
│   ├── round.py                   Modele Round (tour + matchs)
│   └── player.py                  Modele Player
├── controllers/
│   ├── tournament_controller.py   Logique metier : tournois, tours, appariement suisse
│   └── report_controller.py       Logique des rapports
└── views/
    ├── tournament_view.py         Affichage et saisies liees aux tournois
    └── report_view.py             Affichage des rapports
```

Chaque couche a une responsabilité stricte :
- Modèles (models/) : structure des données et logique propre à l'objet (ex. Tournament.compute_scores())
- Contrôleurs (controllers/) : orchestrent la logique métier, ne contiennent aucune instruction d'affichage
- Vues (views/) : gèrent tout l'affichage (print) et toute la saisie (input), aucune logique métier

## Prérequis

- Python 3.10 ou supérieur

## Installation

Aucune dépendance externe n'est requise pour l'exécution (bibliothèque standard uniquement).

Pour le développement (vérification du style de code) :

```
pip install -r requirements.txt
```

## Utilisation

Lancer l'application :

```
python main.py
```

Un menu principal s'affiche, avec les options suivantes :

```
Menu principal :
1. Lister les tournois
2. Creer un tournoi
3. Ajouter un joueur a un tournoi
4. Commencer/Continuer un tournoi
5. Voir le classement d'un tournoi
6. Rapports
0. Quitter
```

Le sous-menu Rapports propose les 5 rapports listés dans les fonctionnalités ci-dessus, avec une option 0. Retour pour revenir au menu principal.

### Déroulé type

1. Créer un tournoi (option 2) : nom, lieu, dates, nombre de tours (4 par défaut)
2. Ajouter des joueurs (option 3) : au moins 2 joueurs sont nécessaires pour démarrer
3. Commencer/Continuer un tournoi (option 4) : génère le tour suivant selon le système suisse, puis invite à saisir le résultat de chaque match
4. Répéter l'étape 3 jusqu'à ce que tous les tours soient joués, le classement final et le vainqueur s'affichent automatiquement
5. Voir le classement (option 5) est accessible à tout moment, y compris en cours de tournoi

## Format des données

Les données sont stockées dans le dossier data/ (créé automatiquement au premier lancement) :

- data/tournaments.json : tournois, avec leurs tours, matchs et joueurs inscrits (par id)
- data/players.json : joueurs, identifiés par un id interne et un identifiant national d'échecs unique

## Qualité de code

Le projet respecte les conventions PEP8, vérifiées via flake8 (configuration dans setup.cfg : longueur de ligne max 119 caractères).

Génération du rapport HTML :

```
flake8 --format=html --htmldir=flake8_report .
```

Le rapport est ensuite consultable en ouvrant flake8_report/index.html dans un navigateur.

## Auteur

(a completer)
