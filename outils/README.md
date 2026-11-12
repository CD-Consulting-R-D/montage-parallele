# outils — l'assemblage des deux éditions

| Script | Rôle | Écrit |
|---|---|---|
| `build_editions.py` | lit `source/*.md` (et `source/en/*.md`) et assemble les deux éditions | les pages de la racine de ce dépôt (édition cd-consulting-rd.be) et le dossier voisin `montage-parallele-cdatso` (édition cdatso.be) |
| `controle_editions.py` | contrôle les deux éditions : tronc commun identique, liens internes, ressources distantes, `canonical` / `hreflang`, publication par soustraction | rien (lecture seule ; code de sortie 0 = conforme) |

## Rejouer

Depuis n'importe quel répertoire (Python 3.12, aucune dépendance) :

```
python -I -B C:\Users\cdats\Claude\CDC\montage-parallele\outils\build_editions.py
python -I -B C:\Users\cdats\Claude\CDC\montage-parallele\outils\controle_editions.py
```

- Le script d'assemblage n'écrit un fichier que si son contenu change : une seconde exécution annonce « 0 fichier ».
- Il affiche le compte de mots par page, par édition et par langue (budget : 400 / 300 / 350 / 700, soit 1 750).
- Les liens absolus (site des films, autres sites) sont listés par le contrôle, pas suivis.

## Ce que fait le gabarit

Chrome, feuilles et fontes de `assets/` (inchangés), plus : un mode sombre (réglage du système par défaut, bouton
« Light / Dark » mémorisé sous la clé `kb-theme`, comme les index des bases de connaissances), la mention de transparence
(AI Act, article 50) au pied, aucune ressource distante. L'ancienne adresse `lecons-du-premier-mois.html` devient une
page-renvoi vers `lecons.html` (édition cd-consulting-rd.be, la seule où elle a existé).
