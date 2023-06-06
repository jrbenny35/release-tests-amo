import time

import pytest
from pypom import Region, Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ManageVersions(Page):
    _addon_name_title_locator = (By.CSS_SELECTOR, 'div[class="section"] header h2')
    _listing_visibility_section_locator = (By.CSS_SELECTOR, '#edit-addon h3:nth-child(1)')
    _visible_listing_radio_locator = (By.CSS_SELECTOR, 'input[value="listed"]')
    _visible_explainer_text_locator = (By.CSS_SELECTOR, '#addon-current-state label:nth-child(1)')
    _invisible_listing_radio_locator = (By.CSS_SELECTOR, 'input[value="hidden"]')
    _invisible_explainer_text_locator = (By.CSS_SELECTOR, '#addon-current-state label:nth-of-type(2)')
    _hide_addon_confirmation_text_locator = (By.CSS_SELECTOR, '#modal-disable p:nth-child(1)')
    _hide_addon_button_locator = (By.CSS_SELECTOR, '#modal-disable p button')
    _hide_addon_cancel_link_locator = (By.CSS_SELECTOR, '#modal-disable p a')
    _version_list_locator = (By.ID, 'version-list')
    _version_approval_status_locator = (
        By.CSS_SELECTOR,
        '#version-list .file-status div:nth-child(1)',
    )
    _incomplete_status_locator = (By.CSS_SELECTOR, '.status-incomplete b')
    _addon_listed_status_locator = (By.CSS_SELECTOR, '.addon-listed-status b')
    _delete_addon_button_locator = (By.CLASS_NAME, 'delete-button.delete-addon')

    def wait_for_page_to_load(self):
        self.wait.until(EC.visibility_of_element_located(self._version_list_locator))
        return self

    @property
    def version_page_title(self):
        return self.find_element(*self._addon_name_title_locator).text

    @property
    def listing_visibility_section(self):
        return self.find_element(*self._listing_visibility_section_locator).text

    def set_addon_visible(self):
        """Selects the Visible option and checks that the radio button is selected"""
        el = self.find_element(*self._visible_listing_radio_locator)
        el.clcik()
        assert el.is_selected()

    @property
    def visible_status_explainer(self):
        return self.find_element(*self._visible_explainer_text_locator).text

    @property
    def invisible_status_explainer(self):
        return self.find_element(*self._invisible_explainer_text_locator).text

    def set_addon_invisible(self):
        """Selects the Invisible option and checks that the radio button is selected"""
        el = self.find_element(*self._invisible_listing_radio_locator)
        el.clcik()
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#modal-disable p:nth-child(1)')))

    def click_hide_addon(self):
        self.find_element(*self._hide_addon_button_locator).click()

    @property
    def hide_addon_confirmation_text(self):
        return self.find_element(*self._hide_addon_confirmation_text_locator).text

    def cancel_hide_addon_process(self):
        """Cancel the hide addon process and check that the Visible radio button is still selected"""
        self.find_element(*self._hide_addon_cancel_link_locator).click()
        assert self.find_element(*self._visible_listing_radio_locator).is_selected()

    @property
    def addon_listed_status(self):
        return self.find_element(*self._addon_listed_status_locator).text

    @property
    def incomplete_status(self):
        return self.find_element(*self._incomplete_status_locator)

    @property
    def version_approval_status(self):
        return self.find_elements(*self._version_approval_status_locator)

    def wait_for_version_autoapproval(self, value):
        """Method that verifies if auto-approval occurs within a set time"""
        timeout_start = time.time()
        # auto-approvals should normally take ~5 minutes;
        # set a loop to verify if approval occurs within this interval
        while time.time() < timeout_start + 420:
            # refresh the page to check if the status has changed
            self.driver.refresh()
            if value not in self.version_approval_status[0].text:
                # wait 30 seconds before we refresh again
                time.sleep(30)
            # break the loop if the status changed to the expected value within set time
            else:
                break
        # if auto-approval took longer than normal, we want to fail the test and capture the final status
        else:
            pytest.fail(
                f'Autoapproval took longer than normal; '
                f'Addon final status was "{self.version_approval_status[0].text}" instead of "{value}"'
            )

    def delete_addon(self):
        self.find_element(*self._delete_addon_button_locator).click()
        return self.DeleteAddonModal(self).wait_for_region_to_load()

    class DeleteAddonModal(Region):
        _root_locator = (By.ID, 'modal-delete')
        _delete_confirmation_string_locator = (
            By.CSS_SELECTOR,
            'p:nth-of-type(2) > label',
        )
        _delete_confirmation_text_input_locator = (
            By.CSS_SELECTOR,
            'input[name="slug"]',
        )
        _delete_button_locator = (By.CSS_SELECTOR, '.delete-button')

        def wait_for_region_to_load(self):
            self.wait.until(EC.visibility_of_element_located(self._root_locator))
            return self

        @property
        def delete_confirmation_string(self):
            """This is the addon slug which is required to confirm deleting an addon"""
            return self.find_element(
                *self._delete_confirmation_string_locator
            ).text.split()[-1]

        def input_delete_confirmation_string(self):
            self.find_element(*self._delete_confirmation_text_input_locator).send_keys(
                self.delete_confirmation_string
            )

        def confirm_delete_addon(self):
            self.find_element(*self._delete_button_locator).click()
            from pages.desktop.developers.addons_manage import ManageAddons

            return ManageAddons(self.driver, self.page.base_url).wait_for_page_to_load()
