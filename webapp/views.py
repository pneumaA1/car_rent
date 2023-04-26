from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from webapp.forms import RegisterUserForm
from webapp.models import Car


def index(request):
    """
      Render the main page of the website with the main car and a selection of cars.

      This view retrieves the 3 most recent cars in the database and the main car,
      which is the first car with the `is_main=True` attribute set. These cars are
      passed to the template context, which is rendered using the `index.html`
      template.

      Args:
          request: An HTTP request object, typically generated by a user's interaction
              with a web browser.

      Returns:
          An HTTP response containing the rendered HTML page.
      """
    cars = Car.objects.all()[:3]
    main_car = Car.objects.filter(is_main=True).first()
    context = {
        'cars': cars,
        'main_car': main_car
    }
    return render(request, 'webapp/index.html', context=context)


class AboutView(TemplateView):
    """
    Renders the 'about' page of the web application.
    Uses the 'about.html' template to display information on the purpose and characteristics
    """
    template_name = 'webapp/about.html'


class ServicesView(TemplateView):
    """
    Renders the 'Services' page of the web application.
    Uses the 'Services.html' template to display information on the purpose and characteristics
    """
    template_name = 'webapp/services.html'


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = 'webapp/contact.html'


class CarListView(ListView):
    """A view displaying a list of all Car objects.

       Attributes:
           template_name (str): A string specifying the name of the template to
               use when rendering the list of cars.
           context_object_name (str): A string specifying the name of the
               variable to use in the template context that contains the list
               of cars.

       Methods:
           get_context_data(**kwargs): Overrides the superclass's method to add
               pagination to the queryset, and returns the updated context
               dictionary.
           get_queryset(): Returns a QuerySet containing all Car objects.
       """
    template_name = 'webapp/cars.html'
    context_object_name = 'cars'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page')
        paginator = Paginator(context['object_list'], 4)
        page_objs = paginator.get_page(page_number)
        context['page_objs'] = page_objs
        return super().get_context_data(**context)

    def get_queryset(self):
        return Car.objects.all()


class CarDetailView(DetailView):
    """
    The `CarDetailView` class inherits from the `DetailView` class and is responsible for rendering a detailed view of a single `Car` object.

    Attributes:
        - `model`: The `Car` model that the view will render details for.
        - `template_name`: The name of the HTML template file that will be used to render the view.

    Methods:
        - `get`: Retrieves the `Car` object that the view is rendering details for and renders the appropriate template with the object's details.
        - `get_context_data`: Overridden method that adds additional context data to the view's context dictionary.
    """
    model = Car
    template_name = 'webapp/car_detail.html'


class CRLoginView(LoginView):
    """
    This view renders the login page and logs in the user if the form is valid.
    Inherits from Django's LoginView and uses its default implementation.
    """
    template_name = 'webapp/login.html'
    redirect_authenticated_user = True


class CRLogoutView(LoginRequiredMixin, LogoutView):
    """
    This view logs out the user and renders the logout page if the request is successful.
    Inherits from Django's LogoutView and uses its default implementation.
    Requires user authentication before accessing the view.
    """
    template_name = 'webapp/logout.html'


class RegisterUserView(CreateView):
    """
    This view handles user registration by rendering the registration page and creating a new user if the form is valid.
    Inherits from Django's CreateView and uses the RegisterUserForm to process registration.
    On successful registration, redirects the user to the "register_done" page.
    """
    model = User
    template_name = 'webapp/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('webapp:register_done')


class RegisterDoneView(TemplateView):
    """
    This view renders the registration success page after a user has successfully registered.
    Inherits from Django's TemplateView and uses its default implementation.
    """
    template_name = 'webapp/register_done.html'
