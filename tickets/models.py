from uuid import uuid4

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db import models


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="tickets"
    )

    movie_session = models.ForeignKey(
        "movie_sessions.MovieSession", on_delete=models.CASCADE, related_name="tickets"
    )

    def send_by_email(self):
        user = self.user
        movie_session = self.movie_session
        cinema = movie_session.cinema
        movie = movie_session.movie
        room = movie_session.room
        seats = [session_seat.seat.name for session_seat in self.session_seats.all()]

        send_mail(
            subject=f"Ingresso para assistir {movie.title} no cinema {cinema.name}",
            message="",
            html_message=f"<h2>Olá, {self.user.first_name}! Muito obrigado por usar o Primeira Fila.</h2>"
            "<p>Seguem as informações pertinentes ao seu ingresso:</p>"
            "<ul>"
            f"<li>Cinema: {cinema.name}</li>"
            f"<li>Endereço: Rua {cinema.address.street}, {cinema.address.number}</li>"
            f"<li>Bairro: {cinema.address.district.name}</li>"
            f"<li>Cidade: {cinema.address.city.name}</li>"
            "<hr>"
            f"<li>Filme: {movie.title}</li>"
            f"<li>3D: {'✅' if movie_session.is_3d else '❌'}</li>"
            f"<li>Sala: {room.name}</li>"
            f"<li>Assentos: {', '.join(seats)}</li>"
            f"<li>Preço por assento: {movie_session.price}</li>"
            f"<li>Total: {movie_session.price * self.session_seats.count()}</li>"
            f"<li>Data: {movie_session.session_datetime.date()}</li>"
            f"<li>Hora: {movie_session.session_datetime.time()}</li>"
            "<hr>"
            f"<li>Nome do comprador: {user.first_name} {user.last_name}</li>"
            f"<li>Email do comprador: {user.email}</li>"
            f"<li>Idade do comprador: {user.age}</li>"
            "</ul>"
            "<p>Atenciosamente, equipe Primeira Fila :)</p>",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
