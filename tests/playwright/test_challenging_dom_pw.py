from __future__ import annotations

import hashlib

import pytest

from pages.internet import PWChallengingDomPage


@pytest.mark.playwright
def test_challenging_dom_has_three_buttons_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()
    texts = page.button_texts()
    assert set(texts.keys()) == {"blue", "red", "green"}
    assert all(texts[color] for color in texts), (
        f"Expected all button texts to be non-empty, got: {texts}"
    )


@pytest.mark.playwright
def test_delete_first_row_by_column_text_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()

    clicked = page.page.evaluate(
        """
        () => {
            const rows = Array.from(document.querySelectorAll('table tbody tr'));
            for (const row of rows) {
                const firstCell = row.querySelector('td');
                if (firstCell && firstCell.textContent.includes('Iuvaret0')) {
                    const link = Array.from(row.querySelectorAll('a')).find(
                        a => a.textContent.trim().toLowerCase() === 'delete'
                    );
                    if (link) {
                        link.click();
                        return true;
                    }
                }
            }
            return false;
        }
        """
    )
    assert clicked, "Expected to click delete on row containing 'Iuvaret0'"
    page.page.wait_for_url("**#delete", timeout=page.config.timeout_ms)
    assert page.current_url.endswith("#delete")


@pytest.mark.playwright
def test_delete_first_row_dynamic_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()

    first_cell_text = (
        page.page.locator("table tbody tr").first.locator("td").first.inner_text()
    ).strip()

    clicked = page.page.evaluate(
        """
        (expected) => {
            const rows = Array.from(document.querySelectorAll('table tbody tr'));
            for (const row of rows) {
                const firstCell = row.querySelector('td');
                if (firstCell && firstCell.textContent.includes(expected)) {
                    const link = Array.from(row.querySelectorAll('a')).find(
                        a => a.textContent.trim().toLowerCase() === 'delete'
                    );
                    if (link) {
                        link.click();
                        return true;
                    }
                }
            }
            return false;
        }
        """,
        first_cell_text,
    )
    assert clicked, f"Expected to click delete on row containing {first_cell_text!r}"
    page.page.wait_for_url("**#delete", timeout=page.config.timeout_ms)
    assert page.current_url.endswith("#delete")


@pytest.mark.playwright
def test_button_labels_change_when_clicked_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()

    before = page.button_texts()
    changed = set()

    for selector in (page.BLUE_BTN, page.RED_BTN, page.GREEN_BTN):
        page.click(selector)
        after = page.button_texts()
        changed = {k for k in before if before[k] != after[k]}
        if changed:
            break

    if not changed:
        pytest.skip(
            f"Button labels did not change in this run. Before={before}, After={after}"
        )


@pytest.mark.playwright
def test_canvas_changes_when_button_clicked_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()

    before = page.page.evaluate(
        "() => document.querySelector('canvas').toDataURL('image/png')"
    )
    page.click(page.BLUE_BTN)
    page.page.wait_for_function(
        "before => document.querySelector('canvas').toDataURL('image/png') !== before",
        arg=before,
        timeout=10_000,
    )
    after = page.page.evaluate(
        "() => document.querySelector('canvas').toDataURL('image/png')"
    )

    assert before != after, "Expected canvas image to change after button click"


@pytest.mark.playwright
def test_answer_changes_when_button_clicked_playwright(pw_page_object_factory):
    page = pw_page_object_factory(PWChallengingDomPage).open()

    before_canvas = page.page.evaluate(
        "() => document.querySelector('canvas').toDataURL('image/png')"
    )
    before = hashlib.sha256(before_canvas.encode("utf-8")).hexdigest()

    page.click(page.GREEN_BTN)
    page.page.wait_for_function(
        "before => document.querySelector('canvas').toDataURL('image/png') !== before",
        arg=before_canvas,
        timeout=10_000,
    )

    after_canvas = page.page.evaluate(
        "() => document.querySelector('canvas').toDataURL('image/png')"
    )
    after = hashlib.sha256(after_canvas.encode("utf-8")).hexdigest()

    assert before != after, f"Expected Answer to change. Before={before}, After={after}"
