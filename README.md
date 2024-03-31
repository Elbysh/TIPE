# TIPE

## Description du projet

Ce projet est mon TIPE 2023 sur le thème de la ville. Il vise à modéliser le trafic routier à une ou plusieurs voies et en déduire des propriétés générales sur les embouteillages. Le projet a commencé en septembre 2022 et a évolué au fil des mois pour aboutir à une simulation du trafic routier basée sur le modèle des automates cellulaires.

![Exemple de simulation sur 3 voies](/visuals/Exemple_implem_3voies.jpg "début de partie")
![Diagramme_Fondamental](/visuals/Diagramme_Fondamental_437_points.png "début de partie")



## Structure du Code

Le code implémente le modèle de Nagel-Schreckenberg, un modèle d’automates cellulaires, modèle microscopique ayant l’avantage de pouvoir mettre en évidence comment le comportement individuel affecte la circulation globale. Un modèle à temps continu avait été envisagé premièrement, mais j’ai finalement tranché pour un modèle d’automates cellulaires pour simplifier son implémentation notamment pour la gestion du changement de voies des véhicules.


### Représentation de la Route

Dans la représentation de la route :
- `0` représente une partie de la route.
- `1` représente une voiture.
- `2` représente le décor.

### Fonctions Principales

Les principales fonctions du code sont les suivantes :

- `circulation_une_voie`: Simule la circulation sur une voie.
- `circulationkvoie`: Simule la circulation sur plusieurs voies.
- `circulation_fantome`: Simule la circulation avec des embouteillages fantômes.
- `Diagramme_fondamental`: Trace le diagramme fondamental du trafic routier.




## Chronologie du projet

1. **Septembre - Octobre 2022** : Suite à la découverte du sujet Centrale 2005 [3], début des recherches bibliographiques sur la modélisation du trafic routier.

2. **Novembre 2022** : Choix du modèle du conducteur intelligent. Début de la simulation informatique sur ce modèle en langage Python.

3. **Décembre 2022** : Programmation de l'affichage graphique et d'une seule voie de circulation.

4. **Janvier - Février 2023** : Problèmes à gérer les changements de voie rencontrés sur la simulation qui ont entrainé l'abandon de cette dernière au profit d'un modèle avec des automates cellulaires.

5. **Mars 2023** : Obtention du diagramme fondamental du trafic routier avec le modèle des automates cellulaires.

6. **Avril - Mai 2023** : Implémentation de la mise en évidence des embouteillages fantômes.

## Installation et utilisation

Le code de ce projet est écrit en Python et requierts les librairies suivantes : <code>pygame</code>,<code>matplolibb</code>,et <code>numpy</code>. Pour l'exécuter, vous aurez besoin d'un environnement Python installé sur votre machine. Il suffit ensuite de décommenter les fonctions que vous souhaitez exécuter.

