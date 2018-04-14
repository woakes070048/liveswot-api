import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from swot_item.models import SwotItem

from swot_item_vote.models import Vote

from utils import testutils

client = APIClient()


class ShapeVoteTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_successful_get_should_respond_with_correct_response_shape(self):
        response = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': 1}),
            content_type='application/json',
        )

        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), list)

    def test_successful_get_should_respond_with_correct_information(self):
        response = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': 1}),
            content_type='application/json',
        )

        response_data = response.data['data']

        self.assertTrue(len(response_data) > 0)
        self.assertTrue(all(['voteId' in vote for vote in response_data]))
        self.assertTrue(all(['swotItemId' in vote for vote in response_data]))
        self.assertTrue(all(['creatorId' in vote for vote in response_data]))
        self.assertTrue(all(['voteType' in vote for vote in response_data]))
        self.assertTrue(all(['creatorUsername' in vote for vote in response_data]))


class GetVoteTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def test_get_all_votes_should_return_empty_list_when_no_vote(self):
        response = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': 5}),
            content_type='application/json',
        )

        response_data = response.data

        self.assertEqual(0, len(response_data['data']))

    def test_get_all_votes_should_return_list_with_the_vote_when_one_vote(self):
        response = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': 6}),
        )

        self.assertEqual(1, len(response.json()['data']))


class PostVoteTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_successful_post_should_respond_with_correct_response_shape(self):
        # swot item with no vote
        swot_item_id = 9
        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': swot_item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(type(response.data['data']), dict)

        Vote.objects.get(swot_item_id=swot_item_id).delete()

    def test_create_new_vote(self):
        # item with no vote
        item_id = 9

        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        res_data = response.data['data']
        self.assertEqual(res_data['swotItemId'], item_id)
        self.assertEqual(res_data['creatorId'], self.auth_data['user']['userId'])
        self.assertEqual(res_data['voteType'], 'up')

        [vote.delete() for vote in Vote.objects.filter(swot_item_id=item_id)]

    def test_create_new_vote_success_should_successfully_save(self):
        # single swot item
        swot_item_id = 11
        # swot with only one item
        swot_id = 7

        original = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': swot_id}),
            content_type='application/json'
        ).data['data']

        client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': swot_item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        actual = client.get(
            reverse('swot_item_vote:get', kwargs={'swot_id': swot_id}),
            content_type='application/json'
        ).data['data']

        self.assertEqual(len(actual), len(original) + 1)
        Vote.objects.get(swot_id=7).delete()


class ErrorVotesTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }
    vote_up = {
        'voteType': 'up',
    }

    def setUp(self):
        testutils.setuptoken(self, self.auth_data, client)

    def test_vote_non_existing_item_should_repond_404(self):
        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': 99}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MultipleVotesTestCase(TestCase):
    fixtures = ['users.json', 'swots.json', 'swotItems.json', 'votes.json']
    auth_data = {
        'user': {
            'userId': 5,
            'email': 'imran.ariffin@liveswot.com',
            'password': 'katakunci'
        }
    }

    def setUp(self):
        self.vote_up = {
            'voteType': 'up',
        }
        self.vote_down = {'voteType': 'down', }

        testutils.setuptoken(self, self.auth_data, client)

    def test_vote_up_twice_should_neutralize(self):
        swot_id = 1
        item = SwotItem.objects.create(
            created_by_id=self.auth_data['user']['userId'],
            text='One vote up',
            swot_id=swot_id,

        )

        item_id = item.id

        # first post
        client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        # second post
        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': {}})

        item.delete()

    def test_vote_up_then_vote_down_should_delete_up_and_create_down(self):
        item_id = 1

        client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        res_data = response.data['data']

        self.assertEqual(res_data['voteType'], 'down')
        self.assertEqual(res_data['swotItemId'], item_id)
        self.assertEqual(res_data['creatorId'], self.auth_data['user']['userId'])

    def test_vote_down_then_vote_up_should_delete_down_and_create_up(self):
        item_id = 1

        client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_down),
            content_type='application/json',
        )

        response = client.post(
            reverse('swot_item_vote:post', kwargs={'swot_item_id': item_id}),
            data=json.dumps(self.vote_up),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        res_data = response.data['data']

        self.assertEqual(res_data['voteType'], 'up')
        self.assertEqual(res_data['swotItemId'], item_id)
        self.assertEqual(res_data['creatorId'], self.auth_data['user']['userId'])

