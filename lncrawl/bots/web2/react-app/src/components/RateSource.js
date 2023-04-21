import { useState, useEffect, useCallback } from "react"
import { useCookies } from 'react-cookie';
import { useLocation } from "react-router-dom";

function RateSource({ novelSlug, sourceSlug }) {
    // We use cookies to track how many times a user has visited a novel page
    // If the user has visited the page 2 times, we show RateSource component else we show nothing
    //The cookie name is numberOfVisit_/novel/${novelSlug}/${sourceSlug}/ and its path is /
    // I have no idea why but when I use a path of /novel/${novelSlug}/${sourceSlug}/, the cookie is read after a full remount
    // It is terrible but I have no idea how to fix it
    const [visitedNovelPageCookies, setVisitedNovelPageCookies] = useCookies([`numberOfVisit_/novel/${novelSlug}/${sourceSlug}/`]);
    const setNumberOfVisit = useCallback((number) => {
        setVisitedNovelPageCookies(`numberOfVisit_/novel/${novelSlug}/${sourceSlug}/`, number.toString(), {
          path: '/',
          sameSite: 'strict',
          maxAge: 2592000 // 3 days
        });
      }, [novelSlug, sourceSlug, setVisitedNovelPageCookies]);

    if (isNaN(parseInt(visitedNovelPageCookies[`numberOfVisit_/novel/${novelSlug}/${sourceSlug}/`]))) {
        setNumberOfVisit("0");
    }
    const numberOfVisit = parseInt(visitedNovelPageCookies[`numberOfVisit_/novel/${novelSlug}/${sourceSlug}/`]);

    const location = useLocation();

    

    // We use this state to make sure useEffect is only executed once. Is reset everytime the user navigates to a new page
    const [executed, setExecuted] = useState(false);
    useEffect(() => {
        setExecuted(false);
    }, [location.pathname]);

    useEffect(() => {
        // If the use already visited the page 2 times, we don't need to do anything. Return early to avoid unnecessary rerenders
        // If the useEffect has already been executed on this page, we don't need to do anything. 
        // Without this check, the useEffect will loop until numberVisit > 2 because setNumberVisit will trigger a rerender
        if (numberOfVisit > 2 || executed) {
            return;
        }
        setNumberOfVisit(numberOfVisit + 1);
        setExecuted(true);

    }, [novelSlug, sourceSlug, executed, numberOfVisit, setNumberOfVisit]);


    const [thanksPanelActive, setThanksPanelActive] = useState(false);
    function sendRating(rating) {
        setNumberOfVisit(100); // Set numberVisit to 100 so that the component is not rendered again
        fetch("/api/rate_source", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                novel: novelSlug,
                source: sourceSlug,
                rating: rating,
            }),
        });

        setThanksPanelActive(true);
        setTimeout(function () { setThanksPanelActive(false); }, 1500);
        
    }

    if (numberOfVisit === 2) {
        return (
            <div className="lnw-modal _show" id="childcomeditor">
                <div className="modal-section">
                    <button onClick={() => setNumberOfVisit(100)} className="_close">
                        <i className="icon-cancel"></i>
                    </button>
                    <div className="modal-header">Is this source well formatted?</div>
                    <div className="modal-body">
                        <p>
                            Please tell us if this source is good. This includes : <br />
                            - Is the text well formatted? <br />
                            - Does it have a fitting cover image? <br />
                            - Are the chapters in order and not missing? <br />
                            - Is the novel in the correct language and is the translation good? <br />
                            ... <br />
                            This will help us improve the quality of the site, Thank you for your help!
                        </p>
                    </div>
                    <div className="modal-rating-area">
                        <div className="upvote">
                            <button id="compostbtn" className="button" onClick={() => sendRating(1)}>
                                <i className="icon-thumbs-up"></i>
                            </button>
                        </div>
                        <div className="downvote">
                            <button id="compostbtn" className="button" onClick={() => sendRating(-1)}>
                                <i className="icon-thumbs-down"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
    else {
        return <div className={"thanks-panel" + (thanksPanelActive ? " active" : "")}>
                <div className="thanks-panel-rating-text">
                    Thank you!
                </div>
            </div>
    }
}

export default RateSource