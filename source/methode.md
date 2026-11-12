<!-- commun -->
# Méthode

## Le cycle : mandat, gates, exécution, audit, consignation

Tout travail suit le même cycle. Le Superviseur rédige un **mandat** : l'objet, les livrables, ce qui est interdit, et les points où
la session doit s'arrêter. L'humain le relit et le dépose ; la session s'ouvre en vérifiant que le calibre qui tourne est bien
celui qui est prévu. Aux arrêts, elle attend un **gate** : une formule explicite, prononcée par l'humain et adressée à la fenêtre
qui l'exécute — « go push … — fenêtre … ». Aucune publication sans gate. L'**exécution** se fait par lots, chacun mesuré avant et
après. Une autre session **audite** ensuite sur pièces, en rejouant les contrôles. Enfin, le Superviseur **consigne** : chaque
décision porte, dans l'historique des versions, une marque qui permet de vérifier qui l'a prise et quand.

## Les registres

La squad travaille sur des registres versionnés : le suivi des tâches, la chronologie datée des décisions, l'inventaire des
risques et de leurs parades, la charte de collaboration, le lexique. Ce sont des documents de travail : ils se corrigent par
erratum, ils ne se réécrivent pas. Toute heure qui y entre est lue à l'horloge, jamais estimée.

## Des règles qu'une machine peut vérifier

Une règle qui dépend du jugement d'un modèle ne survit pas au changement de modèle. Une règle que l'on peut vérifier par un
script — une formule, un préfixe, un compte — tient. Chaque règle nouvelle passe donc un test : quel contrôle dirait qu'elle est
violée ? Et chaque doctrine nouvelle, une autre question : quels rangements existants deviennent faux ?

<!-- cdatso -->
## Un exemple : la chaîne d'une analyse de film

L'humain choisit le film. La skill de production cherche la critique publiée, rédige neuf sections et une bibliographie
numérotée, puis passe des contrôles automatiques qui bloquent la publication au moindre défaut. Deux régimes coexistent : les
Critiques, écrites par l'IA seule, et les Études, reprises ligne à ligne par Christo Datso. La mise en ligne attend son gate. À
côté, une chaîne pilote publie sans relecture, sur une surface d'essai séparée, marquée comme telle sur chaque page : elle sert à
mesurer ce que l'automatisation vaut, pas à se passer de la relecture.

<!-- cdc -->
## Un exemple : la chaîne d'une entrée de base de connaissances

Une entrée naît en Markdown, avec ses sources numérotées. Un générateur la publie par soustraction : l'en-tête de travail est
retiré, le corps reste tel quel. Il écrit la ligne de l'entrée au registre du chapitre, puis reconstruit l'index du chapitre et
l'accueil du site depuis ce registre. La mise en ligne attend son gate. Chaque affirmation renvoie à une source publique que le
lecteur peut rouvrir, et la liste des sources ferme l'entrée. Le même générateur sert les six chapitres : une
correction de gabarit se fait une fois.
