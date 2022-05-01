document.addEventListener('DOMContentLoaded', () => {

//main screen
    function show_posts() {
        document.querySelector('#profile_view').style.display = "block";
        document.querySelector('#create_post').style.display = 'none';
        //edit button listener
        document.querySelectorAll('.edit').forEach((button) => {
            let post_id = button.id.match(/(\d+)/)[0];
            button.addEventListener('click', () => {
                show_edit(post_id)
            })
        })
    }

    // create post listener
    document.querySelector('#cp_button').addEventListener('click', show_create_post)

    // showing create post dialog function
    function show_create_post() {
        document.querySelector('#create_post').style.display = 'block';
        document.querySelector('#control-textarea').value = '';
        document.querySelector('#create_post').style.animationPlayState = 'running';
        document.querySelector('#profile_view').style.animationPlayState = 'running';
    }

    function show_edit(postId) {
        //showing edit text
        document.querySelector('#profile_view').style.display = 'block';
        document.querySelector('#create_post').style.display = 'none';
        document.querySelector(`.post_place${postId}`).style.display = 'none';
        document.querySelector(`.show_edit${postId}`).style.display = 'block';
        document.querySelector(`.textarea${postId}`).value = document.querySelector(`.post_place${postId}`).innerHTML;

        // add listener to the form with post id
        document.querySelector(`#do_edit${postId}`).addEventListener('click',  (e) => {
            console.log('clicked')
            let _post = document.querySelector(`.textarea${postId}`).value;
            let csrf_token = document.querySelector('#csrf_token').value;
            fetch(`/edit_post/${postId}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrf_token
                },
                body: JSON.stringify({'post': _post
                })


            }).then((r)=>{
                if( r["ok"] ===true) {

                    document.querySelector(`.show_edit${postId}`).style.display='none';
                    document.querySelector(`.post_place${postId}`).innerHTML=_post;
                    document.querySelector(`.post_place${postId}`).style.display='block';
                }
            })

        })
    }

//load posts by default
    show_posts();

})

