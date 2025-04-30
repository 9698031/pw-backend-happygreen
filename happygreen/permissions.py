from rest_framework import permissions
from .models import GroupMembership, Post, Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato per consentire ai proprietari di un oggetto di modificarlo.
    """

    def has_object_permission(self, request, view, obj):
        # Le autorizzazioni di lettura sono consentite per qualsiasi richiesta,
        # quindi consentiamo sempre GET, HEAD o OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Le autorizzazioni di scrittura sono consentite solo al proprietario.
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        if hasattr(obj, 'creator'):
            return obj.creator == request.user

        return False


class IsGroupMember(permissions.BasePermission):
    """
    Permesso personalizzato per consentire l'accesso solo ai membri di un gruppo.
    """

    def has_permission(self, request, view):
        # Per POST su /posts/ controlliamo che l'utente sia membro del gruppo specificato
        if request.method == 'POST' and 'group' in request.data:
            group_id = request.data.get('group')
            try:
                return GroupMembership.objects.filter(
                    user=request.user,
                    group_id=group_id
                ).exists()
            except (TypeError, ValueError):
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # Permesso per oggetti specifici (come post che appartengono a un gruppo)
        if isinstance(obj, Post):
            return GroupMembership.objects.filter(
                user=request.user,
                group=obj.group
            ).exists()

        return True


class IsGroupAdmin(permissions.BasePermission):
    """
    Permesso personalizzato per consentire solo agli amministratori del gruppo di modificare.
    """

    def has_object_permission(self, request, view, obj):
        # Le autorizzazioni di lettura sono consentite per qualsiasi richiesta
        if request.method in permissions.SAFE_METHODS:
            return True

        # Se stiamo modificando un gruppo, controlla se l'utente è admin
        if isinstance(obj, Group):
            try:
                membership = GroupMembership.objects.get(
                    user=request.user,
                    group=obj
                )
                return membership.role == 'ADMIN'
            except GroupMembership.DoesNotExist:
                return False

        return False