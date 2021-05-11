

let profile_app = new Vue({
    el: "#profile-app",
    data: {
        new_resumecategory_title: '',
        resumecategories: resumecategories,
        new_resume_title: '',
        add_resume_category_form: add_resume_category_form
    },
    methods: {
        add_category: function () {
            let title = this.new_resumecategory_title
            var posting = $.post(url_add_resume_category,
                {
                    profile_id: profile_id,
                    title: title,
                    csrfmiddlewaretoken: csrfmiddlewaretoken
                }
            );

            // Put the results in a div
            posting.done(function (data) {
                console.log(data)

                if (data.result === 'SUCCEED') {
                    profile_app.resumecategories.push(data.resume_category)
                    profile_app.new_resumecategory_title = ''
                }
            })
        },
        add_resume: function (category_id) {
            let title = this.new_resume_title
            payload = {
                category_id: category_id,
                title: title,
                app_name: 'web',
                csrfmiddlewaretoken: csrfmiddlewaretoken
            }
            // console.log(payload)
            var posting = $.post(url_add_resume, payload);

            // Put the results in a div
            posting.done(function (data) {
                console.log(data)

                if (data.result === 'SUCCEED') {

                    profile_app.resumecategories.forEach(element => {
                        if (element.id == category_id) {
                            element.resumes.push(data.resume)
                        }
                    })


                    profile_app.new_resume_title = ''
                }
            })

        }
    }
})