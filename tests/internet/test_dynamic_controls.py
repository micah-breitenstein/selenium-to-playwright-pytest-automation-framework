from pages import DynamicControlsPage


def test_dynamic_controls_enable_disable_input(page):
    controls = page(DynamicControlsPage)
    controls.go("/dynamic_controls")

    assert not controls.is_input_enabled()

    controls.enable_input()
    assert controls.is_input_enabled()

    controls.disable_input()
    assert not controls.is_input_enabled()
