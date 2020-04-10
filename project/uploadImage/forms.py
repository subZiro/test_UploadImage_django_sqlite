from django import forms


from . models import ImageModel


class UploadForm(forms.Form):
    """создание экз формы загрузки изображения"""
    img_name = forms.ImageField(label='Выберите картинку', required=False)
    img_url = forms.CharField(label='Вставьте url',
                              widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'link for image'}),
                              required=False)

    def clean(self):
        """загрузка файла может быть только одним из способов (локально | с сети)"""
        img_name = self.cleaned_data.get('img_name', False)
        img_url = self.cleaned_data.get('img_url', False)

        if not img_name and not img_url:
            # если не чего не выбрано
            raise forms.ValidationError('Не выбраны поля, выберите один из способов загрузки')

        if img_name and img_url:
            # если заполнили обе формы
            raise forms.ValidationError('Нужно выбрать только один способ загрузки')


class ViewForm(forms.Form):
    """экз формы промотра/редактирования открытого изображения"""
    width = forms.IntegerField(label='Ширина изображения',
                               widget=forms.NumberInput(attrs={'class': 'form-control'}),
                               required=False)

    height = forms.IntegerField(label='Высота изображения',
                                widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                required=False)

    size = forms.IntegerField(label='Размер изображения',
                              widget=forms.NumberInput(attrs={'class': 'form-control'}),
                              required=False)

    def __init__(self, *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ImageModel
        fields = ['width', 'height', 'size']

    def clean(self):
        """проверка корректности ввода значений в поля"""
        width = self.data.get('width', False)
        height = self.data.get('height', False)
        size = self.data.get('size', False)
        e_message = ''

        if width or height or size:
            try:  # проверка ширины
                int(width)
            except:
                e_message += 'В поле ширина введено не корректное значение. '

            try:  # проверка высоты
                int(height)
            except:
                e_message += 'В поле высота введено не корректное значение. '

            try:  # проверка размера
                int(size)
            except:
                e_message += 'В поле размер изображения введено не корректное значение. '

            if e_message:
                # если ошибки при заполнении полей были
                raise forms.ValidationError(e_message)