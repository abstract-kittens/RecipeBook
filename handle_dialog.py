def handle_dialog(request, response, user_storage):
    from addRecipe import addRecipe
    from changeRecipe import changeRecipe
    from openRecipe import openRecipe
    flag = 0
    if(flag == 0):
        if request.is_new_session:
            response.set_text('Привет, я твоя персональная книга рецептов, ты можешь записать рецепт, изменить существующий, или начать готовить.')
            return response, user_storage, flag
        elif request.command.lower() in [
            'запиши рецепт',
            'добавить рецепт',
            'новый рецепт',
            'добавь рецепт',
            ]:
            flag = 1
            #response.set_text('Скажите название нового рецепта.')
            addRecipe(request, response, user_storage)
            return response, user_storage, flag
        
        elif request.command.lower() in [
            'измени рецепт',
            'обнови рецепт',
            'исправь рецепт',
            ]:
            flag = 2  
            #response.set_text('Что изменить')
            changeRecipe(request, response, user_storage)
            return response, user_storage, flag
        
        elif request.command.lower() in [
            'начать готовку',
            'скажи шаги рецепта',
            'воспроизведи рецепт',
            ]:
            flag = 3
            #response.set_text('Шаги:')
            openRecipe(request, response, user_storage)
            return response, user_storage, flag
        else:
            response.set_text("я вас не поняла, повторите")
            return response, user_storage, flag
    elif(flag == 1):
        recipeName = request.command.lower()
        response.set_text(recipeName)
        flag = 0
        return response, user_storage, flag
    
    elif(flag == 2):
        recipeName = request.command.lower()
        response.set_text(recipeName)
        flag = 0
        return response, user_storage, flag
    
    elif(flag == 3):
        recipeName = request.command.lower()
        response.set_text(recipeName)
        flag = 0
        return response, user_storage, flag