from django.http import HttpResponse
from django.shortcuts import render
from .models import Categoria, Produto, Imagem
from PIL import Image, ImageDraw, ImageFont
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def add_produto(request):
   if request.method == "GET":
      categorias = Categoria.objects.all()
      return render(request, 'add_produto.html', {'categorias': categorias} )
   elif request.method == "POST":
      nome = request.POST.get('nome')
      categoria = request.POST.get('categoria')
      quantidade = request.POST.get('quantidade')
      preco_compra = request.POST.get('preco_compra')
      preco_venda = request.POST.get('preco_venda')

      imagens = request.FILES.getlist('imagens')
      produto= Produto(nome=nome, categoria_id=categoria, quantidade=quantidade,preco_compra=preco_compra,preco_venda=preco_venda)


      produto.save()

      for f in request.FILES.getlist('imagens'):
         name= f'{date.today()}-{produto.id}.jpg'
         img = Image.open(f)
         img = img.convert('RGB')
         img = img.resize((500,500))
         draw = ImageDraw.Draw(img)
         draw.text((20, 480), f"MGMODAS {date.today()}",(255,255,255))
         output = BytesIO()
         img.save(output, format='JPEG', quality=100)
         output.seek(0)
         img_final= InMemoryUploadedFile(output, 'ImageField', name, 'imgage/jpeg',sys.getsizeof(output), None )
         img= Imagem(imagem =img_final, produto=produto)
         img.save()

      return HttpResponse('foi')
