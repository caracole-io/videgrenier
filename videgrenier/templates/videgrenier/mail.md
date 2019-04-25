Votre demande d'inscription au vide grenier est maintenant active.

Elle pourra être acceptée dès lors que vous aurez rempli les conditions  suivantes:

1. Envoi du paiement du solde de votre demande : 14 € (12€ pour les adhérents) par chèque à l'ordre de l'association Caracole
2. Envoi d'une photocopie recto-verso de votre pièce d'identité
3. Envoi de l'impression du mail récapitulatif daté et signé
4. Envoi de l'impression de la [charte](https://caracole.io/static/documents/CharteVideGrenier-2015.pdf) signée

Merci de renvoyer cet email imprimé et signé à l'adresse suivante:

> Inscription vide grenier
> Association Caracole, Maison de l'économie Solidaire
> 73 Chemin de Mange-Pommes - 31520 Ramonville-Saint-Agne - France

Permanences de 14h00 à 18h00 pour dépôt de dossier et choix des emplacements:

{% for date in DATES_VIDE_GRENIER.inscriptions %}* {{ date }}
{% endfor %}

## recapitulatif de votre demande de stand(s) pour le vide grenier du {{ DATES_VIDE_GRENIER.event }} de Caracole

Nom : {{ reservation.user.last_name }}
Prénom : {{ reservation.user.first_name }}
Adresse : {{ reservation.address }}
Tél : {{ reservation.phone_number }}
Nombre d'emplacements demandé : {{ reservation.emplacements }}
Nature des objets exposés : {{ reservation.nature }}

## Informations administratives

N° de pièce d'identité : {{ reservation.id_num }}
Date de délivrance de cette pièce : {{ reservation.id_date }}
Autorité de délivrance de cette pièce : {{ reservation.id_org }}

Je soussigné {{ reservation.user.first_name }} {{ reservation.user.last_name }}
prends l'entière responsabilité des objets que je mettrai en vente lors de cette manifestation et m'engage à remporter tous mes invendus en fin de journée.

En signant ce document : j'atteste sur l'honneur l'exactitude des informations figurants sur celui-ci, de la même manière j'atteste sur l'honneur de ma non-participation à deux autres manifestations de même nature au cours de cette année.


Fait à ......................


Le ..........................

Signature :
