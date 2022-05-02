document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.filter-green').forEach(like => {
        let is_liked = like.getAttribute('data-name');
        let post_liked_id = like.id.match(/(\d+)/)[0];
        //set init state
        if (is_liked.toLowerCase() === 'liked') {
            document.querySelector(`#like${post_liked_id}`).style.animationName = 'like';
            document.querySelector(`#like${post_liked_id}`).style.animationPlayState = 'running';
        } else {
            document.querySelector(`#like${post_liked_id}`).style.animationDuration = '1.5s';
            document.querySelector(`#like${post_liked_id}`).style.animationName = 'unlike';
            document.querySelector(`#like${post_liked_id}`).style.animationPlayState = 'running';
        }
        like.addEventListener('click', (e) => {
            e.preventDefault();
            like_post(post_liked_id, is_liked);
            if (is_liked.toLowerCase() === 'liked') {
                is_liked = 'unliked'
            } else {
                is_liked = 'liked'
            }
        })
    })

    function like_post(post_liked_id, is_clicked) {
        let csrf_token_like = document.querySelector('#csrf_token_like').value;

        function like_it(is_clicked) {

            if (is_clicked.toLowerCase() === 'liked') {
                document.querySelector(`#like${post_liked_id}`).style.animationName = 'unlike';
                document.querySelector(`#like${post_liked_id}`).style.animationPlayState = 'running';
            } else {
                document.querySelector(`#like${post_liked_id}`).style.animationName = 'like';
                document.querySelector(`#like${post_liked_id}`).style.animationPlayState = 'running';
            }
        }

        // if in userprofile
        fetch(`/like/${post_liked_id}`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrf_token_like
            },
            body: JSON.stringify({
                'post_id': post_liked_id
            })

        }).then(() => {
            like_it(is_clicked)

        })
    }
})