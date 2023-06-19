from django.db import models
from users.models import User
from django.urls import reverse


class ShopCategory(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품 분류 카테고리 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return str(self.category_name)

    def get_absolute_url(self):
        return reverse('product_view', kwargs={"category_id": self.id})


class ShopProduct(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품의 정보(이름,가격,수량,설명,등록일)를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    product_name = models.CharField(max_length=30)
    product_price = models.PositiveIntegerField(default=0)
    product_stock = models.PositiveIntegerField(default=0)
    product_desc = models.TextField()
    product_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        ShopCategory, on_delete=models.CASCADE, related_name='products')
    hits = models.PositiveIntegerField(default=0)


class ShopOrder(models.Model):
    '''
    작성자 : 장소은
    내용 : 주문 정보를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    order_quantity = models.PositiveIntegerField(default=0)
    order_totalprice = models.PositiveIntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    zip_code = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    address_message = models.CharField(max_length=150)
    receiver_name = models.CharField(max_length=20)
    receiver_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        ShopProduct, on_delete=models.CASCADE, related_name='product_key')


class ShopOrderDetail(models.Model):
    '''
    작성자 : 장소은
    내용 : 주문의 상태를 나타내는 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    product_count = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = (
        (0, "주문 접수 완료"),
        (1, "결제 확인 완료"),
        (2, "주문취소"),
        (3, "배송 시작"),
        (4, "배송 중"),
        (5, "배송 완료")
    )
    order = models.ForeignKey(
        ShopOrder, on_delete=models.CASCADE, related_name='order_info')
    product = models.ForeignKey(
        ShopProduct, on_delete=models.CASCADE, related_name='product_set')
    order_detail_status = models.PositiveSmallIntegerField(
        "진행 상태", choices=STATUS_CHOICES, default=0)

    def get_order_detail_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.order_detail_status, "")

    def __str__(self):
        return self.get_order_detail_status_display()


class ShopImageFile(models.Model):
    '''
    작성자 : 장소은
    내용 : 상품 이미지 모델
    최초 작성일: 2023.06.06
    업데이트 일자:
    '''
    image_file = models.ImageField(null=True, blank=True)
    product = models.ForeignKey(
        ShopProduct, on_delete=models.CASCADE, related_name='images')
