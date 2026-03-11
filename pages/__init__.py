from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

# ---------------------------------------------------------------------------
# Backward-compatible re-exports.
#
# All existing "internet" page objects are accessible directly from `pages`:
#     from pages import LoginPage          # still works
#     from pages.internet import LoginPage  # also works (site-specific)
#
# New sites (saucedemo, demoqa) should be imported from their own sub-package:
#     from pages.saucedemo import SauceDemoLoginPage
# ---------------------------------------------------------------------------
# Delegate to pages.internet for the "internet" site page objects
from pages.internet import _EXPORTS, __all__  # noqa: F401


def __getattr__(name: str) -> Any:
    module_name = _EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(f"{__name__}.internet.{module_name}")

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
    from .internet.ab_test_page import ABTestPage
    from .internet.add_remove_elements_page import AddRemoveElementsPage
    from .internet.basic_auth_page import BasicAuthPage
    from .internet.broken_images_page import BrokenImagesPage
    from .internet.challenging_dom_page import ChallengingDomPage
    from .internet.checkboxes_page import CheckboxesPage
    from .internet.context_menu_page import ContextMenuPage
    from .internet.digest_auth_page import DigestAuthPage
    from .internet.disappearing_elements_page import DisappearingElementsPage
    from .internet.drag_and_drop_page import DragAndDropPage
    from .internet.dropdown_page import DropdownPage
    from .internet.dynamic_content_page import DynamicContentPage
    from .internet.dynamic_controls_page import DynamicControlsPage
    from .internet.dynamic_loading_page import DynamicLoadingPage
    from .internet.entry_ad_page import EntryAdPage
    from .internet.exit_intent_page import ExitIntentPage
    from .internet.file_download_page import FileDownloadPage
    from .internet.file_upload_page import FileUploadPage
    from .internet.floating_menu_page import FloatingMenuPage
    from .internet.forgot_password_page import ForgotPasswordPage
    from .internet.geolocation_page import GeolocationPage
    from .internet.homepage import HomePage
    from .internet.horizontal_slider_page import HorizontalSliderPage
    from .internet.hovers_page import HoversPage
    from .internet.iframe_page import IFramePage
    from .internet.infinite_scroll_page import InfiniteScrollPage
    from .internet.inputs_page import InputsPage
    from .internet.javascript_alerts_page import JavaScriptAlertsPage
    from .internet.javascript_error_page import JavaScriptErrorPage
    from .internet.jqueryui_menu_page import JQueryUIMenuPage
    from .internet.key_presses_page import KeyPressesPage
    from .internet.landing_page import LandingPage
    from .internet.large_dom_page import LargeDomPage
    from .internet.login_page import LoginPage
    from .internet.nested_frames_page import NestedFramesPage
    from .internet.notification_message_page import NotificationMessagePage
    from .internet.redirector_page import RedirectorPage
    from .internet.secure_area_page import SecureAreaPage
    from .internet.secure_file_download_page import SecureFileDownloadPage
    from .internet.shadow_dom_page import ShadowDomPage
    from .internet.shifting_content_image_page import ShiftingContentImagePage
    from .internet.shifting_content_list_page import ShiftingContentListPage
    from .internet.shifting_content_menu_page import ShiftingContentMenuPage
    from .internet.slow_resources_page import SlowResourcesPage
    from .internet.sortable_tables_page import SortableTablesPage
    from .internet.status_codes_page import StatusCodesPage
    from .internet.tinymce_ai_docs_page import TinyMceAiDocsPage
    from .internet.typos_page import TyposPage
    from .internet.windows_page import WindowsPage
