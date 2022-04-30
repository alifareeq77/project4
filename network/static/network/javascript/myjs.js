document.addEventListener('DOMContentLoaded', () => {

//main screen
    function show_posts() {
        document.querySelector('#profile_view').style.display = "block";
        document.querySelector('#create_post').style.display = 'none';
        //edit button listener
            let is_clicked=false;
        document.querySelectorAll('.edit').forEach(btn => {
            btn.onclick = () => {
            if (!is_clicked){
                is_clicked = true;
                document.querySelector('.post_place').style.display='none';
                let post_val = document.querySelector(`#post${btn.id}`).innerHTML;
                document.querySelector(`#post${btn.id}`).style.display='none';
                //create new text area for editing
                const element = document.createElement('div');
                element.classList.add(`edit${btn.id}`);
                element.innerHTML=`<div class="form-group"
                                         style="text-align: start; padding: 10px;margin-bottom: 20px">
                                    </div>
                                    <textarea name="content" class="form-control edit_text" id="control-textarea" cols="30" form="edit_form"></textarea>
                                    <div class="row d-flex justify-content-end" style="margin: 20px 10px 10px 20px">
                                        <button type="submit" class="btn btn-primary">
                                            submit
                                        </button>
                                    </div>
                                `;
                document.querySelector('.show_edit').append(element);
                document.querySelector('.show_edit').style.display='block';
                document.querySelector('.edit_text').value=post_val;
                let new_post=post_val;
                let csrf_token = Cookies.get('csrftoken');

                document.querySelector(`#edit_form${btn.id}`).onsubmit=(ed)=>{
                    ed.preventDefault();
                    new_post=document.querySelector('.edit_text').value;
                    fetch(`/edit_post/${btn.id}`,{
                        method:'POST',
                        credentials:'same-origin',
                        headers:{
                          'X-CSRFToken':csrf_token
                        }

                    }).then((r)=>{
                        console.log('hello ? ')
                        document.querySelector(`.edit${btn.id}`).style.display='none';
                        document.querySelector('.show_edit').style.display='none';
                         document.querySelector(`#post${btn.id}`).innerHTML=new_post;
                         document.querySelector(`#post${btn.id}`).style.display='block';
                         is_clicked=false;
                         document.querySelector('.edit_text').value='';
                    });

                }

            }
        }})

        }

// showing create post dialog
        function show_create_post() {
            document.querySelector('#create_post').style.display = 'block';
            document.querySelector('#control-textarea').value = '';
            document.querySelector('#create_post').style.animationPlayState = 'running';
            document.querySelector('#profile_view').style.animationPlayState = 'running';
            // document.querySelector('#profile_view').style.display='none'


        }

//load posts by default
        show_posts();
        //button listener
        document.querySelector('#cp_button').addEventListener("click", show_create_post)
    function show_edit(post) {

    }
})

