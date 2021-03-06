from django.test import TestCase, Client


class BasicTest(TestCase):
    fixtures = ['basic.json']

    def test_servers_list(self):
        # Query the index
        response = self.client.get('/')

        # Get the servers passed to the templates
        servers = response.context['servers']

        # Check the values
        self.assertEqual(len(servers), 3)
        names = [s.display_name() for s in servers]
        self.assertEqual(names, [u"192.168.0.12", u"Madjar's bazaar", u"Remram's room"])

    def test_files_list(self):
        expected_files = [
            ('/server/192.168.0.12', [
                'mirror'
            ]),
            ('/server/192.168.0.12/mirror/empty', []),
            ('/server/192.168.0.12/mirror/debian-amd64', [
                'debian-testing-amd64-CD-1.iso',
                'debian-testing-amd64-CD-2.iso',
                'debian-testing-amd64-CD-3.iso',
                'debian-testing-amd64-CD-4.iso',
                'debian-testing-amd64-CD-5.iso',
            ]),
            ('/server/192.168.0.42', [
                'dir',
                'requirements.txt',
            ]),
        ]

        for uri, exp in expected_files:
            response = self.client.get(uri)
            files = response.context['files']
            names = [e.name for e in files]
            self.assertEqual(names, exp)

    def test_search(self):
        response = self.client.get('/search/?query=paris')
        self.assertEqual(len(response.context['files']), 1)

        response = self.client.get('/search/?query=testing')
        self.assertEqual(len(response.context['files']), 5)

    def test_search_empty(self):
        response = self.client.get('/search/', follow=False)
        self.assertRedirects(response, '/', status_code=302)

    def test_download_dir(self):
        response = self.client.get('/download/192.168.0.12/mirror', follow=False)
        self.assertEqual(response.status_code, 404)

    def test_download(self):
        response = self.client.get('/download/remram/todo.txt', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'ftp://remram/todo.txt')

        response = self.client.get('/download/192.168.0.42/dir/icon.png', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'ftp://192.168.0.42/dir/icon.png')
