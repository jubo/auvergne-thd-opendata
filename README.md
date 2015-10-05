# Auvergne-THD-OpenData
Objectif : Donner accès aux informations du site http://www.auvergnetreshautdebit.fr/ concernant l'avancement du déploiement de la fibre sous un format exploitable.

* Licence : GPL V3. http://choosealicense.com/licenses/gpl-3.0/
* Url de déploiement Heroku (en attendant une url plus propre :) ) : https://peaceful-hamlet-8506.herokuapp.com/
* Toutes les données FTTH    au format CSV : https://peaceful-hamlet-8506.herokuapp.com/search/

Principe : recherche en fonction de mots clé dans le champ spécifié.

* Exemples d'utilisation :
  * Données FTTH de la phase 1 au format CSV : https://peaceful-hamlet-8506.herokuapp.com/search/?key=ZONE&val=1
  * Données FTTH de la phase 2 au format CSV : https://peaceful-hamlet-8506.herokuapp.com/search/?key=ZONE&val=2
  * Données FTTH de la phase 1 au format JSON : https://peaceful-hamlet-8506.herokuapp.com/search/?key=ZONE&val=1&format=json
  * Données FTTH de la phase 2 au format JSON : https://peaceful-hamlet-8506.herokuapp.com/search/?key=ZONE&val=2&format=json
  * Données FTTH du département 63 au format CSV : https://peaceful-hamlet-8506.herokuapp.com/search/?key=DEPARTEMEN&val=63
  * Données FTTH du département 63 au format JSON : https://peaceful-hamlet-8506.herokuapp.com/search/?key=DEPARTEMEN&val=63&format=json

* Features à venir
  * parsing des dates de déploiement pour analyse
  * récupérer dynamiquement les données du site auvergnetreshautdebit.fr en passant l'url à analyser dans la requête http
  * sortie au format HTML
  * lien vers le site Auvergne HD carto
  * IHM de recherche
  * Statistiques de déploiement sur l'ensemble des communes de la région

* Bugs connus : 
  * Format JSON : Caractères spéciaux mal affichés (encodage sortie) 
  * Clé inconnue dans les SimpleSchema du kml
