from flask_mail import Message
from ..constantes import MAIL_USERNAME
from flask import url_for
from ..app import mail, app
from datetime import datetime

class Classe_mails():
    @staticmethod
    def send_reset_email(user):
        """
        Envoi d'un mail de renouvellement du mot de passe
        :param user: objet de l'utilisateur
        :return: None après envoi du mail
        """
        token = user.get_reset_token()
        msg = Message("Changement de mot de passe",
                      sender=MAIL_USERNAME,
                      recipients=[user.mail])
        msg.body = f'''Pour modifier votre mot de passe, cliquez sur le lien suivant:
    	{url_for('reset_token', token=token, _external=True)}

    Si vous n'êtes pas à l'origine de cette demande, veuillez ne pas tenir compte de cet email.

    Email généré automatiquement, merci de ne pas y répondre.
    '''
        mail.send(msg)

    @staticmethod
    def send_cataloguer_contact_mail(user, numero_inventaire, objet, message, copie):
        """
        Envoi un mail à l'administrateur en cas de problème sur la page de catalogage
        :param user: objet utilisateur
        :param numero_inventaire: numéro d'inventaire de la photo concernée
        :param objet: objet du mail
        :param message: corps du mail
        :param copie: booléen pour le saouhait ou non de recevoir une copie du mail envoyé à l'adminstrateur
        :return: None après envoi du mail
        """
        recipients = [MAIL_USERNAME]
        if copie == True:
            recipients.append(user.mail)
        msg = Message(str(numero_inventaire) + " -- " + objet,
                      sender=MAIL_USERNAME,
                      recipients=recipients)
        msg.body = message
        mail.send(msg)

    @staticmethod
    def daily_db_backup():
        """
        Envoi automatique d'une copie de la base users à l'adresse de la photothèque
        :return: None
        """
        recipients = [MAIL_USERNAME]
        msg = Message("Backup du " + str(datetime.utcnow()),
                      sender=MAIL_USERNAME,
                      recipients=recipients)
        msg.body = ""
        with app.open_resource("users.sqlite") as fp:
            msg.attach("users.sqlite", "application/x-sqlite", fp.read())
        mail.send(msg)