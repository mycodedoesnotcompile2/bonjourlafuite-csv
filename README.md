bonjourlafuite.eu.org CSV dataset
=================================
The automatically daily updated CSV dataset of [bonjourlafuite.eu.org](https://bonjourlafuite.eu.org/)

The data model is following the [upstream one](https://framagit.org/aeris/bonjour-la-fuite/-/blob/257e242ed42e5ddd7fa8a24525278d93e220f681/leaks.yaml):
```
Exemple d'entrée :
- processor: Responsable de traitement concerné
  subcontractor: sous-traitant éventuel
  organization_type: private_company private_company | public_authority | association | federation
  date: 2026-02-19 date de fuite ou de publication
  status: claimed claimed | untrusted, si absent interprété comme "confirmé"
  volume: volume de données concernées
  sensitive: true si les données sont sensibles au sens de l’article 9 du RGPD
  data:
    - Données concernées
  links:
    - https://example.org/preuve
    - img/exemple.png

Le status est à choisir entre :
- 🟢 confirmed : pour celles confirmées (par la presse, notification de données, communiqué de presse…)
- 🟠 claimed : pour une fuite seulement suspectée (publication sur BreachForum…)

organization_type est a choisir entre :
- private_company
- public_authority
- association
- federation
```

Copyright and license
---------------------

All trademarks, service marks, trade names and product names appearing on this repository are the property of their respective owners.  
Material distributed here follow the [upstream MIT licence](https://framagit.org/aeris/bonjour-la-fuite).
