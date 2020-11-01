---
layout: page
title: "Foire aux Questions"
permalink: /faq
---


1. [L\'inventaire](#linventaire)
2. [Site de l\'inventaire](#site-de-linventaire)
    * [Mon compte](#mon-compte)
        * [Comment me connecter et me déconnecter de mon compte?](#comment-me-connecter-et-me-déconnecter-de-mon-compte)
        * [Je souhaite changer de mot de passe, est-ce possible?](#je-souhaite-changer-de-mot-de-passe-est-ce-possible)
        * [J'ai changé d'adresse e-mail, comment la modifier dans mon compte?](#jai-changé-dadresse-e-mail-comment-la-modifier-dans-mon-compte)
        * [À quoi servent mes informations personnelles?](#à-quoi-servent-mes-informations-personnelles)
    * [Effectuer l'inventaire](#effectuer-linventaire)
        * [Où puis-je rentrer les informations sur une photographie?](#où-puis-je-rentrer-les-informations-sur-une-photographie)
        * [Quelles sont les informations obligatoires, et celles optionelles?](#quelles-sont-les-informations-obligatoires-et-celles-optionelles)
        * [Je ne trouve pas la rue, la ville, le site, ou toute autre information, dans les menus déroulants, comment puis-je faire?](#je-ne-trouve-pas-la-rue-la-ville-le-site-ou-toute-autre-information-dans-les-menus-déroulants-comment-puis-je-faire)
        * [Les mots-clés sont vraiment importants, j'aimerais connaître comment les utiliser, existe-t-il une documentation spécifique?](#les-mots-clés-sont-vraiment-importants-jaimerais-connaître-comment-les-utiliser-existe-t-il-une-documentation-spécifique)
        * [J'ai enregistré les informations, mais je souhaite les modifier, comment faire?](#jai-enregistré-les-informations-mais-je-souhaite-les-modifier-comment-faire)
        * [J'ai terminé mon lot de photographies, que faire désormais?](#jai-terminé-mon-lot-de-photographies-que-faire-désormais)
    * [Les données de l'inventaire](#les-donnes-de-linventaire)
        * [Quelles visualisations sont disponibles?](#quelles-visualisations-sont-disponibles)
        * [Comment rechercher dans le catalogue?](#comment-rechercher-dans-le-catalogue)
        * [Comment utiliser à l'API?](#comment-utiliser--lapi)
    * [Le site renvoie une erreur, est-ce normal?](#le-site-renvoie-une-erreur-est-ce-normal)
3. [Informations globales](#informations-globales)
    * [Qui contacter ?](#qui-contacter)
    * [Puis-je réutiliser les données ou le code source?](#puis-je-rutiliser-les-donnes-ou-le-code-source)


## L'inventaire

## Site de l'inventaire
### Mon compte
#### ![question](img/question.png){:height="25px"}Comment me connecter et me déconnecter de mon compte?

Pour remplir l'inventaire, il est nécessaire de disposer d'un compte. 


Si vous êtes autorisé à participer à l'inventaire, un mot de passe a été envoyé à votre adresse mail.


Pour vous **connecter**, il vous suffit alors de cliquer sur [l'onglet "Connexion"](http://parishistoriqueinventaire.eu.pythonanywhere.com/connexion), de rentrer votre nom de famille avec une majuscule au début, puis votre mot de passe.
![bouton_connexion](img/bouton_connexion.png){:width="750px"}
![connexion](img/connexion.png){:width="750px"}


Pour me **déconnecter**, il suffit de cliquer dans l'onglet "Mon compte" > "Déconnexion".
![déconnexion](img/bouton_deconnexion.png){:width="750px"}


#### ![question](img/question.png){:height="25px"}Je souhaite changer de mot de passe, est-ce possible?
Bien sûr! Pour cela, rien de plus simple. Il suffit de cliquer sur "Mot de passe oublié?" sur la [page de connexion](http://parishistoriqueinventaire.eu.pythonanywhere.com/connexion).
![mdp_oublie](img/bouton_mdp_oublie.png){:width="750px"}

Remplissez ensuite votre adresse mail, et vous recevrez un e-mail avec un lien (pensez à regarder vos spams), comme l'exemple suivant.
![mail_reset_mdp](img/mail_mdp.png){:width="750px"}


Cliquer sur ce lien va vous permettre de changer votre mot de passe.

![reset](img/reset_mdp.png){:height="120px"}

#### ![question](img/question.png){:height="25px"}J'ai changé d'adresse e-mail, comment la modifier dans mon compte?

Une page spéciale vous permet de voir et de modifier l'ensemble des informations vous concernant: nom, prénom, et adresse e-mail.
Cette page est disponible à l'adresse [http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/mon_profil](http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/mon_profil) ou bien en cliquant dans l'onglet "Mon espace" > "Mon profil".
![profil](img/mon_profil.png){:width="750px"}


La page obtenue permet de modifier ses informations personnelles, ainsi que de changer de mot de passe.
Des chiffres personnels sont également disponibles afin de voir le travail réalisé.
![page_profil](img/page_profil.png){:width="750px"} 

#### ![question](img/question.png){:height="25px"}À quoi servent mes informations personnelles?

Très peu d'informations sont nécessaires à la réalisation de l'inventaire:
* le *nom* et le *prénom* sont insérés dans l'inventaire afin de pouvoir avoir une trace de la personne qui a réalisé l'inventaire de chaque photographie
* le *mail* vous permet de recevoir le lien de modification de votre mot de passe, à tout moment

**Aucune autre information ne vous sera demandée.**

### Effectuer l'inventaire
#### ![question](img/question.png){:height="25px"}Où puis-je rentrer les informations sur une photographie?

Un seul endroit permet d'enregistrer une photographie: [http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/cataloguer?nom_user=VOTRE_NOM](http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/cataloguer). Cette page est accessible dans l'onglet "Mon espace" > "Cataloguer".
![bouton_cataloguer](img/bouton_cataloguer.png){:width="750px"}

Vous trouverez sur cette page l'ensemble des informations qu'il est possible de remplir sur une photographie. (Voir [Quelles sont les informations obligatoires, et celles optionelles?](#quelles-sont-les-informations-obligatoires-et-celles-optionelles) pour savoir quelles informations il est absolument nécessaire de rentrer.)
![page_cataloguer](img/page_cataloguer.gif){:width="750px"}

#### ![question](img/question.png){:height="25px"}Quelles sont les informations obligatoires, et celles optionelles?

Le catalogage des photographies est très souple et s'adapte aux photographies que vous avez sous les yeux: ainsi, peu de champs seront bloquants s'ils ne sont pas remplis.

Le **numéro d'inventaire** est absolument nécessaire, tout comme l'un des dix descripteurs de **"Généralité architecture"**. L'ensemble des autres champs peut ne pas être rempli si vous n'avez pas les informations pour le faire.

Cependant, n'oubliez pas que le but de l'inventaire est la description des photographies. S'il peut arriver fréquemment que l'on ne connaissance ni l'adresse ni les informations comme les droits ou le photographe, il est normalement toujours possible de poser au moins un ou deux **mots-clés** puisqu'ils sont décidés en fonction du contenu de la photographie.

Concernant la **localisation GPS**, vous n'êtes pas obligé de chercher la localisation sur la carte. Cependant, si vous le faites, il faut être certain que l'adresse remplie plus haut dans le formulaire soit exactement cette localisation GPS: un traitement automatique se fait plusieurs fois par mois afin de relier toutes les adresses similaires à une seule localisation; la localisation rentrée par le formulaire par vos soins est prioritaire face aux données qui sont normalement rapatriées depuis le site du gouvernement.

Enfin, l'inventaire fonctionne pour une majorité des champs selon des **listes déroulantes** à choix: le but de ces listes est de contraindre à l'utilisation commune de mêmes textes. Ainsi, vous ne pourrez pas indiquer ce que vous souhaitez dans ces champs: seuls certains des champs comme la légende ou les notes le permettent. 

#### ![question](img/question.png){:height="25px"}Je ne trouve pas la rue, la ville, le site, ou toute autre information, dans les menus déroulants, comment puis-je faire?

Il arrivera certainement que vous ne trouviez pas le nom d'une rue, d'un site, d'une ville, d'une personne, ou un mot-clé dans les choix proposés. Ne vous en inquiétez pas! Ces listes ne sont pas figées et sont destinées à évoluer selon les besoins que l'on rencontre au cours de l'inventaire. 

Afin que je puisse rajouter le terme dans la liste concernée, vous pouvez me le faire savoir en m'envoyant un mail. 

Sinon, une autre solution est de remplir le formulaire [http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/cataloguer/contact?nom_user=VOTRE_NOM](http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/cataloguer/contact) dont le lien est disponible en haut de la page de catalogage. N'oubliez pas d'indiquer le numéro d'inventaire de la photographie qui a besoin de ce nouveau terme, je le rajouterai en même temps dans les informations que vous avez déjà remplies pour ne pas vous faire perdre votre temps!
![contact_catalogage](img/contact_cataloguer.png){:width="750px"}

#### ![question](img/question.png){:height="25px"}Les mots-clés sont vraiment importants, j'aimerais connaître comment les utiliser, existe-t-il une documentation spécifique?

Vous avez raison, les mots-clés et les descripteurs sont le coeur de l'inventaire. Leur liste exhaustive, et la description de leur utilisation, est disponible sur ce lien: [POST A VENIR]().

Si vous ne trouvez pas le mot-clé nécessaire, voir le sujet [Je ne trouve pas la rue, la ville, le site, ou toute autre information, dans les menus déroulants, comment puis-je faire?](#je-ne-trouve-pas-la-rue-la-ville-le-site-ou-toute-autre-information-dans-les-menus-déroulants-comment-puis-je-faire).

#### ![question](img/question.png){:height="25px"}J'ai enregistré les informations, mais je souhaite les modifier, comment faire?

Pour accéder à la modification d'une photographie, il faut se rendre sur la page qui recense tous vos enregistrements récents dans l'onglet "Mon espace" > "Enregistrements récents". Vous arriverez alors sur la page [http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/enregistrements_recents?nom_user=VOTRE_NOM](http://parishistoriqueinventaire.eu.pythonanywhere.com/espace_personnel/enregistrements_recents).
![enregistrements_recents](img/enregistrements_recents.png){:width="750px"}

Cette page des enregistrements récents vous donne un aperçu des photographies inventoriées, et vous permet de les modifier.
![enr_recents](img/enr_recents.png){:width="750px"}

En cliquant sur le bouton "Mettre à jour", vous pourrez alors modifier les informations que vous aviez remplies auparavant.
![bouton_maj](img/bouton_maj.png){:width="750px"}

#### ![question](img/question.png){:height="25px"}J'ai terminé mon lot de photographies, que faire désormais?

### Les données de l'inventaire
#### ![question](img/question.png){:height="25px"}Quelles visualisations sont disponibles?
#### ![question](img/question.png){:height="25px"}Comment rechercher dans le catalogue?
#### ![question](img/question.png){:height="25px"}Comment utiliser à l'API?

### ![question](img/question.png){:height="25px"}Le site renvoie une erreur, est-ce normal?
404 oui, la page demandée n'existe pas, les 500 reste non

## Informations globales
### ![question](img/question.png){:height="25px"}Qui contacter?

* Pour obtenir plus d'informations sur l'**association du Paris Historique**, 
contacter directement l'association:
    * Site internet: [https://www.paris-historique.org/](https://www.paris-historique.org/)
    * Adresse: 44-46 Rue François Miron, 75004 Paris
    * Téléphone: 01 48 87 74 31
    
* Pour consulter les photographies à la **photothèque**, contacter la phothotèque ou l'association:
    * Page web: [https://www.paris-historique.org/phototheque/](https://www.paris-historique.org/phototheque/)
    * Ouverture du lundi au vendredi de 14h à 18h
    * Téléphone: 01 84 17 26 35
    
* Pour obtenir plus d'informations sur l'**inventaire** de la photothèque, contacter l'association ou le responsable:
    * Association: 
        * Mail: [contact@paris-historique.org](contact@paris-historique.org)
    * Responsable: 
        * Mail: [maxime.challon@gmail.com](maxime.challon@gmail.com)
        
* Pour **participer** à l'inventaire de la photothèque, contacter l'association:
    * Mail: [contact@paris-historique.org](contact@paris-historique.org)
    

### ![question](img/question.png){:height="25px"}Puis-je réutiliser les données ou le code source?

Sauf mention explicite contraire, toutes les données disponibles sur [parishistoriqueinventaire.eu.pythonanywhere.com/](parishistoriqueinventaire.eu.pythonanywhere.com/)
sont réutilisables  et sous license GNU/GPL 3.0 ou ultérieure, de même que le code source du site d'inventaire
disponible sur Github [https://github.com/MaximeChallon/InventaireParisHistorique](https://github.com/MaximeChallon/InventaireParisHistorique/tree/master).

L'[API](http://parishistoriqueinventaire.eu.pythonanywhere.com/api) permet la récupération des données de l'inventaire formatées en JSON.
