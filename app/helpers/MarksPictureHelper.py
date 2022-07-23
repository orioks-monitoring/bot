import textwrap
import os
import qrcode as qrcode
from PIL import Image, ImageDraw, ImageFont
import pathlib
import secrets

from app.helpers.AssetsHelper import assetsHelper
from config import config


class MarksPictureHelper:

    def __init__(self):
        self._font_path = assetsHelper.make_full_path('fonts/PTSansCaption-Bold.ttf')
        self._font_upper_size = 64
        self._font_downer_size = 62

        self._font_upper = ImageFont.truetype(self._font_path, size=self._font_upper_size)
        self._font_downer = ImageFont.truetype(self._font_path, size=self._font_downer_size)

        self._fill_upper = '#FFFFFF'
        self._fill_downer = '#C6F1FF'

        self._width_line = 27

    def _get_image_by_grade(self, current_grade, max_grade):
        if current_grade == 0:
            self.image = Image.open(assetsHelper.make_full_path('images/red.png'))
        elif current_grade / max_grade < 0.5:
            self.image = Image.open(assetsHelper.make_full_path('images/orange.png'))
        elif current_grade / max_grade < 0.7:
            self.image = Image.open(assetsHelper.make_full_path('images/yellow.png'))
        elif current_grade / max_grade < 0.85:
            self.image = Image.open(assetsHelper.make_full_path('images/salt.png'))
        elif current_grade / max_grade >= 0.85:
            self.image = Image.open(assetsHelper.make_full_path('images/green.png'))
        self.draw_text = ImageDraw.Draw(self.image)
        self.image_weight, self.image_height = self.image.size

    def _get_news_image(self):
        self.image = Image.open(assetsHelper.make_full_path('images/news.png'))
        self.draw_text = ImageDraw.Draw(self.image)
        self.image_weight, self.image_height = self.image.size

    def _calculate_count_of_lines_by_width_line(self, text: str) -> int:
        return len(textwrap.wrap(text, width=self._width_line))

    def _calculate_container(self, title_text, side_text, mark_change_text=None, need_qr=False,
                             need_split_mark_change_text=False):
        container_height = 0

        for line in textwrap.wrap(title_text, width=self._width_line):
            container_height += self._font_upper.getsize(line)[1]

        container_height += self._font_upper.getsize(title_text)[1] / 2
        self.container_width = \
            self._font_upper.getsize(title_text)[0] / self._calculate_count_of_lines_by_width_line(title_text)

        for line in textwrap.wrap(side_text, width=self._width_line):
            container_height += self._font_upper.getsize(line)[1]

        if mark_change_text:
            for line in textwrap.wrap(
                    mark_change_text,
                    width=self._width_line if need_split_mark_change_text else len(mark_change_text)
            ):
                container_height += self._font_upper.getsize(line)[1]

            container_height += self._font_upper.getsize(mark_change_text)[1] / 2

        if need_qr:
            container_height += self._font_upper.getsize(side_text)[1] / 2
            container_height += 155

        self.container_height = container_height

    def _draw_qr(
            self,
            url,
            offset
    ):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color='#008CBA', back_color='white')
        self.image.paste(img, ((self.image_weight - img.pixel_size) // 2, int(offset)))

    def _draw_text(
            self,
            text,
            font,
            fill,
            offset,
            need_split=True
    ):
        width_to_split = self._width_line
        if not need_split:
            width_to_split = len(text)
        for line in textwrap.wrap(text, width=width_to_split):
            self.draw_text.text(
                ((self.image_weight - self.draw_text.textsize(line, font=font)[0]) / 2,
                 (self.image_height - self.container_height) / 2 + offset),
                line,
                fill=fill,
                font=font
            )
            offset += self._font_upper.getsize(line)[1]
        return offset

    def _draw_text_news(
            self,
            title_text,
            side_text,
            url
    ):
        offset = 0
        offset = self._draw_text(title_text, self._font_upper, self._fill_upper, offset)
        offset += self._font_upper.getsize(title_text)[1] / 4
        offset = self._draw_text(side_text, self._font_downer, self._fill_downer, offset)
        offset += self._font_upper.getsize(title_text)[1] / 4
        self._draw_qr(url, 750 - (750 - offset) / 2 - 75)

    def _draw_text_marks(
            self,
            title_text,
            mark_change_text,
            side_text,

    ):
        offset = 0
        offset = self._draw_text(title_text, self._font_upper, self._fill_upper, offset)
        offset += self._font_upper.getsize(title_text)[1] / 4
        offset = self._draw_text(mark_change_text, self._font_upper, self._fill_upper, offset, need_split=False)
        offset += self._font_upper.getsize(title_text)[1] / 4
        self._draw_text(side_text, self._font_downer, self._fill_downer, offset)

    def _calculate_font_size_and_text_width(self, title_text, side_text, need_qr: bool = False, mark_change_text=None):
        self._calculate_container(title_text, side_text, need_qr=need_qr, mark_change_text=mark_change_text)
        if self.container_height <= 670:
            return True
        if self.container_height > 670 and self.container_width < 1200:
            self._width_line += 1
        self._font_upper_size -= 1
        self._font_downer_size -= 1
        self._font_upper = ImageFont.truetype(self._font_path, size=self._font_upper_size)
        self._font_downer = ImageFont.truetype(self._font_path, size=self._font_downer_size)
        self._calculate_font_size_and_text_width(title_text, side_text, need_qr=need_qr,
                                                 mark_change_text=mark_change_text)

    def get_image_marks(
            self,
            current_grade: float,
            max_grade: float,
            title_text: str,
            mark_change_text: str,
            side_text: str,
    ) -> pathlib.Path:
        current_grade = 0 if current_grade == 'н' else current_grade
        max_grade = 1 if max_grade == 0 else max_grade
        self._get_image_by_grade(current_grade, max_grade)
        self._calculate_font_size_and_text_width(title_text, side_text, mark_change_text=mark_change_text)
        self._draw_text_marks(title_text, mark_change_text, side_text)
        path_to_result_image = pathlib.Path(os.path.join(config.BASEDIR, f'temp_{secrets.token_hex(15)}.png'))
        self.image.save(path_to_result_image)
        return path_to_result_image

    def get_image_news(
            self,
            title_text: str,
            side_text: str,
            url: str
    ) -> pathlib.Path:
        path_to_result_image = pathlib.Path(os.path.join(config.BASEDIR, f'temp_{secrets.token_hex(15)}.png'))
        self._get_news_image()
        if title_text == '':
            self.image.save(path_to_result_image)
            return path_to_result_image
        self._calculate_font_size_and_text_width(title_text, side_text, need_qr=True)
        self._draw_text_news(title_text, side_text, url)
        self.image.save(path_to_result_image)
        return path_to_result_image