---
title: Animácie v Plotly Dash aplikáciách
author: Martin Rapavý
date: 24.9.2023
path: /dash-adding-animations
language: sk
abstract: Pridávanie animácií z animate.css do Plotly Dash aplikácií.
---

Animácie na webových stránkach môžu mať rôzny účel - či už estetický, alebo môžu slúžiť na upútanie pozornosti na konkrétne prvky. V tomto článku si na dvoch príkladoch ukážeme, ako vieme pomocou projektu [`animate.css`](https://animate.style/) takéto animácie pridať do Dash aplikácií.

### Príprava `animate.css`

`animate.css` je open source projekt, ktorý dáva k dispozícií veľký počet animácií pripravených k jednoduchému použitiu. Pre lepší prehľad sa môžeme pozrieť do oficiálnej [dokumentácie](https://animate.style/), ktorá zároveň slúži ako galéria dostupných animácií.

Aby sme túto knižnicu animácií mohli využiť v našej Dash aplikácií, budeme si musieť stiahnuť [css stylesheet z github repozitáru](https://github.com/animate-css/animate.css/blob/3235f27325ebc721fc4f8435d3c2d436642278bc/animate.css) do priečinku `assets` (pokiaľ ste s priečinkom `assets` ešte nepracovali, viac informácií nájdete v [Dash dokumentácii](https://dash.plotly.com/external-resources)). 

### Vstupná animácia

Jedným z využití animácií sú vstupné animácie, s ktorými sa často stretneme napríklad na osobných stránkach - ich cieľom je hlavne upútať pozornosť a vytvoriť príjemný prvý dojem. 

Predstavme si, že tvoríme projekt o tom, prečo je Dash skvelou knižnicou. Na vstupnej stránke vytvoríme jednoduchý vycentrovaný text, ktorý vygeneroval ChatGPT. Pre lepší dojem by sme radi pridali animáciu, v ktorej sa tento text vyroluje zospodu nahor. 

```python
import dash_mantine_components as dmc  
from dash import Dash  
  
app = Dash(__name__)  
  
app.layout = dmc.Grid(  
    [  
        dmc.Col(  
            dmc.Text(  
                "Knižnica Plotly Dash je nesmierne užitočná pre vývojárov a analytikov dát z niekoľkých dôvodov. "  
 "S jej jednoduchým rozhraním a bohatou paletou komponentov je možné rýchlo vytvárať interaktívne webové" " aplikácie, čím umožňuje užívateľom interagovať s dátami. Táto flexibilita je podporená možnosťou " "vytvárať rôzne typy vizualizácií, ako sú grafy, tabuľky a heatmapy, čo pomáha efektívnejšie " "komunikovať informácie. Plotly Dash je postavený na Pythone, čo uľahčuje integráciu s existujúcimi " "nástrojmi a knižnicami pre analýzu dát. S týmto open-source nástrojom a aktívnou komunitou vývojárov " "máte prístup k pravidelným aktualizáciám a podpore. Navyše, jednoduché nasadenie na rôzne platformy " "robí z Plotly Dash skvelý nástroj pre zdieľanie aplikácií a integráciu do rôznych systémov.",  
                size=20,  
                weight=500,  
            ),  
            span=8,  
            offset=2,  
        )  
    ],  
    align="center",  
    style={"width": "100vw", "height": "100vh"},  
)  
  
if __name__ == "__main__":  
    app.run(debug=True)
```

![enter image description here](https://i.ibb.co/B2p2ZBx/dash-adding-animations-example-preview.png)

Animácie pridáme u komponent z knižnice Dash Mantine Components pomocou parametru `className` (u komponent z knižnice Dash Bootstrap Components by sme použili parameter `class_name`). Do tohto parametru musíme priradiť textový reťazec, ktorý obsahuje `animate__animated` a následne názov danej animácie - v našom prípade to bude `animate__fadeInUp`.  Okrem týchto základných možností môžeme priradiť aj nasledujúce [voliteľné možnosti](https://animate.style/#utilities):

**Rýchlosť animácie:**

- `animate__slow` -	trvanie 2s
- `animate__slower` -	trvanie 3s
- `animate__fast`	-	trvanie 800ms
- `animate__faster`	-	trvanie 500ms
- bez určenia trvá animácia 1s

**Oneskorenie začiatku animácie:**

- `animate__delay-2s`	-	2s
- `animate__delay-3s`	-	3s
- `animate__delay-4s`	-	4s
- `animate__delay-5s`	-	5s

**Počet opakovaní animácie:**

- `animate__repeat-1`	-	1x
- `animate__repeat-2`	-	2x
- `animate__repeat-3`	-	3x
- `animate__infinite`	-	nekonečné opakovanie

V našom príklade si teda navyše animáciu zrýchlime pomocou možnosti `animate__fast`. 

.. admonition::`id` komponenty  
    :icon: mdi:alert
  
	Pokiaľ v našej aplikácii využijeme viacero animácií rovnakého typu na rôzne komponenty, je nutné, aby sme u týchto komponent pridali unikátny identifikátor `id`, inak sa tieto animácie nespustia správne.

Náš kód teda upravíme nasledovne:

```python
import dash_mantine_components as dmc  
from dash import Dash  
  
app = Dash(__name__)  
  
app.layout = dmc.Grid(  
    [  
        dmc.Col(  
            dmc.Text(  
                "Knižnica Plotly Dash je nesmierne užitočná pre vývojárov a analytikov dát z niekoľkých dôvodov. "  
 "S jej jednoduchým rozhraním a bohatou paletou komponentov je možné rýchlo vytvárať interaktívne webové" " aplikácie, čím umožňuje užívateľom interagovať s dátami. Táto flexibilita je podporená možnosťou " "vytvárať rôzne typy vizualizácií, ako sú grafy, tabuľky a heatmapy, čo pomáha efektívnejšie " "komunikovať informácie. Plotly Dash je postavený na Pythone, čo uľahčuje integráciu s existujúcimi " "nástrojmi a knižnicami pre analýzu dát. S týmto open-source nástrojom a aktívnou komunitou vývojárov " "máte prístup k pravidelným aktualizáciám a podpore. Navyše, jednoduché nasadenie na rôzne platformy " "robí z Plotly Dash skvelý nástroj pre zdieľanie aplikácií a integráciu do rôznych systémov.",  
                size=20,  
                weight=500,  
                id="animated-text",  
                className="animate__animated animate__fadeInUp animate__faster",  
            ),  
            span=8,  
            offset=2,  
        )  
    ],  
    align="center",  
    style={"width": "100vw", "height": "100vh"},  
)  
  
if __name__ == "__main__":  
    app.run(debug=True)
```

![enter image description here](https://i.ibb.co/yQkcCcF/dash-adding-animations-text-up.gif)

### Upútanie pozornosti

Častým využitím animácií v aplikáciách je upútanie pozornosti na konkrétne prvky - napríklad aby sme upozornili na to, že tieto prvky sú interaktívne.

V tomto príklade využijeme komponentu [`dmc.Accordion`](https://www.dash-mantine-components.com/components/accordion) a pomocou animácie `animate__flash` by sme chceli upozorniť na šípku v panely. Tým dáme užívateľovi najavo, že na panel je možné kliknúť a akordeón rozbaliť. Vďaka [Styles API](https://www.dash-mantine-components.com/styles-api), konkrétne parametru `classNames`, môžeme animáciu priradiť práve na šípku pomocou selectoru `chevron`. Okrem toho využijeme voliteľné možnosti `animate__delay-3s` (aby sa animácia nespustila hneď pri načítaní stránky) a `animate__repeat-2`(aby sa animácia zopakovala dva krát).

```python
import dash_mantine_components as dmc  
from dash import Dash  
  
app = Dash(__name__)  
  
app.layout = dmc.Stack(  
    [  
        dmc.Divider(  
            label="Example Section",  
            style={"width": "400px"},  
            styles={"label": {"font-size": "20px", "font-weight": 600}},  
        ),  
        dmc.Accordion(  
            children=[  
                dmc.AccordionItem(  
                    [  
                        dmc.AccordionControl("Item"),  
                        dmc.AccordionPanel("This is the first item of the accordion."),  
                    ],  
                    value="item",  
                ),  
                dmc.AccordionItem(  
                    [  
                        dmc.AccordionControl("Another item"),  
                        dmc.AccordionPanel("Second item."),  
                    ],  
                    value="another-item",  
                ),  
                dmc.AccordionItem(  
                    [  
                        dmc.AccordionControl("Super secret item"),  
                        dmc.AccordionPanel("BAZINGA!"),  
                    ],  
                    value="super-secret-item",  
                ),  
            ],  
            chevronPosition="left",  
            variant="separated",  
            style={"width": "400px"},  
            classNames={  
                "chevron": "animate__animated animate__flash animate__delay-3s animate__repeat-2"  
  },  
        ),  
    ],  
    m=40,  
)  
  
if __name__ == "__main__":  
    app.run(debug=True)
```

![enter image description here](https://i.ibb.co/znvRmZf/dash-adding-animations-accordion-chevron.gif)

### Záver

V tomto článku sme sa naučili ako pridať animácie do Dash aplikácie. Nezabúdajme ale na to, že animácie by mali mať jasný účel a nemali by sa používať zbytočne ([Best Practice](https://animate.style/#best-practices) z dokumentácie `animate.css`).
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE0ODI4NTc1MzMsLTEzMjg4NjQ5NDRdfQ
==
-->