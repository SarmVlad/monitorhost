$("#signup-form").validate({
    rules: {
        inputFirstName: {
            required: true,
            minlength: 2,
        },

        inputLastName: {
            required: true,
            minlength: 2,
        },

        inputEmail: {
            required: true,
            email: true,
        },

        inputPassword: {
            required: true,
            minlength: 8,
        },
    },

    messages: {
        inputFirstName: {
            required: 'Поле обязательно для заполнения!',
            minlength: 'Имя должно содержать не менее 2-ух букв!',
        },

        inputLastName: {
            required: 'Поле обязательно для заполнения!',
            minlength: 'Фамилия должна содержать не менее 2-ух букв!',
        },

        inputEmail: {
            required: 'Поле обязательно для заполнения!',
            email: 'Введите корректный адрес электроннй почты!',
        },

        inputPassword: {
            required: 'Поле обязательно для заполнения!',
            minlength: 'Пароль должен содержать не менее 8-ми символов!',
        },
    }
});

$("#signin-form").validate({
    rules: {


    },

    messages: {


    }
})

