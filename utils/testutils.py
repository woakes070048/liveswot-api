import json

from django.urls import reverse


def setuptoken(self, auth_data, client):

    gettoken_response = client.post(
        reverse('authenticationjwt:login'),
        content_type="application/json",
        data=json.dumps(auth_data))

    client.credentials(
        HTTP_AUTHORIZATION='Bearer ' + gettoken_response.data['token']
    )

    self.token = gettoken_response.data['token']