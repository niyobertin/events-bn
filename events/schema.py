import graphene 
from graphene_django.types import DjangoObjectType
from .models import Event

class EventType(DjangoObjectType):
    class Meta:
        model = Event

class Query(graphene.ObjectType):
    all_events = graphene.List(EventType)
    events_by_id = graphene.Field(EventType, id=graphene.Int())

    def resolve_all_events(root, info):
        return Event.objects.all()

    def resolve_events_by_id(root, info, id):
        try:
            return Event.objects.get(pk=id)
        except Event.DoesNotExist:
            return None

class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        available_seats = graphene.Int(required=True)
        start_time = graphene.DateTime(required=True)
        end_time = graphene.DateTime(required=True)
        location = graphene.String(required=True) 

    event = graphene.Field(EventType)   

    def mutate(self, info, title, available_seats, description, start_time, end_time, location):
        event = Event.objects.create(
            title=title,
            description=description,
            available_seats=available_seats,
            start_time=start_time,
            end_time=end_time,
            location=location
        )
        return CreateEvent(event=event)

class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        available_seats = graphene.Int()
        start_time = graphene.DateTime()
        end_time = graphene.DateTime()
        location = graphene.String()

    event = graphene.Field(EventType)
    success = graphene.Boolean()

    def mutate(self, info, id, title=None, description=None, available_seats=None, start_time=None, end_time=None, location=None):
        try:
            event = Event.objects.get(pk=id)
            if title is not None:
                event.title = title
            if description is not None:
                event.description = description
            if available_seats is not None:
                event.available_seats = available_seats
            if start_time is not None:
                event.start_time = start_time
            if end_time is not None:
                event.end_time = end_time
            if location is not None:
                event.location = location
            event.save()
            return UpdateEvent(event=event, success=True)
        except Event.DoesNotExist:
            return UpdateEvent(event=None, success=False)

class DeleteEvent(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            event = Event.objects.get(pk=id)
            event.delete()
            return DeleteEvent(success=True)
        except Event.DoesNotExist:
            return DeleteEvent(success=False)

class Mutation(graphene.ObjectType):
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()
    delete_event = DeleteEvent.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
