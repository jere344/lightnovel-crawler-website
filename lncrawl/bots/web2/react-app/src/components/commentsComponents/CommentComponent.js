import { useState, useEffect } from 'react'
import CommentSection from './CommentSection'
import AdjacentCommentSection from './AdjacentCommentSection.js'
import TermsPrompt from './TermsPrompt'
import { API_URL } from '../../config.js'
import '../../assets/stylesheets/comments.min.css'

// const exemple = {
//     "0": {
//         "name": "Anonymous",
//         "text": "This is a test comment",
//         "date": "2021-08-01T00:00:00.000Z",
//         "id": "0",
//         "rank": "Reader",
//         "likes": "0",
//         "dislikes": "0",
//         "children": {
//             "0": {
//                 "name": "Anonymous",
//                 "text": "This is a test reply",
//                 "date": "2021-08-01T00:00:00.000Z",
//                 "id": "0",
//                 "rank": "Reader",
//                 "likes": "0",
//                 "dislikes": "0",
//                 "children": {},
//             },
//         },
//     },
//     "1": {
//         "name": "Anonymous",
//         "text": "This is a test comment",
//         "date": "2021-08-01T00:00:00.000Z",
//         "id": "1",
//         "rank": "Reader",
//         "likes": "0",
//         "dislikes": "0",
//         "children": {},
//     },
// }

function CommentComponent ({ currentUrl, defaultSort = 'reactions', setMenuOpen }) {
    const url = `${API_URL}/get_comments?page=${currentUrl}`
    const [comments, setComments] = useState([])
    const [adjacents, setAdjacents] = useState([])

    useEffect(() => {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                setComments(data.content)
                setAdjacents(data.adjacent)
            })
    }, [url])

    const [replyTo, setReplyTo] = useState(null)

    const [commenting, setCommenting] = useState(false)

    return (
        <section className='comment-list'>
            <div className='head'>
                <h4>User Comments</h4>
                <button
                    className='button'
                    title='You must be logged in to post a comment.'
                    onClick={() => {
                        if (setMenuOpen) setMenuOpen(false)
                        setReplyTo(false)
                        setCommenting(true)
                    }}
                >
                    Write Comment
                </button>
            </div>
            <div className='comment-policy'>
                <button
                    id='comment-policy-show'
                    onClick={() => {
                        if (setMenuOpen) setMenuOpen(false)
                        setReplyTo(false)
                        setCommenting(true)
                    }}
                >
                    Please read and apply the rules before posting a comment.
                </button>
                <br />
                By sharing your comment, you agree to all the relevant terms.
            </div>
            <div className='comment-wrapper'>
                <CommentSection comments={comments} setReplyTo={setReplyTo} setCommenting={setCommenting} defaultSort={defaultSort} />
            </div>
            <div className='comment-adjacent'>
                <AdjacentCommentSection adjacents={adjacents} setReplyTo={setReplyTo} setCommenting={setCommenting} />
            </div>
            {/* setCommenting is used in TermsPrompt to stop commenting when clickingon the cross */}
            {/* TermsPrompt will call CommentPromt which will use replyTo to post new comment request */}
            {/* TermsPrompt will ask to agree rules then open pannel to post a comment */}
            {commenting ? <TermsPrompt setCommenting={setCommenting} replyTo={replyTo} /> : null}
        </section>
    )
}

export default CommentComponent
