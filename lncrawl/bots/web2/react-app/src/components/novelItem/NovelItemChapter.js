import React from 'react'
import { Link } from 'react-router-dom'

function NovelItemChapter ({ novel }) {
    const source = novel
    if (source.novel === undefined) {
        return null
    }

    let novelUrl = ''
    if (source.novel.slug) {
        novelUrl = `/novel/${source.novel.slug}/${source.slug}`
    }
    let chapterUrl = ''
    if (novelUrl) {
        chapterUrl = `${novelUrl}/chapter-${source.chapter_count}`
    }

    const re = new RegExp('(((Chapter|Chapitre|Ch) ?|C)[0-9]+(.[0-9]+)? ?(-|[:;.])?)|^[0-9]+(.[0-9]+)?')
    let chapterName = source.latest.replace(source.title, '').trim().replace(re, '').trim()
    // chapterName = novel.latest

    function formatTimeAgo (timeAgo) {
        const seconds = Math.floor(timeAgo / 1000)
        const minutes = Math.floor(seconds / 60)
        const hours = Math.floor(minutes / 60)
        const days = Math.floor(hours / 24)
        const months = Math.floor(days / 30)
        const years = Math.floor(months / 12)
        if (seconds < 60) {
            return `${seconds} seconds ago`
        } else if (minutes < 60) {
            return `${minutes} minutes ago`
        } else if (hours < 24) {
            return `${hours} hours ago`
        } else if (days < 30) {
            return `${days} days ago`
        } else if (months < 12) {
            return `${months} months ago`
        } else {
            return `${years} years ago`
        }
    }

    const servertimezone = 0 // server timezone is utc-0
    const usertimezone = new Date().getTimezoneOffset() / 60 // user timezone
    const serverOffset = servertimezone - usertimezone // offset between server and user timezone

    const updateDateInUserTimezone = new Date(
        new Date(source.last_update_date).getTime() + serverOffset * 60 * 60 * 1000
    )
    const formatedTimeAgo = formatTimeAgo(new Date().getTime() - updateDateInUserTimezone.getTime())

    return (
        <li className='novel-item'>
            <div className='cover-wrap'>
                <Link to={chapterUrl} title={source.latest}>
                    <figure className='novel-cover'>
                        <img
                            className='lazyload'
                            data-src={source.cover.replace('.jpg', '.min.jpg')}
                            src={source.cover.replace('.jpg', '.min.jpg')}
                            alt={source.title}
                        />
                    </figure>
                </Link>
            </div>
            <div className='item-body'>
                <Link to={chapterUrl} title={source.latest}>
                    <h4 className='novel-title text1row'>{source.title}</h4>
                    <h5 className='chapter-title text1row'>
                        Chapter {source.chapter_count}
                        {chapterName ? ` : ${chapterName}` : ''}
                    </h5>
                </Link>
                <div className='novel-stats'>
                    <span>
                        <i className='icon-pencil'></i>{' '}
                        <time dateTime={updateDateInUserTimezone}>{formatedTimeAgo}</time>
                    </span>
                </div>
            </div>
        </li>
    )
}

export default NovelItemChapter
