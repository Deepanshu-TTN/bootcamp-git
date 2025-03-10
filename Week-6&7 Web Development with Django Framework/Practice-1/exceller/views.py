from django.shortcuts import render
import openpyxl

def parse_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb.active
        
        data = []
        for row in worksheet.iter_rows(values_only=True):
            data.append(row)

        header = data[0]
        rows = data[1:]

        return render(request, 'results.html', {'header': header, 'rows': rows})
    
    return render(request, 'upload.html')


