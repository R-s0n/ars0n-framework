import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const CacheDeception = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <p><b>Summary:</b> Web Cache Deception occurs when the attacker forces the web cache to <strong>store sensitive content belonging to another user in the cache, allowing the attacker to retreive that sensitive data</strong>.</p>
                    <p><b>Goal(s):</b></p>
                    <ol>
                        <li>Access the sensitive information of other users by forcing the web cache to store and serve a page with sensitive data.</li>
                    </ol>
                    <p><b>Methodology - Identifying Vulnerabilities:</b></p>
                    <ol>
                        <li>Identify a page with sensitive content if a user is logged in.</li>
                        <li>Append a non-existent static file (.css, .js, .png, etc.) to the URL (Ex: http://www.example.com/account.php/nonexistent.js).</li>
                        <li>Log out and attempt to access the same resource, which will include the sensitive information, using the cached URL.</li>
                    </ol>
                    <p><b>Methodology - Exploiting Vulnerabilities:</b></p>
                    <ol>
                        <li>Send malicious URL to logged in user that will force the web cache to store the response.</li>
                        <li>Access the cached response and collect the victim's sensitive information.</li>
                    </ol>
                </div>
            </div>
        </div>
    );

}

export default CacheDeception;