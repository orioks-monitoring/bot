import textwrap

import qrcode as qrcode
from PIL import Image, ImageDraw, ImageFont


class Imager():
    base_dir = 'images/source/'
    font_upper = ImageFont.truetype('source/PTSansCaption-Bold.ttf', size=64)
    font_downer = ImageFont.truetype('source/PTSansCaption-Bold.ttf', size=62)
    fill_upper = '#FFFFFF'
    fill_downer = '#C6F1FF'
    width_line = 27

    def _get_image_by_grade(self, current_grade, max_grade):
        if current_grade / max_grade < 0.5:
            self.image = Image.open(f'{self.base_dir}/red.png')
            self.draw_text = ImageDraw.Draw(self.image)
        elif current_grade / max_grade < 0.7:
            self.image = Image.open(f'{self.base_dir}/yellow.png')
            self.draw_text = ImageDraw.Draw(self.image)
        elif current_grade / max_grade < 0.85:
            self.image = Image.open(f'{self.base_dir}/salt.png')
            self.draw_text = ImageDraw.Draw(self.image)
        elif current_grade / max_grade >= 0.85:
            self.image = Image.open(f'{self.base_dir}/green.png')
            self.draw_text = ImageDraw.Draw(self.image)

        self.image_weight, self.image_height = self.image.size

    def _get_news_image(self):
        self.image = Image.open(f'{self.base_dir}/news.png')
        self.draw_text = ImageDraw.Draw(self.image)
        self.image_weight, self.image_height = self.image.size

    def _calculate_container(self, title_text, side_text, mark_change_text=None, need_qr=False):
        container_height = 0

        for line in textwrap.wrap(title_text, width=self.width_line):
            container_height += self.font_upper.getsize(line)[1]

        container_height += self.font_upper.getsize(title_text)[1] / 2

        for line in textwrap.wrap(side_text, width=self.width_line):
            container_height += self.font_upper.getsize(line)[1]

        if mark_change_text:
            for line in textwrap.wrap(mark_change_text, width=self.width_line):
                container_height += self.font_upper.getsize(line)[1]

            container_height += self.font_upper.getsize(mark_change_text)[1] / 2

        if need_qr:
            container_height += self.font_upper.getsize(side_text)[1] / 2
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
        img = qr.make_image(fill_color="#008CBA", back_color="white")
        self.image.paste(img, (int((self.image_weight - img.pixel_size) / 2), int(offset)))

    def _draw_text(
            self,
            text,
            font,
            fill,
            offset
    ):
        for line in textwrap.wrap(text, width=self.width_line):
            self.draw_text.text(
                ((self.image_weight - self.draw_text.textsize(line, font=font)[0]) / 2,
                 (self.image_height - self.container_height) / 2 + offset),
                line,
                fill=fill,
                font=font
            )
            offset += self.font_upper.getsize(line)[1]
        return offset

    def _draw_text_news(
            self,
            title_text,
            side_text,
            url
    ):
        offset = 0
        offset = self._draw_text(title_text, self.font_upper, self.fill_upper, offset)
        offset += self.font_upper.getsize(title_text)[1] / 4
        offset = self._draw_text(side_text, self.font_downer, self.fill_downer, offset)
        offset += self.font_upper.getsize(title_text)[1] / 4
        offset += self.font_upper.getsize(title_text)[1] / 1
        offset += self.font_upper.getsize(title_text)[1] / 2
        self._draw_qr(url, offset)

    def _draw_text_marks(
            self,
            title_text,
            mark_change_text,
            side_text,

    ):
        offset = 0
        offset = self._draw_text(title_text, self.font_upper, self.fill_upper, offset)
        offset += self.font_upper.getsize(title_text)[1] / 4
        offset = self._draw_text(mark_change_text, self.font_upper, self.fill_upper, offset)
        offset += self.font_upper.getsize(title_text)[1] / 4
        self._draw_text(side_text, self.font_downer, self.fill_downer, offset)

    def get_image_marks(
            self,
            current_grade: int,
            max_grade: int,
            title_text: str,
            mark_change_text: str,
            side_text: str,
    ):
        self._get_image_by_grade(current_grade, max_grade)
        self._calculate_container(title_text, side_text, mark_change_text=mark_change_text)
        self._draw_text_marks(title_text, mark_change_text, side_text)

        return self.image

    def get_image_news(
            self,
            title_text,
            side_text,
            url
    ):
        self._get_news_image()
        self._calculate_container(title_text, side_text, need_qr=True)
        self._draw_text_news(title_text, side_text, url)
        return self.image
