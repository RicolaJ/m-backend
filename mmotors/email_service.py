from django.core.mail import send_mail
from django.conf import settings


def send_dossier_valide(dossier):
    send_mail(
        subject='✅ Votre dossier a été validé — M-Motors',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[dossier.client.email],
        html_message=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1e3a8a; padding: 24px; text-align: center;">
                <h1 style="color: white; margin: 0;">M-Motors</h1>
            </div>
            <div style="padding: 32px; background: #f9fafb;">
                <h2 style="color: #1e3a8a;">Félicitations {dossier.client.first_name} !</h2>
                <p>Votre dossier <strong>{dossier.reference}</strong> pour le véhicule
                <strong>{dossier.vehicle.marque} {dossier.vehicle.modele}</strong>
                a été <span style="color: #16a34a; font-weight: bold;">validé</span>.</p>
                <p>Notre équipe va vous contacter prochainement.</p>
                <div style="text-align: center; margin: 32px 0;">
                    <a href="https://motorsss.netlify.app/espace-client/dossiers/{dossier.id}"
                       style="background: #1e3a8a; color: white; padding: 12px 24px;
                              border-radius: 8px; text-decoration: none; font-weight: bold;">
                        Voir mon dossier
                    </a>
                </div>
                <p style="color: #6b7280; font-size: 14px;">L'équipe M-Motors</p>
            </div>
        </div>
        """,
        fail_silently=True,
    )


def send_dossier_refuse(dossier):
    send_mail(
        subject='❌ Décision sur votre dossier — M-Motors',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[dossier.client.email],
        html_message=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1e3a8a; padding: 24px; text-align: center;">
                <h1 style="color: white; margin: 0;">M-Motors</h1>
            </div>
            <div style="padding: 32px; background: #f9fafb;">
                <h2 style="color: #1e3a8a;">Bonjour {dossier.client.first_name},</h2>
                <p>Votre dossier <strong>{dossier.reference}</strong> n'a pas pu être accepté.</p>
                {f'<p><strong>Motif :</strong> {dossier.motif_refus}</p>' if dossier.motif_refus else ''}
                <div style="text-align: center; margin: 32px 0;">
                    <a href="https://motorsss.netlify.app/vehicules"
                       style="background: #1e3a8a; color: white; padding: 12px 24px;
                              border-radius: 8px; text-decoration: none; font-weight: bold;">
                        Voir nos véhicules
                    </a>
                </div>
                <p style="color: #6b7280; font-size: 14px;">L'équipe M-Motors</p>
            </div>
        </div>
        """,
        fail_silently=True,
    )


def send_dossier_en_cours(dossier):
    send_mail(
        subject='📋 Votre dossier est en cours d\'instruction — M-Motors',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[dossier.client.email],
        html_message=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: #1e3a8a; padding: 24px; text-align: center;">
                <h1 style="color: white; margin: 0;">M-Motors</h1>
            </div>
            <div style="padding: 32px; background: #f9fafb;">
                <h2 style="color: #1e3a8a;">Bonjour {dossier.client.first_name},</h2>
                <p>Votre dossier <strong>{dossier.reference}</strong> est
                <span style="color: #2563eb; font-weight: bold;">en cours d'instruction</span>.</p>
                <p>Vous serez notifié dès qu'une décision sera prise.</p>
                <div style="text-align: center; margin: 32px 0;">
                    <a href="https://motorsss.netlify.app/espace-client/dossiers/{dossier.id}"
                       style="background: #1e3a8a; color: white; padding: 12px 24px;
                              border-radius: 8px; text-decoration: none; font-weight: bold;">
                        Suivre mon dossier
                    </a>
                </div>
                <p style="color: #6b7280; font-size: 14px;">L'équipe M-Motors</p>
            </div>
        </div>
        """,
        fail_silently=True,
    )
