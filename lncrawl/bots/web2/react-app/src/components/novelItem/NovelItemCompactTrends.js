import React from 'react'
import { Link } from 'react-router-dom'

function NovelItemCompactTrends({ novel }) {

    const novelUrl = `/novel/${novel.slug}/${novel.prefered_source}`

    return (
        <li className="novel-item">
            <Link className="item-cover" title={novel.title} to={novelUrl}>
                <div className="novel-cover">
                    <img className=" ls-is-cached lazyloaded" data-src={`/api/image/${novel.cover}`} src={`/api/image/${novel.cover}`} alt={novel.title} />
                </div>
            </Link>
            <div className="item-body">
                <h4 className="novel-title text1row">
                    <Link title={novel.title} to={novelUrl}>
                        {novel.title}
                    </Link>
                </h4>
                <span><i className="icon-eye"></i> {novel.clicks} (Weekly)</span>
            </div>
        </li>)
}

export default NovelItemCompactTrends