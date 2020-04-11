import os
import base64
import imagehash

import urllib.request as urllib

from PIL import Image
from io import BytesIO

from django.core.files import File
from django.core.cache import cache
from django.core.files.temp import NamedTemporaryFile

from django.shortcuts import render, HttpResponseRedirect

from django.views.generic import ListView, TemplateView, DetailView


from . models import ImageModel
from . forms import UploadForm, ViewForm


class Index(ListView):
    """главная страница"""
    template_name = 'index.html'
    model = ImageModel
    paginate_by = 6

    def get_queryset(self):
        return ImageModel.objects.order_by('-date')


class Upload(TemplateView):
    """страница загрузки изображения"""
    template_name = 'upload.html'

    def get_context_data(self, **kwargs):
        """расширение метода родителя (добавение форм)"""
        context = {'UploadForm': UploadForm}
        return context

    def post(self, request, *args, **kwargs):
        """обработка отпрвки формы 'POST'"""
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            # если прошли проверку заполненых полей форм
            img_name = form.cleaned_data["img_name"]
            img_url = form.cleaned_data["img_url"]
            new_image = ImageModel()
            e_message = ''

            if img_name:
                # если загрузка происходит локально
                imageD = form.files.get('img_name')
                hash_img = str(imagehash.average_hash(Image.open(imageD)))
                try:
                    # запись в бд
                    new_image.hash = hash_img
                    new_image.img = img_name
                    new_image.save()
                    return HttpResponseRedirect('/')
                except Exception as e:
                    # если не удалось сохранить файл в бд, возвращаем upload с ошибкой
                    e_message = f'Error, cant write file to db, {e}'
                    context = {'UploadForm': form, 'e_message': e_message}
                    return render(request, 'upload.html', context=context)

            elif img_url:
                # если загрузка изображения ссылке
                img = os.path.basename(img_url)
                url = urllib.urlretrieve(img_url)

                imageU = Image.open(url[0])
                hash_img = str(imagehash.average_hash(imageU))

                tmp = NamedTemporaryFile(delete=True)
                tmp.write(urllib.urlopen(img_url).read())
                tmp.flush()

                try:
                    # запись в бд
                    new_image.hash = hash_img
                    new_image.img.save(img, File(tmp))
                    return HttpResponseRedirect('/')
                except Exception as e:
                    # если не удалось сохранить файл в бд, возвращаем upload с ошибкой
                    e_message = f'Error, cant write file to db, {e}'
                    context = {'UploadForm': form, 'e_message': e_message}
                    return render(request, 'upload.html', context=context)

        else:
            # если не прошли проверку открываем заново форму
            context = {'UploadForm': form}
            return render(request, 'upload.html', context)

    def create_hash(self):
        """генерация хеша изображения"""
        pass


class View(DetailView):
    """страница просмотра/изменения изображения"""
    template_name = 'view.html'
    queryset = ImageModel.objects.all()

    def get_context_data(self, *args, **kwargs):
        """расширение метода родителя (добавение форм)"""
        data = super().get_context_data(**kwargs)
        form = ViewForm(data.get('view').request.GET)
        read_data = self.request.GET
        hash_image = data.get('imagemodel').pk
        e_message = ''

        if form.is_valid():
            # если прошли проверку заполненой формы
            name_image = ImageModel.objects.get(hash=hash_image).img.name
            image = Image.open('upload/' + name_image)

            width = int(read_data.get('width', image.width))
            height = int(read_data.get('height', image.height))
            size = int(read_data.get('size', 0))

            image64 = cache.get("{}_{}_{}_{}".format(hash_image, width, height, size))

            if not image64:
                image = image.resize((width, height), Image.ANTIALIAS)
                buffered = BytesIO()

                if size == 0:
                    image.save(buffered, format="jpeg", quality=100)
                else:
                    for i in range(99, 1, -10):
                        buffered = BytesIO()
                        image.save(buffered, format="jpeg", optimize=True, quality=i)
                        if i == 1 or buffered.tell() < size:
                            break
                        else:
                            buffered.close()

                if (buffered.tell() > size) and size != 0:
                    e_message = """Максимально допустимое сжатие до {} байтов, 
                                           поэтому не удалось достичь желаемого результата в {}.""".format(buffered.tell(), size)

                image64 = str(base64.b64encode(buffered.getvalue()))[2:-1]
                cache.set("{}_{}_{}_{}".format(hash_image, width, height, size), image64, 120)

            # заполнение формы данными открытого изображения
            width = image.width
            height = image.height
            size = os.path.getsize('upload/' + name_image)
            form = ViewForm(initial={'width': width, 'height': height, 'size': size})
            context = {'context': '',
                       'ViewForm': form,
                       'image64': image64,
                       'e_message': e_message}
            return {'context': context}

        else:
            # возврат пустой формы
            context = {'ViewForm': form}
            return {'context': context}
