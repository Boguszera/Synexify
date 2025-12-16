from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user

@login_required(login_url='web:login')
def tag_list(request):
    container = get_container()
    domain_user = get_domain_user(request)

    try:
        tags = container.tags.list_all_tags(domain_user)
    except Exception as e:
        messages.error(request, f"Error loading tags:{str(e)}")
        tags = []

    return render(request, "web/tags/tag_list.html", {
        "tags": tags,
        "can_manage": container.auth.is_admin_or_manager(domain_user)
    })


@login_required(login_url='web:login')
def tag_create(request):
    container = get_container()
    domain_user = get_domain_user(request)

    if request.method == "POST":
        name = request.POST.get("name")
        try:
            container.tags.create_tag(name, domain_user)
            messages.success(request, f"Tag '{name}' created successfully.")
            return redirect("web:tag_list")

        except PermissionDenied:
            messages.error(request, "No permissions to create tags.")
        except ValueError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred:{str(e)}")
    return redirect("web:tag_list")


@login_required(login_url='web:login')
def tag_delete(request, pk):
    container = get_container()
    domain_user = get_domain_user(request)

    if request.method == "POST":
        try:
            container.tags.delete_tag(str(pk), domain_user)
            messages.success(request, "Tag removed successfully.")
        except PermissionDenied:
            messages.error(request, "No permission to delete tags.")
        except ValueError as e:
            messages.error(request, f"Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect("web:tag_list")