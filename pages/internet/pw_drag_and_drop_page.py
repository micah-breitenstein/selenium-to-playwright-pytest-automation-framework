from __future__ import annotations

from pages.core.pw_base_page import PWBasePage


class PWDragAndDropPage(PWBasePage):
    URL_PATH = "/drag_and_drop"

    COLUMN_A = "#column-a"
    COLUMN_B = "#column-b"
    HEADER_A = "#column-a header"
    HEADER_B = "#column-b header"

    def open(self) -> "PWDragAndDropPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.COLUMN_A)
        self.expect_visible(self.COLUMN_B)
        return self

    def header_texts(self) -> tuple[str, str]:
        a = self.get_text(self.HEADER_A)
        b = self.get_text(self.HEADER_B)
        return a, b

    def swap_columns_html5(self) -> "PWDragAndDropPage":
        before = self.header_texts()

        self.page.evaluate(
            "([srcSel, dstSel]) => {"
            " const src = document.querySelector(srcSel);"
            " const dst = document.querySelector(dstSel);"
            " if (!src || !dst) return;"
            " const dataTransfer = new DataTransfer();"
            " const fire = (type, elem) => elem.dispatchEvent(new DragEvent(type, { bubbles: true, cancelable: true, dataTransfer }));"
            " fire('dragstart', src);"
            " fire('dragenter', dst);"
            " fire('dragover', dst);"
            " fire('drop', dst);"
            " fire('dragend', src);"
            "}",
            [self.COLUMN_A, self.COLUMN_B],
        )

        self.page.wait_for_function(
            "([aSel, bSel, left, right]) => {"
            " const a = (document.querySelector(aSel)?.textContent || '').trim();"
            " const b = (document.querySelector(bSel)?.textContent || '').trim();"
            " return a === right && b === left;"
            "}",
            arg=[self.HEADER_A, self.HEADER_B, before[0], before[1]],
            timeout=self.config.timeout_ms,
        )
        return self
