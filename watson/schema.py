import graphene
from graphene import ClientIDMutation
from graphene import Field
from graphene import Node
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from watson.models import Answer
from watson.models import Location
from watson.models import Question
from watson.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        filter_fields = {'name': ['exact']}


class LocationNode(DjangoObjectType):
    class Meta:
        model = Location
        interfaces = (Node,)
        filter_fields = {'name': ['exact', 'icontains', 'istartswith'],
                         'description': ['exact', 'icontains', 'istartswith']
                         }


class QuestionNode(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (Node,)
        filter_fields = {'_type': ['exact'],
                         'about_location__name': ['exact', 'icontains', 'istartswith'],
                         'posted_date': ['exact']
                         }


class LocationQuestionNode(DjangoObjectType):
    """ used for querying questions about a specific location using its name or id """

    class Meta:
        model = Question
        interfaces = (Node,)
        filter_fields = {
            'about_location__name': ['exact'],
            'about_location__gp_id': ['exact']
        }


class AnswerNode(DjangoObjectType):
    class Meta:
        model = Answer
        interfaces = (Node,)
        filter_fields = {
            'to_question__uid': ['exact']
        }


class NewLocation(ClientIDMutation):
    location = Field(LocationNode)

    class Input:
        name = graphene.String()
        description = graphene.String()
        longitude = graphene.Float()
        latitude = graphene.Float()

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        location = Location(
            name=args.get('name'),
            description=args.get('description'),
            longitude=args.get('longitude'),
            latitude=args.get('latitude')
        )
        location.save()
        return NewLocation(location=location)


class NewQuestion(ClientIDMutation):
    question = Field(QuestionNode)

    # location = Field(LocationNode)
    # user = Field(UserNode)

    class Input:
        type = graphene.String()
        user_auth = graphene.String()
        about_location_id = graphene.String()
        body = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        question = Question(_type=args.get('type'),
                            by_user=User.objects.get(auth_token=args.get('user_auth')),
                            about_location=Location.objects.get(pk=args.get('about_location_id')),
                            body=args.get('body'))
        question.save()
        return NewQuestion(question=question)


class NewAnswer(ClientIDMutation):
    answer = Field(AnswerNode)

    # location = Field(LocationNode)
    # user = Field(UserNode)

    class Input:
        body = graphene.String()
        about_question_id = graphene.String()
        user_auth = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        answer = Answer(answer=args.get('body'),
                        provided_by=User.objects.get(auth_token=args.get('user_auth')),
                        to_question=Question.objects.get(pk=args.get('about_question_id')))
        answer.save()
        return NewAnswer(answer=answer)


class Query(graphene.ObjectType):
    # get the questions about a given location (by name/id)
    questions_for_location = DjangoFilterConnectionField(LocationQuestionNode)

    # get a question by it's id
    question = relay.Node.Field(QuestionNode)

    # get an answer for a question, providing answer's id
    answer = relay.Node.Field(AnswerNode)

    # get all answers for a question, providing a question id
    all_answers = DjangoFilterConnectionField(AnswerNode)


class Mutation(object):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
