document.addEventListener('DOMContentLoaded', () => {
//main screen
    function show_posts() {
        document.querySelector('#profile_view').style.display = "block";
        document.querySelector('#create_post').style.display = 'none';
    }

// showing create post dialog
    function show_create_post() {
        document.querySelector('#create_post').style.display = 'block';
        document.querySelector('#control-textarea').value='';
        document.querySelector('#create_post').style.animationPlayState = 'running';
        document.querySelector('#profile_view').style.animationPlayState = 'running';
        // document.querySelector('#profile_view').style.display='none'
    }

//load posts by default
    show_posts();
    //button listener
    document.querySelector('#cp_button').addEventListener("click", show_create_post)
})