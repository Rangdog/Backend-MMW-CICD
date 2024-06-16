from datetime import datetime
from base.models import *
from .serializers import *
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.utils.timezone import now
from rest_framework import status, generics
from rest_framework.response import Response


class StatsImportAndExportView(generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        year = data["year"]

        if year is None:
            return Response(
                {"error": "Thiếu tham số year"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Tính tổng tiền nhập cho từng tháng trong năm
        import_stats = (
            ImportForm.objects.filter(created_date__year=year)
            .annotate(month=ExtractMonth("created_date"))
            .values("month")
            .annotate(total_import=Sum("total"))
            .order_by("month")
        )

        # Tính tổng tiền xuất cho từng tháng trong năm
        export_stats = (
            ExportForm.objects.filter(created_date__year=year)
            .annotate(month=ExtractMonth("created_date"))
            .values("month")
            .annotate(total_export=Sum("total"))
            .order_by("month")
        )

        # Merge kết quả của nhập và xuất
        monthly_stats = []
        for i in range(1, 13):  # 12 tháng
            month_import = next(
                (item for item in import_stats if item["month"] == i),
                {"total_import": 0},
            )
            month_export = next(
                (item for item in export_stats if item["month"] == i),
                {"total_export": 0},
            )

            monthly_stats.append(
                {
                    "month": i,
                    "total_import": month_import["total_import"],
                    "total_export": month_export["total_export"],
                }
            )

        return Response(monthly_stats)


class Top5PopularProductsView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        month = data["month"]
        year = data["year"]

        # Xác định ngày đầu tiên và cuối cùng của tháng
        start_date = datetime(int(year), int(month), 1)
        if int(month) == 12:
            end_date = datetime(int(year) + 1, 1, 1)
        else:
            end_date = datetime(int(year), int(month) + 1, 1)

        # Lấy tất cả các ExportDetail trong tháng được chỉ định
        export_details = ExportDetail.objects.filter(
            form__created_date__gte=start_date, form__created_date__lt=end_date
        )

        # Tính tổng số lượng và tổng giá trị của từng sản phẩm
        product_data = {}
        for detail in export_details:
            product_id = detail.product_id
            quantity = detail.quantity
            price = (
                detail.price * quantity
            )  # Tính tổng giá trị của sản phẩm trong mỗi form
            if product_id in product_data:
                product_data[product_id]["quantity"] += quantity
                product_data[product_id]["value"] += price
            else:
                product_data[product_id] = {"quantity": quantity, "value": price}

        # Sắp xếp sản phẩm theo tổng giá trị giảm dần
        sorted_products = sorted(
            product_data.items(), key=lambda x: x[1]["value"], reverse=True
        )

        # Chuẩn bị dữ liệu trả về
        pie_chart_data = []
        for product_id, data in sorted_products[:5]:
            product = Product.objects.get(pk=product_id)
            pie_chart_data.append(
                {
                    "id": product_id,
                    "label": product.name,
                    "quantity": data["quantity"],
                    "value": data["value"],
                }
            )

        return Response(pie_chart_data)


class TotalImport(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        today = now()
        current_month = today.month
        # Nếu là tháng 1, tháng trước là tháng 12 của năm trước
        previous_month = today.month - 1 or 12
        current_year = today.year
        previous_year = current_year if today.month != 1 else current_year - 1

        # Tính tổng tiền xuất của tháng hiện tại
        current_month_total = (
            ImportForm.objects.filter(
                created_date__year=current_year, created_date__month=current_month
            ).aggregate(Sum("total"))["total__sum"]
            or 0
        )

        # Tính tổng tiền xuất của tháng trước
        previous_month_total = (
            ImportForm.objects.filter(
                created_date__year=previous_year, created_date__month=previous_month
            ).aggregate(Sum("total"))["total__sum"]
            or 0
        )

        # Tính mức tăng và phần trăm tăng
        increase = current_month_total - previous_month_total
        percentage = (
            (increase / previous_month_total * 100) if previous_month_total != 0 else 0
        )

        data = {
            "current": current_month_total,
            "increase": increase,
            "percentage": percentage,
        }

        serializer = ImportStatisticsSerializer(data)
        return Response(serializer.data)


class ToltalExport(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        today = now()
        current_month = today.month
        # Nếu là tháng 1, tháng trước là tháng 12 của năm trước
        previous_month = today.month - 1 or 12
        current_year = today.year
        previous_year = current_year if today.month != 1 else current_year - 1

        # Tính tổng tiền xuất của tháng hiện tại
        current_month_total = (
            ExportForm.objects.filter(
                created_date__year=current_year, created_date__month=current_month
            ).aggregate(Sum("total"))["total__sum"]
            or 0
        )

        # Tính tổng tiền xuất của tháng trước
        previous_month_total = (
            ExportForm.objects.filter(
                created_date__year=previous_year, created_date__month=previous_month
            ).aggregate(Sum("total"))["total__sum"]
            or 0
        )

        # Tính mức tăng và phần trăm tăng
        increase = current_month_total - previous_month_total
        percentage = (
            (increase / previous_month_total * 100) if previous_month_total != 0 else 0
        )

        data = {
            "current": current_month_total,
            "increase": increase,
            "percentage": percentage,
        }

        serializer = ExportStatisticsSerializer(data)
        return Response(serializer.data)
