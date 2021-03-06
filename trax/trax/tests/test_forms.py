import unittest
from test_plus.test import TestCase

from trax.trax import models, forms, handlers
from trax.users.models import User
from django.conf import settings

from dynamic_preferences.registries import global_preferences_registry


class TestForms(TestCase):

    def setUp(self):
        self.preferences = global_preferences_registry.manager()
        self.preferences['trax__slash_command_token'] = 'good_token'

    def test_slash_command_form_requires_valid_token(self):
        data = {
            'channel_id': 'cniah6qa73bjjjan6mzn11f4ie',
            'channel_name': 'town-square',
            'command': '/trax',
            'text': 'start test',
            'team_domain': 'testteam',
            'team_id': 'rdc9bgriktyx9p4kowh3dmgqyc',
            'token': 'wrong_token',
            'user_id': 'testuser',
            'user_name': 'testid',
        }

        form = forms.SlashCommandForm(data)
        form.is_valid()

        self.assertIn('token', form.errors)

    def test_can_validate_form(self):
        payload = {
            'channel_id': 'cniah6qa73bjjjan6mzn11f4ie',
            'channel_name': 'town-square',
            'command': '/trax',
            'text': 'start test timer',
            'team_domain': 'testteam',
            'team_id': 'rdc9bgriktyx9p4kowh3dmgqyc',
            'token': 'good_token',
            'user_id': 'testid',
            'user_name': 'testuser',
        }

        form = forms.SlashCommandForm(payload)
        is_valid = form.is_valid()

        data = form.cleaned_data

        self.assertTrue(is_valid)

        user = User.objects.get(
            is_active=False,
            username=data['user_name'],
            external_id=data['user_id'])

        self.assertEqual(data['user'], user)
        self.assertEqual(data['action'], 'start')
        self.assertEqual(data['arguments'], 'test timer')
        self.assertEqual(data['handler'], handlers.handlers_by_key['start'])
