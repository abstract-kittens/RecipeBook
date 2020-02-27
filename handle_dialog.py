

def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        response.set_text('Hello, mthrfckr')
        return response, user_storage
