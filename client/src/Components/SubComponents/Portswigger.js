import React, {useState, useEffect} from 'react';
import Modal from 'react-modal';

const Portswigger = props => {

    return (
        <div className="container mt-2">
            <div className="row">
                <div className="col-12">
                    <h4>Portswigger</h4>
                    <p>PortSwigger is a UK-based cybersecurity company that is well known for its flagship product, Burp Suite. Burp Suite is an integrated platform for performing security testing of web applications. It is widely used by cybersecurity professionals, including web developers, security researchers, and penetration testers, to identify security vulnerabilities in web applications.</p>
                    <p>The company was founded by Dafydd Stuttard, who is also the creator of Burp Suite. Burp Suite provides various tools for testing web application security, such as intercepting proxies, scanner tools, and numerous options for manual testing. It helps identify various types of security issues, including but not limited to cross-site scripting (XSS), SQL injection, and other vulnerabilities that can be exploited by malicious attackers.</p>
                    <p>PortSwigger's Burp Suite has become a standard tool in the arsenal of security professionals and is widely recognized in the cybersecurity community for its effectiveness and comprehensive features for identifying and addressing web application security issues.</p>
                    
                </div>
            </div>
        </div>
    );

}

export default Portswigger;