<style>
    center > img {
        width:50%;
    }
    .legend{
        text-align:right;
        color:gray;
        font-style:italic;
    }
</style>


# Project Case study - Renting

> Julien DERAMAIX - Zakaria KADDOUR-BETCHIM - Leo RASSINDRAME - Valentin RICARDO - Aaron RANDRIANARISONA

# Introduction

La discrimination dans les processus de location, qu'il s'agisse de logements, est un sujet d'actualité qui mérite une attention particulière. Notre travail consiste à identifier les niveaux à travers l'analyse d'un jeu de données représentant ces processus.

L'objectif est d'explorer plusieurs questions clés :

- Quels sont les chemins suivis par les demandes de location, et leur fréquence ?
- Quels facteurs pourraient conduire à des discriminations, en termes de temps, coût ou accès ?
- Comment ces discriminations se manifestent-elles dans les différentes étapes du processus ?

À travers des analyses sur ce jeu de données, nous visons à sensibiliser aux différents biais et à proposer des recommandations de locations favorisant la réussite de l'échange.

# Dataset Renting

Le jeu de données utilisé pour cette analyse porte sur le processus de location de logements. Il a été collecté dans le but d'étudier les variations dans le traitement des demandes et de détecter d'éventuels comportements discriminatoires ou anomalies au sein de ce processus.

## Origine

Les données utilisées proviennent d'une simulation conçue pour représenter des scénarios plausibles dans le secteur de la location immobilière. Trois journaux d'événements distincts ont été créés pour modéliser des processus typiques de location, intégrant des facteurs potentiellement générateurs de biais.

Le processus simulé débute par la visite du bien, avec la signature du contrat, l’aménagement dans le logement, jusqu'à la fin de la location.

## Degré de discrimination

Les trois journaux d'événements ont été conçus pour refléter différents niveaux de discrimination de la part des propriétaires :

| **Niveau**   | **Description**|
|--|--|
| **Faible** | Les décisions sont ouvertes, et des personnes aux profils variés sont acceptées sans restriction notable. |
| **Modéré** | Les décisions sont modérées, avec des critères plus sélectifs mais pas systématiquement exclusifs. |
| **Élevé** | Les décisions sont strictes, avec des critères rigides qui excluent systématiquement certains profils. |



## Structure des données

Chaque journal (log) est constitué d'un ensemble de traces, chacune contenant plusieurs événements. Les fichiers sont aux format ``.XES``.

Voici la structure des traces et des événements des trois ensembles de données :

Il est important de noter que la propriété `religious affiliation`, qui aurait pu être intéressante à inclure, ne fait pas partie des ensembles de données. Cette exclusion a probablement été faite pour éviter toute controverse et peut causer des erreurs dans la conclusion de notre analyse.

> "*The logs contain attributes that can shed light on potential biases in the process. 'Age', 'citizen', 'German speaking', 'gender', 'religious affiliation', and 'yearsOfEducation' might influence the rental process, leading to potential discrimination.*"

*<u>Source</u> : https://www.pads.rwth-aachen.de/cms/PADS/Forschung/Event-Logs/~bcbswu/-Un-Fair-Event-Logs*

<center>
    
<img src="https://m2-lr.freeboxos.fr/uploads/1743b49e-9c29-4e21-a6c9-879add2d4075.png"/>

</center>




### Entité : Trace

| Nom de la propriété  | Description                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| **@@case_index**     | Identifiant unique pour chaque trace                                      |
| **case**             | Nom ou identifiant du cas spécifique                                      |
| **concept name**     | Description ou nom de l'activité ou du concept étudié dans le cas         |
| **yearsOfEducation** | Nombre d'années d'éducation                                               |
| **german speaking**  | Indique si la personne parle allemand                                     |
| **age**              | Âge de la personne                                                        |
| **gender**           | Genre de la personne considérée comme homme ou femme (valeur booléenne)   |
| **citizen**          | Statut de citoyenneté                                                     |
| **protected**        | Indique si la personne bénéficie d'une protection juridique particulière. |
| **married**          | Indique si la personne est mariée                                         |

---

### Entité : Event

| Nom de la propriété         | Description                                 |
| --------------------------- | ------------------------------------------- |
| **@@Index**                 | Identifiant unique lié à une trace.         |
| **activity / concept:name** | Nom de l'activité ou du concept             |
| **resource**                | La ressource utilisée                       |
| **time / time:timestamp**   | L'heure à laquelle l'activité est effectuée |

Après une analyse visuelle des différentes versions du dataset, nous avons constaté que certaines données présentent des attributs supplémentaires, manquants ou des doublons, comme c'est le cas avec les clés ``time`` et ``time:timestamp``. Bien qu'il n'y ait aucun impact sur la logique, cela peut légèrement affecter la compréhension et le traitement des calculs.


## Les statisques du dataset

Dans un premier temps, dans notre étude de cas, nous visons à obtenir une meilleure compréhension du jeu de données mais également souhaitons guider notre analyse vers des premières pistes potentielles de discrimination dans le dataset. Pour cela, effectuer une analyse statistique serait de première utilité.

### Vue d'ensemble

Il y a avant tout, des données communes à nos trois datasets :

**Nombre total de traces:** `10 000`

**Nombre de types d'activité unique:** ``16``

**Nombre total d'activités effectuées dans l'ensemble des datasets:** `292 000`


<center>

<img src="https://m2-lr.freeboxos.fr/uploads/74540816-854f-42ac-93be-67397af82121.png"/>
</center>

### Taux de succès par propriétées du dataset

Nous allons observer pour chaque propriété du dataset le taux de personnes qui signent une location. Ces données nous permettront d'extraire de potentielles propriétés discriminantes. Cependant, la discrimination pouvant être multi-factorielle, les conclusions faites sur ces statistiques ne seront pas représentatives des vraies sources de discrimination et ce sera donc en addition avec le clustering que l'on obtiendra de meilleures conclusions.

#### Germanophone
<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/d5db3cae-16b5-4e32-a6ed-73d61047fa15.png" alt="Image 1" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/229694b2-7e8c-4502-81c5-f9a2fa2dd1cb.png" alt="Image 2" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/0b0f2d41-d2bc-47c7-8f23-ab15782328a7.png" alt="Image 3" style="width: 50%;" />
  </div>
</div>

Sur ces graphiques, on observe une tendance où les non-germanophones sont légèrement plus refusés. Ainsi on qualifie cette propriété comme légèrement discriminante.


#### Groupe d'âge

<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px; margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/bfd39d99-4d0f-423e-b72e-65e34813c1d5.png" alt="Image 4" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/b41429ed-42a4-4557-ba50-aa74400d34d5.png" alt="Image 5" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/b0bce5bf-41da-4702-88c9-40d3338dfd1f.png" alt="Image 6" style="width: 50%;" />
  </div>
</div>

Ici, on observe de manière globale une baisse des signatures pour les personnes de plus en plus âgées. Cette propriété est donc discriminante.

#### Genre (H/F)

<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/ec622fb1-b559-4fa2-871a-4b74276e5def.png" alt="Image 1" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/7fd5d334-3c08-4157-be21-01514104ed50.png" alt="Image 2" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/bd8d5b7b-5f18-4d63-8df0-40be12d6bd97.png" alt="Image 3" style="width: 50%;" />
  </div>
</div>

Nous avons décidé qu’un homme est symbolisé par True et une femme par False.

Ainsi, ici on observe moins de signatures pour les femmes, on classe donc cette propriété comme discriminante.

#### Citoyenneté

<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/62b52479-d09b-4d32-abb5-a85e467976ac.png" alt="Image 1" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/f0a720a8-278a-4cd0-9c58-c3a9e2f82314.png" alt="Image 2" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/c2317bb6-544e-4287-8c39-568f068f1ce2.png" alt="Image 3" style="width: 50%;" />
  </div>
</div>

Encore une fois, on observe une différence entre ceux qui ont la nationalité et ceux qui ne l'ont pas. 
Cette propriété est donc légèrement discriminante.

#### Statut protégé
<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/2af3f35f-cffa-4569-914b-5f8c1e17b570.png" alt="Image 1" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/aba7127a-7d05-4047-9884-ca20519560c7.png" alt="Image 2" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/43545119-6319-48f7-8514-409341de3631.png" alt="Image 3" style="width: 50%;" />
  </div>
</div>

Ici les observations sont très claires, les possesseurs du statut "protected" signent moins souvent que ceux qui ne l'ont pas.
La propriété est clairement discriminante.

#### Statut marital
<div style="text-align: center;">
  <div style="display: flex; justify-content: center; gap: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/f4e8982d-b078-438c-827d-97a2e22c7195.png" alt="Image 1" style="width: 50%;" />
    <img src="https://m2-lr.freeboxos.fr/uploads/4490614f-c13c-4efb-bbe8-bd7d7d429f0f.png" alt="Image 2" style="width: 50%;" />
  </div>
  <div style="margin-top: 20px;">
    <img src="https://m2-lr.freeboxos.fr/uploads/550966a2-456c-477f-9e90-5f9ac87cd8ca.png" alt="Image 3" style="width: 50%;" />
  </div>
</div>

On observe qu'être marié augmente légèrement les chances de signer le contrat de location, donc la propriété est légèrement discriminante.

<!--
![](https://m2-lr.freeboxos.fr/uploads/43373a13-5829-441f-b185-9a0ff71ec607.png)

![](https://m2-lr.freeboxos.fr/uploads/ec214d96-2435-4418-9849-810f77226f3f.png)
-->

### Conclusion statistiques

Après cette vue d'ensemble, on a noté sur ce tableau les propriétés légèrement discriminantes en bleu, tandis que celles nettement discriminantes en rouge.

<center>

<img src="https://m2-lr.freeboxos.fr/uploads/7ee05529-947b-4402-8475-d13989819590.png"/>
    
</center>


# Algorithme de découverte

Après une rapide vue d'ensemble, nous avons appliqué différents algorithmes (Alpha, heuristiques, induction et fuzzing) connus sur nos jeux de données. Ces algorithmes nous permettent d'analyser en profondeur les processus et d'en extraire des modèles.


## Alpha

<center>
<img src="https://cdn.discordapp.com/attachments/418667174568132618/1313418040716824619/image.png?ex=67500f5f&is=674ebddf&hm=2ae297743bfe9dbb4e4e44c87ef85983408259222cf6e14923be8287ad0b6b08&"/>

<p class="legend">
    Capture d'écran du réseau de Petri généré par PM4PY sur le dataset <code>renting_log_medium</code>
</p>


<img src="https://m2-lr.freeboxos.fr/uploads/e6797957-64d8-48f3-b2bd-a573a7dd52d0.jpg"/>

<p class="legend">
    Capture d'écran du réseau de Petri généré par ProM sur le dataset <code>renting_log_medium</code>
</p>
</center>

| Métrique        | High | Medium | Low  | Moyenne |
| --------------- | ---- | ------ | ---- | ------- |
| Fitness (TBR)   | 0.77 | 0.76   | 0.76 | 0.76    |
| Precision (TBR) | 0.36 | 0.36   | 0.36 | 0.36    |
| Generalization  | 0.98 | 0.98   | 0.98 | 0.98    |
| Simplicity      | 0.62 | 0.62   | 0.62 | 0.62    |
| Precision       | 0.55 | 0.55   | 0.54 | 0.54    |
| Recall          | 0.97 | 0.98   | 0.97 | 0.97    |
| F-score         | 0.70 | 0.70   | 0.70 | 0.70    |

- **Fitness (0.76) :** Son fitness est le plus faible des trois, indiquant une capacité limitée à reproduire les données observées. Cela peut poser problème dans des cas nécessitant une haute adéquation.
- **Precision (0.54) :** Sa faible précision montre qu'il est susceptible de produire des comportements non observés dans les données, ce qui peut nuire à la qualité du modèle.
- **Generalization (0.98) :** Il excelle dans cette métrique, indiquant qu'il génère des modèles très généralisables, capables de capturer les comportements futurs potentiels tout en évitant le surapprentissage.
- **Simplicity (0.62) :** Il est également le moins performant en simplicité, ce qui pourrait rendre ses modèles plus complexes et moins intuitifs.
- **Recall (0.97) :** Avec un rappel très élevé, il couvre la majorité des traces observées, garantissant que les modèles qu'il produit ne laissent pas de comportements non représentés.
- **F-Score (0.7) :** Son équilibre entre précision et rappel est limité par ses performances relativement faibles sur certaines métriques.

L'Alpha Miner ($\alpha$-Algorithm) est un algorithme simple et intuitif, efficace pour modéliser des relations simples, comme lorsqu'une personne visite un bien et se désiste peu après. Cependant, il peine à représenter des comportements plus complexes, tels que des événements répétitifs comme "Pay Rent", qui se renouvelle régulièrement dans les logs. En raison de cette limitation, l'Alpha Miner est particulièrement adapté pour des applications nécessitant une forte généralisation et un bon rappel, mais il montre ses limites dans les scénarios demandant une haute précision ou une représentation des répétitions d'événements. Pour mieux capturer ces comportements complexes, il est recommandé d'utiliser un algorithme plus avancé, tel que l'Inductive Miner.


## Fuzzer

Le Fuzzer Miner est un algorithme de mining de processus qui utilise une approche exploratoire basée sur le "fuzzing". Il perturbe aléatoirement les événements et relations dans les logs pour découvrir de nouveaux modèles de processus, y compris des comportements complexes ou inattendus. Bien qu'il soit robuste face aux anomalies dans les données, il peut produire des modèles plus difficiles à interpréter et moins précis que des algorithmes classiques. Il est utile pour tester la résilience des processus et identifier des comportements non observés dans les logs.

<center>
    
<img src="https://m2-lr.freeboxos.fr/uploads/c70cc25a-814b-4b17-a6a6-13c26322e1cf.png"/>
    

<p class="legend">
     Capture d'écran du fuzzy model généré par Fuzzer Miner avec ProM sur le dataset <code>renting_log_low</code>
</p>
    
</center>

<center>

<img src="https://m2-lr.freeboxos.fr/uploads/53a1bd6c-b92e-491b-b899-c9666304fa44.png"/>


<p class="legend">
     Capture d'écran du fuzzy model généré par Fuzzer Miner avec ProM sur le dataset <code>renting_log_medium</code>
</p>
    
</center>

<center>
    
<img src="https://m2-lr.freeboxos.fr/uploads/b5cc130f-00ed-49ba-a3c9-220b606549dc.png">
    
</center>

Cluster 17: 

<center>
    
<img src="https://m2-lr.freeboxos.fr/uploads/3bac68bb-dd7f-46ad-b84e-f1678fcbe6f2.png"/>
<p class="legend">
     Capture d'écran du fuzzy model généré par Fuzzer Miner avec ProM sur le dataset <code>renting_log_high</code>
</p>
    
</center>


| Métrique                | High | Medium | Low  | Moyenne |
| ----------------------- | ---- | ------ | ---- | ------- |
| Fuzzy model conformance | 0.97 | 0.98   | 0.98 | 0.97    |
| Fuzzy model detail      | 0.75 | 1.0    | 1.0  | 0.92    |


## Heuristics

![](https://m2-lr.freeboxos.fr/uploads/c8fa5fe5-1ab7-4ffb-8dfa-fb255d308aa7.png)
<p class="legend">
     Capture d'écran du réseau de Petri généré par Heuristic Miner avec PM4PY
</p>


| Métrique                       | High  | Medium | Low   | Moyenne |
| ------------------------------ | ----- | ------ | ----- | ------- |
| Fitness Globale                | 0.98  | 0.99   | 0.98  | 0.98    |
| Précision des Traces           | 0.72 | 0.88  | 0.65 | 0.75   |
| Fitness Moyenne des Traces     | 0.99  | 0.99   | 0.99  | 0.99    |
| Précision des Empreintes       | 1.00  | 1.00   | 1.00  | 1.00    |
| Précision (Token-based Replay) | 1.00  | 1.00   | 1.00  | 1.00    |
| Généralisation                 | 0.96  | 0.97   | 0.98  | 0.97    |
| Simplicité du Réseau de Petri  | 0.69  | 0.70   | 0.70  | 0.70    |
| Réseau de Petri Sonore         | Non   | Non    | Non   | Non     |

- **Fitness (0.99) :** Très proche du score parfait, il démontre sa capacité à s'adapter aux données observées.
- **Precision (TBR) (1) :** Il atteint une précision parfaite, ce qui signifie qu'il est extrêmement efficace pour éviter les comportements superflus ou imprévus. Cela en fait un excellent choix pour des processus nécessitant une modélisation stricte.
- **F-Score (0.98) :** Avec un F-Score presque parfait, il équilibre parfaitement précision et rappel, offrant une grande fiabilité pour des modèles de processus.
- **Simplicity (0.7) :** Il offre une simplicité relativement bonne, rendant les modèles compréhensibles pour les utilisateurs finaux.
- **Generalization (0.97) et Recall (0.97) :** Bien qu'il ne domine pas ces métriques, ses scores élevés montrent qu'il reste un choix polyvalent et compétent.

En somme, l'Heuristic Miner est un choix idéal pour des scénarios où la précision stricte et l'équilibre global (F-Score) sont essentiels, tout en restant performant sur les autres aspects. Bien qu'il soit plus adapté que l'Alpha Miner pour traiter des logs réels, il peut parfois produire des modèles plus complexes à interpréter et moins précis que des algorithmes plus avancés, comme l'Inductive Miner. Par exemple, il peut générer des "boîtes noires" ou des transitions silencieuses, compliquant ainsi l'analyse. Cependant, l'Heuristic Miner excelle dans des situations plus complexes, en prenant en compte des relations variées entre les événements, telles que la causalité et la concurrence, ce qui lui permet de mieux capturer des comportements complexes, y compris les répétitions d'événements.


## Inductive

![](https://m2-lr.freeboxos.fr/uploads/e2859de2-352b-403a-a87b-7a170ebd469c.png)

<p class="legend">
    Sortie du réseau de Petri généré par Inductive Miner via PM4PY
</p>


| Métrique        | High | Medium | Low  | Moyenne |
| --------------- | ---- | ------ | ---- | ------- |
| Fitness (TBR)   | 1.00 | 1.00   | 1.00 | 1.00    |
| Precision (TBR) | 0.82 | 0.81   | 0.82 | 0.82    |
| Generalization  | 0.97 | 0.97   | 0.97 | 0.97    |
| Simplicity      | 0.71 | 0.71   | 0.71 | 0.71    |
| Soundness       | True | True   | True | True    |
| Precision       | 0.85 | 0.84   | 0.85 | 0.85    |
| Recall          | 0.97 | 0.97   | 0.97 | 0.97    |
| F-score         | 0.90 | 0.90   | 0.90 | 0.90    |

- **Fitness (1) :** Avec un score parfait de 1, il parvient à reproduire complètement les traces observées, ce qui en fait une option fiable pour des processus où l'adéquation est essentielle.
- **Simplicity (0.71) :** Il obtient la meilleure simplicité parmi les trois, signifiant que le modèle généré est facilement compréhensible et utilisable, ce qui est souvent crucial pour l'analyse métier.
- **Precision (0.85) :** Avec une précision élevée, il montre sa capacité à éviter les comportements qui ne sont pas observés dans les données, réduisant ainsi le bruit.
- **Generalization (0.97) :** Bien qu'il ne surpasse pas Alpha Miner sur cette métrique, son score reste très élevé, indiquant qu'il trouve un bon équilibre entre spécificité et généralisation.
- **Recall (0.97) :** Son rappel élevé garantit qu'il couvre bien les traces observées.
- **F-Score (0.9) :** Ce score élevé reflète son excellent équilibre entre précision et rappel, confirmant sa robustesse globale.

En résumé, l'Inductive Miner est un excellent choix pour ceux qui recherchent un algorithme performant sur plusieurs dimensions clés, notamment la simplicité et la précision, tout en offrant un bon compromis pour des métriques comme la généralisation et le rappel. Cet algorithme, qui construit des modèles à partir de logs d'événements de manière inductive, identifie des structures de contrôle complexes telles que les séquences, les boucles, la concurrence et les choix. Il génère des modèles hiérarchiques et robustes, même en présence de bruit, garantissant des résultats corrects. L'Inductive Miner est particulièrement adapté pour modéliser des processus d'affaires complexes, avec des comportements imbriqués ou répétitifs, tout en restant rapide et efficace.


# Comparaison des modèles
<center>
<img src="https://m2-lr.freeboxos.fr/uploads/b15a76d5-2f22-44e4-bfa0-66f41aa56831.png"/>
</center>

Concernant la soundness des modèles, voici les résultats pour les algorithmes suivants:

| Algorithme       | Soundness|
| ---------------- | -------- |
| Heuristics Miner |  False   |
| Inductives Miner |  True    |

Le choix de l'algorithme optimal pour analyser le dataset Renting dépend fortement des priorités de l'étude. Inductive Miner se distingue par son excellent équilibre entre précision, simplicité et flexibilité, ce qui en fait une option idéale pour des analyses qui nécessitent des modèles interprétables et efficaces, notamment dans un contexte commercial. Il offre également de solides performances en termes de généralisation et de rappel, garantissant une bonne couverture des comportements observés. Heuristics Miner, en revanche, excelle lorsqu’une modélisation précise des étapes du processus est cruciale. Il est particulièrement adapté pour des analyses nécessitant une stricte fidélité aux données d'origine, comme celles visant à optimiser ou valider des processus complexes. Enfin, Alpha Miner est plus pertinent pour des analyses macroscopiques où la détection des tendances générales ou des comportements utilisateur à long terme est privilégiée. Bien qu'il manque de précision et de simplicité comparé aux autres algorithmes, il reste une option viable pour des besoins de généralisation. En somme, le choix de l’algorithme dépend des objectifs spécifiques : Inductive Miner pour un modèle équilibré et interprétable, Heuristics Miner pour une modélisation détaillée et précise, et Alpha Miner pour une approche axée sur la généralisation.

# Clustering et Profils des Groupes

Afin de déterminer distinctement les facteurs discriminants et effectuer des prédictions pour déterminer si un profil d'une nouvelle personne est susceptible de signer un contrat d'appartement, nous avons effecuté un clustering sur nos données. 
<center>
<img src="https://m2-lr.freeboxos.fr/uploads/1b93bdc4-6a00-4447-bcca-fe6eb00b20f8.png"/>
<p class="legend">
    Dendogramme pour sélectionner la coupe optimale (optimal = 2)
</p>
</center>

*Note : À partir d'ici, nous n'avons strictement rien compris à nos manipulations. Malgré l'application des connaissances aquises en cours, toute l'aide extérieure, aussi bien au près de camarades que des IA, nous n'avons pas réussi à obtenir les résultats que nous espérions... Les résultats sont à peine explicable et nous aurions aimé aller plus loin avec ces derniers.*

Maintenant que nous connaissons la coupe optimale, il est temps de découper nos données. Pour déterminer des clusters sur nos jeux de données, nous avons effectué plusieurs approches : 
- `AgglomerativeClustering`
    - Cette approche n'a pas pu se poursuivre pour des raisons techniques `MemoryError: Unable to allocate 3.77 GiB for an array with shape (4047435406, ) and data type bool`
- Kmeans
    - Nous avons effectué plusieurs tests via plusieurs approches dans nos codes, mais rien n'a donné de modèles satisfaisants. Prennons par exemple 2 graphes générés par nos codes `test_kmeans.py` et `test_kmeans_2.py`...

<center>
<img src="https://m2-lr.freeboxos.fr/uploads/1ac8f4bd-4150-408e-a765-384f32848167.png"/>
<p class="legend">
 Figure des clusters générés avec test_kmeans.py
</p>

<img src="https://m2-lr.freeboxos.fr/uploads/6be57eb1-1a08-4fd0-8fde-02d312cc6fe5.png"/>
<p class="legend">
 Figure des clusters générés avec test_kmeans_2.py
</p>
    
</center>

Dans les tests, on effectue une prédiction sur une nouvelle trace pour savoir si elle a ses chances d'avoir un appartement on non, basé sur l'évènement "Sign Contract". Et dû au cluster à la propotion fort discutable, la prédiction n'a pas trop de sens puisque tous les points finissent dans le même cluster. 

Nous sommes également passé par une approche à l'aide de variants pour réduire le nombre de données à traiter, mais même là ce n'est pas pertinant, car les refus de contrats sont des actions souvent répétées en que quelques étapes, donc au total on peut avoir ~4 variants sur +400 cas où une personne loge dans un appartement. Nous avons aussi utilisé l'outil "Orange" en Python pour analyser nos données, et c'est là qu'on s'est rendu compte que cette approche était un peu 
<center>
<img src="https://cdn.discordapp.com/attachments/1293594455391211671/1316787226323062824/Capture_decran_2024-12-12_161708.png?ex=675c512b&is=675affab&hm=0e796e77b76970e78ee3a2d6d03403d2db76d4b028e03f3c37e78c8d31fb2a34&"/>
<p class="legend">
 Affichage généré par Orange de répartition des variants selon la variable "protected", colorié selon "Sign Contract"
</p>
    
</center>

Quelque chose qu'on aurait pû faire pour améliorer nos analyses, c'est **divisier le processus métier en 2 sous parties** : L'un pour **l'acceptation de contrat**, l'autre **pour les résidents**. Mais ça n'a pas pu se faire à défaut de temps. 


# Gestion de projet

Lors de ce projet, nous avons choisi de créer un dépôt GitHub pour centraliser notre code et gérer nos tâches. Pour ce faire, nous avons utilisé les issues et les milestones afin de classer et suivre l'avancement des différentes tâches de manière organisée.

De plus, nous avons eu recours à Discord pour faciliter la communication entre les membres de l’équipe, permettant ainsi un échange rapide et fluide d’informations.

# Réflexion sur la Vie Privée

Le jeu de données repose sur des informations réelles qui ont été anonymisées. Cet anonymat empêche toute identification des individus concernés, garantissant le respect de leur vie privée, grâce à l'utilisation d'identifiants (*id*) plutôt que de stocker en clair le nom des personnes suivies. Si les données n'avaient pas été anonymisées, elles auraient pu inclure des informations sensibles, comme le nom ou l'apparence, ce qui aurait impliqué une responsabilité accrue dans leur gestion et leur utilisation.

# Conclusion

Nos observations montrent qu'il n'y a pas de réelles discriminations entre les données et que le résultat de "Sign Contract" n'est pas plus influencé par l'âge, le temps d'étude, ou si la personne parle allemand par exemple.. D'autant qu'il manque en plus la variable d'appartenance d'éthnie, qui aurait pu donner plus d'indications s'il y a une réelle discrimination.

Comme dit dans la partie cluster, nous aurions pu divisier le processus métier en 2 sous parties : L'un pour l'acceptation de contrat, l'autre pour les résidents. Puisque ça n'a pas trop de sens d'étudier le suivi d'un processus et de le raccourcis vers une fin distincte sur le temps comme là. 


# Références

- [(Un)Fair Event Logs](https://www.pads.rwth-aachen.de/cms/PADS/Forschung/Event-Logs/~bcbswu/-Un-Fair-Event-Logs/)

- [PM4PY](https://pypi.org/project/pm4py/)

- [ProM](https://promtools.org)


