import React from 'react'
import { Link } from 'react-router-dom'

function NovelItemCompactTrends({ novel }) {

    const novelUrl = `/novel/${novel.slug}/${novel.prefered_source}`
    const formatter = Intl.NumberFormat('en', { notation: 'compact' })
    return (
        <li className="novel-item compact">
            <Link className="item-cover" title={novel.title} to={novelUrl}>
                <div className="novel-cover">
                    <img className=" ls-is-cached lazyloaded" data-src={novel.cover} src={novel.cover} alt={novel.title} />
                </div>
            </Link>
            <div className="item-body">
                <h4 className="novel-title text1row">
                    <Link title={novel.title} to={novelUrl}>
                        {novel.title}
                    </Link>
                </h4>
                <span><i className="icon-eye"></i> {formatter.format(novel.current_week_clicks)} (Weekly)</span>
                <span><i className="icon-commenting-o"></i> {formatter.format(novel.comment_count)} comments</span>
            </div>
        </li>)
}

export default NovelItemCompactTrends