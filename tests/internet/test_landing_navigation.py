def test_landing_navigation_to_dynamic_controls(landing):
    page = landing.load().go_to_dynamic_controls()

    assert page.current_url.endswith("/dynamic_controls")
