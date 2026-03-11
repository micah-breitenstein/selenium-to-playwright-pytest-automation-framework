from __future__ import annotations

import shutil
import tempfile
import uuid
from pathlib import Path

from pages.core.pw_base_page import PWBasePage


class PWFileUploadPage(PWBasePage):
    URL_PATH = "/upload"
    FILE_INPUT = "#file-upload"
    SUBMIT_BTN = "#file-submit"
    RESULT_HEADER = "h3"
    UPLOADED_FILENAME = "#uploaded-files"

    def open(self) -> "PWFileUploadPage":
        self.go(self.URL_PATH)
        self.expect_visible(self.FILE_INPUT)
        return self

    def upload_file_with_unique_name(self, original_file: Path | str) -> str:
        original = Path(original_file)
        if not original.exists():
            raise FileNotFoundError(f"Upload file not found: {original}")

        unique_name = f"{original.stem}_{uuid.uuid4().hex[:8]}{original.suffix}"

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir) / unique_name
            shutil.copy(original, temp_path)

            self.page.locator(self.FILE_INPUT).set_input_files(str(temp_path))
            self.click(self.SUBMIT_BTN)
            self.page.wait_for_function(
                "(selector) => (document.querySelector(selector)?.textContent || '').includes('File Uploaded')",
                arg=self.RESULT_HEADER,
                timeout=self.config.timeout_ms,
            )

        return unique_name

    def upload_success_message(self) -> str:
        return self.get_text(self.RESULT_HEADER)

    def uploaded_filename(self) -> str:
        return self.get_text(self.UPLOADED_FILENAME)
