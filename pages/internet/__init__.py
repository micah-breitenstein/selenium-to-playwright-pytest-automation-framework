from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

_EXPORTS: dict[str, str] = {
    "ABTestPage": "ab_test_page",
    "PWABTestPage": "pw_ab_test_page",
    "AddRemoveElementsPage": "add_remove_elements_page",
    "PWAddRemoveElementsPage": "pw_add_remove_elements_page",
    "BasicAuthPage": "basic_auth_page",
    "BrokenImagesPage": "broken_images_page",
    "PWBrokenImagesPage": "pw_broken_images_page",
    "ChallengingDomPage": "challenging_dom_page",
    "CheckboxesPage": "checkboxes_page",
    "PWCheckboxesPage": "pw_checkboxes_page",
    "ContextMenuPage": "context_menu_page",
    "PWContextMenuPage": "pw_context_menu_page",
    "DigestAuthPage": "digest_auth_page",
    "DisappearingElementsPage": "disappearing_elements_page",
    "PWDisappearingElementsPage": "pw_disappearing_elements_page",
    "DragAndDropPage": "drag_and_drop_page",
    "DropdownPage": "dropdown_page",
    "PWDropdownPage": "pw_dropdown_page",
    "DynamicContentPage": "dynamic_content_page",
    "PWDynamicContentPage": "pw_dynamic_content_page",
    "DynamicLoadingPage": "dynamic_loading_page",
    "EntryAdPage": "entry_ad_page",
    "PWEntryAdPage": "pw_entry_ad_page",
    "ExitIntentPage": "exit_intent_page",
    "FileDownloadPage": "file_download_page",
    "FileUploadPage": "file_upload_page",
    "FloatingMenuPage": "floating_menu_page",
    "PWFloatingMenuPage": "pw_floating_menu_page",
    "ForgotPasswordPage": "forgot_password_page",
    "PWForgotPasswordPage": "pw_forgot_password_page",
    "GeolocationPage": "geolocation_page",
    "HorizontalSliderPage": "horizontal_slider_page",
    "PWHorizontalSliderPage": "pw_horizontal_slider_page",
    "HoversPage": "hovers_page",
    "PWHoversPage": "pw_hovers_page",
    "IFramePage": "iframe_page",
    "InfiniteScrollPage": "infinite_scroll_page",
    "InputsPage": "inputs_page",
    "PWInputsPage": "pw_inputs_page",
    "JQueryUIMenuPage": "jqueryui_menu_page",
    "JavaScriptAlertsPage": "javascript_alerts_page",
    "JavaScriptErrorPage": "javascript_error_page",
    "PWJavaScriptErrorPage": "pw_javascript_error_page",
    "KeyPressesPage": "key_presses_page",
    "PWKeyPressesPage": "pw_key_presses_page",
    "LargeDomPage": "large_dom_page",
    "PWLargeDomPage": "pw_large_dom_page",
    "LandingPage": "landing_page",
    "LoginPage": "login_page",
    "PWLoginPage": "pw_login_page",
    "NestedFramesPage": "nested_frames_page",
    "NotificationMessagePage": "notification_message_page",
    "PWNotificationMessagePage": "pw_notification_message_page",
    "RedirectorPage": "redirector_page",
    "PWRedirectorPage": "pw_redirector_page",
    "SecureAreaPage": "secure_area_page",
    "SecureFileDownloadPage": "secure_file_download_page",
    "ShiftingContentImagePage": "shifting_content_image_page",
    "ShiftingContentListPage": "shifting_content_list_page",
    "ShiftingContentMenuPage": "shifting_content_menu_page",
    "PWShiftingContentMenuPage": "pw_shifting_content_menu_page",
    "ShadowDomPage": "shadow_dom_page",
    "SlowResourcesPage": "slow_resources_page",
    "SortableTablesPage": "sortable_tables_page",
    "PWSortableTablesPage": "pw_sortable_tables_page",
    "StatusCodesPage": "status_codes_page",
    "PWStatusCodesPage": "pw_status_codes_page",
    "TinyMceAiDocsPage": "tinymce_ai_docs_page",
    "WindowsPage": "windows_page",
    "PWWindowsPage": "pw_windows_page",
}

__all__ = sorted(_EXPORTS.keys())


def __getattr__(name: str) -> Any:
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(f"{__name__}.{module_name}")

    try:
        value = getattr(module, name)
    except AttributeError as e:
        raise AttributeError(
            f"Module {module.__name__!r} does not define {name!r}"
        ) from e

    globals()[name] = value  # cache it
    return value


# IDE / type checker support (not executed at runtime)
if TYPE_CHECKING:
    from .ab_test_page import ABTestPage
    from .pw_ab_test_page import PWABTestPage
    from .add_remove_elements_page import AddRemoveElementsPage
    from .pw_add_remove_elements_page import PWAddRemoveElementsPage
    from .basic_auth_page import BasicAuthPage
    from .broken_images_page import BrokenImagesPage
    from .pw_broken_images_page import PWBrokenImagesPage
    from .challenging_dom_page import ChallengingDomPage
    from .checkboxes_page import CheckboxesPage
    from .pw_checkboxes_page import PWCheckboxesPage
    from .context_menu_page import ContextMenuPage
    from .pw_context_menu_page import PWContextMenuPage
    from .digest_auth_page import DigestAuthPage
    from .disappearing_elements_page import DisappearingElementsPage
    from .pw_disappearing_elements_page import PWDisappearingElementsPage
    from .drag_and_drop_page import DragAndDropPage
    from .dropdown_page import DropdownPage
    from .pw_dropdown_page import PWDropdownPage
    from .dynamic_content_page import DynamicContentPage
    from .pw_dynamic_content_page import PWDynamicContentPage
    from .dynamic_loading_page import DynamicLoadingPage
    from .entry_ad_page import EntryAdPage
    from .pw_entry_ad_page import PWEntryAdPage
    from .exit_intent_page import ExitIntentPage
    from .file_download_page import FileDownloadPage
    from .file_upload_page import FileUploadPage
    from .floating_menu_page import FloatingMenuPage
    from .pw_floating_menu_page import PWFloatingMenuPage
    from .forgot_password_page import ForgotPasswordPage
    from .pw_forgot_password_page import PWForgotPasswordPage
    from .geolocation_page import GeolocationPage
    from .horizontal_slider_page import HorizontalSliderPage
    from .pw_horizontal_slider_page import PWHorizontalSliderPage
    from .hovers_page import HoversPage
    from .pw_hovers_page import PWHoversPage
    from .iframe_page import IFramePage
    from .infinite_scroll_page import InfiniteScrollPage
    from .inputs_page import InputsPage
    from .pw_inputs_page import PWInputsPage
    from .javascript_alerts_page import JavaScriptAlertsPage
    from .javascript_error_page import JavaScriptErrorPage
    from .pw_javascript_error_page import PWJavaScriptErrorPage
    from .jqueryui_menu_page import JQueryUIMenuPage
    from .key_presses_page import KeyPressesPage
    from .pw_key_presses_page import PWKeyPressesPage
    from .landing_page import LandingPage
    from .large_dom_page import LargeDomPage
    from .pw_large_dom_page import PWLargeDomPage
    from .login_page import LoginPage
    from .pw_login_page import PWLoginPage
    from .nested_frames_page import NestedFramesPage
    from .notification_message_page import NotificationMessagePage
    from .pw_notification_message_page import PWNotificationMessagePage
    from .redirector_page import RedirectorPage
    from .pw_redirector_page import PWRedirectorPage
    from .secure_area_page import SecureAreaPage
    from .secure_file_download_page import SecureFileDownloadPage
    from .shadow_dom_page import ShadowDomPage
    from .shifting_content_image_page import ShiftingContentImagePage
    from .shifting_content_list_page import ShiftingContentListPage
    from .shifting_content_menu_page import ShiftingContentMenuPage
    from .pw_shifting_content_menu_page import PWShiftingContentMenuPage
    from .slow_resources_page import SlowResourcesPage
    from .sortable_tables_page import SortableTablesPage
    from .pw_sortable_tables_page import PWSortableTablesPage
    from .status_codes_page import StatusCodesPage
    from .pw_status_codes_page import PWStatusCodesPage
    from .tinymce_ai_docs_page import TinyMceAiDocsPage
    from .windows_page import WindowsPage
    from .pw_windows_page import PWWindowsPage
