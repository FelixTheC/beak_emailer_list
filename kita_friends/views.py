from kita_friends.forms import KitaFriendsForm
from kita_friends.models import KitaFriends
from kita_representative.views import AssignToEmailer


class AssignFriendToEmailer(AssignToEmailer):
    template_name = 'friends_form.html'
    model = KitaFriends
    form_class = KitaFriendsForm
