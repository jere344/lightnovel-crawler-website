import React from 'react'
import logo from '../assets/logo.png'

function Footer() {
    return (
        <footer translate="no">
            <div className="wrapper">
                <div className="col logo">
                    <a href="/" style={{ "display": "inline-block" }}>
                        <img className="footer-logo" src={logo} alt="logo-footer" width="140" height="90" />
                    </a>
                </div>
                <nav className="col links">
                    <ul>
                        <li>
                            <a href="https://github.com/jere344/lightnovel-crawler/tree/react-dev-dev">Terms of Service</a>
                        </li>
                        <li>
                            <a href="mailto: jeremy.guerin34@yahoo.com">DMCA Notices</a>
                        </li>
                        <li>
                            <a href="mailto: jeremy.guerin34@yahoo.com">Contact Us</a>
                        </li>
                    </ul>
                </nav>
            </div>
        </footer>
    )
}

export default Footer