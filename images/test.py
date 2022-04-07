from imager import Imager

imger = Imager()

# img = imger.get_image_marks(
#     current_grade=15,
#     max_grade=20,
#     title_text='А/П.1 по «Электроника в системе длинных названий, которые очень сложно запомнить»',
#     mark_change_text='0 —> 15 (из 20) (+ 15)',
#     side_text='Изменён балл за контрольное мероприятие'
# )

img = imger.get_image_news(
    title_text='Выбор элективных и факультативных дисциплин на 1 семестр 2022-2023 уч.г.',
    side_text='Опубликована новость',
    url='https://orioks.miet.ru/main/view-news?id=474'
)

img.show()
img.save('1.png')

