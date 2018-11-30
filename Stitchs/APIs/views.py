from django.shortcuts import render
from trello.models import (StitchCard, StitchList, StitchBoard,
                     Members, Label)
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, DestroyAPIView,
                                     CreateAPIView, RetrieveUpdateAPIView,)
from .serializers import (BoardSerializer, CardSerializer,
                          ListSerializer, MemberSerializer,
                          LabelSerializer)
# Create your views here.


class BoardListAPIView(ListAPIView, CreateAPIView):
    """
    Listing and creating Board usin REST
    """
    serializer_class = BoardSerializer

    def get_queryset(self, *args, **kwargs):
        """
        :return: query list for the user logged in
        """
        user_id = self.kwargs['pk']
        queryset = StitchBoard.objects.all()
        queryset_list = queryset.filter(user=user_id)
        return queryset_list


class ListListAPIView(ListAPIView, CreateAPIView):
    """
    Listing all Lists using REST
    """
    serializer_class = ListSerializer

    def get_queryset(self, *args, **kwargs):
        """
        :return: all Lists for one specific board
        """
        queryset = StitchList.objects.all()
        queryset_list = queryset.filter(board=self.kwargs['pk'])
        return queryset_list


class CardListAPIView(ListAPIView, CreateAPIView):
    """
    Listing all Cards using REST
     """
    serializer_class = CardSerializer

    def get_queryset(self, *args, **kwargs):
        """
        :return: all Cards for one specific List
        """
        queryset = StitchCard.objects.all()
        queryset_list = queryset.filter(list=self.kwargs['pk'])
        return queryset_list


class MembersListAPIView(ListAPIView, CreateAPIView):
    """
    Listing all Members using REST
     """
    queryset = Members.objects.all()
    serializer_class = MemberSerializer


class BoardUpdateAPIView(RetrieveUpdateAPIView):
    """
    :return: Specific Board to update using REST
     """
    queryset = StitchBoard.objects.all()
    serializer_class = BoardSerializer


class ListUpdateAPIView(RetrieveUpdateAPIView):
    """
    :return: Specific List to update using REST
     """
    queryset = StitchList.objects.all()
    serializer_class = ListSerializer


class CardUpdateAPIView(RetrieveUpdateAPIView):
    """
    :return: Specific Card to update using REST
     """
    queryset = StitchCard.objects.all()
    serializer_class = CardSerializer


class MemberUpdateAPIView(RetrieveUpdateAPIView):
    """
    :return: Specific Member to update using REST
     """
    queryset = Members.objects.all()
    serializer_class = MemberSerializer


class LabelUpdateAPIView(RetrieveUpdateAPIView):
    """
    :return: Specific Label to update using REST
     """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class LabelListAPIView(ListAPIView, CreateAPIView):
    """
        :return: List all Labels using REST
     """
    serializer_class = LabelSerializer

    def get_queryset(self, *args, **kwargs):
        """
            :return: all Labels for specific Board
        """
        queryset = Label.objects.all()
        queryset_list = queryset.filter(board=self.kwargs['pk'])
        return queryset_list
