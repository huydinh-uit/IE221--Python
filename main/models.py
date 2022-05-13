from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

""""Định nghĩa các class như Product, Category, Banner..."""

# Banner
class Banner(models.Model):
    """"class banner: hiển thị quảng cáo cho store"""
    img=models.ImageField(upload_to="banner_imgs/") # cac img thuộc Banner sẽ có path dạng: banner_imgs/img_1/, tương tự với các class khác như Category, Product...
    alt_text=models.CharField(max_length=300)

    class Meta:
        verbose_name_plural='1. Banners'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category Danh muc
class Category(models.Model):
    """"Danh mục để phân thể loại sản phẩm"""
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="danhmuc_imgs/") #

    class Meta:
        verbose_name_plural='2. Danh muc' #

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

# Brand Tac gia
class Brand(models.Model):
    """"Tác giả"""
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="tacgia_imgs/") #

    class Meta:
        verbose_name_plural='3. Tac gia' #

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size So trang
""""Số trang"""
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Sizes'

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    """"class product, mang thông tin sản phẩm"""
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=400)
    detail=models.TextField()
    specs=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='6. Books' #

    def __str__(self):
        return self.title

# Product Attribute
class ProductAttribute(models.Model):
    """"Class chứa các thuộc tính của class Product"""
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="product_imgs/",null=True)

    class Meta:
        verbose_name_plural='7. ProductAttributes'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Order
""""Trạng thái đơn hàng"""
status_choice=(
        ('process','In Process'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
    )

class CartOrder(models.Model):
    """"Giỏ hàng thanh toán """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_dt=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=status_choice,default='process',max_length=150)

    class Meta:
        verbose_name_plural='8. Orders'

# OrderItems
class CartOrderItems(models.Model):
    """"Thông tin items của giỏ hàng"""
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=150)
    item=models.CharField(max_length=150)
    image=models.CharField(max_length=200)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='9. Order Items'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

# Product Review
""""Có 5 cấp độ sao để đánh giá sản phẩm"""
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)

class ProductReview(models.Model):
    """"Đánh giá sản phẩm: user infor, sản phẩm, review, rating"""
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    """"Danh sách các sản phẩm yêu thích"""
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

# AddressBook
class UserAddressBook(models.Model):
    """"User, địa chỉ, sdt người mua, trạng thái đơn mua"""
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=50,null=True)
    address=models.TextField()
    status=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='AddressBook'

    