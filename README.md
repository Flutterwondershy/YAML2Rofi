# Rofi Menu

Permet de lancer rofi avec les entrées renseignées dans un fichier YAML.

## Utilisation en python3

La classe `RofiMenu` représente un menu. Il y a deux manières de 
renseigner le contenu du menu directement dans le constructeur de la 
classe ou utiliser les crochets pour créer/modifier des entrées dans 
le menu.

```python
from rofimenu import RofiMenu

menu = RofiMenu()

menu["Hiberner"] = "systemctl suspend"
menu["Éteindre"] = "systemctl poweroff"
menu["Redémarrer"] = "systemctl reboot"

menu.show_rofi()
```

Une entrée du menu peut-être elle-même une instance de la classe 
`RofiMenu`. Dans ce cas, lorsque l'utilisateur choisit cet option dans
le menu, un autre menu rofi est ouvert.

## Utilisation avec un fichier YAML
Exemple de fichier YAML représentant un menu:
```yaml
Hiberner: "systemctl suspend"
Éteindre: "systemctl poweroff"
Redémarrer: "systemctl reboot"
```
Commande à exécuter: `rofimenu file.yaml`

Pour faire des menus imbriqués, il suffit d'ajouter un étage
supplémentaire dans le fichier YAML. Par exemple:
```yaml
item1:
  item1.1: "cmd1"
  item1.2: "cmd2"
  item1.3: "cmd3"
  
item2:
  item2.1: "cmd4"
  item2.2: "cmd5"
  
item3: "cmd6"
```

## Liste de menus/commandes
Il est possible d'instaurer une liste de commandes/menus qui seront 
affichés/exécutées de manière séquentielle.

```yaml
- a: "export var=a"
  b: "export var=b"
  c: "export var=c"
- "echo Hello World"
- e: "echo $var"
```

## Utilisation de jinja2
Le yaml interprété par le programme peut être généré à l'aide de jinja2:
```yaml
{% set MAX = 6500 %}
{% set MIN = 2500 %}
{% set STEP = 20 %}

{% for i in range(0, 101, STEP) %}
  {% set value = MIN+(MAX-MIN)*i/100 %}
"{{i}}%": "redshift -P -O {{value}}"
{% endfor %}
```
