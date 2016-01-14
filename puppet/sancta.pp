node default {
    # окружение
    include envs
    # gerrit
    include gerrit
    # дженкинс
    include jenkins
    # кирилл не хотел выносить в отдельный рецепт
    # засрал дефоулт ноду и выебывался, тем, что это правильно
    # кирилл мудак :)
    include kirill_mudak
    # сайт детского сада елочка
    include elochkads
    # эзодаты
    include ezo_date
    # суперкарта
    include bestkarta
    # проект цели
    include aim
    # проект Никиты quqs
    include quqs
}
