import os
from pathlib import Path
from pypom import Page

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.desktop.developers.manage_versions import ManageVersions


class SubmitAddon(Page):
    """A class holding all the components used for addon submissions in DevHub"""

    _my_addons_page_logo_locator = (By.CSS_SELECTOR, '.site-titles')
    _submission_form_header_locator = (By.CSS_SELECTOR, '.is_addon')
    _addon_distribution_header_locator = (
        By.CSS_SELECTOR,
        '.addon-submission-process h3',
    )
    _listed_option_locator = (By.CSS_SELECTOR, 'input[value="listed"]')
    _unlisted_option_locator = (By.CSS_SELECTOR, 'input[value="unlisted"]')
    _change_distribution_link_locator = (By.CSS_SELECTOR, '.addon-submit-distribute a')
    _continue_button_locator = (By.CSS_SELECTOR, '.addon-submission-field button')
    _upload_file_button_locator = (By.CSS_SELECTOR, '.invisible-upload input')
    _firefox_compat_checkbox_locator = (By.CSS_SELECTOR, '.app.firefox input')
    _android_compat_checkbox_locator = (By.CSS_SELECTOR, '.app.android input')
    _create_theme_button_locator = (By.ID, 'wizardlink')
    _submit_file_button_locator = (By.ID, 'submit-upload-file-finish')
    _addon_validation_success_locator = (By.CLASS_NAME, 'bar-success')
    _validation_fail_message_locator = (By.CLASS_NAME, 'status-fail')
    _validation_success_message_locator = (By.ID, 'upload-status-results')

    @property
    def my_addons_page_logo(self):
        return self.find_element(*self._my_addons_page_logo_locator)

    @property
    def submission_form_header(self):
        return self.find_element(*self._submission_form_header_locator)

    @property
    def distribution_header(self):
        return self.find_element(*self._addon_distribution_header_locator)

    def select_listed_option(self):
        self.find_element(*self._listed_option_locator).click()

    def select_unlisted_option(self):
        self.find_element(*self._unlisted_option_locator).click()

    def change_version_distribution(self):
        """Changes the distribution (listed/unlisted) when submitting a new version"""
        self.find_element(*self._change_distribution_link_locator).click()
        self.wait.until(EC.visibility_of_element_located(self._listed_option_locator))

    def click_continue(self):
        self.find_element(*self._continue_button_locator).click()

    def upload_addon(self, addon):
        """Selects an addon from the 'sample-addons' folder and uploads it"""
        button = self.find_element(*self._upload_file_button_locator)
        archive = Path(f'{os.getcwd()}/sample-addons/{addon}')
        button.send_keys(str(archive))

    @property
    def firefox_compat_checkbox(self):
        return self.find_element(*self._firefox_compat_checkbox_locator)

    @property
    def android_compat_checkbox(self):
        return self.find_element(*self._android_compat_checkbox_locator)

    def is_validation_successful(self):
        """Wait for addon validation to complete; if not successful, the test will fail"""
        self.wait.until(
            EC.visibility_of_element_located(self._addon_validation_success_locator)
        )

    @property
    def failed_validation_message(self):
        return self.find_element(*self._validation_fail_message_locator)

    @property
    def success_validation_message(self):
        return self.find_element(*self._validation_success_message_locator)

    def click_continue_upload_button(self):
        self.find_element(*self._submit_file_button_locator).click()
        return UploadSource(self.selenium, self.base_url)

    def submit_button_disabled(self):
        self.find_element(*self._submit_file_button_locator).get_attribute('disabled')


class UploadSource(Page):
    _submit_source_code_page_header_locator = (
        By.CSS_SELECTOR,
        '.addon-submission-process h3',
    )
    _yes_submit_source_radio_button_locator = (By.ID, 'id_has_source_0')
    _no_submit_source_radio_button_locator = (By.ID, 'id_has_source_1')
    _choose_source_file_button_locator = (By.ID, 'id_source')
    _continue_button_locator = (
        By.CSS_SELECTOR,
        '.submission-buttons button:nth-child(1)',
    )
    _upload_source_error_message_locator = (By.CSS_SELECTOR, '.errorlist li')

    @property
    def submit_source_page_header(self):
        return self.find_element(*self._submit_source_code_page_header_locator).text

    def select_yes_to_submit_source(self):
        self.find_element(*self._yes_submit_source_radio_button_locator).click()

    def select_no_to_omit_source(self):
        self.find_element(*self._no_submit_source_radio_button_locator).click()

    def choose_source(self, file):
        button = self.find_element(*self._choose_source_file_button_locator)
        archive = Path(f'{os.getcwd()}/sample-addons/{file}')
        button.send_keys(str(archive))

    def continue_unlisted_submission(self):
        self.find_element(*self._continue_button_locator).click()
        return SubmissionConfirmationPage(
            self.selenium, self.base_url
        ).wait_for_page_to_load()

    def continue_listed_submission(self):
        self.find_element(*self._continue_button_locator).click()
        return ListedAddonSubmissionForm(
            self.selenium, self.base_url
        ).wait_for_page_to_load()

    @property
    def source_upload_fail_message(self):
        return self.find_element(*self._upload_source_error_message_locator).text


class ListedAddonSubmissionForm(Page):
    _addon_name_field_locator = (By.CSS_SELECTOR, '#trans-name input:nth-child(1)')
    _edit_addon_slug_link_locator = (By.ID, 'edit_slug')
    _edit_addon_slug_field_locator = (By.ID, 'id_slug')
    _addon_summary_field_locator = (By.ID, 'id_summary_0')
    _addon_detail_fields_info_text_locator = (By.CSS_SELECTOR, '.edit-addon-details')
    _summary_character_count_locator = (
        By.CSS_SELECTOR,
        ".char-count[data-for-startswith='id_summary_'] > b",
    )
    _addon_description_field_locator = (By.ID, 'id_description_0')
    _is_experimental_checkbox_locator = (By.ID, 'id_is_experimental')
    _requires_payment_checkbox_locator = (By.ID, 'id_requires_payment')
    _categories_section_locator = (By.ID, 'addon-categories-edit')
    _firefox_categories_locator = (
        By.CSS_SELECTOR,
        '.addon-app-cats:nth-of-type(1) > ul input',
    )
    _android_categories_locator = (
        By.CSS_SELECTOR,
        '.addon-app-cats:nth-of-type(2) > ul input',
    )
    _email_input_field_locator = (By.ID, 'id_support_email_0')
    _support_site_input_field_locator = (By.ID, 'id_support_url_0')
    _license_options_locator = (By.CLASS_NAME, 'license')
    _license_details_link_locator = (By.CSS_SELECTOR, '.xx.extra')
    _custom_license_name_locator = (By.ID, 'id_license-name')
    _custom_license_text_locator = (By.ID, 'id_license-text')
    _privacy_policy_checkbox_locator = (By.ID, 'id_has_priv')
    _privacy_policy_textarea_locator = (By.ID, 'id_privacy_policy_0')
    _reviewer_notes_textarea_locator = (By.ID, 'id_approval_notes')
    _submit_addon_button_locator = (
        By.CSS_SELECTOR,
        '.submission-buttons button:nth-child(1)',
    )
    _cancel_addon_submission_button_locator = (
        By.CSS_SELECTOR,
        '.submission-buttons button:nth-child(2)',
    )

    def wait_for_page_to_load(self):
        self.wait.until(
            EC.visibility_of_element_located(self._addon_summary_field_locator)
        )
        return self

    def set_addon_name(self, value):
        self.find_element(*self._addon_name_field_locator).send_keys(value)

    @property
    def addon_name_field(self):
        return self.find_element(*self._addon_name_field_locator)

    def edit_addon_slug(self, value):
        self.find_element(*self._edit_addon_slug_link_locator).click()
        edit_field = WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_element_located(self._edit_addon_slug_field_locator)
        )
        edit_field.send_keys(value)

    def set_addon_summary(self, value):
        self.find_element(*self._addon_summary_field_locator).send_keys(value)

    def addon_detail_fields_info_text(self):
        self.find_elements(*self._addon_detail_fields_info_text_locator)

    @property
    def summary_character_count(self):
        return self.find_element(*self._summary_character_count_locator).text

    def set_addon_description(self, value):
        self.find_element(*self._addon_description_field_locator).send_keys(value)

    @property
    def is_experimental(self):
        return self.find_element(*self._is_experimental_checkbox_locator)

    @property
    def requires_payment(self):
        return self.find_element(*self._requires_payment_checkbox_locator)

    @property
    def categories_section(self):
        return self.find_element(*self._categories_section_locator)

    def select_firefox_categories(self, count):
        self.find_elements(*self._firefox_categories_locator)[count].click()

    def select_android_categories(self, count):
        self.find_elements(*self._android_categories_locator)[count].click()

    def email_input_field(self, value):
        self.find_element(*self._email_input_field_locator).send_keys(value)

    def support_site_input_field(self, value):
        self.find_element(*self._support_site_input_field_locator).send_keys(value)

    @property
    def select_license_options(self):
        return self.find_elements(*self._license_options_locator)

    def license_option_names(self, count, value):
        return self.select_license_options[count].get_attribute(value)

    def license_details_link(self):
        self.find_element(*self._license_details_link_locator).click()

    def set_custom_license_name(self, value):
        self.find_element(*self._custom_license_name_locator).send_keys(value)

    def set_custom_license_text(self, value):
        self.find_element(*self._custom_license_text_locator).send_keys(value)

    def set_privacy_policy(self, value):
        self.find_element(*self._privacy_policy_checkbox_locator).click()
        self.find_element(*self._privacy_policy_textarea_locator).send_keys(value)

    def set_reviewer_notes(self, value):
        self.find_element(*self._reviewer_notes_textarea_locator).send_keys(value)

    def submit_addon(self):
        self.find_element(*self._submit_addon_button_locator).click()
        return SubmissionConfirmationPage(
            self.selenium, self.base_url
        ).wait_for_page_to_load()

    def cancel_submission(self):
        self.find_element(*self._cancel_addon_submission_button_locator).click()
        from pages.desktop.developers.edit_addon import EditAddon

        return EditAddon(self.selenium, self.base_url).wait_for_page_to_load()


class SubmissionConfirmationPage(Page):
    _confirmation_page_header_locator = (
        By.CSS_SELECTOR,
        '.addon-submission-process h3',
    )
    _confirmation_messages_locator = (By.CSS_SELECTOR, '.addon-submission-process p')
    _manage_listing_button_locator = (By.LINK_TEXT, 'Go to My Submissions')
    _edit_version_button_locator = (
        By.CSS_SELECTOR,
        '.addon-submission-process p:nth-child(6) > a',
    )
    _edit_listing_button_locator = (By.LINK_TEXT, 'Manage Listing')
    _theme_preview_locator = (By.CSS_SELECTOR, '.addon-submission-process img')

    def wait_for_page_to_load(self):
        self.wait.until(
            EC.visibility_of_element_located(self._confirmation_page_header_locator)
        )
        return self

    @property
    def submission_confirmation_messages(self):
        return self.find_elements(*self._confirmation_messages_locator)

    def click_manage_listing_button(self):
        self.find_element(*self._manage_listing_button_locator).click()
        from pages.desktop.developers.addons_manage import ManageAddons

        return ManageAddons(self.selenium, self.base_url).wait_for_page_to_load()

    def click_edit_version_button(self):
        self.find_element(*self._edit_version_button_locator).click()
        return ManageVersions(self.selenium, self.base_url)

    def click_edit_listing_button(self):
        self.find_element(*self._edit_listing_button_locator).click()
        from pages.desktop.developers.edit_addon import EditAddon

        return EditAddon(self.selenium, self.base_url).wait_for_page_to_load()

    @property
    def generated_theme_preview(self):
        return self.find_element(*self._theme_preview_locator)
