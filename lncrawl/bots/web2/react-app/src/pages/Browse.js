import React, { useEffect, useState } from 'react';
import Metadata from '../components/Metadata';
import NovelList from '../components/NovelList';
import Pagination from '../components/Pagination';
import { useParams } from 'react-router-dom';

import "../assets/stylesheets/navbar.min.css"
import "../assets/stylesheets/media-mobile.min.css"
import "../assets/stylesheets/media-768.min.css"
import "../assets/stylesheets/media-1024.min.css"
import "../assets/stylesheets/media-1270.min.css"
import "../assets/stylesheets/fontello.css"
import "../assets/stylesheets/pagedlist.css"
import "../assets/stylesheets/browsepg.min.css"



function Browse() {

    const title = "Read Light Novels Online For Free | LnCrawler";
    const description = "Read world famous Japanese Light Novels, Chinese Light Novels and Korean Light Novels in any language from more that 140 different websites."
    const imageUrl = "WEBSITE_URL + '/static/assets/logo.bmp'"
    const imageAlt = "LnCrawler"
    const imageType = "image/bmp"

    const [novels, setNovels] = useState({});
    const { page } = useParams();

    useEffect(() => {
        fetch(`/api/novels?page=${parseInt(page) - 1}`).then(
            response => response.json()
        ).then(
            data => {
                setNovels(data);
            }
        )
    }, [page]);


    const pagination = (typeof novels.metadata === 'undefined') ? <div>Loading ...</div> : <Pagination page={parseInt(page)} maxPage={novels.metadata.total_pages} />;

    return (


        <main role="main">
            <Metadata description={description} title={title} imageUrl={imageUrl} imageAlt={imageAlt} imageType={imageType} />
            <article id="explore" className="container">
                <header id="Result">
                    <h1>{title}</h1>
                    <p className="description">{description}</p>
                    <nav className="paging">
                        <div className="pagination-container">
                            <ul className="pagination">
                                {pagination}
                            </ul>
                        </div>
                    </nav>
                </header>
                <ul className="novel-list horizontal col2">
                    {(typeof novels.content === 'undefined') ? (
                        <div>Loading...</div>
                    ) : (<NovelList novels={novels.content} />)
                    }

                </ul>
                <footer className="pagination" style={{ "height": "auto" }}>
                    <nav className="paging">
                        <div className="pagination-container">
                            <ul className="pagination">
                                {pagination}
                            </ul>
                        </div>
                    </nav >
                </footer >
            </article >
        </main >
    )
}

export default Browse