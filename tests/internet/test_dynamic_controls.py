from pages import DynamicControlsPage


def test_dynamic_controls_checkbox_toggle(page):
    controls = page(DynamicControlsPage)
    controls.go("/dynamic_controls")

    assert controls.is_checkbox_visible()

    controls.toggle_checkbox()
    assert "gone" in controls.message_text().lower()
    assert not controls.is_checkbox_visible()

    controls.toggle_checkbox()
    assert "back" in controls.message_text().lower()
    assert controls.is_checkbox_visible()


def test_dynamic_controls_enable_disable_input(page):
    controls = page(DynamicControlsPage)
    controls.go("/dynamic_controls")

    assert not controls.is_input_enabled()

    controls.enable_input()
    assert "enabled" in controls.message_text().lower()
    assert controls.is_input_enabled()

    controls.disable_input()
    assert "disabled" in controls.message_text().lower()
    assert not controls.is_input_enabled()
