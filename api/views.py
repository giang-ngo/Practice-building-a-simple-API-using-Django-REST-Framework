from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from rest_framework import status
from .models import Product,product_collection

# Create your views here.
@api_view(['GET'])
def api_overview(request):
    api_urls={
        'List':'/product-list/',
        'Detail View':'/product-detail/<str:pk>/',
        'Create':'/product-create/',
        'Update':'/product-update/<str:pk>/',
        'Delete':'/product-delete/<str:pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def product_list(request):
	products = Product.objects.all().order_by('-id')
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
	products = Product.objects.get(id=pk)
	serializer = ProductSerializer(products, many=False)
	return Response(serializer.data)


# thêm api vào mongodb và vào backend
@api_view(['POST'])
def product_create(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        # Lấy dữ liệu đã xác nhận từ serializer
        validated_data = serializer.validated_data
        validated_data['price'] = float(validated_data['price'])  # Chuyển đổi Decimal sang float
        # Kết nối đến MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['your_database_name']  # Thay 'your_database_name' bằng tên cơ sở dữ liệu của bạn
        collection = db['your_collection_name']  # Thay 'your_collection_name' bằng tên collection của bạn

        # Chèn dữ liệu vào MongoDB
        inserted_data = collection.insert_one(validated_data)
        
        # Trả về thông tin của đối tượng đã được chèn
        return Response({
            'id': str(inserted_data.inserted_id),
            'message': 'Data inserted successfully'
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def product_update(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def product_delete(request, pk):
	product = Product.objects.get(id=pk)
	product.delete()
	return Response('Item successfully deleted!')
