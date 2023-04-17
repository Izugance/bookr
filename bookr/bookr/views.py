"""For the trivial rendering of a user profile."""
from io import BytesIO

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

# Tools for converting site info to graphs and excel docs:
from plotly.offline import plot
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet
import plotly.graph_objs as graphs

from .utils import get_books_read_by_month, get_read_books

# "login_url" is the url to redirect unauthenticated users to. It
# defaults to settings.LOGIN_URL, which is the same as follows.
# "redirect_field_name" is displayed next to the success url in the
# url query.
@login_required(login_url="/accounts/login/", redirect_field_name="redirect_to")
def profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    permissions = user.get_all_permissions()
    books_read_by_month = get_books_read_by_month(user.username)
    # Init x- and y-axes values.
    months = [i + 1 for i in range(12)]
    books_read = [0 for _ in range(12)]

    for num_books_read in books_read_by_month:
        list_index = num_books_read["date_created__month"] - 1
        books_read[list_index] = num_books_read["book_count"]

    figure = graphs.Figure()
    scatter = graphs.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type="div")

    context = {"user": user, "permissions": permissions, "books_read_plot": plot_html}
    return render(request, "profile.html", context=context)


@login_required(redirect_field_name="redirect_to")
def download_read_history(request: HttpRequest) -> HttpResponse:
    username = request.user.username
    read_books = get_read_books(username)
    read_books_buffer = BytesIO()  # In-memory => faster.

    workbook = Workbook(read_books_buffer)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Read Books")
    for row, book in enumerate(read_books):
        # Start from the next row.
        worksheet.write(row + 1, 0, book)
    workbook.close()

    excel_data = read_books_buffer.getvalue()  # Data to be written.
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=reading_history.xlsx"
    response.write(excel_data)
    return response
