from time import sleep

from selenium.webdriver.common.by import By

from project.test_base.test_admin import TestAdminSeleniumBase, TestAdminBase
from project.test_base.test_models import TestPostsModelBase
from blog import models as blog_models


class PostAdminTestCase(TestAdminBase):

    def setUp(self):

        # Submit endpoint
        super().setUp()
        self.endpoint = "/admin/blog/post/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class ImageAdminTestCase(TestAdminBase):

    def setUp(self):

        # Submit endpoint
        super().setUp()
        self.endpoint = "/admin/blog/image/"

    def test_search_bar(self):
        """Validate search bar working"""

        self.submit_search_bar(self.endpoint)


class ImageAdminTestCaseSelenium(TestAdminSeleniumBase, TestPostsModelBase):

    def setUp(self):

        # Create image instance
        self.image = self.create_image()

        # Login
        super().setUp()

        self.endpoint = "/admin/blog/image"

        self.selectors = {
            "actions_btn": "tr td:last-child div span",
            "copy_btn": "a[href*='/copy_link']",
            "image": f"img[src*='{self.image.image.url}']",
        }

    def test_image_list_view(self):
        """Check if image list view is loaded"""

        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)

        # Check if image is displayed in list view
        elems = self.get_selenium_elems(self.selectors)
        image_elem = elems["image"]
        self.assertTrue(image_elem, "Image not found in list view")

    def test_image_detail_view(self):
        """Check if image detail view is loaded"""

        # Submit endpoint
        self.set_page(f"{self.endpoint}/{self.image.id}/change/")
        sleep(2)

        # Check if image is displayed in detail view
        elems = self.get_selenium_elems(self.selectors)
        image_elem = elems["image"]
        self.assertTrue(image_elem, "Image not found in detail view")

    def test_copy_buttons_loaded(self):
        """validate copy buttons (2 of them) visible in page"""

        # Delete old posts
        blog_models.Post.objects.all().delete()

        self.create_image(None, "test2.webp")

        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)

        # Get buttons
        actions_btn = self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["actions_btn"]
        )
        actions_btn.click()
        sleep(2)
        buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors["copy_btn"])
        self.assertEqual(len(buttons), 2, "Copy button missing")

    def test_copy_buttons_action(self):
        """Clock in copy button and validate if copied to clipboard"""

        # Submit endpoint
        self.set_page(self.endpoint)
        sleep(2)

        # Click button
        actions_btn = self.driver.find_element(
            By.CSS_SELECTOR, self.selectors["actions_btn"]
        )
        actions_btn.click()
        sleep(2)
        buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors["copy_btn"])
        buttons[0].click()
        sleep(2)

        # Focus current page
        self.driver.switch_to.window(self.driver.current_window_handle)
        sleep(2)

        # Check if image is copied to clipboard
        copied_image = self.driver.execute_script(
            "return navigator.clipboard.readText();"
        )
        self.assertIn(
            self.image.image.url, copied_image, "Image not copied to clipboard"
        )
