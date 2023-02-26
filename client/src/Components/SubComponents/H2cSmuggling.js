import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const H2cSmuggling = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> When using HTTP/2, many front-end services downgrade the request to HTTP/1.1 before forwarding a request to the back-end servers.  This downgrading process can be exploited to execute HTTP request smuggling attacks.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Byass front-end security controls (Ex: Access /admin endpoint that would normally return a 403).</li>
                        <li>Reveal changes the front-end makes to incoming requests.</li>
                        <li>Capture the requests of other users.</li>
                        <li>Increase the impact of reflected XSS by using HTTP request smuggling to deliver the XSS payload.</li>
                        <li>Increase the impact of an internal open-redirect to a wide-open redirect.</li>
                        <li>Leverage HTTP request smuggling to perform web cache poisoning/deception.</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Identify application using the HTTP/2 protocol.</li>
                        <li><a href="https://portswigger.net/web-security/request-smuggling/advanced">https://portswigger.net/web-security/request-smuggling/advanced</a></li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li></li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default H2cSmuggling;