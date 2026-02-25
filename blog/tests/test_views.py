from rest_framework import status
from project.test_base.test_views import TestPostsViewsBase


class PostViewSetTestCase(TestPostsViewsBase):

    def setUp(self):
        # Set endpoint
        super().setUp(endpoint="/api/posts/")

    # def test_get_summary(self):
    #     """Test authenticated user get request in eng and es
    #     to render properti main data
    #     """

    #     # Make request
    #     response = self.client.get(self.endpoint, {"summary": True})

    #     # Check response
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Validate response extra content
    #     json_data = response.json()
    #     self.assertEqual(json_data["count"], 2)
    #     self.assertIsNone(json_data["next"])
    #     self.assertIsNone(json_data["previous"])
    #     self.assertEqual(len(json_data["results"]), 2)

    #     # Loop results
    #     results = json_data["results"]
    #     posts = [self.post_1, self.post_2]
    #     for post in posts:

    #         # Filter post data
    #         result = list(filter(lambda result: result["id"] == post.id, results))[0]

    #         # Check summary post data
    #         self.assertEqual(result["title"], post.title)
    #         self.assertEqual(result["slug"], post.slug)
    #         self.assertEqual(result["lang"], post.lang)
    #         self.assertEqual(result["banner_image_url"], post.banner_image_url)
    #         self.assertEqual(result["description"], post.description)
    #         self.assertEqual(result["author"], post.author)

    # def test_get_details(self):
    #     """Test authenticated user get request in eng and es
    #     to render properti main data
    #     """

    #     # Make request
    #     response = self.client.get(self.endpoint, {"details": True})

    #     # Check response
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Validate response extra content
    #     json_data = response.json()
    #     self.assertEqual(json_data["count"], 2)
    #     self.assertIsNone(json_data["next"])
    #     self.assertIsNone(json_data["previous"])
    #     self.assertEqual(len(json_data["results"]), 2)

    #     # Loop results
    #     results = json_data["results"]
    #     posts = [self.post_1, self.post_2]
    #     for post in posts:

    #         # Filter post data
    #         result = list(filter(lambda result: result["id"] == post.id, results))[0]

    #         # Check summary post data
    #         self.assertEqual(result["title"], post.title)
    #         self.assertEqual(result["slug"], post.slug)
    #         self.assertEqual(result["lang"], post.lang)
    #         self.assertEqual(result["banner_image_url"], post.banner_image_url)
    #         self.assertEqual(result["description"], post.description)
    #         self.assertEqual(result["keywords"], post.keywords)
    #         self.assertEqual(result["author"], post.author)
    #         self.assertEqual(result["content"], post.content)

    # def test_get_details_single(self):
    #     """Test authenticated user get single post request"""

    #     # Make request
    #     response = self.client.get(
    #         f"{self.endpoint}{self.post_1.slug}/", {"details": True}
    #     )

    #     # Check response
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Validate response extra content
    #     json_data = response.json()

    #     # Check summary post data
    #     self.assertEqual(json_data["title"], self.post_1.title)
    #     self.assertEqual(json_data["slug"], self.post_1.slug)
    #     self.assertEqual(json_data["lang"], self.post_1.lang)
    #     self.assertEqual(json_data["banner_image_url"], self.post_1.banner_image_url)
    #     self.assertEqual(json_data["description"], self.post_1.description)
    #     self.assertEqual(json_data["keywords"], self.post_1.keywords)
    #     self.assertEqual(json_data["author"], self.post_1.author)
    #     self.assertEqual(json_data["content"], self.post_1.content)

    def test_get_details_related_post(self):
        """validate related post in post details"""

        # Create second post
        post_2 = self.create_post(
            title="Test Post 2 new",
            lang="es",
            description="Test Description 2",
            content="Test Content 2",
        )

        # Relate first post to second post
        self.post_1.related_post = post_2
        self.post_1.save()

        # Make request
        response = self.client.get(
            f"{self.endpoint}{self.post_1.slug}/",
            {"details": True},
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Check related post
        self.assertEqual(json_data["related_post"], post_2.slug)

    def test_get_details_no_related_post(self):
        """validate no related post in post details"""

        # Make request
        response = self.client.get(
            f"{self.endpoint}{self.post_1.slug}/",
            {"details": True},
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate response extra content
        json_data = response.json()

        # Check related post
        self.assertIsNone(json_data["related_post"])

    def test_get_langs(self):
        """Tess get posts in each language"""

        langs = ["en", "es"]

        for lang in langs:
            # Make request
            response = self.client.get(
                self.endpoint,
                HTTP_ACCEPT_LANGUAGE=lang,
            )

            # Check response
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Validate response extra content
            json_data = response.json()
            self.assertEqual(json_data["count"], 1)
            self.assertIsNone(json_data["next"])
            self.assertIsNone(json_data["previous"])
            self.assertEqual(len(json_data["results"]), 1)

            # Loop results
            results = json_data["results"]
            post = self.post_1 if lang == "es" else self.post_2

            # Filter post data
            result = list(filter(lambda result: result["id"] == post.id, results))[0]

            # Check summary post data
            self.assertEqual(result["title"], post.title)
            self.assertEqual(result["slug"], post.slug)
            self.assertEqual(result["lang"], post.lang)

    def test_page_size_1(self):
        """Test if the page size is set to 1"""

        self.endpoint += "?page-size=1"

        # Make request
        response = self.client.get(
            self.endpoint,
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["results"]), 1)
